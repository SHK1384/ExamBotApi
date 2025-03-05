from profile import Profile
from tkinter.font import names

from django.urls import path
from api.views import ProfileView, result_view, exam_id

get_exam_box_list = ProfileView.as_view({
    'get': 'get_exam_box_list'
})

add_exam_result = ProfileView.as_view({
    'post': 'add_exam_result'
})

get_user_by_id = ProfileView.as_view({
    'get': 'get_user_by_id'
})

get_prev_exam_result = ProfileView.as_view({
    'get': 'get_prev_exam_result'
})

get_user_state = ProfileView.as_view({
    'get': 'get_user_state'
})

set_user_state = ProfileView.as_view({
    'post': 'set_user_state'
})
register_new_user = ProfileView.as_view({
    'post': 'register_new_user'
})
update_new_user = ProfileView.as_view({
    'post': 'update_new_user'
})
get_all_users = ProfileView.as_view({
    'get': 'get_all_users'
})
set_user_answers_state = ProfileView.as_view({
    'post': 'set_user_answer_state'
})
set_user_current_message_id = ProfileView.as_view({
    'post': 'set_current_message_id'
})
set_user_current_question = ProfileView.as_view({
    'post': 'set_user_current_question'
})
set_current_exam_message_id = ProfileView.as_view({
    'post': 'set_current_exam_message_id'
})
urlpatterns = [
    path('get-exam-box-list/<int:user_id>', get_exam_box_list, name='get_exam_box_list'),
    path('add-exam-result/', add_exam_result, name='add_exam_result'),
    path('get-user-by-id/<int:user_id>', get_user_by_id, name='get_user_by_id'),
    path('get-prev-exam-result/<int:user_id>/<int:exam_id>', get_prev_exam_result, name='get_prev_exam_result'),
    path('get-user-state/<int:user_id>', get_user_state, name='get_user_state'),
    path('set-user-state/', set_user_state, name='set_user_state'),
    path('get-exam-result/<int:department_id>/<int:exam_id>', result_view, name='get_exam_result'),
    path('get-exam-id/', exam_id, name='get_exam_id'),
    path('register-new-user/', register_new_user, name='register_new_user'),
    path('update-new-user/', update_new_user, name='update_new_user'),
    path('get-all-users/', get_all_users, name='get_all_users'),
    path('set-user-answers-state/', set_user_answers_state, name='set_user_answers_state'),
    path('set-current-message-id/', set_user_current_message_id, name='set_user_current_message_id'),
    path('set-current-question/', set_user_current_question, name='set_current_question'),
    path('set-current-exam-message-id/', set_current_exam_message_id, name='set_current_exam_message_id'),
]