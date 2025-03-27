from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone_number', 'country', 'birth_date', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        # בדיקה שהמשתמש לא מנסה להירשם כיועץ
        if cleaned_data.get('registration_type') == 'advisor':
            raise ValidationError('This form is for customer registration only.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.registration_type = 'customer'
        if commit:
            user.save()
        return user

class AdvisorRegistrationForm(UserCreationForm):
    expertise = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Please describe your expertise and experience"
    )
    hourly_rate = forms.DecimalField(
        validators=[MinValueValidator(0)],
        help_text="Your hourly rate in USD"
    )
    verification_documents = forms.FileField(
        required=True,
        help_text="Please upload your professional certification or license"
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone_number', 'country', 'birth_date', 
                 'expertise', 'hourly_rate', 'verification_documents', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        # בדיקה שהמשתמש לא מנסה להירשם כלוקוח
        if cleaned_data.get('registration_type') == 'customer':
            raise ValidationError('This form is for advisor registration only.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.registration_type = 'advisor'
        if commit:
            user.save()
        return user 