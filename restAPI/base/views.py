from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication


from rest_framework_simplejwt.tokens import RefreshToken

class PersonAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    
    def get(self, request):

        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many = True)
        return Response({"payload": serializer.data})
    
    def post(self, request):

        data = request.data
        serializer = PersonSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({"payload": serializer.data})
        
        return Response({"error": serializer.errors})

class Authorization(APIView):

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        
        if not serializer.is_valid():
            return Response({"error": serializer.errors})
        
        serializer.save()

        user = User.objects.get(username = serializer.data['username'])
        # token, _ = Token.objects.get_or_create(user=user)
        refresh = RefreshToken.for_user(user)


        return Response({"message": str(refresh.access_token)})
