def add(a, b):
    """Return the sum of two numbers.

    Parameters
    ----------
    a : int | float
        The first addend.
    b : int | float
        The second addend.

    Returns
    -------
    int | float
        The arithmetic sum of *a* and *b*.
    """
    return a + b


def _demo():
    """Demonstrate adding 1 and 2 when run as a script."""
    result = add(1, 2)
    print(f"1 + 2 = {result}")


if __name__ == "__main__":
    _demo()
