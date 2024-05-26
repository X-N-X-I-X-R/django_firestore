from django.utils import timezone
from dateutil.relativedelta import relativedelta



# validation for birth date 
def validate_birth_date(value):
    today = timezone.now().date()
    if value > today or value < today - relativedelta(years=18):
        raise ValidationError("Invalid birth date")

def default_date():
    return timezone.now().date() - relativedelta(years=18)

def validate_image_file_size(value):
    valid_types = ["image/png", "image/jpg", "image/jpeg", "image/gif", "image/bmp", "image/webp", "image/svg+xml", "image/tiff", "image/vnd.microsoft.icon", "image/vnd.wap.wbmp", "image/x-icon", "image/x-jng", "image/x-ms-bmp", "image/x-portable-bitmap", "image/x-xbitmap", "image/x-xpixmap", "image/x-xwindowdump"]
    
    if value.content_type not in valid_types:
        raise ValidationError("Unsupported file type")
    
    filesize = value.size
    
    if filesize < 4000000 or filesize > 7000000:  # 4MB to 7MB
        raise ValidationError("The file size must be between 4MB and 7MB")

def default_image():
    return "myapp/public/default.jpeg"

def validate_country():
    valid_countries = ['USA', 'UK', 'CAN', 'AUS', 'IND', 'GER', 'FRA', 'ITA', 'SPA', 'BRA', 'JPN', 'CHN', 'RUS', 'MEX', 'ARG', 'COL', 'PER', 'CHI', 'IL', 'EGY', ]
    return valid_countries