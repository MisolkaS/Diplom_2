import pytest
import allure
import requests

from data.data_user import *
from data.data_url import *

class TestApiUserLoginPost:
    @allure.title("Проверка логина под существующим пользователем")
    def test_login_user_with_existing_email(self, fixture_login_user_with_existing_email):
        email, password = fixture_login_user_with_existing_email
        payload = {
            "email": email,
            "password": password
        }
        with allure.step(f"Авторизация пользователя {payload['email']}, {payload['password']}"):
            response = requests.post(api_user_login_url, json=payload)
            allure.attach(f"Response: {response.text}")

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}. Текст: {response.text}"

        with allure.step("Проверка структуры ответа"):
            response_json = response.json()
            assert "success" in response_json, "Ответ не содержит поле 'success'"
            assert response_json["success"] is True, "Поле 'success' должно быть True"
            assert "accessToken" in response_json, "Ответ не содержит поле 'accessToken'"
            assert "refreshToken" in response_json, "Ответ не содержит поле 'refreshToken'"
            assert "user" in response_json, "Ответ не содержит поле 'user'"

            user = response_json["user"]
            assert "email" in user, "Объект 'user' не содержит поле 'email'"
            assert "name" in user, "Объект 'user' не содержит поле 'name'"

            assert user["email"] == email, "Email в ответе не соответствует ожидаемому"

            assert response_json["accessToken"].startswith("Bearer "), "accessToken должен начинаться с 'Bearer '"

    @allure.title("Проверка ошибки при авторизации с неправильным логином")
    def test_login_user_with_invalid_email(self, fixture_login_user_with_existing_email):
        email, password = fixture_login_user_with_existing_email
        payload = {
            "email": f"inv{email}",
            "password": password
        }
        with allure.step(f"Авторизация пользователя {payload['email']}, {payload['password']}"):
            response = requests.post(api_user_login_url, json=payload)
            allure.attach(f"Response: {response.text}")


        expected_message = "email or password are incorrect"
        with allure.step('Проверка ответа'):
            success = response.json().get("success")
            assert success is False, f"Ожидалось сообщение False, но получено {success}"
            allure.attach(f"Ожидалось сообщение False, получено {success}",
                          name="Проверка success", attachment_type=allure.attachment_type.TEXT)

        with allure.step('Проверка кода ответа'):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"
            allure.attach(f"Ожидался статус 401, получен {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step('Проверка сообщения'):
            message = response.json().get("message")
            assert message == expected_message, f"Ожидалось сообщение {expected_message}, но получено {message}"
            allure.attach(f"Ожидалось сообщение {expected_message}, получен {message}",
                          attachment_type=allure.attachment_type.TEXT)

    @allure.title("Проверка ошибки при авторизации с неправильным паролем")
    def test_login_user_with_invalid_password(self, fixture_login_user_with_existing_email):
        email, password = fixture_login_user_with_existing_email
        payload = {
            "email": email,
            "password": f"inv{password}"
        }
        with allure.step(f"Авторизация пользователя {payload['email']}, {payload['password']}"):
            response = requests.post(api_user_login_url, json=payload)
            allure.attach(f"Response: {response.text}")


        expected_message = "email or password are incorrect"
        with allure.step('Проверка ответа'):
            success = response.json().get("success")
            assert success is False, f"Ожидалось сообщение False, но получено {success}"
            allure.attach(f"Ожидалось сообщение False, получено {success}",
                          name="Проверка success", attachment_type=allure.attachment_type.TEXT)

        with allure.step('Проверка кода ответа'):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"
            allure.attach(f"Ожидался статус 401, получен {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step('Проверка сообщения'):
            message = response.json().get("message")
            assert message == expected_message, f"Ожидалось сообщение {expected_message}, но получено {message}"
            allure.attach(f"Ожидалось сообщение {expected_message}, получен {message}",
                          attachment_type=allure.attachment_type.TEXT)