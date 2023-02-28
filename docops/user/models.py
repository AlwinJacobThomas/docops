from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

from django.db.models.signals import post_save
from django.dispatch import receiver
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
        
#------------Patient------------------------------        
class PatientManager(BaseUserManager):
     def get_queryset(self,*args,**kwargs):
          results = super().get_queryset(*args,**kwargs)
          return results.filter(role=User.Role.PATIENT)
#patient role class     
class Patient(User):
    base_role = User.Role.PATIENT

    patient = PatientManager()

    class Meta:
            proxy = True

#Automatic creation of UserProfile during UserCreation
@receiver(post_save,sender=Patient)
def create_user_profile(sender,instance,created,**kwargs):
     if created and instance.role == "PATIENT":
          PatientProfile.objects.create(user=instance)

#userprofile to created user
class PatientProfile(models.Model):
     user = models.OneToOneField(User,on_delete=models.CASCADE)
     patient_id = models.IntegerField(null=True,blank=True)

     def __str__(self):
          return self.user.username
#---------------Doctor---------------------------------------- 
class DoctorManager(BaseUserManager):
     def get_queryset(self,*args,**kwargs):
          results = super().get_queryset(*args,**kwargs)
          return results.filter(role=User.Role.DOCTOR)
#doctor role class     
class Doctor(User):
    base_role = User.Role.DOCTOR

    doctor = DoctorManager()

    class Meta:
            proxy = True

#Automatic creation of UserProfile during UserCreation
@receiver(post_save,sender=Doctor)
def create_user_profile(sender,instance,created,**kwargs):
     if created and instance.role == "DOCTOR":
          DoctorProfile.objects.create(user=instance)

#userprofile to created user
class DoctorProfile(models.Model):
     user = models.OneToOneField(User,on_delete=models.CASCADE)
     doctor_id = models.IntegerField(null=True,blank=True)

     def __str__(self):
          return self.user.username
