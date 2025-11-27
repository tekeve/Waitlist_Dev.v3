from django.shortcuts import render, redirect

def index(request):
    """
    The main landing page. 
    If logged in, redirect to Fleet Dashboard.
    """
    if request.user.is_authenticated:
        return redirect('fleets:dashboard')

    context = {
        'page_title': 'Home',
    }
    return render(request, 'core/index.html', context)