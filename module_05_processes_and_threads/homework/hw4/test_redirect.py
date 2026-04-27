import io
import unittest
import os
import sys

sys.path.append(os.path.dirname(__file__))

from redirect import Redirect

class TestRedirect(unittest.TestCase):
    def test_stdout_redirect(self):
        """
        Тест проверяет, что stdout перенаправляется в другой поток
        """
        fake_stdout = io.StringIO()

        with Redirect(stdout=fake_stdout):
            print("Hello stdout")

        self.assertIn("Hello stdout", fake_stdout.getvalue())

    def test_stderr_redirect(self):
        """
        Тест проверяет, что stderr перенаправляется в другой поток
        """
        fake_stderr = io.StringIO()

        with Redirect(stderr=fake_stderr):
            raise ValueError("Hello stderr")

        self.assertIn("ValueError: Hello stderr", fake_stderr.getvalue())

    def test_stdout_and_stderr_redirect(self):
        """
        Тест проверяет, что можно одновременно перенаправить stdout и stderr.
        """
        fake_stdout = io.StringIO()
        fake_stderr = io.StringIO()

        with Redirect(stdout=fake_stdout, stderr=fake_stderr):
            print("Hello stdout")
            raise RuntimeError("Hello stderr")

        self.assertIn("Hello stdout", fake_stdout.getvalue())
        self.assertIn("RuntimeError: Hello stderr", fake_stderr.getvalue())

    def test_only_stdout_argument(self):
        """
        Тест проверяет, что контекстный менеджер корректно работает,
        если передан только stdout.
        """
        fake_stdout = io.StringIO()

        with Redirect(stdout=fake_stdout):
            print("Only stdout")

        self.assertIn("Only stdout", fake_stdout.getvalue())

    def test_only_stderr_argument(self):
        """
        Тест проверяет, что контекстный менеджер корректно работает,
        если передан только stderr.
        """
        fake_stderr = io.StringIO()

        with Redirect(stderr=fake_stderr):
            raise Exception("Only stderr")

        self.assertIn("Exception: Only stderr", fake_stderr.getvalue())

    def test_without_arguments(self):
        """
        Тест проверяет, что контекстный менеджер не ломается,
        если аргументы не переданы.
        """
        with Redirect():
            result = 1 + 1

        self.assertEqual(result, 2)

if __name__ == '__main__':
    unittest.main()
    # with open('test_results.txt', 'a') as test_file_stream:
    #     runner = unittest.TextTestRunner(stream=test_file_stream)
    #     unittest.main(testRunner=runner)
