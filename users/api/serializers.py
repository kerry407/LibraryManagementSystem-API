from django.contrib.auth.models import User 
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class AccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})
    
    class Meta:
        model = User 
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }
        
    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("The two passwords do not match")
        return data 
    
    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = make_password(validated_data["password"])
        confirm_account = User.objects.filter(email=email)
        if confirm_account.exists():
            raise serializers.ValidationError("An account already exists with this email")
        new_account = User(username=username, email=email, password=password)
        new_account.save()
        return new_account