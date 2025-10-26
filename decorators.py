import time
from typing import Callable, Any, Tuple


# ... (Your existing 'timer' decorator code)


class Product:
    # ... (Your existing __init__, @property, and @price.setter code)

    def __init__(self, name: str, price: float):
        self.name = name
        self._price = price

    @property
    def price(self) -> float:
        """Getter: Returns the product's price."""
        return self._price

    @price.setter
    def price(self, new_price: float):
        """Setter: Validates and sets a new price."""
        if not Product.is_valid_price(
            new_price
        ):  # Using the static method for validation
            raise ValueError("Price cannot be negative.")
        self._price = new_price

    # 1. Static Method
    @staticmethod
    def is_valid_price(price: float) -> bool:
        """
        Static method: Checks if a price is valid (non-negative).
        It does not receive the instance (self) or the class (cls).
        """
        return price >= 0

    # 2. Class Method
    @classmethod
    def create_from_tuple(cls, data_tuple: Tuple[str, float]):
        """
        Class method: Creates a new Product instance from a tuple of (name, price).
        It receives the class itself (cls) as the first argument.
        """
        name, price = data_tuple
        # The key is using 'cls(name, price)' to instantiate the class
        return cls(name, price)


if __name__ == "__main__":
    print("-" * 30)
    # --- Example 1: Static Method Use ---
    # Called directly on the class without needing an instance
    print(f"Is 500 a valid price? {Product.is_valid_price(500.00)}")
    print(f"Is -50 a valid price? {Product.is_valid_price(-50.00)}")

    # --- Example 2: Class Method Use ---
    data = ("Keyboard", 75.50)
    # Called directly on the class. 'cls' inside the method will be 'Product'.
    keyboard = Product.create_from_tuple(data)
    print("-" * 30)
    print("Instance created via class method:")
    print(f"Name: {keyboard.name}, Price: {keyboard.price}")

    # --- Example 3: Property Setter with Static Method Validation ---
    item = Product("Monitor", 300.00)
    # The setter now internally uses Product.is_valid_price(250.00)
    item.price = 250.00
    # item.price = -10.00 # Uncommenting this will raise ValueError
