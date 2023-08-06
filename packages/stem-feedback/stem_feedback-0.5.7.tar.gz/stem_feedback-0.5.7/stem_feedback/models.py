from django.db import models
from django.utils.translation import ugettext_lazy as _
import json


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


class FeedbackFiles(models.Model):
    owner = models.IntegerField(default=1, verbose_name='ID покупателя')
    file = models.FileField(upload_to='feedback_files/')

    class Meta:
        verbose_name = 'Файл покупателя'
        verbose_name_plural = 'Файлы покупателей'
        db_table = 'feedback_files'


class Customers(models.Model):
    user_id = models.IntegerField(default=1, verbose_name='ID пользователя')
    customer_id = models.IntegerField(default=1, verbose_name='ID покупателя')
    customer_erp_id = models.IntegerField(default=1, verbose_name='ERP покупателя')
    customer_name = models.CharField(
        max_length=255,
        default='',
        verbose_name='Наименование покупателя',
        help_text='Наименование покупателя')

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатель'
        db_table = 'customers'

    def __str__(self):
        return f'{self.customer_name}'

# под вопросом,нужно ли вообще


class Feedback(models.Model):
    from_email = models.EmailField(max_length=255, default='', null=True, blank=True, verbose_name=_('Ваш email'))
    type = models.ForeignKey('stem_feedback.FeedBackType', default=None, null=True, blank=True,
                             verbose_name='Тип обратной связи',
                             on_delete=models.PROTECT)
    subject = models.CharField(max_length=255, default='', verbose_name="Тема обращения")
    message = models.CharField(max_length=255, default='', verbose_name="Обращение")

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратные связи'
        db_table = 'feedback'


class Currency(models.Model):
    name = models.CharField(max_length=255, default='', unique=True, verbose_name='Название')
    iso_code = models.CharField(max_length=255, default='', verbose_name='ISO', unique=True)
    abbr = models.CharField(max_length=255, default='', unique=True,
                            verbose_name='Буквенный код валюты')
    simbol = models.CharField(max_length=4, default='', unique=True)

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
        db_table = 'currency'

    def __str__(self):
        return f'{self.simbol}'


class EventCustomers(models.Model):
    user_id = models.IntegerField(default=1, verbose_name='ID пользователя')
    customer_id = models.IntegerField(default=1, verbose_name='ID покупателя')
    customer_erp_id = models.IntegerField(default=1, verbose_name='ERP покупателя')
    customer_name = models.CharField(
        max_length=255,
        default='',
        verbose_name='Наименование покупателя',
        help_text='Наименование покупателя')

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатель'
        db_table = 'event_customers'

    def __str__(self):
        return f'{self.customer_name}'