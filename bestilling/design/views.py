#-*- encoding: utf-8 -*-

from datetime import datetime

from bestilling.baseviews import BaseFormView, BaseOrderView
from design.models import DesignOrder
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404
from django.template import Context, Template
from django.template.loader import get_template

class DesignFormView(BaseFormView):
    template_name = "design/form.html"
    trello_board_id = '5181797902c4ab210d002449'
    params_list = [
        'format',
        'format_other',
        'paper_size',
        'paper_size_other',
        'colour',
        'marger',
        'content',
    ]

    def _get_errors(self, params):
        errors = super(DesignFormView, self)._get_errors(params)
        errors.update({
            'format_error' : params['format'] == '',
            'format_other_error' : params['format'] == 'other' and params['format_other'] == '',
            'paper_size_error' : params['paper_size'] == '',
            'paper_size_other_error' : params['paper_size'] == 'other' and params['paper_size_other'] == '',
            'colour_error' : params['colour'] == '',
            'marger_error' : params['marger'] == '',
            'content_error' : False,
        })
    
        # Filter out all errors that are False:
        return dict((error, True) for error, has_happened in errors.iteritems() if has_happened is True)

    def _get_order_url(self, request, order):
        return request.build_absolute_uri('/design/order/{uuid}/'.format(uuid=order.uuid))

    def _save_data(self, request, params):
        params['format_type'] = params['format'] if params['format'] != 'other' else params['format_other']
        params['paper_size'] = params['paper_size'] if params['paper_size'] != 'other' else params['paper_size_other']

        deadline = datetime.strptime(params['deadline'], '%Y-%m-%d')

        card = self._save_to_trello(
            card_name = params['client'], 
            card_description = "", 
            card_due=datetime.strftime(deadline, '%m/%d/%y'),
        )

        card_id = card.id

        order = DesignOrder(
                client = params['client'],
                deadline = deadline.date(),
                contact_name = params['contact_name'],
                contact_email = params['contact_email'],
                contact_number = params['contact_number'],
                format_type = params['format_type'],
                paper_size = params['paper_size'],
                colour = params['colour'],
                marger = params['marger'],
                content = params['content'],
                trello_card_id = str(card_id)
        ) 
        order.save()

        params['url'] = request.build_absolute_uri('/design/order/{uuid}/'.format(uuid=order.uuid))
        card_template = get_template('trello_card.txt')
        description = card_template.render(Context(params))
        card.set_description(description)

        return order

class DesignOrderView(BaseOrderView):
    template_name = "design/order.html"

    def _get_order(self, order_id):
        return DesignOrder.objects.get(uuid=order_id)
