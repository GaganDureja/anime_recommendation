import requests
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from .serializers import *
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import User
from .models import UserPreferences
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser

User = get_user_model()

'''
Anime Queries
'''


# Anilist Graphql
url = "https://graphql.anilist.co"

search_query = """
query ($search: String, $genres: [String], $minScore: Int, $maxScore: Int) {
  Media(search: $search, type: ANIME, genre_in: $genres, averageScore_greater: $minScore, averageScore_lesser: $maxScore) {
    id
    title {
      romaji
      english
      native
    }
    description
    genres
    averageScore
  }
}
"""

recommendation_query = """
query ($animeId: Int) {
    Media(id: $animeId) {
    id
    title {
        romaji
        english
        native
    }
    description
    genres
    averageScore
    recommendations(sort: ID_DESC) {
        edges {
        node {
            mediaRecommendation {
            id
            title {
                romaji
                english
                native
            }
            genres
            averageScore
            description
            }
        }
        }
    }
    }
}
"""
def make_request(query, variables):
    response = requests.post(url, json={"query": query, "variables": variables})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("No data found kindly retry again.")



"""
Authentication Management
"""
def UserAuthenticate(username,password):
    user = User.objects.get(username=username)
    if user:
        if user.check_password(password):
            return user
        else:
            return None

class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="User Signup",
        operation_description="User Signup",
        manual_parameters=[
            openapi.Parameter('first_name', openapi.IN_FORM, type=openapi.TYPE_STRING ,description='First Name'),
            openapi.Parameter('last_name', openapi.IN_FORM, type=openapi.TYPE_STRING ,description='Last Name'),
            openapi.Parameter('username', openapi.IN_FORM, type=openapi.TYPE_STRING ,description='Username'),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Password'),
            openapi.Parameter('confirm_password', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Confirm Password'),
        ]
    )
    def post(self, request, *args, **kwargs):
        if User.objects.filter(username=request.data.get('username')):
            return Response({"message":"There is already a registered user with this username.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('password') == request.data.get('confirm_password'):
            return Response({"message":"Password and Confirm password doesn't match!.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(
            first_name = request.data.get('first_name'),
            last_name = request.data.get('last_name'),
            username = request.data.get('username'),
            password = make_password(request.data.get('password')),
        )
        try:
            token=Token.objects.get(user = user)
        except:
            token=Token.objects.create(user = user)
        data = UserSerializer(user,context = {"request":request}).data
        return Response({"message":"User registered successfully!","data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="User Login ",
        operation_description="User Login ",
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Username'),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Password'),
        ]
    )

    def post(self, request, *args, **kwargs):

        if not request.data.get('username') :
            return Response({"message":("Please login using username"),"status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('username'):
            try:
                user = User.objects.get(username=request.data.get('username'))
            except:
                return Response({"message":("Invalid Login Credentials."), "status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if not user:
            return Response({"message":("Invalid Login Credentials."), "status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserAuthenticate(username = request.data.get("username").strip(),password = request.data.get("password").strip())
        except:
            return Response({"message":("Invalid Login Credentials."), "status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if user :
            Token.objects.filter(user=user).delete()
            login(request,user)
        else:
            return Response({"message":("Invalid Login Credentials."),"status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        data = UserSerializer(user,context = {"request":request}).data
        return Response({"message":("Logged in successfully"),"data":data,"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)

class UserPreferencesView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        tags=["User Preferences API's"],
        operation_id="User Preferences",
        operation_description="Save or Update User Preferences",
        manual_parameters=[
            openapi.Parameter('fav_genres', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='Favorite Genres'),
            openapi.Parameter('min_score', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='Minimum Score'),
            openapi.Parameter('max_score', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='Maximum Score'),
        ]
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        data = {
            "fav_genres": request.data.get('fav_genres', []),
            "min_score": request.data.get('min_score', 0),
            "max_score": request.data.get('max_score', 100)
        }

        user_preferences, created = UserPreferences.objects.get_or_create(user=user)
        for key, value in data.items():
            setattr(user_preferences, key, value)
        user_preferences.save()

        return Response({"message": "User preferences saved/updated successfully.", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)



class AnimeSearch(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        tags=["Anime API's"],
        operation_id="Anime Search",
        operation_description="Search Anime by Title",
        manual_parameters=[openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Anime Title')]
    )
    def get(self, request, *args, **kwargs):
        search_query_param = request.query_params.get('search')
        if not search_query_param:
            return Response({"message": "Search query is required.", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


        user = request.user
        user_preferences = UserPreferences.objects.filter(user=user).first()


        genres = user_preferences.fav_genres if user_preferences else []
        min_score = user_preferences.min_score if user_preferences else 0
        max_score = user_preferences.max_score if user_preferences else 100


        variables = {
            "search": search_query_param,
            "genres": genres if genres else None,
            "minScore": min_score,
            "maxScore": max_score
        }

        try:
            result = make_request(search_query, variables)
            anime_data = result.get('data', {}).get('Media', None)

            if anime_data is None:
                return Response({"message": "Anime not found.", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "Search results.", "data": anime_data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Not Found.", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


class AnimeRecommendation(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        tags=["Anime API's"],
        operation_id="Anime Recommendations",
        operation_description="Fetch Anime Recommendations",
        manual_parameters=[openapi.Parameter('anime_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Anime ID')]
    )
    def get(self, request, *args, **kwargs):
        anime_id = request.query_params.get('anime_id')
        if not anime_id:
            return Response({"message": "anime_id is required.", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user_preferences = UserPreferences.objects.filter(user=user).first()


        genres = user_preferences.fav_genres if user_preferences else []
        min_score = user_preferences.min_score if user_preferences else 0
        max_score = user_preferences.max_score if user_preferences else 100


        variables = {"animeId": anime_id}

        try:
            result = make_request(recommendation_query, variables)
            recommendations = result.get('data', {}).get('Media', {}).get('recommendations', {}).get('edges', [])

            filtered_recommendations = [
                rec['node']['mediaRecommendation']
                for rec in recommendations
                if (
                    not genres or any(genre in genres for genre in rec['node']['mediaRecommendation']['genres'])
                ) and (
                    min_score <= rec['node']['mediaRecommendation']['averageScore'] <= max_score
                )
            ]

            if not filtered_recommendations:
                return Response({"message": "No recommendations found matching user preferences.", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "Recommendations found.", "data": filtered_recommendations, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Not Found.", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
