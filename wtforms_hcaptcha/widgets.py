"""hCaptcha WTForms widgets."""

from markupsafe import Markup

HCAPTCHA_HTML = Markup("""<div class="h-captcha" data-sitekey="{site_key}"></div>
<script defer src="https://hcaptcha.com/1/api.js" async defer></script>
""")


class Hcaptcha(object):
    """hCaptcha widget that displays HTML."""

    def __call__(self, field, **kwargs):
        """Create the widget."""
        html = HCAPTCHA_HTML.format(site_key=field.site_key)
        return html
