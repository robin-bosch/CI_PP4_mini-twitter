'''
Account models

IMPORTANT:
Contains the custom user model which replaces the django model
'''
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, \
                                       BaseUserManager, \
                                       PermissionsMixin


# Models
class CustomUserManager(BaseUserManager):
    '''
    Custom user manager
    '''
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and save a user with the given email, password, and username.
        """
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)

        user = self.model(email=email, username=username, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        '''
        Creates a superuser
        '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    '''
    Custom User model
    '''
    email = models.EmailField(
        unique=True
    )

    username = models.TextField(
        max_length=50,
        unique=True
    )

    user_picture = models.URLField(
        blank=True
    )

    user_text = models.TextField(
        blank=True
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    def switch_active(self):
        '''
        Switches the is_active field
        This is used as an action in the admin panel
        '''
        self.is_active = not self.is_active
        self.save()

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
