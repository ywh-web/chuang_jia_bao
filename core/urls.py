from django.urls import path
from .views import assistant_chat, comment_like_api, comments_api, contact_inquiry_create, health_check, ugc_api, ugc_like_api


urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('assistant/chat/', assistant_chat, name='assistant-chat'),
    path('contact-inquiries/', contact_inquiry_create, name='contact-inquiry-create'),
    path('comments/', comments_api, name='comments-api'),
    path('comments/<int:pk>/like/', comment_like_api, name='comment-like-api'),
    path('ugc/', ugc_api, name='ugc-api'),
    path('ugc/<int:pk>/like/', ugc_like_api, name='ugc-like-api'),
]


