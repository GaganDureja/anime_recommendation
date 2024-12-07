from rest_framework.serializers import ModelSerializer
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields= ("id","first_name","last_name","username")


class UserPreferencesSerializer(ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['fav_genres', 'min_score', 'max_score']
