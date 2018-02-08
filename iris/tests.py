import json
from unittest import mock

from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Result, IrisModelConfig, IrisModel
from .tasks import classify_iris


def get_token_for_testing():
    user = User.objects.create(
        username='test', email='test@gmail.com', password='password', is_active=True
    )
    return Token.objects.create(user=user).key


class ResultTestCase(TestCase):

    def setUp(self):
        Result.objects.create(petal_width=2.0, petal_length=0.98)

    def test_prediction_is_recorded(self):
        result = Result.objects.all().first()
        self.assertEqual(float(result.petal_width), 2.0)
        self.assertEqual(float(result.petal_length), 0.98)
        self.assertIsNone(result.classification)


class IrisModelConfigTestCase(TestCase):

    def test_iris_model_configuration(self):
        self.assertDictEqual(
            IrisModelConfig.CLASSIFICATION,
            {
                0: 'SETOSA',
                1: 'VERSICOLOR',
                2: 'VIRGINICA'
            }
        )

        self.assertEqual(IrisModelConfig.MODEL_PKL, 'iris_predictor.pkl')


class IrisModelTestCase(TestCase):

    def test_load_model(self):
        # TODO: If model gets bigger probably we should mock open (built in) call
        self.assertTrue(IrisModel.get_instance() is not None)
        self.assertTrue(IrisModel._instance is not None)

        with self.assertRaises(ValueError):
            IrisModel()  # Model was already loaded, might be problematic when the model gets updated


@mock.patch('iris.views.classify_iris.delay', return_value=None)
class IrisPredictorViewTestCase(TestCase):

    def setUp(self):
        self.token = get_token_for_testing()

    def test_request_a_prediction(self, mocked_celery_task):
        data = {
            'petal_length': 2.1,
            'petal_width': 3.1
        }

        response = self.client.post(
            reverse_lazy('iris-predictor'),
            json.dumps(data),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token)
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('petal_length'), '2.10')
        self.assertEqual(response.data.get('petal_width'), '3.10')
        self.assertIsNone(response.data.get('classification'))

    def test_request_a_prediction_without_petal_width(self, mocked_celery_task):
        data = {
            'petal_length': 2.1,
        }

        response = self.client.post(
            reverse_lazy('iris-predictor'),
            json.dumps(data),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token)
        )

        self.assertEqual(response.status_code, 400)


class IrisViewTestCase(TestCase):

    def setUp(self):
        self.prediction = Result.objects.create(petal_width=2.0, petal_length=2.0, classification='SETOSA')
        self.token = get_token_for_testing()

    def test_get_prediction(self):
        response = self.client.get(
            reverse_lazy('iris', kwargs={'pk': self.prediction.pk}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token {}'.format(self.token)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('petal_length'), '2.00')
        self.assertEqual(response.data.get('petal_width'), '2.00')
        self.assertEqual(response.data.get('classification'), 'SETOSA')


class IrisModelTaskTestCase(TestCase):

    def setUp(self):
        self.prediction = Result.objects.create(petal_width=2.0, petal_length=2.0)

    def test_predict_iris(self):
        # TODO: We probably should mock predict method (performance)
        classify_iris(self.prediction.pk)
        self.prediction.refresh_from_db()
        self.assertEqual(self.prediction.classification, 'VIRGINICA')
