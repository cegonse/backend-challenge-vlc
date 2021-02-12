import unittest

from src import email_sender
from src import shipping_labels
from src import subscription_service
from src.bootstrap import Address
from src.bootstrap import CreditCard
from src.bootstrap import Customer
from src.bootstrap import Item
from src.bootstrap import ItemType
from src.bootstrap import Order
from src.bootstrap import OrderItems
from src.bootstrap import Payment
from src.email_sender import Email
from src.email_sender import EmailTemplate
from src.shipping_labels import ShippingLabel


class TestCombinedItemOrderPayments(unittest.TestCase):
    def test_processing_the_payment_of_an_order_containing_a_physical_item_and_a_subscription(self):
        screwdriver = Item(
            type=ItemType.PHYSICAL,
            price=10.0,
            name='Screwdriver'
        )
        gogol_music = Item(
            type=ItemType.SUBSCRIPTION,
            price=5.0,
            name='Gogol Music'
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
                OrderItems(item=screwdriver, quantity=2),
                OrderItems(item=gogol_music, quantity=2),
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
        assert payment.order.items[1].item == gogol_music

        latest_shipping_label = shipping_labels.latest()
        assert latest_shipping_label == ShippingLabel(
            shipping_address=address,
            customer=customer
        )

        assert email_sender.latest() == Email.from_template(
            template=EmailTemplate.SUBSCRIPTION_ACTIVATION,
            order=order
        )

        assert gogol_music in subscription_service.activated_subscriptions_for_customer(customer)
