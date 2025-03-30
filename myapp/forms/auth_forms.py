from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from django_countries import countries
from ..models import CustomUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from ..utils.phone_utils import PhoneNumberFormatter

class BaseRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(
        required=True,
        help_text=PhoneNumberFormatter.get_help_text()
    )
    country = CountryField().formfield()
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Enter your date of birth (MM/DD/YYYY)"
    )

    def clean_password1(self):
        """Validate password strength"""
        password = self.cleaned_data.get('password1')
        validate_password(password)
        return password

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        country = self.cleaned_data.get('country')
        
        if phone_number and country:
            try:
                return PhoneNumberFormatter.validate_phone_number(
                    phone_number, 
                    country_code=country
                )
            except ValidationError as e:
                raise forms.ValidationError(str(e))
        
        return phone_number

class CustomerRegistrationForm(BaseRegistrationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'country', 'date_of_birth', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('registration_type') == 'advisor':
            raise ValidationError('This form is for customer registration only.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.registration_type = 'customer'
        if commit:
            user.save()
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
        required=True,
        help_text="Upload your professional certifications, licenses, or relevant credentials (PDF, JPG, or PNG)"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'country', 'date_of_birth', 
                 'expertise', 'hourly_rate', 'verification_documents', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('registration_type') == 'customer':
            raise ValidationError('This form is for advisor registration only.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.registration_type = 'advisor'
        if commit:
            user.save()
        return user 