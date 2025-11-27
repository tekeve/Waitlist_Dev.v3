from django.contrib.auth import login, logout  # Make sure logout is imported here
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from esi.models import Token

def login_callback(request):
    """
    Manually handle the EVE SSO callback to force a Django login.
    """
    code = request.GET.get('code')
    
    if not code:
        messages.error(request, "Login failed: No authorization code received from EVE.")
        return redirect('index')

    try:
        # Use django-esi's built-in manager to exchange the code for a valid Token
        token = Token.objects.create_from_request(request)
    except Exception as e:
        messages.error(request, f"Login failed during token exchange: {str(e)}")
        return redirect('index')

    # Get character details from the token
    character_name = token.character_name
    character_id = token.character_id

    # Find or Create a User for this character
    try:
        # FIX: Use character_id (as string) for the immutable username
        user = User.objects.get(username=str(character_id))
        
        # Update the display name (first_name) in case the user renamed their character
        if user.first_name != character_name:
            user.first_name = character_name
            user.save()
            
    except User.DoesNotExist:
        # Check if this is the first user in the system
        is_first_user = not User.objects.exists()

        # Create new user
        user = User.objects.create_user(
            username=str(character_id),   # FIX: Use ID for username
            first_name=character_name,    # FIX: Use Character Name for display name
            email=f"{character_name.replace(' ', '_')}@eve-example.com"
        )
        user.set_unusable_password() 
        
        # Grant superuser status if this is the first user
        if is_first_user:
            user.is_superuser = True
            user.is_staff = True
            
        user.save()

    # Assign the token to this user so they 'own' this character
    token.user = user
    token.save()

    # Force login the user into Django
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    
    messages.success(request, f"Welcome back, {character_name}!")
    return redirect('index')

def logout_user(request):
    """
    Logs the user out and redirects to the homepage.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')