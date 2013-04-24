from django.core.context_processors import csrf
from django.http import HttpResponse, Http404
from django.template import Context, Template
from django.template.loader import get_template
from django.views.decorators.http import require_GET, require_POST

@require_GET
def form(request):
    template = get_template('design/form.html')
    context_data = {}
    context_data.update(csrf(request))

    response = template.render(Context(context_data))
    return HttpResponse(response)

@require_POST
def submit(request):
    params = {
        'client' : request.POST.get('client', ''),
        'deadline' : request.POST.get('deadline', ''),
        'contact_name' : request.POST.get('contact_name', ''),
        'contact_email' : request.POST.get('contact_email', ''),
        'contact_number' : request.POST.get('contact_number', ''),
        'format' : request.POST.get('format', ''),
        'format_other' : request.POST.get('format_other', ''),
        'paper_size' : request.POST.get('paper_size', ''),
        'paper_size_other' : request.POST.get('paper_size_other', ''),
        'colour' : request.POST.get('colour', ''),
        'marger' : request.POST.get('marger', ''),
        'content' : request.POST.get('content', ''),
    }

    errors = {
        'client_error' : params['client'] == '',
        'deadline_error' : params['deadline'] == '',
        'contact_name_error' : params['contact_name'] == '',
        'contact_email_error' : params['contact_email'] == '',
        'contact_number_error' : params['contact_number'] == '',
        'format_error' : params['format'] == '',
        'format_other_error' : params['format'] == 'other' and params['format_other'] == '',
        'paper_size_error' : params['paper_size'] == '',
        'paper_size_other_error' : params['paper_size'] == 'other' and params['paper_size_other'] == '',
        'colour_error' : params['colour'] == '',
        'marger_error' : params['marger'] == '',
        'content_error' : params['content'] == '',
    }

    # For debugging purposes:
    #all_errors = map(lambda x: x[0],filter(lambda item: item[1], errors.items()))

    template = get_template('design/form.html')
    context_data = params.copy()
    context_data['errors'] = errors
    context_data.update(csrf(request))

    response = template.render(Context(context_data))
    return HttpResponse(response)
