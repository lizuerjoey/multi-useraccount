from venv import logger
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Permission
from django.contrib.contenttypes.models import ContentType

class Organisation(models.Model):
    # organisations should be unique
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    contact = models.IntegerField()

# inherits from BaseUserManager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # raise error if email is not provided
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email) # converts to lowercase for consistency
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # sets the password and hashes it
        user.save(using=self._db)

        return user # returns the created user object
    
    def assign_permissions(self, user):
        content_type = ContentType.objects.get_for_model(user)
        if user.role in ['Admin', 'Co-Admin']:
            permissions = Permission.objects.filter(content_type=content_type, codename__in=['add_members', 'view_members'])
        elif user.role == 'Member':
            permissions = Permission.objects.filter(content_type=content_type, codename__in=['view_members'])

        user_permission, created = CustomUserPermission.objects.get_or_create(user=user)
        user_permission.permissions.set(permissions)

    # Superusers are required to use the Django admin page
    # def create_superuser(self, name, email, password, **extra_fields):
    #     extra_fields.setdefault('is_member', True) # default true for superuser
    #     extra_fields.setdefault('is_admin', True) # default true for superuser
    #     return self.create_user(name, email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True) # email must be unique
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organisation, on_delete=models.CASCADE) # creates an organisation
    role = models.CharField(max_length=255)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'organization', 'role']

    def __str__(self):
        return self.email
        
    class Meta:
        ordering = ['name']  # Order users by name
        permissions = [
            ('add_members', 'Add members to an organisation'),  # Set custom permissions
            ('view_members', 'View members of an organisation')
        ]

class CustomUserPermission(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission)