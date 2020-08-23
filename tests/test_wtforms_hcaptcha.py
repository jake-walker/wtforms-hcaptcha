"""WTForms hCaptcha tests."""

from wtforms.form import Form

from wtforms_hcaptcha.fields import HcaptchaField
from wtforms_hcaptcha.validators import Hcaptcha

import pytest


class HcaptchaSuccessfulValidatorMockup(Hcaptcha):
    """Validator subclass to emulate a successful hCaptcha API call."""
    def _call_verify(self, params):
        return {
            "success": True
        }


class HcaptchaFailedValidatorMockup(Hcaptcha):
    """Validator subclass to emulate a failed hCaptcha API call."""
    def _call_verify(self, params):
        return {
            "success": False,
            "error-codes": [
                "invalid-or-already-seen-response"
            ]
        }


class HcaptchaInternalFailedValidatorMockup(Hcaptcha):
    """Validator subclass to emulate a failed hCaptcha API call."""
    def _call_verify(self, params):
        return {
            "success": False,
            "error-codes": [
                "bad-request"
            ]
        }


class RequestDictMock(dict):
    """Dictionary subclass to emulate a multidict."""

    def getall(self, key):
        """Return a list of all values for a key.

        Args:
            key (str): The key to return values for.

        Returns:
            list: List of all values for the key.
        """
        data = []
        if key in self:
            data.append(self[key])
        return data


def test_missing_keys():
    """Test that the form raises an error if no keys are provided."""
    with pytest.raises(ValueError):
        class CaptchaForm(Form):
            captcha = HcaptchaField()

        CaptchaForm()


def test_form_widget():
    """Test that the form is correctly building the widget."""
    class CaptchaForm(Form):
        captcha = HcaptchaField(site_key="testsite", secret_key="testsec")

    form = CaptchaForm()

    expected_widget = """<div class="h-captcha" data-sitekey="testsite"></div>
<script src="https://hcaptcha.com/1/api.js" async defer></script>"""

    assert str(form.captcha).rstrip() == expected_widget.rstrip()


def test_missing_data():
    """Test that the form raises an error if no data is provided."""
    with pytest.raises(ValueError):
        class CaptchaForm(Form):
            captcha = HcaptchaField(site_key="testsite", secret_key="testsec")

        CaptchaForm(RequestDictMock())


def test_missing_response():
    """Test that the form errors if there is no response."""
    class CaptchaForm(Form):
        captcha = HcaptchaField(site_key="testsite", secret_key="testsec")

    form = CaptchaForm(RequestDictMock(), captcha={"ip_address": "127.0.0.1"})
    assert form.validate() is False
    captcha_error = form.errors.get("captcha")
    assert captcha_error is not None
    assert captcha_error[0] == Hcaptcha.empty_error_text


def test_incorrect_solution():
    """Test that the form errors with an incorrect solution."""
    class CaptchaForm(Form):
        captcha = HcaptchaField(site_key="testsite", secret_key="testsec",
                                validators=[
                                    HcaptchaFailedValidatorMockup()])

    form = CaptchaForm(RequestDictMock({
        "h-captcha-response": "testresponse"
    }), captcha={"ip_address": "127.0.0.1"})
    assert form.validate() is False
    captcha_error = form.errors.get("captcha")
    assert captcha_error is not None
    assert captcha_error[0] == Hcaptcha.errors[
        "invalid-or-already-seen-response"]


def test_internal_error():
    """Test that the form errors with an internal error."""
    class CaptchaForm(Form):
        captcha = HcaptchaField(site_key="testsite", secret_key="testsec",
                                validators=[
                                    HcaptchaInternalFailedValidatorMockup()])

    form = CaptchaForm(RequestDictMock({
        "h-captcha-response": "testresponse"
    }), captcha={"ip_address": "127.0.0.1"})
    assert form.validate() is False
    captcha_error = form.errors.get("captcha")
    assert captcha_error is not None
    assert captcha_error[0] == Hcaptcha.internal_error_text


def test_solved_captcha():
    """Test that the form validates with a correct solve."""
    class CaptchaForm(Form):
        captcha = HcaptchaField(site_key="testsite", secret_key="testsec",
                                validators=[
                                    HcaptchaSuccessfulValidatorMockup()])

    form = CaptchaForm(RequestDictMock({
        "h-captcha-response": "testresponse"
    }), captcha={"ip_address": "127.0.0.1"})
    assert form.validate() is True
