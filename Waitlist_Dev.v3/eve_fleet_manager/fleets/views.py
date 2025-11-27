from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Fleet, WaitlistEntry

@login_required
def dashboard(request):
    # Get the active fleet (if multiple are open, get the most recent one)
    active_fleet = Fleet.objects.filter(is_open=True).order_by('-start_time').first()

    if not active_fleet:
        return render(request, 'fleets/no_fleet.html')

    # Get all entries for this fleet
    entries = active_fleet.entries.all()

    # Bucket them into columns
    # 'X Up' contains anything not yet accepted
    x_up = entries.filter(is_accepted=False)
    
    # Accepted roles
    dps = entries.filter(is_accepted=True, role=WaitlistEntry.ROLE_DPS)
    logi = entries.filter(is_accepted=True, role=WaitlistEntry.ROLE_LOGI)
    sniper = entries.filter(is_accepted=True, role=WaitlistEntry.ROLE_SNIPER)

    # Check if current user is FC (or admin)
    is_fc = (request.user == active_fleet.fc) or request.user.is_superuser

    context = {
        'fleet': active_fleet,
        'x_up': x_up,
        'dps': dps,
        'logi': logi,
        'sniper': sniper,
        'is_fc': is_fc,
    }
    return render(request, 'fleets/dashboard.html', context)