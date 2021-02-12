class ShippingLabel:
    def __init__(self, shipping_address, customer, is_tax_exempt=False):
        self.customer = customer
        self.shipping_address = shipping_address
        self.is_tax_exempt = is_tax_exempt

    def __repr__(self):
        return str(f'ShippingLabel <TaxExempt: {self.is_tax_exempt}>')

    def __eq__(self, other):
        return isinstance(other, ShippingLabel) and self.__dict__ == other.__dict__


pending_labels = []


def add(shipping_label):
    pending_labels.append(shipping_label)


def latest():
    return pending_labels[-1]
