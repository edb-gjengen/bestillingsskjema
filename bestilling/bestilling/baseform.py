from django.core.context_processors import csrf
from django.http import HttpResponse, Http404
from django.template import Context, Template
from django.template.loader import get_template
from django.views.generic import TemplateView

class BaseFormView(TemplateView):
    template_name = None
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

        return HttpResponse('<html><head><title>Suksess!</title></head><body><p>Bestillingen har blitt sendt.</p></body></html>')

    def _get_errors(self, params):
        return {}
