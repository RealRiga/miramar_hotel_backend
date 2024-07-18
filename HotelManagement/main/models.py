from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, PermissionsMixin

class User(AbstractUser, PermissionsMixin):
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='main_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='main_user_permission_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    class Meta:
        app_label = 'main'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

class Room(models.Model):
    destTitle = models.CharField(max_length=100)
    desc = models.TextField()
    beds = models.CharField(max_length=50)
    wifi = models.BooleanField(default=True)
    bathtub = models.BooleanField(default=False)
    shuttle = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.destTitle

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    approved = models.BooleanField(default=False)

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.email}'

class Offer(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)
    beds = models.IntegerField(default=1)
    bathtub = models.IntegerField(default=1)
    wifi = models.BooleanField(default=True)
    shuttle = models.BooleanField(default=False)
    image = models.ImageField(upload_to='offers/')

    def __str__(self):
        return self.title
