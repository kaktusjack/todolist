from django.urls import path
from .views import tasklist,detaialView,TaskCreate,TaskUpdate,TaskDelete,Login,Register
from django.contrib.auth.views import LogoutView
urlpatterns=[
    path('login/',Login.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',Register.as_view(),name='register'),
    path('',tasklist.as_view(),name='tasks'),
    path('task/<int:pk>/',detaialView.as_view(),name='details'),
    path('create-task/',TaskCreate.as_view(),name='task-create'),
    path('update-task/<int:pk>/',TaskUpdate.as_view(),name='task-update'),
    path('delete-task/<int:pk>/',TaskDelete.as_view(),name='task-delete'),
    
]