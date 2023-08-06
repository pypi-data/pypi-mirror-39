import django.dispatch

valid_notification_received = django.dispatch.Signal(providing_args=['instance'])
invalid_notification_received = django.dispatch.Signal(providing_args=['instance'])

payment_was_succeed = django.dispatch.Signal(providing_args=['instance'])
payment_was_failed = django.dispatch.Signal(providing_args=['instance'])
payment_is_pending = django.dispatch.Signal(providing_args=['instance'])
payment_was_flagged = django.dispatch.Signal(providing_args=['instance'])
