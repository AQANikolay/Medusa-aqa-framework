import allure
import pytest


@allure.epic("Каталог и Склад")
@allure.feature("API Товаров")
@allure.story("Успешное создание")
@allure.title("Успешное создание нового кроссовка")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.smoke
def test_create_product_success(api_client, generate_product_payload):
    payload = generate_product_payload()
    response = api_client.create_product(payload)
    assert response.status == 200, f"Ошибка создания: {response.text()}"
    product_id = response.json()["product"]["id"]
    assert product_id.startswith("prod_")
    api_client.delete_product(product_id)


@allure.epic("Каталог и Склад")
@allure.feature("API Товаров")
@allure.story("Граничные значения цен")
@allure.title("Проверка создания товара с разными ценами")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.parametrize(
    "test_price,expected_status",
    [(0, 200), (100000000, 200), (-50, 200), (50.123, 200), ("argsdf", 400)],
)
def test_create_product_prices(
    api_client, generate_product_payload, test_price, expected_status
):
    payload = generate_product_payload(price_usd=test_price)
    response = api_client.create_product(payload)
    assert response.status == expected_status, f"Ошибка на цене: {test_price}"
    if response.status == 200:
        product_id = response.json()["product"]["id"]
        api_client.delete_product(product_id)


@allure.epic("Каталог и Склад")
@allure.feature("API Товаров")
@allure.story("Валидация полей")
@allure.title("Ошибка создания товара без названия")
@pytest.mark.api
@pytest.mark.negative
def test_create_product_without_title(api_client, generate_product_payload):
    payload = generate_product_payload(title="Bad Test")
    del payload["title"]
    response = api_client.create_product(payload)
    assert response.status == 400
    assert "title" in response.text().lower()


@allure.epic("Каталог и Склад")
@allure.feature("API Товаров")
@allure.story("Безопасность")
@allure.title("Попытка удаления товара без токена")
@pytest.mark.api
@pytest.mark.negative
def test_delete_product_unauthorized(auth_client):
    with pytest.raises(Exception) as e:
        auth_client.delete_product("prod_fake_123")
    assert "login" in str(e.value)
