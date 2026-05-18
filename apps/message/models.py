from config.models import BaseModel
from django.db import models
from apps.user.models import User


# defining a database table to store messages
class Message(BaseModel):
    chat = models.ForeignKey("chat.Chat", on_delete=models.CASCADE, related_name="messages")

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )

    content = models.TextField()

    def __str__(self):
        return f"Message from {self.sender} in {self.chat.name}"


# defining a database table to store message status
class MessageStatus(BaseModel):
    class Status(models.TextChoices):
        SENT = "SENT", "Sent"
        DELIVERED = "DELIVERED", "Delivered"
        READ = "READ", "Read"

    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="statuses"
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="message_statuses"
    )

    status = models.CharField(max_length=10, choices=Status.choices)

    def __str__(self):
        return f"{self.user.email} has got {self.status} message"
