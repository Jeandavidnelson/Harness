from architecture_harness.metrics.tokens import measure_tokens


def test_token_measurement_is_deterministic_and_nonzero():
    first = measure_tokens("PaymentService -> StripeClient")
    second = measure_tokens("PaymentService -> StripeClient")
    assert first == second
    assert first.count > 0

