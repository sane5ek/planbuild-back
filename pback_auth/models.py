from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def get_queryset(self):
        return super(UserManager, self).get_queryset().select_related('science_degree', 'science_title', 'post')

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    # add additional fields here
    username = None
    email = models.EmailField('email address', unique=True, error_messages={'required': 'Пользователь с такой почтой уже существует.'})
    post = models.ForeignKey('pback_main.Post', null=True, default=None, on_delete=models.SET_DEFAULT)
    science_degree = models.ForeignKey('pback_main.ScienceDegree', null=True, default=None, on_delete=models.SET_NULL)
    science_title = models.ForeignKey('pback_main.ScienceTitle', null=True, default=None, on_delete=models.SET_NULL)
    salary = models.FloatField(null=True, default=1)
    adopted_fields = models.ForeignKey('pback_auth.User', null=True, default=None, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

