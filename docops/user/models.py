from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.

class User(AbstractUser):
    #adding custom field "role" in default User model
    class Role(models.TextChoices):
        ADMIN = "ADMIN",'Admin'
        DOCTOR = "DOCTOR",'Doctor'
        PATIENT = "PATIENT",'Patient'

    base_role = Role.ADMIN

    role = models.CharField(max_length=50,choices=Role.choices)
     
    def save(self,*args,**kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args,**kwargs)
        
class PatientManager(BaseUserManager):
     def get_queryset(self,*args,**kwargs):
          results = super().get_queryset(*args,**kwargs)
          return results.filter(role=User.Role.PATIENT)
     
class Patient(User):
    base_role = User.Role.PATIENT

    patient = PatientManager()

    class Meta:
            proxy = True

class DoctorManager(BaseUserManager):
     def get_queryset(self,*args,**kwargs):
          results = super().get_queryset(*args,**kwargs)
          return results.filter(role=User.Role.DOCTOR)
     
class Doctor(User):
    base_role = User.Role.DOCTOR

    doctor = DoctorManager()

    class Meta:
            proxy = True