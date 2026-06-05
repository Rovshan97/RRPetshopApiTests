import allure
import requests
import pytest
import jsonschema
from tests.schemas.inventory_schema import INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:

    @allure.title("Размещение нового заказа")
    def test_new_order(self):
        with allure.step("Подготовка данных для создания нового заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на создание нового заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)

        with allure.step("Проверка статуса статуса ответа и текстового содержимого"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.json() == payload, "Текстовое содержимое ответа не совпало с ожидаемым"


    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_order):

        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200
            assert response.json()["id"] == order_id

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_order):

        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ошибки не совпал с ожидаемым"
            assert response.json()["id"] == order_id

        with allure.step("Проверка удаления заказа по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 404, "Код ошибки не совпал с ожидаемым"
            assert response.text == "Order not found", "Текст сообщения не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order_by_id(self):

        with allure.step("Отправка запроса на получение информации по несуществующему заказу"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статус кода и текстового сообщения ответа"):
            assert response.status_code == 404, "Код ошибки не совпал с ожидаемым"
            assert response.text == "Order not found", "Текст сообщения не совпал с ожидаемым"

    @allure.title("Получение информации об инвентаре магазина")
    def test_get_store_inventory(self):

        with allure.step("Отправка запроса на получение информации об инвентаре"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статус кода ответа и валидация JSON схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), INVENTORY_SCHEMA)

