import os
import django
from django.urls import get_resolver, URLResolver, URLPattern

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

def print_urls(patterns, prefix=''):
    """Recursively print URL patterns."""
    for pattern in patterns:
        if isinstance(pattern, URLPattern):
            # Found a URL!
            name = pattern.name
            url = prefix + str(pattern.pattern)
            if 'sso' in url or (name and 'login' in name):
                print(f"  Path: {url:<40} | Name: {name}")
                
        elif isinstance(pattern, URLResolver):
            # Found a grouping (like include(...))
            new_prefix = prefix + str(pattern.pattern)
            namespace = pattern.namespace
            if namespace:
                print(f"\n[Namespace '{namespace}']: {new_prefix}")
            print_urls(pattern.url_patterns, new_prefix)

print("="*80)
print("SCANNING FOR LOGIN URLS")
print("="*80)
resolver = get_resolver()
print_urls(resolver.url_patterns)
print("="*80)