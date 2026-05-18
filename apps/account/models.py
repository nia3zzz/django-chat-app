from config.models import BaseModel
from django.db import models
from apps.user.models import User


# a database table that will store all the hashed codes for the users this is for login, password changes etc
class HashedCode(BaseModel):
    code = models.CharField(max_length=255)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hashed_codes"
    )

    def __str__(self):
        return f"HashedCode for {self.user.email}"


# a database table that will store all the sessions for the users
class RefreshSession(BaseModel):
    session_token = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")

    def __str__(self):
        return f"Refresh session for {self.user.email}"
