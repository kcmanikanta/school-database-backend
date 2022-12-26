from  django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import DeclareResult
from .serializers import resultAddSerializer, resultListSerializer

# Create your views here.


class addResult(generics.CreateAPIView):
    queryset = DeclareResult.objects.all()
    serializer_class = resultAddSerializer


class ResultList(generics.ListAPIView):
    queryset = DeclareResult.objects.all()
    serializer_class = resultListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['select_student']