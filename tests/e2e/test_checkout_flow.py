import allure
import pytest
import time
from config import Config
from playwright.sync_api import expect


@allure.epic("E2E Сценарии")
@allure.feature("Покупка товара")
@allure.story("От поиска до корзины")
@allure.title("Успешное добавление лимитированного товара в корзину покупателя")
@pytest.mark.e2e
@pytest.mark.positive
def test_buyer_adds_sneaker_to_cart(
    api_client, generate_product_payload, storefront_page, page
):
    sneaker_name = f"Limited black woman hand{int(time.time() * 1000)}"
    sneaker_price = 2000

    with allure.step(f"Админка создает товар: {sneaker_name}"):
        sc_id = api_client.get_default_sales_channel_id()
        payload = generate_product_payload(title=sneaker_name, price_usd=sneaker_price)
        payload["sales_channels"] = [{"id": sc_id}]
        payload["variants"][0]["manage_inventory"] = False
        prod_res = api_client.create_product(payload)
        assert prod_res.status == 200, f"Товар не создан: {prod_res.text()}"
        product_id = prod_res.json()["product"]["id"]

    with allure.step("Покупатель открывает главную страницу витрины"):
        storefront_page.open_storefront()

    with allure.step("Открываем боковое меню"):
        storefront_page.go_to_store_catalog()
        page.wait_for_timeout(2000)

    with allure.step("Меняем страну доставки на Германию"):
        storefront_page.change_country_to_germany()

    with allure.step("Открываем каталог Store через боковое меню"):
        storefront_page.go_to_store_catalog()

    with allure.step("Покупатель открывает карточку товара"):
        storefront_page.open_product_card(sneaker_name)
        price_element = page.get_by_test_id("product-price")
        expect(price_element).to_contain_text("200,000")

    with allure.step("Покупатель кладет товар в корзину"):
        page.wait_for_timeout(3000)
        storefront_page.add_current_product_to_cart()

    with allure.step("Покупатель переходит в корзину"):
        storefront_page.go_to_checkout()
        expect(page.get_by_text(sneaker_name)).to_be_visible()
        print(f"\n {sneaker_name} Успешно донесены до корзины")

    with allure.step("Админ удаляет тестовый товар"):
        api_client.delete_product(product_id)
