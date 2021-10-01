# WTForms hCaptcha

> Custom WTForms field that handles [hCaptcha](https://www.hcaptcha.com/) display and validation.

<a href="https://github.com/jake-walker/wtforms-hcaptcha/actions"><img alt="Build Status" src="https://img.shields.io/github/workflow/status/jake-walker/wtforms-hcaptcha/Main/master?style=flat-square"></a>
<a href="https://pypi.org/project/wtforms-hcaptcha/"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/wtforms-hcaptcha?style=flat-square"></a>
<img alt="GitHub License" src="https://img.shields.io/github/license/jake-walker/wtforms-hcaptcha?style=flat-square">

[hCaptcha](https://www.hcaptcha.com/) is a CAPTCHA service that 'protects user privacy, rewards websites, and helps companies get their data labelled'. This helps to prevent spam on websites by adding a challenge to forms that are hard for computers to solve, but easy for humans to solve.

I wanted to use hCaptcha in one of my projects and although there are already Python libraries for working with hCaptcha, I had already used the WTForms ecosystem in that project so I wanted a drop in solution and as there were none at the time, I decided to create my own.

This is a modified version of [`wtforms-recaptcha`](https://pypi.org/project/wtforms-recaptcha/) by [Artem Gluvchynsky](excieve@gmail.com) to work with hCaptcha.

## Installation

Use `pip` to install on all systems:

```bash
pip install wtforms-hcaptcha
```

## Usage Example

This example creates an empty form with just a CAPTCHA field.

```python
from wtforms.form import Form
from wtforms_hcaptcha.fields import HcaptchaField

class MyForm(Form):
    captcha = HcaptchaField(site_key="YOUR_SITE_KEY_HERE", secret_key="YOUR_SECRET_KEY_HERE")

form = MyForm(request.form, captcha={
    # note this needs to be edited to get the correct IP address when using a reverse proxy
    "ip_address": request.remote_addr
})

if form.validate():
    print("You are not a robot!")
else:
    print(form.errors["captcha"])
```

## Development Setup

This project uses Poetry to manage dependencies and packaging. [Here](https://python-poetry.org/docs/#installation) are the installation instructions for Poetry.

## Contributing

1. Fork it (https://github.com/jake-walker/wtforms-hcaptcha/fork)
2. Create your feature branch (`git checkout -b feature/foobar`)
3. Commit your changes (`git commit -am "Add some foobar"`)
4. Push to the branch (`git push origin feature/foobar`)
5. Create a new pull request
