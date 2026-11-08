

import re
from decimal import Decimal
from typing import Callable, Iterator


NUMBER_PATTERN = re.compile(r"(?<!\S)\d+(?:\.\d+)?(?!\S)")


def generator_numbers(text: str) -> Iterator[Decimal]:

    for match in NUMBER_PATTERN.finditer(text):

        yield Decimal(match.group())


def sum_profit(text: str, func: Callable[[str], Iterator[Decimal]]) -> Decimal:

    return sum(func(text), Decimal("0"))


if __name__ == "__main__":
    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими надходженнями "
        "27.45 і 324.00 доларів."
    )
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")