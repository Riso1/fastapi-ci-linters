"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from hw1_registration import app

class TestRegistration(unittest.TestCase):
    """
    Набор тестов для endpoint /registration.
    Проверяют, какие данные проходят валидацию, а какие должны возвращать ошибку 400.
    """
    @classmethod
    def setUpClass(cls):
        """
        Функция выполняется однократно перед запуском всех тестов класса.
        Включает тестовый режим Flask, отключает CSRF и создает тестовый клиент.
        :return:
        """
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        cls.client = app.test_client()

    @classmethod
    def valid_data():
        """
        Базовый шаблон для тестов.
        :return:
        """
        return {
            "email": "aleksandr@example.com",
            "phone": "9998887766",
            "name": "Aleksandr",
            "address": "Omsk",
            "index": "644010",
            "comment": "Hello, World!"
        }

    def test_registration_valid_data(self):
        """
        Проверяет, что полностью корректные данные проходят валидацию.
        """
        response = self.client.post("/registration", data=self.valid_data())
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Successfully registered user", response_text)

    def test_email_required(self):
        """
        Проверяет, что пустой email не проходит валидацию.
        """
        data = self.valid_data()
        data["email"] = ""

        response = self.client.post("/registration", data=data)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response_text)

    def test_email_invalid_format(self):
        """
        Проверяет, что email в неправильном формате не проходит валидацию.
        """
        data = self.valid_data()
        data["email"] = "not_email"

        response = self.client.post("/registration", data=data)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response_text)

    def test_phone_required(self):
        """
        Проверяет, что пустой phone не проходит валидацию.
        """
        data = self.valid_data()
        data["phone"] = ""

        response = self.client.post("/registration", data=data)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response_text)

    def test_phone_must_be_number(self):
        """
        Проверяет, что phone должен содержать только число.
        """
        data = self.valid_data()
        data["phone"] = "abcde"

        response = self.client.post("/registration", data=data)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response_text)

    def test_phone_must_be_positive(self):
        """
        Проверяет, что phone должен быть положительным числом.
        """
        data = self.valid_data()
        data["phone"] = "-9991234567"

        response = self.client.post("/registration", data=data)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response_text)

    def test_phone_length_invalid(self):
        """
        Проверяет, что phone должен содержать ровно 10 цифр.
        """
        data = self.valid_data()
        data["phone"] = "12345"

        response = self.client.post("/registration", data=data)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response_text)

    def test_name_required(self):
        """
        Проверяет, что пустое поле name не проходит валидацию.
        """
        data = self.valid_data()
        data["name"] = ""

        response = self.client.post("/registration", data=data)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response_text)

    def test_address_required(self):
        """
        Проверяет, что пустое поле address не проходит валидацию.
        """
        data = self.valid_data()
        data["address"] = ""

        response = self.client.post("/registration", data=data)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn("address", response_text)

    def test_index_required(self):
        """
        Проверяет, что пустой index не проходит валидацию.
        """

        data = self.valid_data()
        data["index"] = ""

        response = self.client.post("/registration", data=data)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn("index", response_text)

    def test_index_must_be_number(self):
        """
        Проверяет, что index должен содержать только число.
        """
        data = self.valid_data()
        data["index"] = "abc"

        response = self.client.post("/registration", data=data)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 400)
        self.assertIn("index", response_text)

    def test_comment_is_optional(self):
        """
        Проверяет, что поле comment необязательное
        и пустое значение не мешает успешной валидации.
        """
        data = self.valid_data()
        data["comment"] = ""

        response = self.client.post("/registration", data=data)
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Successfully registered user", response_text)


if __name__ == '__main__':
    unittest.main()
