import pytest
import allure
import requests

from data.data_user import *
from data.data_url import *

class TestApiUserUpdatePatch:
    @allure.title("Обновление email пользователя с авторизацией")
    def test_update_user_data_email_with_authorization(self, fixture_update_user_data_with_authorization):
        email, password, name, accessToken = fixture_update_user_data_with_authorization
        payload = {
            "email": f"update{email}"
        }
        headers = {
            "Authorization": f"{accessToken}",
            "Content-Type": "application/json"
        }

        with allure.step("Обновляем данные о пользователе"):
            response = requests.patch(api_user_url, json=payload, headers=headers)
            allure.attach(f"Response: {response.text}")

        with allure.step("Проверяем код ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}. Текст: {response.text}"
            allure.attach(f"Ожидался статус 200, получен {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверяем структуру ответа"):
            response_json = response.json()
            assert "success" in response_json, "Ответ не содержит поле 'success'"
            assert response_json["success"] is True, "Поле 'success' должно быть True"
            assert "user" in response_json, "Ответ не содержит поле 'user'"

            user = response_json["user"]
            assert "email" in user, "Объект 'user' не содержит поле 'email'"
            assert "name" in user, "Объект 'user' не содержит поле 'name'"


        with allure.step("Проверяем изменения email и отсутствие изменений в name"):
            assert user["email"] == payload["email"], "Email в ответе не соответствует обновленному email"
            allure.attach(f"Ожидался email {payload['email']}, получен {user['email']}",
                          attachment_type=allure.attachment_type.TEXT)
            assert user["name"] == name, "Имя в ответе не соответствует обновленному имени"
            allure.attach(f"Ожидался имя {name}, получен {user['name']}",
                          attachment_type=allure.attachment_type.TEXT)

    @allure.title("Обновление name пользователя с авторизацией")
    def test_update_user_data_name_with_authorization(self, fixture_update_user_data_with_authorization):
        email, password, name, accessToken = fixture_update_user_data_with_authorization
        payload = {
            "name": f"update{name}"
        }
        headers = {
            "Authorization": f"{accessToken}",
            "Content-Type": "application/json"
        }

        with allure.step("Обновляем данные о пользователе"):
            response = requests.patch(api_user_url, json=payload, headers=headers)
            allure.attach(f"Response: {response.text}")

        with allure.step("Проверяем код ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}. Текст: {response.text}"
            allure.attach(f"Ожидался статус 200, получен {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверяем структуру ответа"):
            response_json = response.json()
            assert "success" in response_json, "Ответ не содержит поле 'success'"
            assert response_json["success"] is True, "Поле 'success' должно быть True"
            assert "user" in response_json, "Ответ не содержит поле 'user'"

            user = response_json["user"]
            assert "email" in user, "Объект 'user' не содержит поле 'email'"
            assert "name" in user, "Объект 'user' не содержит поле 'name'"


        with allure.step("Проверяем изменения name и отсутствие изменений в email"):
            assert user["name"] == payload["name"], "Имя в ответе не соответствует обновленному имени"
            allure.attach(f"Ожидался имя {payload['name']}, получен {user['name']}",
                          attachment_type=allure.attachment_type.TEXT)

            assert user["email"] == email, "Email в ответе не соответствует обновленному email"
            allure.attach(f"Ожидался email {email}, получен {user['email']}",
                          attachment_type=allure.attachment_type.TEXT)

    @allure.title("Обновление пароля пользователя с авторизацией")
    def test_update_user_data_password_with_authorization(self, fixture_update_user_data_with_authorization):
        email, password, name, accessToken = fixture_update_user_data_with_authorization
        payload = {
            "password": f"update{password}"
        }
        headers = {
            "Authorization": f"{accessToken}",
            "Content-Type": "application/json"
        }

        with allure.step("Обновляем данные о пользователе"):
            response = requests.patch(api_user_url, json=payload, headers=headers)
            allure.attach(f"Response: {response.text}")

        with allure.step("Проверяем код ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}. Текст: {response.text}"
            allure.attach(f"Ожидался статус 200, получен {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверяем структуру ответа"):
            response_json = response.json()
            assert "success" in response_json, "Ответ не содержит поле 'success'"
            assert response_json["success"] is True, "Поле 'success' должно быть True"
            assert "user" in response_json, "Ответ не содержит поле 'user'"

            user = response_json["user"]
            assert "email" in user, "Объект 'user' не содержит поле 'email'"
            assert "name" in user, "Объект 'user' не содержит поле 'name'"

        with allure.step("Проверяем изменения name и email"):
            assert user["name"] == name, "Имя в ответе не соответствует обновленному имени"
            allure.attach(f"Ожидался имя {name}, получен {user['name']}",
                          attachment_type=allure.attachment_type.TEXT)

            assert user["email"] == email, "Email в ответе не соответствует обновленному email"
            allure.attach(f"Ожидался email {email}, получен {user['email']}",
                          attachment_type=allure.attachment_type.TEXT)


    def test_update_user_data_without_authorization(self, fixture_update_user_data_without_authorization):
        email, name, password, update_str = fixture_update_user_data_without_authorization
        allure.dynamic.title(f'Обновление данных {update_str} пользователя без авторизации')
        value_to_update = 'inv'+locals()[update_str]

        payload = {
            update_str: value_to_update
        }

        headers = {
            "Content-Type": "application/json"
        }


        with allure.step("Обновляем данные неавторизированного пользователя"):
            response = requests.patch(api_user_url, json=payload, headers=headers)
            allure.attach(response.text, "Response", allure.attachment_type.TEXT)

        with allure.step("Проверяем код ответа"):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}. Текст: {response.text}"
            allure.attach(f"Ожидался статус 401, получен {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверяем структуру ответа"):
            response_json = response.json()
            assert "success" in response_json, "Ответ не содержит поле 'success'"
            assert response_json["success"] is False, "Поле 'success' должно быть False"
            assert "message" in response_json, "Ответ не содержит поле 'message'"


            assert response_json["message"] == "You should be authorised", "Сообщение об ошибке не соответствует ожидаемому"
            allure.attach(
                f"Ожидалось сообщение: You should be authorised, получено: {response_json['message']}",
                attachment_type=allure.attachment_type.TEXT
            )
