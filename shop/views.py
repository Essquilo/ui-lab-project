from django.contrib import auth
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import ShopItem, Manufacturer, Packaging, Designation
from .serializers import UserSerializer, ShopItemSerializer, DesignationSerializer, ManufacturerSerializer, \
    PackagingSerializer


@api_view(['GET'])
def index(request):
    return render(request, 'index.html')


class Register(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer


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

        if packaging:
            queryset = queryset.filter(packaging__id__in=packaging)
        if manufacturer:
            queryset = queryset.filter(manufacturer__id__in=manufacturer)
        if designation:
            queryset = queryset.filter(designation__id__in=designation)
        if max_cost is not None:
            queryset = queryset.filter(cost__lte=max_cost)
        if min_cost is not None:
            queryset = queryset.filter(cost__gte=min_cost)
        if name is not None:
            queryset = queryset.filter(name__startswith=name)
        return queryset


class CartView(generics.ListAPIView):
    serializer_class = ShopItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.request.user.profile.cart
        return queryset


class PackagingList(generics.ListAPIView):
    serializer_class = PackagingSerializer
    queryset = Packaging.objects.all()


class ManufacturerList(generics.ListAPIView):
    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()


class DesignationList(generics.ListAPIView):
    serializer_class = DesignationSerializer
    queryset = Designation.objects.all()


class AddToCart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.profile.cart.add(ShopItem.objects.get(pk=request.data['id']))
        return Response({}, status=status.HTTP_200_OK)


class RemoveFromCart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.profile.cart.remove(ShopItem.objects.get(pk=request.data['id']))
        return Response({}, status=status.HTTP_200_OK)


@api_view(['POST'])
def logout(request):
    auth.logout(request)
    return Response({}, status=status.HTTP_204_NO_CONTENT)
