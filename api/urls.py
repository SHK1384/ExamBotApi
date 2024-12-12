from django.urls import path
from api.views import ProfileView

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
urlpatterns = [
    path('get-exam-box-list/<int:user_id>', get_exam_box_list, name='get_exam_box_list'),
    path('add-exam-result/', add_exam_result, name='add_exam_result'),
    path('get-user-by-id/<int:user_id>', get_user_by_id, name='get_user_by_id'),
    path('get-prev-exam-result/<int:user_id>/<int:exam_id>', get_prev_exam_result, name='get_prev_exam_result'),
    path('get-user-state/<int:user_id>', get_user_state, name='get_user_state'),
    path('set-user-state/', set_user_state, name='set_user_state'),
]