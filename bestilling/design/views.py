#-*- encoding: utf-8 -*-

from datetime import datetime

from bestilling.baseviews import BaseFormView, BaseOrderView
from design.models import DesignOrder
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404
from django.template import Context, Template
from django.template.loader import get_template
from django.views.decorators.http import require_GET, require_POST

class DesignFormView(BaseFormView):
    template_name = 'design/form.html'
    trello_board_id = '517870177cd0f3fa3e0036c7'
    params_list = [
        'client',
        'deadline',
        'contact_name',
        'contact_email',
        'contact_number',
        'format',
        'format_other',
        'paper_size',
        'paper_size_other',
        'colour',
        'marger',
        'content',
    ]

    def _get_errors(self, params):
        errors = {
            'client_error' : params['client'] == '',
            'deadline_error' : params['deadline'] == '',
            'contact_name_error' : params['contact_name'] == '',
            'contact_email_error' : params['contact_email'] == '',
            'contact_number_error' : False,
            'format_error' : params['format'] == '',
            'format_other_error' : params['format'] == 'other' and params['format_other'] == '',
            'paper_size_error' : params['paper_size'] == '',
            'paper_size_other_error' : params['paper_size'] == 'other' and params['paper_size_other'] == '',
            'colour_error' : params['colour'] == '',
            'marger_error' : params['marger'] == '',
            'content_error' : False,
        }
    
        return dict((error, True) for error, has_happened in errors.iteritems() if has_happened is True)

    def _save_data(self, params):
        format_type = params['format'] if params['format'] != 'other' else params['format_other']
        paper_size = params['paper_size'] if params['paper_size'] != 'other' else params['paper_size_other']

        description = u"""\
**Fra:** {client}
**Navn:** {contact_name}
**Epost:** {contact_email}
**Tlf:** {contact_number}
**Format:** {format_type}
**Papirstr.:** {paper}
**Farger:** {colour}
**Marger:** {marger}
---
{content}""".format(format_type=format_type, paper=paper_size, **params)
        deadline = datetime.strptime(params['deadline'], '%Y-%m-%d')

        card_id = self._save_to_trello(
            card_name = params['client'], 
            card_description = description, 
            card_due=datetime.strftime(deadline, '%m/%d/%y'),
        )

        order = DesignOrder(
                client = params['client'],
                deadline = deadline.date(),
                contact_name = params['contact_name'],
                contact_email = params['contact_email'],
                contact_number = params['contact_number'],
                format_type = format_type,
                paper_size = paper_size,
                colour = params['colour'],
                marger = params['marger'],
                content = params['content'],
                trello_card_id = str(card_id)
        ) 
        order.save()
        return order

class DesignOrderView(BaseOrderView):
    template_name = "design/order.html"

    def _get_order(self, order_id):
        try:
            order = DesignOrder.objects.get(pk=order_id)
            return order
        except DesignOrder.DoesNotExist:
            raise Http404

    def _get_additional_data(self, order):
        card = self._get_from_trello(order.trello_card_id)
        card.fetch()
        return self._get_data_from_card(card)
        
