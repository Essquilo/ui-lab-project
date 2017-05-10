from django.contrib import auth
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from shop import serializers
from shop.models import ShopItem
from .serializers import UserSerializer, ShopItemSerializer


def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        print('User ' + str(request.user))
        return render(request, 'index.html', {'title': 'Shop'})


def register(request):
    return render(request, 'register.html', {'title': 'Register'})


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'login.html', {'title': 'Login'})


class Register(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer


class Login(APIView):
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        credentials = serializers.LoginSerializer(data=request.data)

        if not credentials.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = auth.authenticate(username=credentials.validated_data['username'],
                                 password=credentials.validated_data['password'])

        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Okay, security check complete. Log the user in.
        auth.login(request, user)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopItemsList(generics.ListAPIView):
    serializer_class = ShopItemSerializer

    def get_queryset(self):
        """
        This view should return a list of all the items for
        the user as determined by the username portion of the URL.
        """
        queryset = ShopItem.objects.all()

        packaging = self.request.query_params.getlist('manufacturer', None)
        manufacturer = self.request.query_params.getlist('manufacturer', None)
        designation = self.request.query_params.getlist('designation', None)
        max_cost = self.request.query_params.get('max_cost', None)
        min_cost = self.request.query_params.get('min_cost', None)
        name = self.request.query_params.get('name', None)

        if packaging is not None:
            queryset = queryset.filter(packaging__id__in=packaging)
        if manufacturer is not None:
            queryset = queryset.filter(manufacturer__id__in=manufacturer)
        if designation is not None:
            queryset = queryset.filter(designation__id__in=designation)
        if max_cost is not None:
            queryset = queryset.filter(cost__lte=max_cost)
        if min_cost is not None:
            queryset = queryset.filter(cost__gte=min_cost)
        if name is not None:
            queryset = queryset.filter(name__startswith=name)
        return queryset


@api_view(['POST'])
def logout(request):
    auth.logout(request)
    return Response({}, status=status.HTTP_204_NO_CONTENT)
