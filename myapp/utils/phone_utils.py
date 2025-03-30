from django_countries import countries
import logging
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

class PhoneNumberFormatter:
    """
    Utility class for handling phone number formatting and validation
    """
    # Common country phone prefixes
    PHONE_PREFIXES = {
        'IL': '+972',  # Israel
        'US': '+1',    # United States
        'GB': '+44',   # United Kingdom
        'DE': '+49',   # Germany
        'FR': '+33',   # France
        'IT': '+39',   # Italy
        'ES': '+34',   # Spain
        'RU': '+7',    # Russia
        'CN': '+86',   # China
        'JP': '+81',   # Japan
        'KR': '+82',   # South Korea
        'IN': '+91',   # India
        'BR': '+55',   # Brazil
        'AU': '+61',   # Australia
        'CA': '+1',    # Canada
        'MX': '+52',   # Mexico
        'AR': '+54',   # Argentina
        'ZA': '+27',   # South Africa
        'EG': '+20',   # Egypt
        'AE': '+971',  # United Arab Emirates
        'SA': '+966',  # Saudi Arabia
        'TR': '+90',   # Turkey
        'PL': '+48',   # Poland
        'NL': '+31',   # Netherlands
        'BE': '+32',   # Belgium
        'SE': '+46',   # Sweden
        'NO': '+47',   # Norway
        'DK': '+45',   # Denmark
        'FI': '+358',  # Finland
        'IE': '+353',  # Ireland
        'PT': '+351',  # Portugal
        'GR': '+30',   # Greece
        'HU': '+36',   # Hungary
        'CZ': '+420',  # Czech Republic
        'SK': '+421',  # Slovakia
        'RO': '+40',   # Romania
        'BG': '+359',  # Bulgaria
        'HR': '+385',  # Croatia
        'SI': '+386',  # Slovenia
        'EE': '+372',  # Estonia
        'LV': '+371',  # Latvia
        'LT': '+370',  # Lithuania
        'CY': '+357',  # Cyprus
        'MT': '+356',  # Malta
        'LU': '+352',  # Luxembourg
        'IS': '+354',  # Iceland
        'CH': '+41',   # Switzerland
        'AT': '+43',   # Austria
    }

    @classmethod
    def get_country_prefix(cls, country_code):
        """
        Get the phone prefix for a given country code
        """
        return cls.PHONE_PREFIXES.get(country_code, '+')

    @classmethod
    def format_phone_number(cls, phone_number, country_code='IL'):
        """
        Format phone number according to country code
        """
        try:
            # Remove any spaces or special characters
            phone_number = ''.join(filter(str.isdigit, phone_number))
            
            # If number already has country prefix, return as is
            if phone_number.startswith('+'):
                return phone_number
            
            # Get country prefix
            country_prefix = cls.get_country_prefix(country_code)
            
            # Special handling for Israeli numbers
            if country_code == 'IL':
                return f"+972{phone_number.lstrip('0')}"
            
            # For other countries, add the country prefix
            return f"{country_prefix}{phone_number}"
            
        except Exception as e:
            logger.error(f"Phone number formatting error: {str(e)}")
            raise ValidationError(f"Invalid phone number format: {str(e)}")

    @classmethod
    def validate_phone_number(cls, phone_number, country_code='IL'):
        """
        Validate phone number format and return formatted number
        """
        try:
            formatted_number = cls.format_phone_number(phone_number, country_code)
            return formatted_number
        except ValidationError as e:
            logger.error(f"Phone number validation error: {str(e)}")
            raise

    @classmethod
    def get_help_text(cls, country_code='US'):
        """
        Get help text for phone number input based on country
        """
        examples = {
            'US': "Enter your phone number (e.g., 1234567890)",
            'IL': "Enter your phone number (e.g., 0501234567)",
            'GB': "Enter your phone number (e.g., 7911123456)",
            'default': "Enter your phone number with country code"
        }
        return examples.get(country_code, examples['default']) 