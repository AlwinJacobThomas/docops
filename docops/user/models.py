from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
#-------------------USER-------------------------
#--------usermanager----------
class UserAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        if other_fields.get('is_admin') is not True:
            raise ValueError(
                'Superuser must be assigned to is_admin=True.')

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email,
                            **other_fields)
        user.set_password(password)
        user.save()
        return user
    
#--------user----------
class User(AbstractBaseUser,PermissionsMixin):
    #adding custom field "role" in default User model
    class Role(models.TextChoices):
        ADMIN = "ADMIN",'Admin'
        DOCTOR = "DOCTOR",'Doctor'
        PATIENT = "PATIENT",'Patient'

    base_role = Role.ADMIN
    
    role = models.CharField(max_length=50,choices=Role.choices,default=Role.ADMIN)
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
      
    # special permission which define that
    # the new user is doctor or patient 
    is_doctor = models.BooleanField(default = False)
    is_patient = models.BooleanField(default = False)
    
      
    USERNAME_FIELD = "email"
      
    # defining the manager for the UserAccount model
    objects = UserAccountManager()
      
    def __str__(self):
        return str(self.email)
      
    def has_perm(self , perm, obj = None):
        return self.is_admin
      
    def has_module_perms(self , app_label):
        return True
    def save(self,*args,**kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args,**kwargs)
        
#------------Patient------------------------------        
class PatientManager(models.Manager):

     # def create_user(self , email , password = None):
     #    if not email or len(email) <= 0 : 
     #        raise  ValueError("Email field is required !")
     #    if not password :
     #        raise ValueError("Password is must !")
     #    email  = email.lower()
     #    user = self.model(
     #        email = email
     #    )
     #    user.set_password(password)
     #    user.save(using = self._db)
     #    return user    

     def get_queryset(self,*args,**kwargs):
          results = super().get_queryset(*args,**kwargs)
          return results.filter(role=User.Role.PATIENT)
#patient proxy class  for setting baserole    
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
     first_name = models.CharField(max_length=150, blank=True)
     last_name = models.CharField(max_length=150, blank=True)
     address = models.CharField(max_length=50,null=True,blank=True)

     def __str__(self):
          return self.user.username
#---------------Doctor---------------------------------------- 
class DoctorManager(models.Manager):
     # def create_user(self , email , password = None):
     #    if not email or len(email) <= 0 : 
     #        raise  ValueError("Email field is required !")
     #    if not password :
     #        raise ValueError("Password is must !")
     #    email  = email.lower()
     #    user = self.model(
     #        email = email
     #    )
     #    user.set_password(password)
     #    user.save(using = self._db)
     #    return user    
     
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
     first_name = models.CharField(max_length=150, blank=True)
     last_name = models.CharField(max_length=150, blank=True)

     def __str__(self):
          return self.user.username
