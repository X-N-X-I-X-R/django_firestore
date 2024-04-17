# models imports  

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator,RegexValidator,FileExtensionValidator
from dateutil.relativedelta import relativedelta 
from django.core.validators import FileExtensionValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  # For raising validation errors from save method
from django.core.exceptions import ValidationError


