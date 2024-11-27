from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
class BloodTestRecord(models.Model):
    patient_id = models.IntegerField()
    test_name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    test_date = models.DateTimeField()
    is_abnormal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.test_name} for Patient {self.patient_id}"
