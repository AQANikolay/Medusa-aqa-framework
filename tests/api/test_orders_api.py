import allure
import pytest


@allure.epic("Корзины и Заказы")
@allure.feature("API Заказов")
@allure.story("Получение списка")
@allure.title("Успешное получение списка заказов администратором")
@pytest.mark.api
@pytest.mark.positive
def test_get_order_list_success(api_client):
    with allure.step("Отправляем запрос на получение заказов"):
        response = api_client.get_orders()

    with allure.step("Проверяем статус код и структуру JSON ответа"):
        assert response.status == 200, f"Ошибка: {response.text()}"
        body = response.json()
        assert "orders" in body, "Ключ 'orders' отсутствует в ответе"
        assert type(body["orders"]) is list, "Список заказов должен быть массивом"


@allure.epic("Корзины и Заказы")
@allure.feature("API Заказов")
@allure.story("Поиск заказа")
@allure.title("Ошибка при запросе несуществующего заказа")
@pytest.mark.api
@pytest.mark.negative
def test_get_fake_order_by_id(api_client):
    fake_order_id = "order_fake_pussy_1111"

    with allure.step(f"Запрашиваем заказ с id: {fake_order_id}"):
        response = api_client.get_order_by_id(fake_order_id)

    with allure.step("Ожидаем 404 ошибку"):
        assert response.status == 404, f"Ожидался 404 получили: {response.status}"
        assert "not_found" in response.text().lower()


@allure.epic("Корзины и Заказы")
@allure.feature("API Заказов")
@allure.story("Безопасность")
@allure.title("Попытка получить список заказов без авторизации")
@pytest.mark.api
@pytest.mark.negative
def test_get_orders_unauthorized(auth_client):
    with allure.step("Попытка получить заказы без токена"):
        with pytest.raises(Exception) as exc_info:
            auth_client.get_orders()
        assert "login" in str(exc_info.value).lower()
