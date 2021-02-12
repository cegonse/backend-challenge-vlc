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
            surname='Smith'
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
