import logging
from celery.decorators import task

from .models import Result, IrisModel, IrisModelConfig

logger = logging.getLogger(__name__)


@task
def classify_iris(pk):
    """Call the model and predict classification"""
    result = None

    try:
        result = Result.objects.get(pk=pk)
    except Result.DoesNotExist:
        logger.exception('No result record found in the DB')
        return

    iris_model = IrisModel.get_instance()

    if iris_model is None:
        raise Exception('Predictions are not available')

    prediction = iris_model.predict([[result.petal_length, result.petal_width]])
    result.classification = IrisModelConfig.CLASSIFICATION.get(prediction[0])
    result.save()
