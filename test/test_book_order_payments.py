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


class TestBookOrderPayments(unittest.TestCase):
    def test_processing_the_payment_for_an_order_containing_multiple_books(self):
        lord_of_the_cubes = Item(
            type=ItemType.BOOK,
            price=10.0,
            name='Lord of the Cubes'
        )
        midnight = Item(
            type=ItemType.BOOK,
            price=5.0,
            name='Midnight'
        )
        customer = Customer(
            name='John',
            surname='Smith',
            email_address='john.smith@gogol.eus'
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
                OrderItems(item=lord_of_the_cubes, quantity=2),
                OrderItems(item=midnight, quantity=2),
            ]
        )
        payment = Payment(
            payment_method=CreditCard.fetch_by_hased('VISA-xxx'),
            order=order
        )

        payment.pay()

        assert payment.is_paid
        assert payment.order.subtotal == 30.0
        assert payment.order.items[0].item == lord_of_the_cubes
        assert payment.order.items[1].item == midnight

        latest_shipping_label = shipping_labels.latest()
        assert latest_shipping_label == ShippingLabel(
            shipping_address=address,
            customer=customer,
            is_tax_exempt=True
        )
