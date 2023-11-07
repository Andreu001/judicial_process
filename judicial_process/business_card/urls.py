# ice_cream/urls.py
from django.urls import path
from . import views


app_name = 'business_card'

urlpatterns = [
    # Главная страница
    path(
        'business_card/<slug:slug>/', views.business_card, name='business_card'
        ),
    path('', views.index, name='index'),
    path('profile/<str:username>/', views.profile, name='profile'),
    # Страница с карточкой дела
    path('create/', views.card_create, name='card_create'),
    path(
        'business_card/<int:card_id>/business_card_detail',
        views.business_card_detail,
        name='business_card_detail'
        ),
    path(
        'business_card/<int:post_id>/edit/', views.card_edit, name='card_edit'
        ),
    path(
        'business_card/<int:card_id>/add_side', views.add_side, name='add_side'
        ),
    path(
        'edit_side/<int:side_case_id>/edit_side',
        views.edit_side,
        name='edit_side'
        ),
    path(
        'delete_side/<int:side_case_id>/',
        views.delete_side,
        name='delete_side'
        ),
    path(
        'business_card/<int:decision_case_id>/add_movement',
        views.add_movement,
        name='add_movement'
        ),
    path(
        'edit_movement/<int:decision_case_id>/edit_movement',
        views.edit_movement,
        name='edit_movement'
        ),
    path(
        'delete_movement/<int:decision_case_id>/',
        views.delete_movement,
        name='delete_movement'
        ),
    path(
        'business_card/<int:card_id>/add_petition',
        views.add_petition,
        name='add_petition'
        ),
    path(
        'edit_petition/<int:petition_case_id>/edit_petition',
        views.edit_petition,
        name='edit_petition'
        ),
    path(
        'delete_petition/<int:petition_case_id>/',
        views.delete_petition,
        name='delete_petition'
        ),
]
