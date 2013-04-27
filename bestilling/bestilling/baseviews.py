from datetime import datetime, timedelta
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
from django.views.generic import TemplateView
from settings import TRELLO_API_KEY, TRELLO_TOKEN
import trello

class BaseFormView(TemplateView):
    template_name = None
    trello_board_id = None
    params_list = None

    def get(self, request):
        template = get_template(self.template_name)
        context_data = {}
        context_data.update(csrf(request))
    
        response = template.render(Context(context_data))
        return HttpResponse(response)
    
    def post(self, request):
        params = dict((key, request.POST.get(key, '')) for key in self.params_list)
        errors = self._get_errors(params)
    
        # If there were errors in parsing form (missing parameters etc.):
        if errors is not None and len(errors) > 0:
            template = get_template(self.template_name)
            context_data = params.copy()
            context_data['errors'] = errors
            context_data.update(csrf(request))
    
            response = template.render(Context(context_data))
            return HttpResponse(response)

        order = self._save_data(params)
        return HttpResponse('<html><head><title>Suksess!</title></head><body><p>Bestillingen har blitt sendt.<br/>card_id = {}</p></body></html>'.format(order.id))

    def _get_errors(self, params):
        return {}

    def _save_data(self, params):
        raise NotImplementedError

    def _save_to_trello(self, card_name, card_description, card_due, card_colour="green", list_name='Bestillinger'):
        client = trello.TrelloClient(api_key=TRELLO_API_KEY, token=TRELLO_TOKEN)

        board = client.get_board(self.trello_board_id)

        all_lists = board.all_lists()
        order_list = filter(lambda x: x.name == list_name and (x.fetch() or x.closed == False), all_lists)

        if len(order_list) == 0:
            order_list.append(board.add_list(list_name))
            
        order_list = order_list[0]
        card = order_list.add_card(card_name, card_description)

        # Set card deadline
        card._set_remote_attribute('due', card_due)

        # Set colour of the card. We have to do this like this, because there is no shortcut and _set_remote_attribute() uses PUT
        card.client.fetch_json('/cards/'+card.id+'/labels', http_method="POST", post_args = { 'value' : card_colour })
        return card.id


class BaseOrderView(TemplateView):
    template_name = None

    def get(self, request, order_id):
        try:
            template = get_template(self.template_name)
            order = self._get_order(order_id)
            data = self._get_additional_data(order)
        except trello.ResourceUnavailable:
            raise Http404

        context_data = {
            'order' : order,
            'data' : data,
        }
    
        response = template.render(Context(context_data))
        return HttpResponse(response)

    def _get_order(self, order_id):
        raise NotImplementedError

    def _get_additional_data(self, order):
        raise NotImplementedError

    def _get_from_trello(self, card_id):
        client = trello.TrelloClient(api_key=TRELLO_API_KEY, token=TRELLO_TOKEN)

        obj = client.fetch_json('/cards/' + card_id)

        class MockObject(object):
            pass
        tmp_list = MockObject()
        tmp_list.client = client

        card = trello.Card(
            card_id = obj['id'],
            trello_list = tmp_list,
            name = obj['name']
        )
        return card

    def _get_data_from_card(self, card):
        now = datetime.now()
        due =  datetime.strptime(card.badges['due'][:-5], "%Y-%m-%dT%H:%M:%S")
        days_left = due - now if due > now else timedelta(0)

        return {
            "card" : card,
            "created" : card.create_date,
            "due" : due,
            "days_left" : days_left.days,
            "members" : self._list_members_from_card(card),
        }

    def _list_members_from_card(self, card):
        client = trello.TrelloClient(api_key=TRELLO_API_KEY, token=TRELLO_TOKEN)
        
        if not hasattr(card, "member_ids"):
            card.fetch()

        return map(lambda member_id: client.get_member(member_id).fetch(), card.member_ids)
