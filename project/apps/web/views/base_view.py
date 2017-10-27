from django.shortcuts import redirect
from django.shortcuts import render

from .. import web_constant

# Global context
def_context = {"CONSTANTS": web_constant}


def home(request):
    return redirect("/admin/")


def handler404(request):
    context = def_context
    context.update({'page_title': '404 Error'})
    return render(request, 'errors/404.html', context)


def handler500(request):
    context = def_context
    context.update({'page_title': '500 Error'})
    return render(request, 'errors/500.html', context)


def error_handler(request, data=None):
    context = def_context
    context.update({'page_title': 'Error'})
    if data:
        context.update(data)
    return render(request, 'errors/custom_error.html', context)