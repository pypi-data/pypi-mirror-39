from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.template.loader import get_template
import json


class FeedbackEmailView(View):

    def get(self, request):
        form = FeedbackEmailForm()
        return render(request, "feedback.html", {'form': form})

    def post(self, request):
        form = FeedbackEmailForm(request.POST)
        if form.is_valid():
            feed_back_type = form.cleaned_data['feed_back_type']
            subject = 'Feedback.' + form.cleaned_data['subject']
            message = form.cleaned_data['message']

            if request.user.is_authenticated():
                from_email = request.user.email
                # phone = request.user.phone
                # main_customer = request.user.main_customer
                user = request.user.username
                templ = dict({'user': user,
                              'email': from_email,
                              # 'phone': phone,
                              # 'main_customer': main_customer,
                              'type': feed_back_type,
                              'subject': subject,
                              'text': message,
                              })
            else:
                from_email = form.cleaned_data['from_email']
                templ = dict({
                    'email': from_email,
                    'type': feed_back_type,
                    'subject': subject,
                    'text': message,
                })

            html = get_template('html-message.html')
            html_content = html.render(templ)

            try:
                if feed_back_type:
                    to_email = FeedBackType.objects.get(name=feed_back_type).email
                    send_mail(subject, message, from_email, [to_email], html_message=html_content)

                else:
                    to_email = settings.CONST_EMAIL
                    send_mail(subject, message, from_email, [to_email], html_message=html_content)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'email_complete.html')
        return render(request, "feedback.html", {'form': form})


# def get_json(self, request):
#
#     event_json = {}
#     event_json['type'] = []
#
#     event_json['type'].append({
#         'type': 'event',
#     })

    # event_json = {
    #     'id': 'c15291784c5c9ff1ffee12d66399ad80',  # feedback_id
    #     'type': 'event',
    #     'subject': 'Feedback from Шитов Максим. Пожелания по работе с сайтом -> c15291784c5c9ff1ffee12d66399ad80',
    #     'message': 'Прошу добавть на сайт функционал оплаты банковской картой',
    #     'user': {
    #         'user_id': '23',
    #         'user_name': 'bublik.sergey',
    #         'email': 'user@example.com',
    #         'customer': {
    #             'customer_id': '4',
    #             'customer_erp_id': 'CN-23423423',
    #             'customer_name': 'ООО Автозапчасть',
    #         },
    #     },
    # }





