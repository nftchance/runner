import base64
from decimal import Decimal
import json  

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from utils.tests.user import PASSWORD, create_user

class AuthenticationTest(APITestCase):
    def test_user_can_sign_up(self):
        response = self.client.post(
            reverse("user-sign-up"),
            data={
                "username": "user@example.com",
                "first_name": "Test",
                "last_name": "User",
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
        )
        user = get_user_model().objects.last()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        print(response.data)
        self.assertEqual(response.data["id"], user.id)
        self.assertEqual(response.data["username"], user.username)
        self.assertEqual(response.data["first_name"], user.first_name)
        self.assertEqual(response.data["last_name"], user.last_name)

    def test_user_can_log_in(self):
        user = create_user()
        response = self.client.post(
            reverse("log-in"),
            data={
                "username": user.username,
                "password": PASSWORD,
            },
        )

        # Parse payload data from access token.
        access = response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data["refresh"])
        self.assertEqual(payload_data["id"], user.id)
        self.assertEqual(payload_data["username"], user.username)
        self.assertEqual(payload_data["first_name"], user.first_name)
        self.assertEqual(payload_data["last_name"], user.last_name)

    def test_user_can_log_out(self):
        user = create_user()
        response = self.client.post(
            reverse("log-in"),
            data={
                "username": user.username,
                "password": PASSWORD,
            },
        )

        access = response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data["refresh"])
        self.assertEqual(payload_data["id"], user.id)
        self.assertEqual(payload_data["username"], user.username)
        self.assertEqual(payload_data["first_name"], user.first_name)
        self.assertEqual(payload_data["last_name"], user.last_name)

        response = self.client.post(
            reverse("user-log-out"),
            data={'refresh_token': response.data['refresh']},
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )
        self.assertEqual(status.HTTP_205_RESET_CONTENT, response.status_code)

    def test_user_can_change_password(self):
        user = create_user()
        user_response = self.client.post(
            reverse("log-in"),
            data={
                "username": user.username,
                "password": PASSWORD,
            },
        )

        access = user_response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        self.assertEqual(status.HTTP_200_OK, user_response.status_code)
        self.assertIsNotNone(user_response.data["refresh"])
        self.assertEqual(payload_data["id"], user.id)
        self.assertEqual(payload_data["username"], user.username)
        self.assertEqual(payload_data["first_name"], user.first_name)
        self.assertEqual(payload_data["last_name"], user.last_name)

        response = self.client.put(
            reverse("user-update-password", kwargs={"user_id": user.id}),
            data={
                "old_password": PASSWORD,
                "password1": PASSWORD + 'test',
                "password2": PASSWORD + 'test',
            },
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # log out user
        response = self.client.post(
            reverse("user-log-out"),
            data={'refresh_token': user_response.data['refresh']},
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )

        # log in with new password
        response = self.client.post(
            reverse("log-in"),
            data={
                "username": user.username,
                "password": PASSWORD + 'test',
            },
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        access = response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        self.assertIsNotNone(response.data["refresh"])
        self.assertEqual(payload_data["id"], user.id)
        self.assertEqual(payload_data["username"], user.username)
        self.assertEqual(payload_data["first_name"], user.first_name)
        self.assertEqual(payload_data["last_name"], user.last_name)
        
    
    def test_user_can_update_user(self):
        user = create_user()
        response = self.client.post(
            reverse("log-in"),
            data={
                "username": user.username,
                "password": PASSWORD,
            },
        )

        access = response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data["refresh"])
        self.assertEqual(payload_data["id"], user.id)
        self.assertEqual(payload_data["username"], user.username)
        self.assertEqual(payload_data["first_name"], user.first_name)
        self.assertEqual(payload_data["last_name"], user.last_name)

        response = self.client.put(
            reverse("user-detail", kwargs={"user_id": user.id}),
            data={
                "first_name": "Test",
                "last_name": "User",
                "email": "chance@utc24.io",
                "username": "nftchance"
            },
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["first_name"], "Test")
        self.assertEqual(response.data["last_name"], "User")

    def test_user_cannot_update_user_to_non_unique_data(self):
        user = create_user()
        response = self.client.post(
            reverse("log-in"),
            data={
                "username": user.username,
                "password": PASSWORD,
            },
        )

        access = response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data["refresh"])
        self.assertEqual(payload_data["id"], user.id)
        self.assertEqual(payload_data["username"], user.username)
        self.assertEqual(payload_data["first_name"], user.first_name)
        self.assertEqual(payload_data["last_name"], user.last_name)

        response = self.client.put(
            reverse("user-detail", kwargs={"user_id": user.id}),
            data={
                "first_name": "Test",
                "last_name": "User",
                "email": "chance@utc24.io",
                "username": "nftchance"
            },
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["first_name"], "Test")
        self.assertEqual(response.data["last_name"], "User")

        # create second user
        user2 = create_user(username="nftchance-test")
        response = self.client.post(
            reverse("log-in"),
            data={
                "username": user2.username,
                "password": PASSWORD,
            },
        )

        access = response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data["refresh"])
        self.assertEqual(payload_data["id"], user2.id)
        self.assertEqual(payload_data["username"], user2.username)
        self.assertEqual(payload_data["first_name"], user2.first_name)
        self.assertEqual(payload_data["last_name"], user2.last_name)
        self.assertEqual(float(payload_data['balance']), user2.balance)

        # try and use duplicate username
        response = self.client.put(
            reverse("user-detail", kwargs={"user_id": user2.id}),
            data={
                "first_name": "Test",
                "last_name": "User",
                "email": "chance@utc24.io",
                "username": "nftchance"
            },
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(response.data["username"][0], "A user with that username already exists.")

    def test_user_cannot_update_user_to_non_unique_email(self):
        user = create_user()
        response = self.client.post(
            reverse("log-in"),
            data={
                "username": user.username,
                "password": PASSWORD,
            },
        )

        access = response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data["refresh"])
        self.assertEqual(payload_data["id"], user.id)
        self.assertEqual(payload_data["username"], user.username)
        self.assertEqual(payload_data["first_name"], user.first_name)
        self.assertEqual(payload_data["last_name"], user.last_name)

        response = self.client.put(
            reverse("user-detail", kwargs={"user_id": user.id}),
            data={
                "first_name": "Test",
                "last_name": "User",
                "email": "chance@utc24.io",
                "username": "nftchance"
            },
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["first_name"], "Test")
        self.assertEqual(response.data["last_name"], "User")

        # create second user
        user2 = create_user(username="nftchance-test")
        response = self.client.post(
            reverse("log-in"),
            data={
                "username": user2.username,
                "password": PASSWORD,
            },
        )

        access = response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data["refresh"])
        self.assertEqual(payload_data["id"], user2.id)
        self.assertEqual(payload_data["username"], user2.username)
        self.assertEqual(payload_data["first_name"], user2.first_name)
        self.assertEqual(payload_data["last_name"], user2.last_name)
        self.assertEqual(float(payload_data['balance']), user2.balance)

        # try and use duplicate username
        response = self.client.put(
            reverse("user-detail", kwargs={"user_id": user2.id}),
            data={
                "first_name": "Test",
                "last_name": "User",
                "email": "chance@utc24.io",
                "username": "nftchance-test"
            },
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        print(response.data)
        self.assertEqual(response.data["email"], "This email is already in use.")

    def test_user_can_log_out_all(self):
        user = create_user()
        response = self.client.post(
            reverse("log-in"),
            data={
                "username": user.username,
                "password": PASSWORD,
            },
        )

        access = response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data["refresh"])
        self.assertEqual(payload_data["id"], user.id)
        self.assertEqual(payload_data["username"], user.username)
        self.assertEqual(payload_data["first_name"], user.first_name)
        self.assertEqual(payload_data["last_name"], user.last_name)

        response = self.client.post(
            reverse("user-log-out-all"),
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )
        self.assertEqual(status.HTTP_205_RESET_CONTENT, response.status_code)