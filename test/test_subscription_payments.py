import unittest

from src import email_sender
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


class TestSubscriptionPayments(unittest.TestCase):
    def test_processing_the_payment_for_an_order_containing_multiple_physical_items(self):
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
                OrderItems(item=gogol_music, quantity=1)
            ]
        )
        payment = Payment(
            payment_method=CreditCard.fetch_by_hased('VISA-xxx'),
            order=order
        )

        payment.pay()

        assert payment.is_paid
        assert payment.order.subtotal == 5.0
        assert payment.order.items[0].item == gogol_music

        assert email_sender.latest() == Email.from_template(
            template=EmailTemplate.SUBSCRIPTION_ACTIVATION,
            order=order
        )

        assert gogol_music in subscription_service.activated_subscriptions_for_customer(customer)
