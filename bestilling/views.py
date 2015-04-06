from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.views.generic import TemplateView

from rest_framework import generics
import trello

from bestilling.models import Attachment
from bestilling.serializers import AttachmentSerializer


class IndexView(TemplateView):
    def get(self, request):
        template = get_template('index.html')
        context_data = {}
    
        response = template.render(Context(context_data))
        return HttpResponse(response)
    

class AttachmentView(generics.ListCreateAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

    def post_save(self, obj, created=False):

        if obj.order_object is not None:
            client = trello.TrelloClient(api_key=settings.TRELLO_API_KEY, token=settings.TRELLO_TOKEN)
            attachment = client.fetch_json(
                '/cards/' + obj.order_object.trello_card_id + '/attachments',
                http_method='POST',
                post_args={'url': obj.uploaded_file.url}
            )
            # Persist trello attachment id
            obj.trello_id = attachment['id']
            obj.save()