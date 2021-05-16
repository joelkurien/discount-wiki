from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createpage/", views.createpage, name='createpage'),
    path("random/",views.randompage, name='random'),
    path("edit/", views.editpage, name='edit'),
    path('postedit/', views.postedit, name='postedit'),
    path("<str:title>/", views.find, name='find')
]
