from enum import Enum


class EmailTemplate(Enum):
    SUBSCRIPTION_ACTIVATION = 'subscription_activation'


class Email:
    def __init__(self, template, order):
        self.order = order
        self.template = template

    @staticmethod
    def from_template(template, order):
        return Email(template, order)

    def __eq__(self, other):
        return isinstance(other, Email) and other.__dict__ ==  self.__dict__


emails = []


def send(email):
    emails.append(email)


def latest():
    return emails[-1]
