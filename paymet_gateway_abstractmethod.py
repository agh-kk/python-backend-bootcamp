from abc import ABC, abstractmethod


class PaymentGateway(ABC):

    @abstractmethod
    def initialize_payment(self, amount, recipient):
        pass

    @abstractmethod
    def refund_payment(self, transaction_id):
        pass

    class UPIPaymentGateway(PaymentGateway):
        def initialize_payment(self, amount, recipient):
            print(f"Initializing UPI payment of {amount} to {recipient}.")

        def refund_payment(self, transaction_id):
            print(f"Refunding UPI payment with transaction ID: {transaction_id}.")
