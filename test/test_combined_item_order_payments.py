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
    def test_processing_the_payment_of_an_order_containing_all_types_of_items(self):
        order = Order(
            customer=self.customer,
            shipping_address=self.address,
            billing_address=self.address,
            items=[
                OrderItems(item=self.screwdriver, quantity=2),
                OrderItems(item=self.gogol_music, quantity=2),
                OrderItems(item=self.book, quantity=2),
                OrderItems(item=self.movie, quantity=1)
            ]
        )
        payment = Payment(
            payment_method=CreditCard.fetch_by_hased('VISA-xxx'),
            order=order
        )

        payment.pay()

        assert payment.is_paid
        assert payment.order.subtotal == 50.0
        assert payment.order.items[0].item == self.screwdriver
        assert payment.order.items[1].item == self.gogol_music
        assert payment.order.items[2].item == self.book
        assert payment.order.items[3].item == self.movie

        assert self.regular_shipping_label in shipping_labels.pending_labels
        assert self.tax_exempt_shipping_label in shipping_labels.pending_labels

        self.assert_email_was_sent_generated_from_template(order, EmailTemplate.SUBSCRIPTION_ACTIVATION)
        self.assert_email_was_sent_generated_from_template(order, EmailTemplate.DIGITAL_MEDIA_ACCESS)
        self.assert_email_was_sent_generated_from_template(order, EmailTemplate.DISCOUNT_VOUCHER)

        assert self.gogol_music in subscription_service.activated_subscriptions_for_customer(self.customer)

    def setUp(self):
        self.screwdriver = Item(
            type=ItemType.PHYSICAL,
            price=10.0,
            name='Screwdriver'
        )
        self.gogol_music = Item(
            type=ItemType.SUBSCRIPTION,
            price=5.0,
            name='Gogol Music'
        )
        self.book = Item(
            type=ItemType.BOOK,
            price=5.0,
            name='Midnight'
        )
        self.movie = Item(
            type=ItemType.DIGITAL_MEDIA,
            price=10.0,
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
        self.tax_exempt_shipping_label = ShippingLabel(
            shipping_address=self.address,
            customer=self.customer,
            is_tax_exempt=True
        )
        self.regular_shipping_label = ShippingLabel(
            shipping_address=self.address,
            customer=self.customer
        )

    def assert_email_was_sent_generated_from_template(self, order, template):
        assert Email.from_template(template=template, order=order) in email_sender.sent_emails
