Little Lemon REST API — peer review guide

SETUP
1. Install Python 3.11+ and MySQL.
2. Create a MySQL database:
   CREATE DATABASE littlelemon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
3. Copy .env.example to .env and set your local MySQL credentials.
4. Run:
   pip install pipenv
   pipenv install
   pipenv shell
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver

The site is served at http://127.0.0.1:8000/
Django admin is at http://127.0.0.1:8000/admin/

API PATHS TO TEST IN INSOMNIA
Menu:
  GET    http://127.0.0.1:8000/api/menu/
  GET    http://127.0.0.1:8000/api/menu/1/
  POST   http://127.0.0.1:8000/api/menu/
  PUT    http://127.0.0.1:8000/api/menu/1/
  PATCH  http://127.0.0.1:8000/api/menu/1/
  DELETE http://127.0.0.1:8000/api/menu/1/

Bookings (authenticated):
  GET    http://127.0.0.1:8000/api/booking/tables/
  GET    http://127.0.0.1:8000/api/booking/tables/1/
  POST   http://127.0.0.1:8000/api/booking/tables/
  PUT    http://127.0.0.1:8000/api/booking/tables/1/
  PATCH  http://127.0.0.1:8000/api/booking/tables/1/
  DELETE http://127.0.0.1:8000/api/booking/tables/1/

Authentication:
  POST   http://127.0.0.1:8000/auth/users/
  POST   http://127.0.0.1:8000/auth/token/login/
  POST   http://127.0.0.1:8000/auth/token/logout/

For POST /api/menu/ JSON example:
{
  "title": "Greek Salad",
  "price": "12.50",
  "inventory": 20
}

For POST /api/booking/tables/ JSON example:
{
  "name": "Adil",
  "no_of_guests": 2,
  "booking_date": "2026-12-13T19:00:00Z"
}

For authentication:
1. POST /auth/users/ with {"username":"reviewer1","password":"StrongPass123!"}
2. POST /auth/token/login/ with the same credentials.
3. Copy the returned auth_token value.
4. In Insomnia, add header:
   Authorization: Token YOUR_TOKEN
5. Use this header for booking endpoints and for protected menu write requests.

IMPORTANT
- Menu listing/detail is public; creating/updating/deleting menu items requires authentication.
- Booking endpoints require authentication.
- Use a valid menu item ID / booking ID for detail, update, and delete requests.
- This is a starter implementation. Configure MySQL locally and run the tests before submitting.
