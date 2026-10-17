from rest_framework import serializers
from .models import Booking, MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "inventory"]

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "name", "no_of_guests", "booking_date", "user"]
        read_only_fields = ["id", "user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
