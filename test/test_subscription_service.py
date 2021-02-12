import unittest

from src import subscription_service
from src.bootstrap import Customer
from src.bootstrap import Item
from src.bootstrap import ItemType


class TestSubscriptionService(unittest.TestCase):
    def test_activating_a_subscription_for_a_customer(self):
        gogol_music = Item(
            type=ItemType.SUBSCRIPTION,
            name='Gogol Music',
            price=10.0
        )
        customer = Customer(
            name='John',
            surname='Smith',
            email_address='john.smith@gogol.eus'
        )

        subscription_service.activate_subscription(customer, gogol_music)

        assert gogol_music in subscription_service.activated_subscriptions_for_customer(customer)

    def test_activating_many_subscriptions_for_a_customer(self):
        gogol_music = Item(
            type=ItemType.SUBSCRIPTION,
            name='Gogol Music',
            price=10.0
        )
        spotofy = Item(
            type=ItemType.SUBSCRIPTION,
            name='Spotofy',
            price=10.0
        )
        customer = Customer(
            name='John',
            surname='Smith',
            email_address='john.smith@gogol.eus'
        )

        subscription_service.activate_subscription(customer, gogol_music)
        subscription_service.activate_subscription(customer, spotofy)

        assert gogol_music in subscription_service.activated_subscriptions_for_customer(customer)
        assert spotofy in subscription_service.activated_subscriptions_for_customer(customer)

    def test_activating_many_subscriptions_for_different_customers(self):
        gogol_music = Item(
            type=ItemType.SUBSCRIPTION,
            name='Gogol Music',
            price=10.0
        )
        spotofy = Item(
            type=ItemType.SUBSCRIPTION,
            name='Spotofy',
            price=10.0
        )
        john = Customer(
            name='John',
            surname='Smith',
            email_address='john.smith@gogol.eus'
        )
        peter = Customer(
            name='Peter',
            surname='Smith',
            email_address='john.smith@gogol.eus'
        )

        subscription_service.activate_subscription(john, gogol_music)
        subscription_service.activate_subscription(john, spotofy)
        subscription_service.activate_subscription(peter, gogol_music)
        subscription_service.activate_subscription(peter, spotofy)

        assert gogol_music in subscription_service.activated_subscriptions_for_customer(john)
        assert spotofy in subscription_service.activated_subscriptions_for_customer(john)
        assert gogol_music in subscription_service.activated_subscriptions_for_customer(peter)
        assert spotofy in subscription_service.activated_subscriptions_for_customer(peter)
