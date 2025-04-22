from helpers import *

test_cases_for_register_new_user = {
    "Успешное добавление курьера с валидным логином и паролем и заполненным именем": {
        "request": {
            "email": f"{generate_random_string(7)}@yandex.ru",
            "password": generate_random_string(7),
            "name": "Username"
        },
        "response": {
            "success": True,
            "status_code": 200
        }
    }
}
test_cases_for_register_new_user_invalid_data = {
    "Ошибка при добавлении курьера с пустым email, с валидным паролем и именем": {
        "request": {
            "email": "",
            "password": generate_random_string(7),
            "name": generate_random_string(7)
        },
        "response": {
            "success": False,
            "status_code": 403,
            "message": "Email, password and name are required fields"
        }
    },
    "Ошибка при добавлении курьера с пустым паролем, с валидным email и именем": {
        "request": {
            "email": f"{generate_random_string(7)}@yandex.ru",
            "password": "",
            "name": generate_random_string(7)
        },
        "response": {
            "success": False,
            "status_code": 403,
            "message": "Email, password and name are required fields"
        }
    },
    "Ошибка при добавлении курьера с пустым именем, с валидным паролем и email": {
        "request": {
            "email": f"{generate_random_string(7)}@yandex.ru",
            "password": generate_random_string(7),
            "name": ""
        },
        "response": {
            "success": False,
            "status_code": 403,
            "message": "Email, password and name are required fields"
        }
    }
}