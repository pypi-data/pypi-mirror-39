from django import forms

from django_paymentsos.models import PaymentOSNotification


class PaymentNotificationForm(forms.ModelForm):
    class Meta:
        model = PaymentOSNotification
        fields = '__all__'
