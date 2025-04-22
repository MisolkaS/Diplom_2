import pytest
import allure
import requests
from data.data_url import *


class TestApiUserListOrders:
    @allure.title("Получение списка заказов конкретного пользователя")
    def test_get_list_orders_with_authorization(self, fixture_get_list_orders_with_authorization):
        accessToken = fixture_get_list_orders_with_authorization

        headers = {
            "Authorization": f"{accessToken}",
            "Content-Type": "application/json"
        }

        with allure.step("Получение заказов пользователя"):
            response = requests.get(api_orders_url, headers=headers)
            allure.attach(f"Response: {response.text}")

        with allure.step("Проверяем код ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}. Текст: {response.text}"
            allure.attach(f"Ожидался статус 200, получен {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверяем структуру ответа"):
            response_json = response.json()


            assert "orders" in response_json, "Отсутствует ключ 'orders' в ответе"
            assert "total" in response_json, "Отсутствует ключ 'total' в ответе"
            assert "totalToday" in response_json, "Отсутствует ключ 'totalToday' в ответе"

            assert isinstance(response_json["orders"], list), "'orders' должен быть списком"

            assert len(response_json["orders"]) == response_json["total"], "Количество заказов не соответствует total"


            for order in response_json["orders"]:
                assert isinstance(order, dict), "Каждый заказ должен быть словарем"
                assert "ingredients" in order, "Отсутствует ключ 'ingredients' в заказе"
                assert isinstance(order["ingredients"], list), "'ingredients' должен быть списком"
                assert "status" in order, "Отсутствует ключ 'status' в заказе"
                assert "number" in order, "Отсутствует ключ 'number' в заказе"
                assert "createdAt" in order, "Отсутствует ключ 'createdAt' в заказе"
                assert "updatedAt" in order, "Отсутствует ключ 'updatedAt' в заказе"

    @allure.title("Получение списка заказов без авторизации")
    def test_get_list_orders_without_authorization(self):

        with allure.step("Получение заказов без авторизации"):
            response = requests.get(api_orders_url)
            allure.attach(f"Response: {response.text}")

        with allure.step("Проверяем код ответа"):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}. Текст: {response.text}"
            allure.attach(f"Ожидался статус 401, получен {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step('Проверка структуры ответа'):
            success = response.json().get("success")
            assert success is False, f"Ожидалось сообщение False, но получено {success}"
            allure.attach(f"Ожидалось сообщение False, получено {success}",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step('Проверка сообщения'):
            message = response.json().get("message")
            expected_message = "You should be authorised"
            assert message == expected_message, f"Ожидалось сообщение {expected_message}, но получен {message}"
            allure.attach(f"Ожидалось сообщение {expected_message}, получен {message}",
                          attachment_type=allure.attachment_type.TEXT)



