# -*- encoding: utf-8 -*-

from datetime import datetime
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

from bestilling.baseviews import BaseFormView, BaseOrderView
from tekst.models import TekstOrder


class TekstFormView(BaseFormView):
    form_template_name = 'tekst/form.html'
    trello_board_id = settings.TRELLO_TEKST_BOARD_ID
    mail_from = settings.MAIL_KAK_TEKST
    params_list = [
        'client',
        'deadline',
        'contact_name',
        'contact_email',
        'contact_number',
        'text_type',
        'text_type_other',
        'length',
        'image',
        'interview_name',
        'interview_contact',
        'content',
    ]

    def _get_errors(self, params):
        errors = super(TekstFormView, self)._get_errors(params)
        errors.update({
            'text_type_error': params['text_type'] == '' or len(params['text_type']) > 50,
            'text_type_other_error': params['text_type'] == 'other' and (params['text_type_other'] == '' or len(params['text_type_other']) > 50),
            'length_error': params['length'] == '' or len(params['length']) > 50,
            'image_error': params['image'] == '' or len(params['image']) > 50,
            'interview_name_error': len(params['interview_name']) > 20,
            'content_error': False,
        })
    
        # Filter out all errors that are False:
        return dict((error, True) for error, has_happened in errors.items() if has_happened is True)

    def _get_order_url(self, request, order):
        return request.build_absolute_uri('/tekst/order/{uuid}/'.format(uuid=order.uuid))

    def _save_data(self, request, params):
        params.update({
            'text_type': params['text_type'] if params['text_type'] != 'other' else params['text_type_other'],
        })

        deadline = datetime.strptime(params['deadline'], '%Y-%m-%d')

        card = self._save_to_trello(
            card_name=params['client'], 
            card_description="", 
            card_due=datetime.strftime(deadline, '%m/%d/%y'),
        )

        card_id = card.id

        order = TekstOrder(
            client=params['client'],
            deadline=deadline.date(),
            contact_name=params['contact_name'],
            contact_email=params['contact_email'],
            contact_number=params['contact_number'],
            text_type=params['text_type'],
            length=params['length'],
            image=params['image'],
            interview_name=params['interview_name'],
            interview_contact=params['interview_contact'],
            content=params['content'],
            trello_card_id=str(card_id)
        ) 
        order.save()
        
        params['url'] = request.build_absolute_uri('/tekst/order/{uuid}/'.format(uuid=order.uuid))
        card_template = get_template('trello_card.txt')
        description = card_template.render(Context(params))
        card.set_description(description)

        return order


class TekstOrderView(BaseOrderView):
    template_name = "tekst/order.html"

    def _get_order(self, order_id):
        return TekstOrder.objects.get(uuid=order_id)
