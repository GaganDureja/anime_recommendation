from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    email=models.EmailField(blank=True,null=True)
    username=models.EmailField(unique=True,blank=True,null=True)
    first_name=models.CharField(max_length=100,blank=True,null=True)
    last_name=models.CharField(max_length=100,blank=True,null=True)

    class Meta:
        managed = True
        default_permissions = ()
        db_table = 'user'

    def __str__(self):
        return str(self.first_name)


class UserPreferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fav_genres = models.JSONField(default=list)
    min_score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=100)

    def __str__(self):
        return f"Preferences "
