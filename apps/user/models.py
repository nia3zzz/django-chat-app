from config.models import BaseModel
from django.db import models


# defining a database table to store user information
class User(BaseModel):
    name = models.CharField(max_length=255)

    username = models.CharField(max_length=255, unique=True)

    phone_number = models.CharField(max_length=20, unique=True)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=255)

    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class UserProfile(BaseModel):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        BUSY = "busy", "Busy"
        OFFLINE = "offline", "Offline"

    class ColorTheme(models.TextChoices):
        LIGHT = "light", "Light"
        DARK = "dark", "Dark"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    bio = models.TextField(blank=True)

    avatar = models.TextField(
        blank=True,
        default="https://static.vecteezy.com/system/resources/previews/020/765/399/non_2x/default-profile-account-unknown-icon-black-silhouette-free-vector.jpg",
    )

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.ACTIVE
    )

    color_theme = models.CharField(
        max_length=10, choices=ColorTheme.choices, default=ColorTheme.LIGHT
    )

    def __str__(self):
        return f"{self.user.name}'s Profile"
