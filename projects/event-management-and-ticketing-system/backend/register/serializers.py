from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from .models import Contact
from django.contrib.auth.hashers import make_password


class ContactSerializer(serializers.ModelSerializer):
    # # uniqueness validation of username and email fields 
    username = serializers.CharField(
        max_length = 100,
        validators = [UniqueValidator(queryset=Contact.objects.all())]
        )
    
    email = serializers.EmailField(
        validators = [UniqueValidator(queryset=Contact.objects.all())]
        )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'username', 'password1', 'password2']
        extrta_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True},
            # By providing extra_kwargs in this manner, we are explicitly specifying that 
            # password1 and password2 fields should be treated as write-only, 
            # meaning they will not be included in the serialized representation of the object. 
            # This ensures that the password fields are used for deserialization only, 
            # such as during user creation or update, 
            # but are not exposed in the API response or any serialized output.


            
            # 'email': {'validators': []}
            # To bypass the UniqueValidator for update operations
            # By setting an empty list ([]) as the validators for the email field, 
            # we are effectively removing any validators for that field, including the UniqueValidator. 
            # This allows updates to the email field without triggering uniqueness checks.
            
        }



    # creating a new user with the given validated data 
    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")

        validated_data['password'] = make_password(password1)

        # Create the user object
        user = User.objects.create(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        
        # Save the user object
        user.save()

        """
        # alternative way to create the user object
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        """        
        
        # Create the YourModel object
        new_contact = Contact.objects.create(**validated_data)

        return new_contact
    
    """
    def create(self, validated_data):
        
        return user
    """