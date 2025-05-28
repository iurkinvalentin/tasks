import inspect


def strict(func):
    sig = inspect.signature(func)
    annotations = func.__annotations__

    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

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


@strict
def sum_two(a: int, b: int) -> int:
    return a + b

print(sum_two(1, 2))       # 3
print(sum_two(1, 2.4))     # TypeError
