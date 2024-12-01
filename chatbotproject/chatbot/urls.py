from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('main-categories/', views.get_main_categories, name='get_main_categories'),
    path('main-categories/<int:main_category_id>/sub-categories/', views.get_sub_categories, name='get_sub_categories'),
    path('sub-categories/<int:sub_category_id>/products/', views.get_products, name='get_products'),
    path('sub-categories/<int:sub_category_id>/recommend-products/', views.recommend_products, name='recommend_products'),
    path('aspects/', views.get_aspects, name='get_aspects'),
]