from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from datetime import date


# now = timezone.now()
# Create your models here.


class Prescription(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instructions = models.TextField(
        max_length=250, default='Please refer to the instructions provided by your doctor or pharmacist.')
    date_issued = models.DateField('Prescription Date', default=date.today)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('prescription_index')


class Care_provider(models.Model):
    name = models.CharField(max_length=50)
    facility = models.CharField(max_length=75)
    department = models.CharField(max_length=50)

    # Many to many relationship for patients >--< care providers
    users = models.ManyToManyField(User)

    def delete(self, *args, **kwargs):
        # Remove the relationship with users
        self.users.clear()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        User = get_user_model()
        user = User.objects.get(id=self.users.first().id)
        return reverse('users_detail', kwargs={'user_id': user.id})


class Appointment(models.Model):
    date = models.DateField('Appointment Date')
    time = models.TimeField('Appointment Time')
    location = models.CharField(max_length=75)
    purpose = models.TextField(max_length=250, default='Check up')
    care_provider = models.ForeignKey(
        Care_provider, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('users_detail', kwargs={'user_id': self.user_id})


class Photo(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for user: {self.user.id} @{self.url}"


@receiver(post_delete, sender=Photo)
def delete_image_file(sender, instance, **kwargs):
    if instance.url:
        file_path = instance.url.split(
            settings.AWS_STORAGE_BUCKET_NAME + '/')[1]
        if default_storage.exists(file_path):
            default_storage.delete(file_path)


post_delete.connect(delete_image_file, sender=Photo)
