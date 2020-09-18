from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ExifTags
from django.templatetags.static import static


# Create your models here.

class Profile(models.Model):
    GenderChoice = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pics")
    gender = models.CharField(max_length=6, choices=GenderChoice)
    birthdate = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}s profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)

                try:
                    image_exif = img._getexif()
                    image_orientation = image_exif[274]
                    if image_orientation in (2, '2'):
                        return img.transpose(Image.FLIP_LEFT_RIGHT)
                    elif image_orientation in (3, '3'):
                        return img.transpose(Image.ROTATE_180)
                    elif image_orientation in (4, '4'):
                        return img.transpose(Image.FLIP_TOP_BOTTOM)
                    elif image_orientation in (5, '5'):
                        return img.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)
                    elif image_orientation in (6, '6'):
                        return img.transpose(Image.ROTATE_270)
                    elif image_orientation in (7, '7'):
                        return img.transpose(Image.ROTATE_270).transpose(Image.FLIP_TOP_BOTTOM)
                    elif image_orientation in (8, '8'):
                        return img.transpose(Image.ROTATE_90)
                    else:
                        return img

                except (KeyError, AttributeError, TypeError, IndexError):
                    return img

            img.save(self.image.path)
