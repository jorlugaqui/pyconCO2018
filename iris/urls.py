from django.urls import path

from .views import IrisPredictorView, IrisView


urlpatterns = [
    path('', IrisPredictorView.as_view(), name='iris-predictor'),
    path('<int:pk>/', IrisView.as_view(), name='iris')
]
