"""hCaptcha WTForms validators."""

import logging
from urllib.request import urlopen
from urllib.parse import urlencode
from wtforms.validators import ValidationError
import json

logger = logging.getLogger(__name__)


class Hcaptcha(object):
    """Validates captcha using hCaptcha API."""

    errors = {
        "missing-input-secret": "The secret key is missing.",
        "invalid-input-secret": "The secret key is invalid or malformed.",
        "missing-input-response": ("The response parameter (verification "
                                   "token) is missing."),
        "invalid-input-response": ("The response parameter (verification "
                                   "token) is invalid or malformed."),
        "bad-request": "The request is invalid or malformed.",
        "invalid-or-already-seen-response": ("The response parameter has "
                                             "already been checked, or has "
                                             "another issue."),
        "sitekey-secret-mismatch": ("The sitekey is not registered with the "
                                    "provided secret."),
        "not-reachable": "Could not connect to hCaptcha."
    }

    empty_error_text = "This field is required"
    internal_error_text = "Internal error, please try again later"

    def _call_verify(self, params):
        """Performs a call to hCaptcha API with given parameters."""
        data = None

        try:
            response = urlopen("https://hcaptcha.com/siteverify",
                               data=urlencode(params).encode("utf-8"))
            data = json.loads(response.read().decode("utf-8"))
            response.close()
        except Exception as e:
            logger.error(str(e))
            raise ValidationError(self.errors["not-reachable"])

        return data

    def __call__(self, form, field):
        """Validate the field."""
        if not field.data:
            raise ValidationError(field.gettext(self.empty_error_text))

        params = (
            ("secret", field.secret_key),
            ("response", field.data),
            ("remoteip", field.ip_address),
            ("sitekey", field.site_key)
        )

        data = self._call_verify(params)
        if data["success"] is not True:
            if ("error-codes" in data and
                    "invalid-or-already-seen-response" in data["error-codes"]):
                raise ValidationError(field.gettext(
                    self.errors["invalid-or-already-seen-response"]))

            logger.error(data["error-codes"] if "error-codes" in data else
                         data)
            raise ValidationError(field.gettext(self.internal_error_text))
