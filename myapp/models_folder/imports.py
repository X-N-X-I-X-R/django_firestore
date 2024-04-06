from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator,MinLengthValidator, MaxLengthValidator,RegexValidator,FileExtensionValidator
from dateutil.relativedelta import relativedelta 
from datetime import date
from django.core.validators import FileExtensionValidator
from PIL import Image
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  # For raising validation errors from save method
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError

