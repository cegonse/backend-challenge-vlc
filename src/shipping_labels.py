class ShippingLabel:
    def __init__(self, shipping_address, customer):
        self.customer = customer
        self.shipping_address = shipping_address

    def __eq__(self, other):
        return isinstance(other, ShippingLabel) and self.__dict__ == other.__dict__


pending_labels = []


def add(shipping_label):
    pending_labels.append(shipping_label)


def latest():
    return pending_labels[-1]
