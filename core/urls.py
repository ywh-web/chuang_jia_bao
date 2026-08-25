from django.urls import path
from .views import assistant_chat, contact_inquiry_create, health_check


urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('assistant/chat/', assistant_chat, name='assistant-chat'),
    path('contact-inquiries/', contact_inquiry_create, name='contact-inquiry-create'),
]

