import pytest
import allure
import requests
from data.data_user import *
from data.data_url import *


class TestApiCreateOrderPost:
    @allure.title("Создание заказа с авторизацией")
    def test_creating_order_with_authorization(self, fixture_creating_order_with_authorization):
        accessToken, order = fixture_creating_order_with_authorization


        headers = {
            "Authorization": f"{accessToken}",
            "Content-Type": "application/json"
        }

        with allure.step("Создаем заказ"):
            response = requests.post(api_orders_url, json=order, headers=headers)
            allure.attach(f"Response: {response.text}")

        with allure.step("Проверяем код ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}. Текст: {response.text}"
            allure.attach(f"Ожидался статус 200, получен {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверяем структуру ответа"):
            response_json = response.json()
            assert "success" in response_json, "Ответ не содержит поле 'success'"
            assert response_json["success"] is True, "Поле 'success' должно быть True"

            assert "name" in response_json, "Ответ не содержит поле 'name'"

            order = response_json["order"]
            assert "number" in order, "Объект 'order' не содержит поле 'number'"


    @allure.title("Создание заказа без авторизации")
    def test_creating_order_without_authorization(self, fixture_creating_order_without_authorization):
        order = fixture_creating_order_without_authorization


        with allure.step("Создаем заказ"):
            response = requests.post(api_orders_url, json=order)

            allure.attach(f"Response: {response.text}")

        with allure.step("Проверяем код ответа"):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}. Текст: {response.text}"
            allure.attach(f"Ожидался статус 401, получен {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)



    @allure.title("Создание заказа с авторизацией и с неправильными ингредиентами")
    def test_creating_order_with_authorization_invalid_ingredients(self, fixture_creating_order_with_authorization_invalid_ingredients):
        accessToken, order = fixture_creating_order_with_authorization_invalid_ingredients

        headers = {
            "Authorization": f"{accessToken}",
            "Content-Type": "application/json"
        }

        with allure.step("Создаем заказ"):
            response = requests.post(api_orders_url, json=order, headers=headers)
            allure.attach(f"Response: {response.text}")

        with allure.step("Проверяем код ответа"):
            assert response.status_code == 500, f"Ожидался статус 500, но получен {response.status_code}. Текст: {response.text}"
            allure.attach(f"Ожидался статус 500, получен {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)

    @allure.title("Создание заказа с авторизацией и без ингредиентов")
    def test_creating_order_with_authorization_without_ingredients(self, fixture_creating_order_with_authorization_without_ingredients):
        accessToken, order = fixture_creating_order_with_authorization_without_ingredients

        headers = {
            "Authorization": f"{accessToken}",
            "Content-Type": "application/json"
        }

        with allure.step("Создаем заказ"):
            response = requests.post(api_orders_url, json=order, headers=headers)
            allure.attach(f"Response: {response.text}")

        with allure.step("Проверяем код ответа"):
            assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}. Текст: {response.text}"
            allure.attach(f"Ожидался статус 400, получен {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)


