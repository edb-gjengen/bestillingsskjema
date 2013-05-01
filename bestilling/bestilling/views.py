from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.views.generic import TemplateView

class IndexView(TemplateView):
    def get(self, request):
        template = get_template('index.html')
        context_data = {}
    
        response = template.render(Context(context_data))
        return HttpResponse(response)
    

