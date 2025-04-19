from django.db import models
from UserModule.models import User

STATUS_CHOICES = [
    ('open', 'Open'),
    ('closed', 'Closed'),
    ('pending', 'Pending'),
]

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]


class Ticket(models.Model):
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    subject = models.CharField(max_length=255)
    related_order_id = models.CharField(max_length=30, null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.subject}"


class Message(models.Model):
    SENDER_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    ]

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    text = models.TextField()
    timestamp = models.DateTimeField()

    message = models.TextField()
    file_id = models.CharField(max_length=30, unique=True)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField()
    file_url = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.id} ({self.sender})"
