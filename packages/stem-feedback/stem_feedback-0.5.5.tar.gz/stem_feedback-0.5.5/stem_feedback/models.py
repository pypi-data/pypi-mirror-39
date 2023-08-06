from django.db import models
from django.utils.translation import ugettext_lazy as _


class FeedBackType(models.Model):
    """
    Тип обратных связей от клиентов.
    Указывается (используется) в форме обратной связи
    """
    EVENT = 'event'
    RETURN = 'return'
    PAYMENT_NOTIFICATION = 'payment_notification'
    FEEDBACK_TYPE = (
        (EVENT, _('Обычное обращение')),
        (RETURN, _('Возврат')),
        (PAYMENT_NOTIFICATION, _('Сообщение об оплате'))
    )
    feedback_type = models.CharField(
        max_length=30, choices=FEEDBACK_TYPE, default=EVENT, blank=True,
        verbose_name=_('Тип обратной связи'),
        help_text=_('Тип обратной связи')
    )

    desc = models.CharField(
        max_length=255, default='', blank=True,
        verbose_name=_('Описание'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование обращения ',
        help_text='Наименование обращения')

    email = models.EmailField(
        max_length=255, default='',
        verbose_name='E-mail',
        help_text='Адрес, на который будут приходить собщения с данным типом. '
                  'Например, сообщения с типом "Сообщить об оплате" должны приходить сотруднику финансовой (службы).'
    )

    class Meta:
        db_table = 'feed_back_type'
        verbose_name = _('Тип обратной связи')
        verbose_name_plural = _('Типы обратной связи')

    def __str__(self):
        return f'{self.name}'
