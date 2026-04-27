import os
import sys
import unittest
sys.path.append(os.path.dirname(__file__))
from block_errors import BlockErrors

class TestBlockErrors(unittest.TestCase):
    def test_error_is_ignored(self):
        """
        Тест проверяет, что переданное исключение игнорируется
        """
        try:
            with BlockErrors({ZeroDivisionError}):
                1 / 0
        except Exception:
            self.fail("ZeroDivisionError не должен был быть проброшен")

    def test_error_is_raised(self):
        """
        Тест проверяет, что исключение, которое не было передано, пробрасывается выше
        """
        with self.assertRaises(TypeError):
            with BlockErrors({ZeroDivisionError}):
                1 / "0"

    def test_inner_error_raised_and_outer_ignored(self):
        """
        Тест проверяет, что исключение пробрасывается из внутреннего блока
        и игнорируется внешним блоком
        """
        try:
            with BlockErrors({TypeError}):
                with BlockErrors({ZeroDivisionError}):
                    1 / "0"
        except Exception:
            self.fail("TypeError должен был быть подавлени внешним блоком")

    def test_child_exception_is_ignored(self):
        """
        Тест проверяет, что дочерние исключения тоже игнорируются
        """
        try:
            with BlockErrors({Exception}):
                1 / "0"
        except Exception:
            self.fail("Дочернее исключение не должно было быть проброшено")

if __name__ == '__main__':
    unittest.main()
