from django import forms
from django.contrib.auth import get_user_model
from .models import Letter
from django.forms.widgets import ClearableFileInput

User = get_user_model()

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

class LetterCreateForm(forms.ModelForm):


    attachments = forms.FileField(
        required=False,
        label="Attachments"
    )

    class Meta:
        model = Letter
        fields = ["recipient", "subject", "body", "attachments"]
        widgets = {
            "subject": forms.TextInput(attrs={'class': 'form-control'}),
            "body": forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
    def __init__(self, *args, **kwargs):
        self.action = kwargs.pop('action', 'send')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if self.action == 'send':
            recipient = cleaned_data.get('recipient')
            subject = cleaned_data.get('subject')
            body = cleaned_data.get('body')
            if not recipient:
                self.add_error(
                    'recipient',
                    "Recipient cannot be empty."
                )

            if not subject:
                self.add_error(
                    'subject',
                    "Subject cannot be empty."
                )

            if not body:
                self.add_error(
                    'body',
                    "Body cannot be empty."
                )

        return cleaned_data

class ReplyLetterForm(forms.ModelForm):


    attachments = forms.FileField(
        required=False,
        label="Attachments"
    )

    class Meta:
        model = Letter
        fields = ["body", "attachments"]
        widgets = {
            "body": forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    # def clean(self):
    #     cleaned_data = super().clean()

    #     if self.action == 'send':
    #         recipient = cleaned_data.get('recipient')
    #         subject = cleaned_data.get('subject')
    #         body = cleaned_data.get('body')
    #         if not recipient:
    #             self.add_error(
    #                 'recipient',
    #                 "Recipient cannot be empty."
    #             )

    #         if not subject:
    #             self.add_error(
    #                 'subject',
    #                 "Subject cannot be empty."
    #             )

    #         if not body:
    #             self.add_error(
    #                 'body',
    #                 "Body cannot be empty."
    #             )

        # return cleaned_data
