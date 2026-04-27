import os.path
import sys
import unittest

sys.path.append(os.path.dirname(__file__))

from remote_execution import app

class TestRemoteExecution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Выполняется один раз перед запуском всех тестов.
        """
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        cls.client = app.test_client()

    def test_run_code_success(self):
        """
        Тест проверяет, что корректный Python-код успешно выполняется.
        """
        response = self.client.post("/run_code", data={
            "code": "print('Hello world!')",
            "timeout": "5"
        })

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("Hello world!", data["stdout"])

    def test_run_code_timeout(self):
        """
        Тест проверяет, что процесс завершается по тайм-ауту.
        """
        response = self.client.post("/run_code", data={
            "code": "import time; time.sleep(5); print('Done')",
            "timeout": "1"
        })

        self.assertEqual(response.status_code, 408)

        data = response.get_json()
        self.assertEqual(data["status"], "timeout")
        self.assertEqual(data["message"], "Execution timed out")

    def test_invalid_form_data(self):
        """
        Тест проверяет невалидные данные формы:
        пустой код и слишком большой тайм-аут.
        """
        response = self.client.post("/run_code", data={
            "code": "",
            "timeout": "31"
        })

        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertEqual(data["status"], "error")
        self.assertIn("code", data["errors"])
        self.assertIn("timeout", data["errors"])

    def test_shell_injection_does_not_work(self):
        """
        Тест проверяет, что небезопасный ввод не срабатывает как shell injection.
        """
        response = self.client.post("/run_code", data={
            "code": 'print("safe")"; echo hacked',
            "timeout": "5"
        })

        self.assertIn(response.status_code, (200, 408))

        data = response.get_json()
        stdout = data.get("stdout", "")
        stderr = data.get("stderr", "")

        self.assertNotIn("safe\nhacked", stdout)
        self.assertNotEqual(stdout.strip(), "hacked")

if __name__ == '__main__':
    unittest.main()
