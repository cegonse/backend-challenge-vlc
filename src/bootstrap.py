from enum import Enum

from src import shipping_labels
from src.shipping_labels import ShippingLabel


class ItemType(Enum):
    PHYSICAL = 'physical'


class Item:
    def __init__(self, type, price, name):
        self.name = name
        self.price = price
        self.type = type


class Customer:
    def __init__(self, name, surname):
        self.surname = surname
        self.name = name


class Address:
    def __init__(self, zip_code, street):
        self.street = street
        self.zip_code = zip_code


class Order:
    def __init__(self, customer, billing_address, shipping_address, items):
        self.items = items
        self.shipping_address = shipping_address
        self.billing_address = billing_address
        self.customer = customer

    @property
    def subtotal(self):
        total = 0.0

        for order_items in self.items:
            total = total + order_items.quantity * order_items.item.price

        return total


class OrderItems:
    def __init__(self, item, quantity):
        self.quantity = quantity
        self.item = item


class Payment:
    def __init__(self, payment_method, order):
        self.order = order
        self.payment_method = payment_method
        self.is_paid = False

    def pay(self):
        self.is_paid = True

        shipping_labels.add(ShippingLabel(
            customer=self.order.customer,
            shipping_address=self.order.shipping_address
        ))


class CreditCard:
    @staticmethod
    def fetch_by_hased(hash_string):
        return CreditCard()
