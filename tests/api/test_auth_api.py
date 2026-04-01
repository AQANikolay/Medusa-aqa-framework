import allure
import pytest
from config import Config


@allure.epic("Безопасность")
@allure.feature("API Авторизация")
@allure.title("Успешный вход с правильными данными")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.smoke
def test_login_success(auth_client):
    with allure.step("Отправка запроса на логин"):
        response = auth_client.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
    with allure.step("Проверка кода ответа"):
        assert response.status == 200
    with allure.step("Проверка сохранения токена"):
        assert auth_client.token is not None


@allure.epic("Безопасность")
@allure.feature("API Авторизация")
@allure.title("Блокировка входа с неверным паролем")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.smoke
def test_login_invalid_password(auth_client):
    with allure.step("Отправляем запрос с невалидным паролем"):
        response = auth_client.login(Config.ADMIN_EMAIL, "wrong_password_1111111")
    with allure.step("Проверка статус кода"):
        assert response.status == 401, f"Статус: {response.status}"


@allure.epic("Безопасность")
@allure.feature("API Авторизация")
@allure.title("Блокировка входа с пустыми полями")
@pytest.mark.api
@pytest.mark.negative
def test_login_empty_fields(auth_client):
    with allure.step("Отправляем пустые строки вместо логина и пароля"):
        response = auth_client.login("", "")
    with allure.step("Проверяем статус ошибки"):
        assert response.status in [400, 401, 422]
