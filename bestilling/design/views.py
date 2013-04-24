from django.core.context_processors import csrf
from django.http import HttpResponse, Http404
from django.template import Context, Template
from django.template.loader import get_template
from django.views.decorators.http import require_GET, require_POST
from bestilling.baseform import BaseFormView

class DesignForm(BaseFormView):
    template_name = 'design/form.html'
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

