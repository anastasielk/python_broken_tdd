"""Order checkout.

The rules live in `src/shop/specs/checkout.md` - read it first.
Both functions below are stubs: their signature is final, the bodies are yours.
Do not change the constants: the tests rely on them.
"""

from shop.money import percent_of

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


def validate_line(number: int, line: dict[str, str]) -> str | None:
    """Return the reason why one order line is invalid, or None if it is fine."""
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
    if int(line["unit_price_kopecks"]) < 0:
        return f"line {number}: unit_price_kopecks must not be negative"
    return None


def validate_order(
    lines: list[dict[str, str]],
    promo_code: str = "",
    shipping_city: str = "",
) -> str | None:
    """Return a human readable reason why the order is invalid, or None if it is fine."""
    if not lines:
        return "order has no lines"
    seen_skus: set[str] = set()
    for number, line in enumerate(lines, start=1):
        reason = validate_line(number, line)
        if reason is not None:
            return reason
        if line["sku"] in seen_skus:
            return f"line {number}: sku {line['sku']!r} is repeated"
        seen_skus.add(line["sku"])
    if promo_code and promo_code not in PROMO_CODES:
        return f"unknown promo code {promo_code!r}"
    if shipping_city and shipping_city not in SUPPORTED_CITIES:
        return f"unsupported shipping city {shipping_city!r}"
    return None


def calculate_order_total(
    lines: list[dict[str, str]],
    promo_code: str = "",
    shipping_city: str = "",
) -> int | None:
    """Return the order total in kopecks, or None if the order is invalid."""
    if validate_order(lines, promo_code, shipping_city) is not None:
        return None
    subtotal = sum(int(line["qty"]) * int(line["unit_price_kopecks"]) for line in lines)
    units = sum(int(line["qty"]) for line in lines)
    discount_percent = 0
    # Thresholds are sorted ascending, so the last match is the highest one, as the spec requires.
    for threshold, tier_percent in TIER_DISCOUNTS:
        if units >= threshold:
            discount_percent = tier_percent
    discounted_subtotal = subtotal - percent_of(subtotal, discount_percent)
    return discounted_subtotal + percent_of(discounted_subtotal, VAT_PERCENT)
