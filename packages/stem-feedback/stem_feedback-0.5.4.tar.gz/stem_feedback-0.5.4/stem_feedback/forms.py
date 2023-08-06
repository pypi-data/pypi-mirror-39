from django.forms.fields import CharField
from stem_feedback.models import *
from django import forms
from django.utils.translation import ugettext as _


class FeedbackEmailForm(forms.Form):
    from_email = forms.EmailField(required=True, label=_('Ваш email'))
    subject = CharField(max_length=30, required=False, label=_("Тема обращения"))
    feed_back_type = forms.ModelChoiceField(queryset=FeedBackType.objects.all(),
                                            required=False,
                                            label=_('Тип обращения'))
    message = forms.CharField(widget=forms.Textarea, required=True, label=_('Текст'))

    # def __init__(self, request, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

        # if request.user.is_authenticated():
        #     self.fields['from_email'] = forms.EmailField(
        #         required=False,
        #         widget=forms.HiddenInput(),
        #     )