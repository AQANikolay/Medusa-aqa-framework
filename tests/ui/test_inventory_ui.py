import re
import allure
import pytest
from playwright.sync_api import expect
from config import Config
import time


#                               ПОЗИТИВНЫЕ ТЕСТЫ
# =====================================================================================================================
@allure.epic("Интерфейс Админки")
@allure.feature("Каталог и Склад (UI)")
@allure.story("Создание товара")
@allure.title("Успешное добавление кроссовок через форму")
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.smoke
def test_create_product_via_ui(login_page, products_page, create_product_page, page):
    test_product_name = f"Travis Scott Phantom Shades {int(time.time() * 1000)}"

    with allure.step("Заходим в админку"):
        login_page.open(Config.ADMIN_URL)
        login_page.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)

        expect(page.get_by_role("link", name="Products")).to_be_visible(
            timeout=Config.UI_TIMEOUT
        )

    with allure.step("Открываем список товаров и жмем 'create' "):
        products_page.open_products_list()
        products_page.click_create_button()

    with allure.step(f"Вводим данные {test_product_name}"):
        create_product_page.create_simple_product(
            title=test_product_name,
        )

    with allure.step("Ждем сообщение об успехе"):
        is_created = create_product_page.is_creation_successful()
        assert is_created == True, "Всплывающее окно не появилось"

    with allure.step("Идем в таблицу смотреть товар через поиск"):
        products_page.open_products_list()
        products_page.search_for_product(test_product_name)
        is_in_table = products_page.is_text_visible(test_product_name)
        assert (
            is_in_table == True
        ), f"Товар {test_product_name} не найден в таблице после создания"


@allure.epic("Интерфейс Админки")
@allure.feature("Каталог и Склад (UI)")
@allure.story("Поиск товаров")
@allure.title("Фильтрация таблицы через строку поиска")
@pytest.mark.ui
@pytest.mark.positive
def test_search_product_in_table(
    api_client, login_page, products_page, generate_product_payload, page
):
    unique_name = f"Search Test Sneaker {int(time.time() * 1000)}"
    with allure.step(f"Создаем товар: {unique_name} через API"):
        payload = generate_product_payload(title=unique_name)
        prod_res = api_client.create_product(payload)
        product_id = prod_res.json()["product"]["id"]

    with allure.step("Авторизуемся и переходим в Товары"):
        login_page.open(Config.ADMIN_URL)
        login_page.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
        products_page.open_products_list()

    with allure.step(f"Вводим {unique_name} в строку поиска"):
        products_page.search_for_product(unique_name)
        page.wait_for_timeout(2000)

    with allure.step("Проверка что товар остался в таблице"):
        assert (
            products_page.is_product_visible(unique_name) == True
        ), "Созданный товар не найден"

    with allure.step("Вводим несуществующее имя и проверяем пустую таблицу"):
        products_page.search_for_product("FakeHackHackHacker22222")
        page.wait_for_timeout(2000)
        assert (
            products_page.is_product_visible(unique_name) == False
        ), "Таблица не отфильтровала старый товар"

    with allure.step("Удаляем товар через апишку"):
        api_client.delete_product(product_id)


@allure.epic("Интерфейс Админки")
@allure.feature("Каталог и Склад (UI)")
@allure.story("Пагинация таблицы")
@allure.title("Проверка переключения страниц (Next / Previous)")
@pytest.mark.ui
@pytest.mark.positive
def test_pagination_buttons(login_page, products_page, page):
    with allure.step("Авторизуемся и переходим в товары"):
        login_page.open(Config.ADMIN_URL)
        login_page.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
        products_page.open_products_list()

    with allure.step("Скроллим вниз и проверяем кнопку Next"):
        if (
            products_page.next_page_button.is_enabled()
            and products_page.next_page_button.is_enabled()
        ):

            with allure.step("Кликаем Next и ждем изменения URL"):
                products_page.go_to_next_page()
                expect(page).to_have_url(re.compile(r"offset=20"))
                print("\nУспешный переход на вторую страницу")
        else:
            print("\n[SKIP] Товаров мало для пагинации")


#                           НЕГАТИВНЫЕ ТЕСТЫ
# ============================================================================================================================================================


@allure.epic("Интерфейс Админки")
@allure.feature("Каталог и Склад (UI)")
@allure.story("Поиск товаров")
@allure.title("Отображение заглушки при поиске несуществующего товара")
@pytest.mark.ui
@pytest.mark.negative
def test_search_no_results_ui(login_page, products_page, page):
    with allure.step("Авторизуемся и переходим в товары"):
        login_page.open(Config.ADMIN_URL)
        login_page.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
        products_page.open_products_list()
    with allure.step("Вводим в поиск несуществующую строку"):
        products_page.search_for_product("FAKe_Uncreated_Goods")
    with allure.step(
        "Проверяем что появился текст говорящий об отсутствии такого товара"
    ):
        expect(products_page.no_results_message).to_be_visible(timeout=3000)


@allure.epic("Интерфейс Админки")
@allure.feature("Каталог и Склад (UI)")
@allure.story("Отмена действий")
@allure.title("Отмена создания товара закрывает форму без сохранения")
@pytest.mark.ui
@pytest.mark.negative
def test_cancel_product_creation(login_page, products_page, create_product_page, page):
    with allure.step("Авторизуемся и переходим в товары"):
        login_page.open(Config.ADMIN_URL)
        login_page.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
        products_page.open_products_list()
    with allure.step("Открываем форму создания и вводим текст"):
        products_page.click_create_button()
        create_product_page.fill_basic_info("Fucking goods")

    with allure.step("Нажимаем Escape"):
        create_product_page.cancel_creation()
        confirm_leave = page.locator('button:has-text("Continue")').last
        if confirm_leave.is_visible():
            confirm_leave.click()

    with allure.step("Проверяем что вернулись в таблицу (URL /products)"):
        expect(create_product_page.title_input).to_be_hidden()
        page.wait_for_url("**/*products*")
