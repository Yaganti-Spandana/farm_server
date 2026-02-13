from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

from .models import Animal,MilkRecord,Sale,Expense,FeedStock,FeedUsage

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = "__all__"

class MilkRecordSerializer(serializers.ModelSerializer):
    animal_name = serializers.CharField(source="animal.name", read_only=True)

    class Meta:
        model = MilkRecord
        fields = "__all__"

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = "__all__"

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Expense
        fields = "__all__"

class FeedStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedStock
        fields = "__all__"

class FeedUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedUsage
        fields = "__all__"
