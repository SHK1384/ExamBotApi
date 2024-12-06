from django.urls import path
from api.views import ProfileView

get_exam_box_list = ProfileView.as_view({
    'get': 'get_exam_box_list'
})

add_exam_result = ProfileView.as_view({
    'post': 'add_exam_result'
})
urlpatterns = [
    path('get-exam-box-list/<int:user_id>', get_exam_box_list, name='get_exam_box_list'),
    path('add-exam-result', add_exam_result, name='add_exam_result'),
]