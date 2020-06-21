import base64

from django.test import TestCase

from api.models.user import User
from api.serializers.user_serializer import UserSerializer


class UserApiTestCase(TestCase):
    """
    run:
    docker-compose exec django-drf-user-api-web manage.py test api.tests.UserApiTestCase
    """

    fixtures = [
        "test_users.json",
    ]

    @classmethod
    def setUpClass(cls):
        super(UserApiTestCase, cls).setUpClass()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=1)
        cls.valid_data = {
            "username": "test_username",
            "bio": "test bio",
            "email": "john@doe.com",
            "password": "Mypasswd1",
            "first_name": "test name",
            "last_name": "test last name",
        }
        cls.valid_data_2 = {
            "username": "mr_test",
            "password": "Mypassword1",
            "bio": "test bio",
        }

    def test_user_serializer_instance(self):
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(
            set(data.keys()),
            set(["username", "email", "password", "first_name", "last_name", "bio"]),
        )
        self.assertEqual(data["username"], self.user.username)
        self.assertEqual(data["email"], self.user.email)
        self.assertEqual(data["first_name"], self.user.first_name)
        self.assertEqual(data["last_name"], self.user.last_name)
        self.assertEqual(data["bio"], self.user.bio)

    def test_user_serializer_valid_data(self):
        serializer = UserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_user_serializer_blank_data(self):
        serializer = UserSerializer(data={})
        self.assertFalse(serializer.is_valid())

    def test_get_me_without_login(self):
        response = self.client.get("/users/me/")
        self.assertEqual(response.status_code, 401)

    def test_get_me_with_basic_auth(self):
        auth_headers = {
            "HTTP_AUTHORIZATION": "Basic "
            + base64.b64encode("kadir:123456".encode()).decode(),
        }
        response = self.client.get("/users/me/", **auth_headers)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]["username"], self.user.username)
        self.assertEqual(response_json[0]["email"], self.user.email)
        self.assertEqual(response_json[0]["first_name"], self.user.first_name)
        self.assertEqual(response_json[0]["last_name"], self.user.last_name)
        self.assertEqual(response_json[0]["bio"], self.user.bio)

    def test_sign_up_valid_data(self):
        user_count = User.objects.all().count()
        response = self.client.post("/users/sign-up/", self.valid_data)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json["status"], "User created.")
        self.assertNotEqual(user_count, User.objects.all().count())

    def test_sign_up_valid_limitted_data(self):
        user_count = User.objects.all().count()
        response = self.client.post("/users/sign-up/", self.valid_data_2)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json["status"], "User created.")
        self.assertNotEqual(user_count, User.objects.all().count())

    def test_sign_up_blank_data(self):
        user_count = User.objects.all().count()
        response = self.client.post("/users/sign-up/", {})
        self.assertEqual(response.status_code, 400)
        response_json = response.json()
        self.assertTrue("username" in response_json)
        self.assertTrue("password" in response_json)
        self.assertTrue("bio" in response_json)
        self.assertEqual(user_count, User.objects.all().count())

    def test_get_search_without_query_params(self):
        user_count = User.objects.all().count()
        auth_headers = {
            "HTTP_AUTHORIZATION": "Basic "
            + base64.b64encode("kadir:123456".encode()).decode(),
        }
        response = self.client.get("/users/search/", **auth_headers)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(len(response_json), user_count)

    def test_get_search(self):
        auth_headers = {
            "HTTP_AUTHORIZATION": "Basic "
            + base64.b64encode("kadir:123456".encode()).decode(),
        }
        response = self.client.get("/users/search/?username=kadir", **auth_headers)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]["first_name"], self.user.first_name)

    def test_get_search_with_unmatched_username(self):
        auth_headers = {
            "HTTP_AUTHORIZATION": "Basic "
            + base64.b64encode("kadir:123456".encode()).decode(),
        }
        response = self.client.get("/users/search/?username=nonexist", **auth_headers)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(len(response_json), 0)

    def test_get_search_without_auth(self):
        response = self.client.get("/users/search/")
        self.assertEqual(response.status_code, 401)
