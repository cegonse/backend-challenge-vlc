subscriptions = {}


def activated_subscriptions_for_customer(customer):
    return subscriptions[customer]


def activate_subscription(customer, item):
    if customer not in subscriptions:
        subscriptions[customer] = []

    subscriptions[customer].append(item)
