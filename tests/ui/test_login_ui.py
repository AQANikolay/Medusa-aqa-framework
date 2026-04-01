import allure
import pytest
from playwright.sync_api import expect
from config import Config


@allure.epic("Интерфейс Админки")
@allure.feature("UI Авторизация")
@allure.story("Негативные сценарии")
@allure.title("Проверка появления ошибки при неверном пароле")
@pytest.mark.ui
@pytest.mark.negative
def test_login_invalid_credentials(login_page, page):
    with allure.step("Открываем страницу логина"):
        login_page.open(Config.ADMIN_URL)

    with allure.step("Вводим валидный email и невалидный пароль"):
        login_page.login(Config.ADMIN_EMAIL, "fakeass_password_21312")

    with allure.step("Проверяем появление сообщения об ошибке"):
        error_toast = page.get_by_text("Invalid email or password")
        expect(error_toast).to_be_visible(timeout=3000)


@allure.epic("Интерфейс Админки")
@allure.feature("UI Авторизация")
@allure.story("Фронтенд валидация")
@allure.title("Ошибка при попытке входа с пустыми полями")
@pytest.mark.ui
@pytest.mark.negative
def test_login_empty_fields_validation(login_page, page):
    with allure.step("Открываем страницу логина"):
        login_page.open(Config.ADMIN_URL)
    with allure.step("Не вводим креды и жмем войти"):
        login_page.login_button.click()

    with allure.step("Проверяем что появилось сообщение об ошибке"):
        error_toast = page.get_by_text("Invalid email")
        expect(error_toast).to_be_visible(timeout=3000)
