from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    #post view
    path('<int:page_idx>', views.post_list, name='post_list'),
    path('tag/<str:tag_slug>/<int:page_idx>', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<str:post>',
            views.post_detail,
            name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),

]