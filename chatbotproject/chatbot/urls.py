from django.urls import path
from . import views

urlpatterns = [
    # path('get/', views.getMainCaterogy, name='main_categories'),

    path('', views.getMainCaterogy, name='index'),
    path('get_sub_categories/<int:main_category_id>/', views.get_sub_categories, name='get_sub_categories'),
]
