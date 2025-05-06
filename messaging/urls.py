from django.urls import path

from .views import MessagingView

get_all_messages = MessagingView.as_view({
    'get': 'get_all_messages'
})

set_message_sent_bool = MessagingView.as_view({
    'post': 'set_message_sent_bool'
})

urlpatterns = [
    path('get-all-messages/', get_all_messages, name='get_all_messages'),
    path('set-message-sent-bool/', set_message_sent_bool,
         name='set_message_sent_bool'),
]
