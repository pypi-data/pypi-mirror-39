from django.forms import Form, CharField, EmailField, Textarea, TextInput, EmailInput
from django.core.validators import RegexValidator

NoClickBait = RegexValidator(regex="https?://",
                             message='Please remove all URLs.',
                             inverse_match=True)

recontact_validators = [NoClickBait]

try:
    from django.conf import settings
    if settings.RECONTACT_CONFIG.get('allow_click_bait', False):
        recontact_validators = []
except:
    pass

class RecontactForm(Form):
    """
    Django form which collects data for a contact email message.
    """

    sender = CharField(label='', widget=TextInput(
        attrs={'placeholder': 'Your Name', 'class': 'recontact'}),
        validators=recontact_validators)

    reply_to = EmailField(label='', widget=EmailInput(
        attrs={'placeholder': 'Your email address', 'class': 'recontact'}))

    subject = CharField(label='', widget=TextInput(
        attrs={'placeholder': 'Subject', 'class': 'recontact'}),
        validators=recontact_validators)

    message = CharField(label='', widget=Textarea(
        attrs={'placeholder': 'Message', 'class': 'recontact'}),
        validators=recontact_validators)
