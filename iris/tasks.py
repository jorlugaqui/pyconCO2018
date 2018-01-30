import pickle
from celery.decorators import task

from .models import Result


@task
def classify_iris(pk):
    result = Result.objects.get(pk=pk)
    iris_model = pickle.load(open('data/iris_predictor.pkl', 'rb'))
    prediction = iris_model.predict([[result.petal_length, result.petal_width]])
    result.classification = str(prediction)
    result.save()
