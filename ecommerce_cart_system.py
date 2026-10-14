"""A small e-commerce cart demo cleaned up for Lab 5 static analysis."""

import hashlib
import json
import logging
import math
import secrets
from pathlib import Path

LOGGER = logging.getLogger(__name__)

CART_ITEMS = {
    "ITEM1": {"name": "Wireless Mouse", "price": 25.0, "qty": 2},
    "ITEM2": {"name": "Mechanical Keyboard", "price": 80.0, "qty": 1},
    "ITEM3": {"name": "USB-C Hub", "price": 45.0, "qty": 3},
}


def add_item_to_cart(item_id, name, price, qty=1, audit_log=None):
    """Add a new item to the cart after validating its details.

    Return False if the item ID already exists. Invalid item details raise
    ValueError rather than being added to the cart.
    """
    if not isinstance(item_id, str) or not item_id.strip():
        raise ValueError("Item ID must be a non-empty string.")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Item name must be a non-empty string.")
    if isinstance(price, bool) or not isinstance(price, (int, float)):
        raise ValueError("Price must be a number.")
    if not math.isfinite(price) or price < 0:
        raise ValueError("Price must be finite and cannot be negative.")
    if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
        raise ValueError("Quantity must be a positive integer.")
    if item_id in CART_ITEMS:
        LOGGER.warning("Item %s already exists in the cart.", item_id)
        return False

    CART_ITEMS[item_id] = {
        "name": name.strip(),
        "price": float(price),
        "qty": qty,
    }

    if audit_log is not None:
        audit_log.append(f"Added {item_id} at {float(price):.2f} each.")
    LOGGER.info("Added item %s to the cart.", item_id)
    return True


def remove_item_from_cart(item_id):
    """Remove an item from the cart and report whether it was present."""
    removed_item = CART_ITEMS.pop(item_id, None)
    if removed_item is None:
        LOGGER.warning("Cannot remove %s: item was not found.", item_id)
        return False

    LOGGER.info("Removed item %s from the cart.", item_id)
    return True


def check_cart_status(item_id):
    """Return True when the item exists and has a positive quantity."""
    item = CART_ITEMS.get(item_id)
    return item is not None and item["qty"] > 0


def calculate_discounted_total(item_id, discount_rate=0.10):
    """Return the discounted unit price for an item.

    ``discount_rate`` is a fraction from 0.0 to 1.0. Accepting a numeric rate
    instead of an expression string avoids executing user-supplied code.
    """
    item = CART_ITEMS.get(item_id)
    if item is None:
        raise KeyError(f"Item {item_id!r} was not found in the cart.")
    is_numeric_rate = isinstance(discount_rate, (int, float))
    if isinstance(discount_rate, bool) or not is_numeric_rate:
        raise ValueError("Discount rate must be a number between 0 and 1.")
    if not math.isfinite(discount_rate) or not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")

    return round(item["price"] * (1.0 - discount_rate), 2)


def generate_item_hash(item_id):
    """Return a SHA-256 digest for a product identifier.

    This digest is an identifier/checksum, not an authentication mechanism.
    """
    if not isinstance(item_id, str):
        raise TypeError("Item ID must be a string.")
    return hashlib.sha256(item_id.encode("utf-8")).hexdigest()


def generate_checkout_pin():
    """Generate a four-digit PIN using a cryptographically secure generator."""
    return secrets.randbelow(9000) + 1000


def export_cart_receipt(filename="receipt.txt"):
    """Write a JSON-formatted snapshot of the current cart to a file."""
    receipt_path = Path(filename)
    receipt_path.write_text(
        json.dumps(CART_ITEMS, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    LOGGER.info("Receipt saved to %s", receipt_path)
    return receipt_path


def calculate_cart_total(items=None):
    """Calculate the total value of the selected cart items."""
    source_items = CART_ITEMS if items is None else items
    total = sum(
        float(details["price"]) * int(details["qty"])
        for details in source_items.values()
    )
    return round(total, 2)


def get_cart_summary(items=None):
    """Return the total quantity of items with a positive quantity."""
    source_items = CART_ITEMS if items is None else items
    return sum(
        int(details["qty"])
        for details in source_items.values()
        if int(details["qty"]) > 0
    )


def main():
    """Run a short demonstration of the cart operations."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    audit_log = []

    add_item_to_cart("ITEM4", "Monitor Stand", 35.0, 1, audit_log)
    remove_item_from_cart("ITEM2")

    print("Is ITEM1 in cart:", check_cart_status("ITEM1"))
    print("Discounted Price:", calculate_discounted_total("ITEM1"))
    print("Item Hash:", generate_item_hash("ITEM1"))
    print("Checkout PIN generated securely.")
    print("Total items:", get_cart_summary())
    print("Cart total:", f"${calculate_cart_total():.2f}")

    for entry in audit_log:
        LOGGER.info("Audit: %s", entry)

    export_cart_receipt()


if __name__ == "__main__":
    main()
