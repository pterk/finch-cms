from django.conf import settings

TEMPLATE_CHOICES = [("content.html", "default")]
TEMPLATE_CHOICES = getattr(settings, 'FINCH_TEMPLATE_CHOICES', TEMPLATE_CHOICES)
