from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings
from django.db.models.deletion import SET_NULL


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and saves a new user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that supports email as username"""
    email = models.EmailField(verbose_name='ایمیل', max_length=255,
                              unique=True)
    name = models.CharField(verbose_name='نام', max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tags to be used for animal"""
    name = models.CharField(verbose_name='تگ', max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=SET_NULL
    )

    class Meta:
        verbose_name = "تگ ها"
        verbose_name_plural = "تگ ها"

    def __str__(self):
        return self.name


class WorkGroup(models.Model):
    """WorkGroups for animals"""
    name = models.CharField(verbose_name='نام کارگروه', max_length=255,
                            unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=SET_NULL,
        verbose_name='کاربر'
    )

    class Meta:
        verbose_name = "کارگروه"
        verbose_name_plural = "کارگروه ها"

    def __str__(self):
        return self.name


class Animal(models.Model):
    """Animal Profile"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=SET_NULL,
        verbose_name='کاربر'
    )
    species = models.CharField(
        verbose_name="گونه",
        default='dog',
        max_length=255,
        )
    breed = models.CharField(max_length=255, verbose_name="نژاد", blank=True)
    name = models.CharField(max_length=255, verbose_name="نام",
                            blank=False)
    age = models.CharField(max_length=255, verbose_name="سن")
    gender = models.CharField(max_length=255, verbose_name="جنسیت", default='')
    support = models.CharField(verbose_name='نام حامی',
                               max_length=255,
                               default='ندارد'
                               )
    visit_cost = models.IntegerField(verbose_name='هزینه ویزیت', default=0)
    med_cost = models.IntegerField(verbose_name='هزینه دارو', default=0)
    op_cost = models.IntegerField(verbose_name='هزینه عمل', default=0)
    food_cost = models.IntegerField(verbose_name='هزینه غذا', default=0)
    keep_cost = models.IntegerField(verbose_name='هزینه نگهداری', default=0)
    sum_cost = models.IntegerField(verbose_name="جمع هزینه ها", default=0)
    work_group = models.ManyToManyField('WorkGroup', verbose_name='کارگروه',
                                        blank=True)
    tags = models.ManyToManyField('Tag', verbose_name='تگ', blank=True)

    class Meta:
        verbose_name = "حیوان"
        verbose_name_plural = "حیوانات"

    def __str__(self):
        return str(self.species)+" "+str(self.name)
