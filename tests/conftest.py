import pytest
import allure
from data.data_user import *
from data.data_update_user import *

@pytest.fixture(params=test_cases_for_register_new_user.items())
def fixture_register_new_user(request):

    title, case_data = request.param
    r_code = {'response_code': None}
    yield case_data, title, r_code

    email = case_data["request"]["email"]
    name = case_data["request"]["name"]
    password = case_data["request"]["password"]

    if r_code['response_code'] == 200:
        with allure.step(f'Удаление созданного пользователя {email} и {name}'):
            new_accessToken = authorize_user(email, password)
            delete_user(email, new_accessToken)


@pytest.fixture(params=test_cases_for_register_new_user_invalid_data.items())
def fixture_register_new_user_with_invalid_data(request):
    title, case_data = request.param

    yield case_data, title


@pytest.fixture
def fixture_register_new_user_with_existing_email():

    case_data = create_new_user()
    email, name, password = case_data

    yield email, name

    with allure.step(f'Удаление созданного пользователя {email} и {name}'):
        new_accessToken = authorize_user(email, password)
        delete_user(email, new_accessToken)

@pytest.fixture
def fixture_login_user_with_existing_email():

    case_data = create_new_user()
    email, name, password = case_data

    yield email, password

    with allure.step(f'Удаление созданного пользователя {email} и {name}'):
        new_accessToken = authorize_user(email, password)
        delete_user(email, new_accessToken)


@pytest.fixture
def fixture_update_user_data_with_authorization():

    case_data = create_new_user()
    email, name, password = case_data
    accessToken = authorize_user(email, password)

    yield email, password, name, accessToken

    with allure.step(f'Удаление созданного пользователя'):
        delete_user(email, accessToken)


@pytest.fixture(params=test_cases_for_update_user)
def fixture_update_user_data_without_authorization(request):

    case_data = create_new_user()
    email, name, password  = case_data
    param_key = request.param
    yield email, name, password, param_key

    with allure.step(f'Удаление созданного пользователя'):
        accessToken = authorize_user(email, password)
        delete_user(email, accessToken)


@pytest.fixture
def fixture_creating_order_with_authorization():

    case_data = create_new_user()
    email, name, password = case_data
    accessToken = authorize_user(email, password)
    order = get_random_order()

    yield accessToken, order

    with allure.step(f'Удаление созданного пользователя {email} и {name}'):

        delete_user(email, accessToken)

@pytest.fixture
def fixture_creating_order_without_authorization():

    order = get_random_order()

    yield order


@pytest.fixture
def fixture_creating_order_with_authorization_invalid_ingredients():

    case_data = create_new_user()
    email, name, password = case_data
    accessToken = authorize_user(email, password)
    order = f"'ingredients': ['61c0c5a71d', '61c0c5a71d1f82001bdaaa70', '61c0c5a71d1f82001bdaaa72']"

    yield accessToken, order

    with allure.step(f'Удаление созданного пользователя {email} и {name}'):
        delete_user(email, accessToken)

@pytest.fixture
def fixture_creating_order_with_authorization_without_ingredients():

    case_data = create_new_user()
    email, name, password = case_data
    accessToken = authorize_user(email, password)
    order = f"'ingredients': []"

    yield accessToken, order

    with allure.step(f'Удаление созданного пользователя {email} и {name}'):
        delete_user(email, accessToken)

@pytest.fixture
def fixture_get_list_orders_with_authorization():

    case_data = create_new_user()
    email, name, password = case_data
    accessToken = authorize_user(email, password)
    create_new_order(accessToken)
    create_new_order(accessToken)
    create_new_order(accessToken)

    yield accessToken

    with allure.step(f'Удаление созданного пользователя {email} и {name}'):
        delete_user(email, accessToken)