from django.http import request

def global_settings(request):
    return {
        "APP_NAME" : "HCH System",
    }