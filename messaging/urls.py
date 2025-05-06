from django.urls import path

from .views import get_all_messages, set_message_sent_bool

urlpatterns = [
    path('get-all-messages/', get_all_messages, name='get_all_messages'),
    path('set-message-sent-bool/', set_message_sent_bool,
         name='set_message_sent_bool'),
]
