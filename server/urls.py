from django.urls import path
from server import views

urlpatterns = [
    path('api/', views.test_REST),
    # path('snippets/<int:pk>/', views.snippet_detail),
]