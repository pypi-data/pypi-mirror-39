import hmac

from django_paymentsos.settings import paymentsos_settings as settings


def get_signature(event_type, webhook_id, account_id, payment_id, created, app_id, data_id, status, category,
                  sub_category, response_code, reconciliation_id, amount, currency):
    fmt = '{},{},{},{},{},{},{},{},{},{},{},{},{},{}'
    data = fmt.format(event_type, webhook_id, account_id, payment_id, created, app_id, data_id, status, category,
                      sub_category, response_code, reconciliation_id, amount, currency)
    return hmac.new(settings.PRIVATE_KEY.encode('utf'), data.encode('utf')).hexdigest()
