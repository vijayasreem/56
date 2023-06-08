from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('update_index/', update_index, name='update_index'),
]