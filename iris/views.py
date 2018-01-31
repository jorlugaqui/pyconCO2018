from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .serializers import ResultSerializer
from .tasks import classify_iris
from .models import Result


class IrisPredictorView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            classify_iris.delay(result.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IrisView(generics.RetrieveAPIView):

    serializer_class = ResultSerializer
    queryset = Result.objects.all()
