from django.urls import path

from .views import IrisPredictor, Iris


urlpatterns = [
    path('', IrisPredictor.as_view(), name='iris-predictor'),
    path('<int:pk>/', Iris.as_view(), name='iris')
]
