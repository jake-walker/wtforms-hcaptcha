"""hCaptcha WTForms fields."""

from wtforms.fields import Field

from . import widgets
from . import validators as local_validators


class HcaptchaField(Field):
    """Handles captcha field display and validation via hCaptcha."""

    widget = widgets.Hcaptcha()

    def __init__(self, label="", validators=None, site_key=None,
                 secret_key=None, **kwargs):
        """Create a new hCaptcha WTForms field.

        Args:
            label (str, optional): The label for the field. Defaults to "".
            validators (list, optional): A list of WTForms validators.
                Defaults to None.
            site_key (str, required): The hCaptcha site key. Defaults to None.
            secret_key (str, required): The hCaptcha secret key. Defaults to
                None.

        Raises:
            ValueError: No site key or secret key are provided
        """
        validators = validators or [local_validators.Hcaptcha()]
        super(HcaptchaField, self).__init__(label, validators, **kwargs)

        if not site_key or not secret_key:
            raise ValueError("hCaptcha site key and secret key are required.")

        self.site_key = site_key
        self.secret_key = secret_key

        self.ip_address = None

    def process(self, formdata, data={}):
        """Handles multiple formdata fields that are required for hCaptcha."""
        self.process_errors = []

        if isinstance(data, dict):
            self.ip_address = data.pop("ip_address", None)

        try:
            self.process_data(data)
        except ValueError as e:
            self.process_errors.append(e.args[0])

        if formdata is not None:
            if not self.ip_address:
                raise ValueError("IP Address is required.")

            try:
                self.raw_data = formdata.getlist("h-captcha-response")
                self.process_formdata(self.raw_data)
            except ValueError as e:
                self.process_errors.append(e.args[0])

        for filter in self.filters:
            try:
                self.data = filter(self.data)
            except ValueError as e:
                self.process_errors.append(e.args[0])
