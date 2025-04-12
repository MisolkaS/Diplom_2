import pytest
import allure
import requests

from data.data_user import *
from data.data_url import *

class TestApiUserPost:
    # тестирование ручки Создание пользователя
    def test_register_new_user(self, fixture_register_new_user):
        case_data, title, r_code = fixture_register_new_user
        allure.dynamic.title(title)
        payload = case_data["request"]
        expected_response = case_data["response"]

        with allure.step('Создание пользователя'):
            response = requests.post(api_registration_url, json=payload)
            allure.attach(f"Response: {response.text}")
            r_code['response_code'] = response.status_code



        with allure.step('Проверка ответа'):
            success = response.json().get("success")
            assert success == expected_response['success'], f"Ожидалось сообщение {expected_response['success']}, но получено {success}"
            allure.attach(f"Ожидалось сообщение {expected_response['success']}, получено {success}", attachment_type=allure.attachment_type.TEXT)

        with allure.step('Проверка кода ответа'):
            assert response.status_code == expected_response["status_code"], \
                f"Ожидался статус {expected_response['status_code']}, но получен {response.status_code}"
            allure.attach(f"Ожидался статус {expected_response['status_code']}, получен {response.status_code}", attachment_type=allure.attachment_type.TEXT)

        with allure.step('Проверка email пользователя'):
            user_data = response.json().get("user", {})
            actual_email = user_data.get('email')
            expected_email = payload["email"]
            assert actual_email == expected_email, f"Ожидалось сообщение {expected_email}, но получено {actual_email}"
            allure.attach(
                f"Ожидалось сообщение: {expected_email}, получено: {actual_email}",
                name="Сравнение email",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step('Проверка имени пользователя'):
            expected_name = payload.get("name")
            actual_name = user_data.get('name')
            assert actual_name == expected_name, f"Ожидалось имя {expected_name}, но получено {actual_name}"
            allure.attach(
                    f"Ожидалось имя: {expected_name}, получено: {actual_name}",
                    name="Сравнение имени",
                    attachment_type=allure.attachment_type.TEXT
                )

        with allure.step('Проверка токенов'):
            access_token = response.json().get("accessToken")
            refresh_token = response.json().get("refreshToken")
            assert access_token is not None, "Access token не должен быть None"
            assert refresh_token is not None, "Refresh token не должен быть None"
            allure.attach(f"Access Token: {access_token}", name="Access Token", attachment_type=allure.attachment_type.TEXT)
            allure.attach(f"Refresh Token: {refresh_token}", name="Refresh Token", attachment_type=allure.attachment_type.TEXT)



    def test_register_new_user_with_invalid_data(self, fixture_register_new_user_with_invalid_data):
        case_data, title = fixture_register_new_user_with_invalid_data
        allure.dynamic.title(title)
        payload = case_data["request"]
        expected_response = case_data["response"]

        with allure.step('Создание пользователя'):
            response = requests.post(api_registration_url, json=payload)
            allure.attach(f"Response: {response.text}")



        with allure.step('Проверка ответа'):
            success = response.json().get("success")
            assert success == expected_response['success'], f"Ожидалось сообщение {expected_response['success']}, но получено {success}"
            allure.attach(f"Ожидалось сообщение {expected_response['success']}, получено {success}", name="Проверка success", attachment_type=allure.attachment_type.TEXT)

        with allure.step('Проверка кода ответа'):
            assert response.status_code == expected_response["status_code"], \
                f"Ожидался статус {expected_response['status_code']}, но получен {response.status_code}"
            allure.attach(f"Ожидался статус {expected_response['status_code']}, получен {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step('Проверка сообщения'):
            message = response.json().get("message")
            assert message == expected_response["message"], \
                f"Ожидалось сообщение {expected_response['message']}, но получено {message}"
            allure.attach(f"Ожидалось сообщение {expected_response['message']}, получен {message}",
                          attachment_type=allure.attachment_type.TEXT)


    @allure.title("Проверка появления ошибки при создании пользователя с email, который уже есть")
    def test_register_new_user_with_existing_email(self, fixture_register_new_user_with_existing_email):
        email, name = fixture_register_new_user_with_existing_email

        new_payload = {
            "email": email,
            "password": generate_random_string(7),
            "name": name
        }

        message = 'User already exists'
        with allure.step('Проверка, что повторно пользователь не создается'):
            response = requests.post(api_registration_url, json=new_payload)
            allure.attach(f"Response: {response.text}")

        with allure.step('Проверка кода ответа'):
            assert response.status_code == 403, f"Ожидался статус 403, но получен {response.status_code}"
            allure.attach(f"Ожидался статус 403, получен {response.status_code}")

        with allure.step('Проверка текста сообщения'):
            assert response.json().get("message") == message, f"Ожидалось сообщение {message}, но получено {response.json().get('message')}"
            allure.attach(f"Ожидалось сообщение {message}, получено {response.json().get('message')}")
