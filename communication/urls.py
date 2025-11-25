from django.urls import path
from . import views

urlpatterns = [
    path('send_interest/<int:user_id>/', views.send_interest, name='send_interest'),
    path('matches/', views.matches_list, name='matches_list'),
    path('chat/<int:user_id>/', views.chat_view, name='chat_view'),
]
