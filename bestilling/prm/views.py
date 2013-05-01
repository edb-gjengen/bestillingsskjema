#-*- encoding: utf-8 -*-

from datetime import datetime

from bestilling.baseviews import BaseFormView, BaseOrderView
from prm.models import PrmOrder
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template

class PrmFormView(BaseFormView):
    template_name = 'prm/form.html'
    trello_board_id = '5181797902c4ab210d002449'
    params_list = [
        'client',
        'deadline',
        'contact_name',
        'contact_email',
        'contact_number',
        'assignment_type',
        'assignment_type_other',
        'content',
    ]

    def _get_errors(self, params):
        errors = super(PrmFormView, self)._get_errors(params)
        errors.update({
            'assignment_type_error' : params['assignment_type'] == '',
            'assignment_type_other_error' : params['assignment_type'] == 'other' and params['assignment_type_other'] == '',
            'content_error' : params['content'] == '',
        })
    
        # Filter out all errors that are False:
        return dict((error, True) for error, has_happened in errors.iteritems() if has_happened is True)

    def _get_order_url(self, request, order):
        return request.build_absolute_uri('/prm/order/{uuid}/'.format(uuid=order.uuid))

    def _save_data(self, request, params):
        params.update({
            'assignment_type' : params['assignment_type'] if params['assignment_type'] != 'other' else params['assignment_type_other'],
        })

        deadline = datetime.strptime(params['deadline'], '%Y-%m-%d')

        card = self._save_to_trello(
            card_name = params['client'], 
            card_description = "", 
            card_due=datetime.strftime(deadline, '%m/%d/%y'),
        )

        card_id = card.id

        order = PrmOrder(
                client = params['client'],
                deadline = deadline.date(),
                contact_name = params['contact_name'],
                contact_email = params['contact_email'],
                contact_number = params['contact_number'],
                assignment_type = params['assignment_type'],
                content = params['content'],
                trello_card_id = str(card_id)
        ) 
        order.save()
        
        params['url'] = request.build_absolute_uri('/prm/order/{uuid}/'.format(uuid=order.uuid))
        card_template = get_template('trello_card.txt')
        description = card_template.render(Context(params))
        card.set_description(description)

        return order

class PrmOrderView(BaseOrderView):
    template_name = "prm/order.html"

    def _get_order(self, order_id):
        return PrmOrder.objects.get(uuid=order_id)
