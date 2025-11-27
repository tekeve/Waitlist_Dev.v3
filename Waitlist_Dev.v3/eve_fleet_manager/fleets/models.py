from django.db import models
from django.contrib.auth.models import User

class Fleet(models.Model):
    """
    Represents a fleet session (e.g., 'Saturday Night Roam').
    """
    name = models.CharField(max_length=100)
    fc = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='commanded_fleets')
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)
    
    # Simple doctrine link (we will expand this later)
    doctrine_type = models.CharField(max_length=50, blank=True, help_text="e.g. 'Nano Gang' or 'Heavy Armor'")

    def __str__(self):
        return f"{self.name} (FC: {self.fc})"

class WaitlistEntry(models.Model):
    """
    A pilot submitting a fit to a specific fleet.
    """
    ROLE_X_UP = 'xup'
    ROLE_DPS = 'dps'
    ROLE_LOGI = 'logi'
    ROLE_SNIPER = 'sniper'
    
    ROLE_CHOICES = [
        (ROLE_X_UP, 'X Up'),
        (ROLE_DPS, 'DPS'),
        (ROLE_LOGI, 'Logistics'),
        (ROLE_SNIPER, 'Sniper'),
    ]

    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE, related_name='entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # In the future, we will parse this into JSON, but for now, store raw EFT text
    fit_text = models.TextField()
    
    # We will derive this from the fit_text later using SDE
    ship_name = models.CharField(max_length=100, default="Unknown Ship") 
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_X_UP)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.first_name} - {self.ship_name}"