import unittest

from src import email_sender
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


class TestDigitalMediaOrderPayments(unittest.TestCase):
    def test_processing_the_payment_for_an_order_containing_multiple_digital_media(self):
        order = Order(
            customer=self.customer,
            shipping_address=self.address,
            billing_address=self.address,
            items=[
                OrderItems(item=self.avator, quantity=2),
                OrderItems(item=self.mission_possible, quantity=2),
            ]
        )
        payment = Payment(
            payment_method=CreditCard.fetch_by_hased('VISA-xxx'),
            order=order
        )

        payment.pay()

        assert payment.is_paid
        assert payment.order.subtotal == 30.0
        assert payment.order.items[0].item == self.avator
        assert payment.order.items[1].item == self.mission_possible

        self.assert_email_was_sent_generated_from_template(order, EmailTemplate.DIGITAL_MEDIA_ACCESS)
        self.assert_email_was_sent_generated_from_template(order, EmailTemplate.DISCOUNT_VOUCHER)

    def setUp(self):
        self.avator = Item(
            type=ItemType.DIGITAL_MEDIA,
            price=10.0,
            name='Avator'
        )
        self.mission_possible = Item(
            type=ItemType.DIGITAL_MEDIA,
            price=5.0,
            name='Mission Possible'
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

    def assert_email_was_sent_generated_from_template(self, order, template):
        assert Email.from_template(template=template, order=order) in email_sender.sent_emails
