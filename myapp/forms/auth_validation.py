from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from django_countries import countries
from ..models import User, CustomerProfile, AdvisorProfile
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from ..utils.phone_utils import PhoneNumberFormatter

class BaseRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    def clean_password1(self):
        """Validate password strength"""
        password = self.cleaned_data.get('password1')
        validate_password(password)
        return password

class CustomerRegistrationForm(BaseRegistrationForm):
    full_name = forms.CharField(max_length=255, required=True)
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Enter your date of birth (MM/DD/YYYY)"
    )
    bio = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Tell us about yourself"
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            CustomerProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                birth_date=self.cleaned_data['birth_date'],
                bio=self.cleaned_data.get('bio', ''),
                profile_picture=self.cleaned_data.get('profile_picture')
            )
        return user

class AdvisorRegistrationForm(BaseRegistrationForm):
    expertise = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Please describe your professional expertise, certifications, and years of experience"
    )
    hourly_rate = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        validators=[MinValueValidator(0)],
        help_text="Enter your hourly consultation rate in USD (e.g., 150.00)"
    )
    verification_documents = forms.FileField(
        required=False,
        help_text="Upload your professional certifications, licenses, or relevant credentials (PDF, JPG, or PNG) - Optional"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            AdvisorProfile.objects.create(
                user=user,
                expertise=self.cleaned_data['expertise'],
                hourly_rate=self.cleaned_data['hourly_rate'],
                verification_documents=self.cleaned_data.get('verification_documents')
            )
        return user 