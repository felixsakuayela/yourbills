from django.db import models
from django.contrib.auth.models import User
import reversion


@reversion.register
class Expense(models.Model):
    name = models.CharField(max_length=48)
    user_create = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
@reversion.register
class Spent(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=48, null=True, blank=True)
    date = models.DateField()
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spents')
    users_shared = models.ManyToManyField(User, related_name='share_request', blank=True)
    active = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

@reversion.register
class ShareRequest(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Refused'),
    ]
    spent = models.ForeignKey(Spent, on_delete=models.CASCADE)
    user_requesting = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_made')
    user_approving = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_received')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    date_create = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.status
