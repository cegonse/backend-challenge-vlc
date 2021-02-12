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


class TestPaymentProcessingAction(unittest.TestCase):
    def test_processing_the_payment_for_an_order_containing_one_physical_item_generates_a_shipping_label(self):
        screwdriver = Item(
            type=ItemType.PHYSICAL,
            price=10.0,
            name='Screwdriver'
        )
        customer = Customer(
            name='John',
            surname='Smith'
        )
        address = Address(
            zip_code='46001',
            street='C/ xxx'
        )
        order = Order(
            customer=customer,
            shipping_address=address,
            billing_address=address,
            items=[
                OrderItems(item=screwdriver, quantity=1)
            ]
        )
        payment = Payment(
            payment_method=CreditCard.fetch_by_hased('VISA-xxx'),
            order=order
        )

        payment.pay()

        assert payment.is_paid
        assert payment.order.subtotal == 10.0
        assert payment.order.items[0].item == screwdriver

        latest_shipping_label = shipping_labels.latest()
        assert latest_shipping_label == ShippingLabel(
            shipping_address=address,
            customer=customer
        )

    def test_processing_the_payment_for_an_order_containing_multiple_physical_items(self):
        screwdriver = Item(
            type=ItemType.PHYSICAL,
            price=10.0,
            name='Screwdriver'
        )
        hammer = Item(
            type=ItemType.PHYSICAL,
            price=5.0,
            name='Hammer'
        )
        customer = Customer(
            name='John',
            surname='Smith'
        )
        address = Address(
            zip_code='46001',
            street='C/ xxx'
        )
        order = Order(
            customer=customer,
            shipping_address=address,
            billing_address=address,
            items=[
                OrderItems(item=screwdriver, quantity=2),
                OrderItems(item=hammer, quantity=2),
            ]
        )
        payment = Payment(
            payment_method=CreditCard.fetch_by_hased('VISA-xxx'),
            order=order
        )

        payment.pay()

        assert payment.is_paid
        assert payment.order.subtotal == 30.0
        assert payment.order.items[0].item == screwdriver
        assert payment.order.items[1].item == hammer

        latest_shipping_label = shipping_labels.latest()
        assert latest_shipping_label == ShippingLabel(
            shipping_address=address,
            customer=customer
        )
