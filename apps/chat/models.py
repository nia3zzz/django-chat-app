from config.models import BaseModel
from django.db import models
from apps.user.models import User


# a database table that will store all the chats between users
class Chat(BaseModel):
    class UserStatus(models.TextChoices):
        DIRECTMESSAGE = "DM", "Direct Message"
        GROUPCHAT = "GC", "Group Chat"

    type = models.CharField(max_length=2, choices=UserStatus.choices)

    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Chat type={self.type}, name={self.name}"


# a database table that will store all chat members
class ChatMember(BaseModel):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="members")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_memberships"
    )

    last_read_message = models.ForeignKey(
        "message.Message",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="last_read_by",
    )

    def __str__(self):
        return f"ChatMember {self.user.email} type={self.chat.type}"
