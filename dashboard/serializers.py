from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Address, Client, Invoice

UserModel = User

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )

        return user

    class Meta:
        model = UserModel
        fields = ('id', 'username', "password", 'first_name', 'last_name', 'email')

class SupplierSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'email')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'street')

class ClientSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    supplier = SupplierSerializer()
    
    def create (self, validated_data):
        address_data = validated_data.pop('address')
        user_data = validated_data.pop('supplier')
        user_id = self.context.get('user_id')
        
        # address_serializer = AddressSerializer(data=address_data)
        # address_serializer.is_valid(raise_exception=True)
        # address = address_serializer.save()

        user = User.objects.get(id=user_id)
        address = Address.objects.all()
        print(address)

        client = Client.objects.create(
            address=address, 
            supplier=user, 
            **validated_data)
        
        return client

    class Meta:
        model = Client
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    supplier = UserSerializer()
    client = ClientSerializer()
    class Meta:
        model = Invoice
        fields = '__all__'
