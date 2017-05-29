from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

from rest_framework import serializers

from shop.models import ShopItem, Packaging, Manufacturer, Designation, Profile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'date_joined',
                  'first_name', 'last_name', 'password',
                  'confirm_password',)
        read_only_fields = ('date_joined', 'id')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.profile = Profile()
        user.save()

        return user

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)
        if not confirm_password and not User.objects.get_by_natural_key(username=username).check_password(password):
            raise serializers.ValidationError("Incorrect username/password pair.")
        if confirm_password and password != confirm_password:
            raise serializers.ValidationError("Passwords don't match.")
        data.pop('confirm_password')
        return data

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        password = validated_data.get('password', None)
        instance.set_password(password)
        instance.save()
        update_session_auth_hash(self.context.get('request'), instance)
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=128)


class PackagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packaging
        fields = ('id', 'name')


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('id', 'name')


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ('id', 'name')


class ShopItemSerializer(serializers.ModelSerializer):
    packaging = PackagingSerializer()
    manufacturer = ManufacturerSerializer()
    designation = DesignationSerializer()

    class Meta:
        model = ShopItem
        fields = ('id', 'packaging', 'manufacturer', 'designation', 'name', 'cost', 'img')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopItem
        fields = ('id', )
