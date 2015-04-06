from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType
from django.core.context_processors import csrf
from django.core import mail
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
from django.views.generic import TemplateView
from django.conf import settings
import trello

from bestilling import utils

from bestilling.models import Attachment

class BaseFormView(TemplateView):
    mail_template_name = "confirmation_mail.txt"
    mail_from = 'no-reply@studentersamfundet.no'
    form_template_name = None
    trello_board_id = None
    params_list = None

    def get(self, request):
        template = get_template(self.form_template_name)
        context_data = self._get_params()
        context_data.update(csrf(request))
    
        response = template.render(Context(context_data))
        return HttpResponse(response)
    
    def post(self, request):
        params = dict((key, request.POST.get(key, '')) for key in self.params_list)
        errors = self._get_errors(params)
    
        # If there were errors in parsing form (missing parameters etc.):
        if errors is not None and len(errors) > 0:
            template = get_template(self.form_template_name)
            context_data = params.copy()
            context_data.update(self._get_params())
            context_data['errors'] = errors
            context_data.update(csrf(request))
    
            response = template.render(Context(context_data))
            return HttpResponse(response)

        order = self._save_data(request, params)
        self._send_confirmation_mail(request, order)

        template = get_template('form_success.html')
        context_data = {
            'url': self._get_order_url(request, order),
        }
        response = template.render(Context(context_data))
        return HttpResponse(response)

    def _get_params(self):
        return {}

    def _get_errors(self, params):
        return {
            'client_error': params['client'] == '' or len(params['client']) > 50,
            'deadline_error': params['deadline'] == '',
            'contact_name_error': params['contact_name'] == '' or len(params['contact_name']) > 50,
            'contact_email_error': not utils.is_email_valid(params['contact_email']),
            'contact_number_error': not utils.is_phone_valid(params['contact_number']),
        }

    def _get_order_url(self, request, order):
        raise NotImplementedError

    def _save_data(self, request, params):
        raise NotImplementedError

    def _save_to_trello(self, card_name, card_description, card_due, card_colour="green", list_name='Bestillinger'):
        client = trello.TrelloClient(api_key=settings.TRELLO_API_KEY, token=settings.TRELLO_TOKEN)

        board = client.get_board(self.trello_board_id)

        all_lists = board.all_lists()
        order_list = filter(lambda x: x.name == list_name and (x.fetch() or x.closed == False), all_lists)

        if len(order_list) == 0:
            order_list.append(board.add_list(list_name))
            
        order_list = order_list[0]
        card = order_list.add_card(card_name, card_description)

        # Set card deadline
        card._set_remote_attribute('due', card_due)

        # Set colour of the card.
        # Note: We have to do it like this, because there is no shortcut and _set_remote_attribute() uses PUT
        card.client.fetch_json('/cards/'+card.id+'/labels', http_method="POST", post_args={'value': card_colour})
        return card

    def _send_confirmation_mail(self, request, order):
        template = get_template(self.mail_template_name)
        context_data = {
            'order': order,
            'url': self._get_order_url(request, order),
        }

        mail_from = self.mail_from
        mail_to = order.contact_email
        mail_subject = "{id}: Bestillingen din er mottatt.".format(id=order.client)
        mail_content = template.render(Context(context_data))

        mail.send_mail(mail_subject, mail_content, mail_from, [mail_to], fail_silently=True)


class BaseOrderView(TemplateView):
    template_name = None

    def get(self, request, order_id):
        try:
            template = get_template(self.template_name)
            order = self._get_order(order_id)
            data = self._get_additional_data(order)
            content_type = ContentType.objects.get_for_model(order)
            attachments = self._get_attachments(order, content_type)
        except (trello.ResourceUnavailable, ObjectDoesNotExist):
            raise Http404

        context_data = {
            'order': order,
            'data': data,
            'content_type_id': content_type.pk,
            'attachments': attachments
        }
        context_data.update(csrf(request))

        response = template.render(Context(context_data))
        return HttpResponse(response)

    def _get_order(self, order_id):
        raise NotImplementedError

    def _get_additional_data(self, order):
        card = self._get_from_trello(order.trello_card_id)
        card.fetch()
        return self._get_data_from_card(card)

    def _get_attachments(self, order, content_type):
        return Attachment.objects.filter(
            content_type=content_type.pk,
            object_id=order.pk)

    def _get_from_trello(self, card_id):
        client = trello.TrelloClient(api_key=settings.TRELLO_API_KEY, token=settings.TRELLO_TOKEN)

        obj = client.fetch_json('/cards/' + card_id)

        class MockObject(object):
            pass
        tmp_list = MockObject()
        tmp_list.client = client

        card = trello.Card.from_json(tmp_list, obj)
        return card

    def _get_data_from_card(self, card):
        due = None
        days_left = None
        if card.badges['due'] is not None:
            now = datetime.now()
            due = datetime.strptime(card.badges['due'][:-5], "%Y-%m-%dT%H:%M:%S")
            days_left = (due - now).days if due > now else timedelta(0).days

        return {
            "card": card,
            "created": card.create_date,
            "due": due,
            "days_left": days_left,
            "members": self._list_members_from_card(card),
        }

    def _list_members_from_card(self, card):
        client = trello.TrelloClient(api_key=settings.TRELLO_API_KEY, token=settings.TRELLO_TOKEN)
        
        if not hasattr(card, "member_ids"):
            card.fetch()

        return map(lambda member_id: client.get_member(member_id).fetch(), card.member_ids)
