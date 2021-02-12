from enum import Enum


class EmailTemplate(Enum):
    SUBSCRIPTION_ACTIVATION = 'subscription_activation'
    DIGITAL_MEDIA_ACCESS = 'digital_media_access'
    DISCOUNT_VOUCHER = 'digital_media_access'


class Email:
    def __init__(self, template, order):
        self.order = order
        self.template = template

    @staticmethod
    def from_template(template, order):
        return Email(template, order)

    def __eq__(self, other):
        return isinstance(other, Email) and other.__dict__ ==  self.__dict__


sent_emails = []


def send(email):
    sent_emails.append(email)


def latest():
    return sent_emails[-1]
