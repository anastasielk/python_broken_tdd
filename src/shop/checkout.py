"""Order checkout.

The rules live in `src/shop/specs/checkout.md` - read it first.
Both functions below are stubs: their signature is final, the bodies are yours.
Do not change the constants: the tests rely on them.
"""

PROMO_CODES = {"WELCOME10": 10, "SUMMER15": 15, "VIP35": 35}
SUPPORTED_CITIES = ("msk", "spb")
MAX_DISCOUNT_PERCENT = 30
VAT_PERCENT = 20
SHIPPING_KOPEKS = 49_000
FREE_DELIVERY_FROM_KOPEKS = 500_000
TIER_DISCOUNTS = ((10, 5), (25, 10), (50, 15))
REQUIRED_LINE_KEYS = ("sku", "qty", "unit_price_kopecks")


def is_int(value: str) -> bool:
    """Tell whether int() would accept the value, without calling it under try/except."""
    digits = value.strip()
    # A sign is valid for int(); negative numbers are rejected later as a separate rule.
    if digits[:1] in ("+", "-"):
        digits = digits[1:]
    return digits.isdecimal()


def validate_order(
    lines: list[dict[str, str]],
    promo_code: str = "",
    shipping_city: str = "",
) -> str | None:
    """Return a human readable reason why the order is invalid, or None if it is fine."""
    if not lines:
        return "order has no lines"
    for number, line in enumerate(lines, start=1):
        for key in REQUIRED_LINE_KEYS:
            if key not in line:
                return f"line {number} is missing key {key!r}"
        if not line["sku"]:
            return "sku must not be empty"
        if not is_int(line["qty"]):
            return f"line {number}: qty must be a whole number"
        if int(line["qty"]) <= 0:
            return f"line {number}: qty must be greater than zero"
        if not is_int(line["unit_price_kopecks"]):
            return f"line {number}: unit_price_kopecks must be a whole number"
    return None


def calculate_order_total(
    lines: list[dict[str, str]],
    promo_code: str = "",
    shipping_city: str = "",
) -> int | None:
    """Return the order total in kopecks, or None if the order is invalid."""
    ...
