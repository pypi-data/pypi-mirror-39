from django.forms.fields import CharField
from stem_feedback.models import *
from django import forms
from django.utils.translation import ugettext as _
from stem_feedback.middleware import current_user


class FeedbackEmailForm(forms.ModelForm):
    from_email = forms.EmailField(required=True, label=_('Ваш email'))
    subject = CharField(max_length=30, required=False, label=_("Тема обращения"))
    type = forms.ModelChoiceField(queryset=FeedBackType.objects.all(),
                                            required=False,
                                            label=_('Тип обращения'))
    message = forms.CharField(widget=forms.Textarea, required=True, label=_('Текст'))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if self.user !='':
            self.fields['from_email'] = forms.EmailField(
                required=False,
                widget=forms.HiddenInput(),
            )

    class Meta:
        model = Feedback
        fields = (
            'from_email',
            'subject',
            'type',
            'message',
        )


SETTLEMENT_ACCOUNT = 'settlement_account'
CARD_ACCOUNT = 'card_account'
COURIER = 'courier'
PAYMENT_CHOICES = (
    (SETTLEMENT_ACCOUNT, 'Расчетный счет'),
    (CARD_ACCOUNT, 'Карточный счет'),
    (COURIER, 'Курьер'),
)


class PaymentNotificationForm(forms.Form):
    type = forms.ModelChoiceField(queryset=FeedBackType.objects.all(),
                                  required=False,
                                  label=_('Тип обращения'))
    payment_type = forms.ChoiceField(choices=PAYMENT_CHOICES,
                                     widget=forms.RadioSelect(), label=_("Форма оплаты"))
    sum = CharField(max_length=255, required=False, label=_("Сумма"))

    currency = forms.ChoiceField(required=False,
                                 choices=[],
                                 widget=forms.Select, label=_('Валюта'))

    customer = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select, label=_('Покупатель')
    )

    def __init__(self, customers, currency, *args, **kwargs):
        self.customers = customers
        self.currency = currency
        super().__init__(*args, **kwargs)
        self.fields['customer'].choices = self.customers
        self.fields['currency'].choices = self.currency