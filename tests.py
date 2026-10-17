from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from .models import Booking, MenuItem

class MenuAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item = MenuItem.objects.create(title="Greek Salad", price=Decimal("12.50"), inventory=20)

    def test_menu_list_is_public(self):
        response = self.client.get("/api/menu/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["title"], "Greek Salad")

    def test_unauthenticated_user_cannot_create_menu_item(self):
        response = self.client.post("/api/menu/", {
            "title": "Bruschetta", "price": "8.00", "inventory": 10
        }, format="json")
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_can_create_menu_item(self):
        user = get_user_model().objects.create_user(username="chef", password="TestPass123!")
        self.client.force_authenticate(user=user)
        response = self.client.post("/api/menu/", {
            "title": "Bruschetta", "price": "8.00", "inventory": 10
        }, format="json")
        self.assertEqual(response.status_code, 201)

class BookingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username="guest", password="TestPass123!")
        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_can_create_booking(self):
        response = self.client.post("/api/booking/tables/", {
            "name": "Alex", "no_of_guests": 2,
            "booking_date": (timezone.now() + timedelta(days=1)).isoformat()
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/booking/tables/")
        self.assertEqual(response.status_code, 401)

    def test_users_only_see_their_own_bookings(self):
        other = get_user_model().objects.create_user(username="other", password="TestPass123!")
        Booking.objects.create(name="Other", no_of_guests=1,
                               booking_date=timezone.now() + timedelta(days=2), user=other)
        response = self.client.get("/api/booking/tables/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
