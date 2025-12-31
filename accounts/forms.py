from django.contrib.auth import password_validation
from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        label=_("First Name")
    )
    last_name = forms.CharField(
        max_length=50,
        label=_("Last Name")
    )
    phone = forms.CharField(
        min_length=11,
        max_length=11,
        label=_("Phone Number")
    )
    city = forms.CharField(
        max_length=50,
        label=_("City")
    )
    username = forms.CharField(
        max_length=50,
        required=False,
        label=_("Email")
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=4,
        label=_("Password")
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        min_length=4,
        label=_("Confirm Password")
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=False,
        label=_("Email")
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        min_length=4,
        label=_("Password")
    )

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="رمز فعلی",
        widget=forms.PasswordInput()
    )
    new_password1 = forms.CharField(
        label="رمز جدید",
        widget=forms.PasswordInput(),
        # help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        label="تکرار رمز جدید",
        widget=forms.PasswordInput()
    )

    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    #     super().__init__(*args, **kwargs)

    # def clean_old_password(self):
    #     old_password = self.cleaned_data.get('old_password')
    #     if not self.user.check_password(old_password):
    #         raise forms.ValidationError("رمز فعلی نادرست است.")
    #     return old_password

    # def clean(self):
    #     cleaned_data = super().clean()
    #     p1 = cleaned_data.get('new_password1')
    #     p2 = cleaned_data.get('new_password2')
    #     if p1 and p2 and p1 != p2:
    #         self.add_error('new_password2', "رمزهای جدید با هم تطابق ندارند.")
    #     return cleaned_data

    # def save(self, commit=True):
    #     password = self.cleaned_data['new_password1']
    #     self.user.set_password(password)
    #     if commit:
    #         self.user.save()
    #     return self.user
    


# class ProfileForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=50, label="نام")
#     last_name = forms.CharField(max_length=50, label="نام خانوادگی")
#     email = forms.EmailField(label="ایمیل")
#     # permissions = forms.ModelMultipleChoiceField(
#     #     queryset=AccessPermission.objects.all(),
#     #     widget=forms.CheckboxSelectMultiple,
#     #     required=False,
#     #     label="دسترسی‌ها"
#     # )

#     class Meta:
#         model = Profile
#         exclude = ['user', 'updated_at', 'status', 'visit_count',
#                    'allow_comments', 'slug', 'categories', 'tags']
#     field_order = [
#         'avatar',
#         'first_name',
#         'last_name',
#         'email',
#         # 'image',
#     ]

# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile



class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="First name", max_length=150)
    last_name = forms.CharField(label="Last name", max_length=150)
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = Profile
        fields = ['avatar','first_name', 'last_name','email','password','role', 'phone_number', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            user = self.instance.user
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['password'].required = False
        else:
            self.fields['password'].required = True    

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(username=email)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.user.pk)

        if qs.exists():
            raise forms.ValidationError("User with this email already exists")

        return email


    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.instance.pk:
            # ===== UPDATE =====
            user = profile.user
        else:
            # ===== CREATE =====
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
            )

        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        if commit:
            user.save()
            profile.user = user
            profile.save()

        return profile