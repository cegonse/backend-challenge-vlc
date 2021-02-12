import unittest

from src import shipping_labels
from src.bootstrap import Address
from src.bootstrap import CreditCard
from src.bootstrap import Customer
from src.bootstrap import Item
from src.bootstrap import ItemType
from src.bootstrap import Order
from src.bootstrap import OrderItems
from src.bootstrap import Payment
from src.shipping_labels import ShippingLabel


class TestPhysicalItemOrderPayments(unittest.TestCase):
    def test_processing_the_payment_for_an_order_containing_multiple_physical_items(self):
        order = Order(
            customer=self.customer,
            shipping_address=self.address,
            billing_address=self.address,
            items=[
                OrderItems(item=self.screwdriver, quantity=2),
                OrderItems(item=self.hammer, quantity=2),
            ]
        )
        payment = Payment(
            payment_method=CreditCard.fetch_by_hased('VISA-xxx'),
            order=order
        )

        payment.pay()

        assert payment.is_paid
        assert payment.order.subtotal == 30.0
        assert payment.order.items[0].item == self.screwdriver
        assert payment.order.items[1].item == self.hammer

        latest_shipping_label = shipping_labels.latest()
        assert latest_shipping_label == ShippingLabel(
            shipping_address=self.address,
            customer=self.customer
        )

    def setUp(self):
        self.screwdriver = Item(
            type=ItemType.PHYSICAL,
            price=10.0,
            name='Screwdriver'
        )
        self.hammer = Item(
            type=ItemType.PHYSICAL,
            price=5.0,
            name='Hammer'
        )
        self.customer = Customer(
            name='John',
            surname='Smith',
            email_address='john.smith@gogol.eus'
        )
        self.address = Address(
            zip_code='46001',
            street='C/ xxx'
        )
