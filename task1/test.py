import unittest
import inspect

def strict(func):
    sig = inspect.signature(func)
    annotations = func.__annotations__

    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            if name in annotations:
                expected_type = annotations[name]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Argument '{name}' must be {expected_type.__name__}, "
                        f"got {type(value).__name__}"
                    )
        return func(*args, **kwargs)

    return wrapper

# Тестовые функции с декоратором @strict
@strict
def sum_two(a: int, b: int) -> int:
    return a + b

@strict
def concat(s1: str, s2: str) -> str:
    return s1 + s2

@strict
def check_bool(b: bool) -> bool:
    return b

@strict
def multiply_float(a: float, b: float) -> float:
    return a * b

@strict
def mixed_types(a: int, b: str, c: float) -> float:
    return a + len(b) + c

class TestStrictDecorator(unittest.TestCase):
    def test_sum_two_correct(self):
        """Тестирование корректных аргументов (int) для sum_two."""
        self.assertEqual(sum_two(1, 2), 3)
        self.assertEqual(sum_two(0, -5), -5)

    def test_sum_two_incorrect_type(self):
        """Тестирование некорректных типов для sum_two."""
        with self.assertRaises(TypeError) as cm:
            sum_two(1, 2.4)
        self.assertEqual(str(cm.exception), "Argument 'b' must be int, got float")

        with self.assertRaises(TypeError) as cm:
            sum_two("1", 2)
        self.assertEqual(str(cm.exception), "Argument 'a' must be int, got str")

    def test_sum_two_named_args(self):
        """Тестирование именованных аргументов для sum_two."""
        self.assertEqual(sum_two(a=1, b=2), 3)
        with self.assertRaises(TypeError) as cm:
            sum_two(a=1, b="2")
        self.assertEqual(str(cm.exception), "Argument 'b' must be int, got str")

    def test_concat_correct(self):
        """Тестирование корректных аргументов (str) для concat."""
        self.assertEqual(concat("hello", "world"), "helloworld")
        self.assertEqual(concat("", "test"), "test")

    def test_concat_incorrect_type(self):
        """Тестирование некорректных типов для concat."""
        with self.assertRaises(TypeError) as cm:
            concat("hello", 123)
        self.assertEqual(str(cm.exception), "Argument 's2' must be str, got int")

    def test_check_bool_correct(self):
        """Тестирование корректных аргументов (bool) для check_bool."""
        self.assertEqual(check_bool(True), True)
        self.assertEqual(check_bool(False), False)

    def test_check_bool_incorrect_type(self):
        """Тестирование некорректных типов для check_bool."""
        with self.assertRaises(TypeError) as cm:
            check_bool(1)
        self.assertEqual(str(cm.exception), "Argument 'b' must be bool, got int")

        with self.assertRaises(TypeError) as cm:
            check_bool("True")
        self.assertEqual(str(cm.exception), "Argument 'b' must be bool, got str")

    def test_multiply_float_correct(self):
        """Тестирование корректных аргументов (float) для multiply_float."""
        self.assertEqual(multiply_float(2.5, 3.0), 7.5)
        self.assertEqual(multiply_float(0.0, 1.5), 0.0)

    def test_multiply_float_incorrect_type(self):
        """Тестирование некорректных типов для multiply_float."""
        with self.assertRaises(TypeError) as cm:
            multiply_float(2.5, "3.0")
        self.assertEqual(str(cm.exception), "Argument 'b' must be float, got str")

    def test_mixed_types_correct(self):
        """Тестирование корректных аргументов для mixed_types."""
        self.assertEqual(mixed_types(1, "abc", 2.5), 6.5)  # 1 + len("abc") + 2.5 = 6.5

    def test_mixed_types_incorrect_type(self):
        """Тестирование некорректных типов для mixed_types."""
        with self.assertRaises(TypeError) as cm:
            mixed_types(1, "abc", "2.5")
        self.assertEqual(str(cm.exception), "Argument 'c' must be float, got str")

if __name__ == '__main__':
    unittest.main()