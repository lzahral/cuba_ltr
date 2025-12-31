from django import forms
from django.contrib.auth import get_user_model
from .models import *
from django.forms.widgets import ClearableFileInput
from datetime import datetime

User = get_user_model()



class TaskCreateForm(forms.ModelForm):


    attachments = forms.FileField(
        required=False,
        label="Attachments"
    )

    class Meta:
        model = Task
        fields = [ "title", "description","assignee", "deadline","attachments"]
        # fields = '__all__'
    def clean_deadline(self):
        date_str = self.cleaned_data.get("deadline")
        print(date_str)
        if isinstance(date_str, str):
            return datetime.strptime(date_str, "%B %d, %Y")
        return date_str
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

    #     return cleaned_data


class TaskSubmissionForm(forms.ModelForm):
    class Meta:
        model = TaskSubmission
        fields = ['comment', 'file']