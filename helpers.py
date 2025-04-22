import random
import string
import requests
import allure
import json
from data.data_url import *
import random

def generate_random_string(length, language='english'):
    if language == 'english':
        letters = string.ascii_lowercase
    elif language == 'russian':
        letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def delete_user(email, accessToken):
    headers = {
        'Authorization': accessToken
    }

    response = requests.delete(api_user_url, headers=headers)

    if response.status_code == 202:
        allure.attach(f"Пользователь {email} успешно удален", name="Результат удаления",
                      attachment_type=allure.attachment_type.TEXT)
        return True
    else:
        allure.attach(f"Ошибка при удалении пользователя {email}: статус {response.status_code}, текст: {response.text}",
                      name="Ошибка удаления", attachment_type=allure.attachment_type.TEXT)
        return False

def create_new_user():

    payload = {
        "email": f"{generate_random_string(7)}@yandex.ru",
        "password": generate_random_string(7),
        "name": generate_random_string(7)
    }
    with allure.step(f"Создание пользователя {payload['email']}, {payload['name']}, {payload['password']}"):
        response = requests.post(api_registration_url, json=payload)

        if response.status_code == 200:
            return payload['email'], payload['name'], payload['password']
        else:
            allure.attach(f"Ошибка при создании пользователя: статус {response.status_code}", name="Ошибка поиска",
                          attachment_type=allure.attachment_type.TEXT)
            return None

def authorize_user(email, password):
    payload = {
        "email": email,
        "password": password
    }
    with allure.step(f"Авторизация пользователя {payload['email']}, {payload['password']}"):
        login_response = requests.post(api_user_login_url, json=payload)

        if login_response.status_code == 200:
            return login_response.json().get("accessToken")
        else:
            allure.attach(f"Не удалось авторизоваться: статус {login_response.status_code}, текст: {login_response.text}",
                          name="Ошибка авторизации", attachment_type=allure.attachment_type.TEXT)

            return None


def get_random_order():

    response = requests.get(api_ingredients_url)
    data = response.json()

    ingredients = data["data"]
    buns = [item for item in ingredients if item["type"] == "bun"]
    mains = [item for item in ingredients if item["type"] == "main"]
    sauces = [item for item in ingredients if item["type"] == "sauce"]

    chosen_bun = random.choice(buns)
    chosen_main = random.choice(mains)
    chosen_sauce = random.choice(sauces)

    with allure.step(f"Создание заказа {chosen_bun['name']}, {chosen_main['name']}, {chosen_sauce['name']}"):
        order = {
            "ingredients": [chosen_bun["_id"], chosen_main["_id"], chosen_sauce["_id"]]
        }

    return order

def create_new_order(accessToken):
    order = get_random_order()
    headers = {
        "Authorization": f"{accessToken}",
        "Content-Type": "application/json"
    }
    with allure.step("Создаем заказ пользователя"):
        requests.post(api_orders_url, json=order, headers=headers)
