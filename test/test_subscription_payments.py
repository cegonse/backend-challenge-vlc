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
    def test_processing_the_payment_for_an_order_containing_multiple_subscriptions(self):
        order = Order(
            customer=self.customer,
            shipping_address=self.address,
            billing_address=self.address,
            items=[
                OrderItems(item=self.gogol_music, quantity=1),
                OrderItems(item=self.spotofy, quantity=1)
            ]
        )
        payment = Payment(
            payment_method=CreditCard.fetch_by_hased('VISA-xxx'),
            order=order
        )

        payment.pay()

        assert payment.is_paid
        assert payment.order.subtotal == 10.0
        assert payment.order.items[0].item == self.gogol_music
        assert payment.order.items[1].item == self.spotofy

        assert email_sender.latest() == Email.from_template(
            template=EmailTemplate.SUBSCRIPTION_ACTIVATION,
            order=order
        )

        assert self.gogol_music in subscription_service.activated_subscriptions_for_customer(self.customer)
        assert self.spotofy in subscription_service.activated_subscriptions_for_customer(self.customer)

    def setUp(self):
        self.gogol_music = Item(
            type=ItemType.SUBSCRIPTION,
            price=5.0,
            name='Gogol Music'
        )
        self.spotofy = Item(
            type=ItemType.SUBSCRIPTION,
            price=5.0,
            name='Spotofy'
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
