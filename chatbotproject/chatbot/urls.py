from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('main-categories', views.get_main_categories, name='get_main_categories'),
    path('main-categories/<int:main_category_id>/sub-categories', views.get_sub_categories, name='get_sub_categories'),
]