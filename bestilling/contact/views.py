#-*- encoding: utf-8 -*-

from datetime import datetime

from bestilling.baseviews import BaseFormView
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404
from django.template import Context, Template
from django.template.loader import get_template

class ContactFormView(BaseFormView):
    template_name = "contact/form.html"

    def _get_errors(self, params):
        errors = {
            'client_error' : params['client'] == '',
            'deadline_error' : params['deadline'] == '',
            'contact_name_error' : params['contact_name'] == '',
            'contact_email_error' : not utils.is_email_valid(params['contact_email']),
            'contact_number_error' : not utils.is_phone_valid(params['contact_number']),
        }
 
        # Filter out all errors that are False:
        return dict((error, True) for error, has_happened in errors.iteritems() if has_happened is True)

