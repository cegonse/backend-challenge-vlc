from enum import Enum

from src import email_sender
from src import shipping_labels
from src import subscription_service
from src.email_sender import Email
from src.email_sender import EmailTemplate
from src.shipping_labels import ShippingLabel


class ItemType(Enum):
    PHYSICAL = 'physical'
    SUBSCRIPTION = 'subscription'
    BOOK = 'book'
    DIGITAL_MEDIA = 'digital_media'


class Item:
    def __init__(self, type, price, name):
        self.name = name
        self.price = price
        self.type = type


class Customer:
    def __init__(self, name, surname, email_address):
        self.email_address = email_address
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
    def contains_subscriptions(self):
        return self.__contains_item_of_type(ItemType.SUBSCRIPTION)

    @property
    def contains_physical_items(self):
        return self.__contains_item_of_type(ItemType.PHYSICAL)

    @property
    def contains_books(self):
        return self.__contains_item_of_type(ItemType.BOOK)

    @property
    def contains_digital_media(self):
        return self.__contains_item_of_type(ItemType.DIGITAL_MEDIA)

    @property
    def subtotal(self):
        total = 0.0

        for order_items in self.items:
            total = total + order_items.quantity * order_items.item.price

        return total

    def __contains_item_of_type(self, type):
        for order_items in self.items:
            if order_items.item.type == type:
                return True

        return False


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

        if self.order.contains_physical_items:
            self.__postprocess_physical_items()

        if self.order.contains_subscriptions:
            self.__postprocess_digital_subscriptions()

        if self.order.contains_books:
            self.__postprocess_books()

        if self.order.contains_digital_media:
            self.__postprocess_digital_media()

    def __postprocess_digital_subscriptions(self):
        self.__send_email_from_template(EmailTemplate.SUBSCRIPTION_ACTIVATION)

    def __postprocess_physical_items(self):
        self.__generate_shipping_label(is_tax_exempt=False)

    def __postprocess_books(self):
        self.__generate_shipping_label(is_tax_exempt=True)

    def __postprocess_digital_media(self):
        self.__send_email_from_template(EmailTemplate.DIGITAL_MEDIA_ACCESS)
        self.__send_email_from_template(EmailTemplate.DISCOUNT_VOUCHER)

    def __generate_shipping_label(self, is_tax_exempt):
        shipping_labels.add(ShippingLabel(
            customer=self.order.customer,
            shipping_address=self.order.shipping_address,
            is_tax_exempt=is_tax_exempt
        ))

    def __send_email_from_template(self, template):
        email_sender.send(
            Email.from_template(
                template=template,
                order=self.order
            )
        )
        self.__activate_digital_subscriptions()

    def __activate_digital_subscriptions(self):
        digital_subscriptions = [order_item.item for order_item in self.order.items if order_item.item.type == ItemType.SUBSCRIPTION]

        for subscription in digital_subscriptions:
            subscription_service.activate_subscription(self.order.customer, subscription)


class CreditCard:
    @staticmethod
    def fetch_by_hased(hash_string):
        return CreditCard()
