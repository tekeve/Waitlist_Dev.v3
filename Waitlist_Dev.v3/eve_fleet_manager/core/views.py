from django.shortcuts import render

def index(request):
    """
    The main landing page. 
    Eventually, this will show the 'Login with EVE' button or the Fleet Dashboard if logged in.
    """
    context = {
        'page_title': 'Home',
    }
    return render(request, 'core/index.html', context)