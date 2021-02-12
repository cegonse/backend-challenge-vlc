import unittest

from src.bootstrap import Address
from src.bootstrap import Customer
from src.bootstrap import Item
from src.bootstrap import ItemType
from src.bootstrap import Order
from src.bootstrap import OrderItems


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.customer = Customer(
            name='John',
            surname='Smith',
            email_address='john.smith@gogol.kr'
        )
        self.address = Address(
            zip_code='46001',
            street='C/ xxx'
        )

    def test_getting_the_subtotal_for_an_order_containing_one_unit_of_one_item(self):
        screwdriver = Item(
            type=ItemType.PHYSICAL,
            price=10.0,
            name='Screwdriver'
        )

        order = Order(
            customer=self.customer,
            shipping_address=self.address,
            billing_address=self.address,
            items=[
                OrderItems(item=screwdriver, quantity=1)
            ]
        )

        assert order.subtotal == 10.0

    def test_getting_the_subtotal_for_an_order_containing_many_units_of_one_item(self):
        screwdriver = Item(
            type=ItemType.PHYSICAL,
            price=10.0,
            name='Screwdriver'
        )
        order = Order(
            customer=self.customer,
            shipping_address=self.address,
            billing_address=self.address,
            items=[
                OrderItems(item=screwdriver, quantity=3)
            ]
        )

        assert order.subtotal == 30.0

    def test_getting_the_subtotal_for_an_order_containing_many_units_of_many_items(self):
        screwdriver = Item(
            type=ItemType.PHYSICAL,
            price=10.0,
            name='Screwdriver'
        )
        hammer = Item(
            type=ItemType.PHYSICAL,
            price=100.0,
            name='Hammer'
        )

        order = Order(
            customer=self.customer,
            shipping_address=self.address,
            billing_address=self.address,
            items=[
                OrderItems(item=screwdriver, quantity=3),
                OrderItems(item=hammer, quantity=1)
            ]
        )

        assert order.subtotal == 130.0

    def test_order_reports_it_contains_a_physical_item(self):
        screwdriver = Item(
            type=ItemType.PHYSICAL,
            price=10.0,
            name='Screwdriver'
        )
        order = Order(
            customer=self.customer,
            shipping_address=self.address,
            billing_address=self.address,
            items=[
                OrderItems(item=screwdriver, quantity=3)
            ]
        )

        assert order.contains_physical_items is True

    def test_order_reports_it_contains_a_digital_subscription_item(self):
        gogol_music = Item(
            type=ItemType.SUBSCRIPTION,
            price=10.0,
            name='Gogol Music'
        )
        order = Order(
            customer=self.customer,
            shipping_address=self.address,
            billing_address=self.address,
            items=[
                OrderItems(item=gogol_music, quantity=3)
            ]
        )

        assert order.contains_subscriptions is True

    def test_order_reports_it_contains_a_book(self):
        book = Item(
            type=ItemType.BOOK,
            price=10.0,
            name='Python for Dummies'
        )
        order = Order(
            customer=self.customer,
            shipping_address=self.address,
            billing_address=self.address,
            items=[
                OrderItems(item=book, quantity=3)
            ]
        )

        assert order.contains_books is True

    def test_order_reports_it_contains_a_digital_item(self):
        song = Item(
            type=ItemType.DIGITAL_MEDIA,
            price=10.0,
            name='Imagine'
        )
        order = Order(
            customer=self.customer,
            shipping_address=self.address,
            billing_address=self.address,
            items=[
                OrderItems(item=song, quantity=3)
            ]
        )

        assert order.contains_digital_media is True
