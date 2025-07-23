from src.application.ports import PaymentServicePort


class MockPaymentService(PaymentServicePort):
    def charge(self, amount: float) -> bool:
        return amount > 0
