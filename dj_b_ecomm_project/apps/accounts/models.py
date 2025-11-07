from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Allow Unicode letters, numbers, and special characters
unicode_username_validator = RegexValidator(
    regex=r'^[\w.@+\-_\u00C0-\uFFFF]+$',
    message="Enter a valid username. Unicode letters, numbers, and @/./+/-/_ characters only."
)


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Basic', 'Basic'),
        ('Advanced', 'Advanced'),
        ('Professional', 'Professional'),
        ('Admin', 'Admin'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='basic'
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[unicode_username_validator],
    )
    analytics_level = models.CharField(
    max_length=20,
    default="Basic",
    choices=[
        ("Basic", "Basic"),
        ("Advanced", "Advanced"),
        ("Professional", "Professional"),
    ]
)
    display_name = models.CharField(max_length=150, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    is_private = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    dark_mode = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.role in ["Basic", "Advanced", "Professional"]:
            self.analytics_level = self.role
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['username']

    def __str__(self):
        return self.display_name or self.username or "Unnamed User"

    @property
    def profile_status(self):
        return "Private" if self.is_private else "Public"


class Block(models.Model):
    blocker = models.ForeignKey(CustomUser, related_name='blocking', on_delete=models.CASCADE)
    blocked = models.ForeignKey(CustomUser, related_name='blocked_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Block"
        verbose_name_plural = "Blocks"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"

from django.utils.translation import gettext_lazy as _

from django.db import models
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    ROLE_CHOICES = [
        ("admin", _("Superuser")),
        ("staff", _("Staff")),
        ("active", _("Active User")),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)