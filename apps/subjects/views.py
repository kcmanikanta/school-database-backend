from rest_framework import generics
from .models import SubjectCombination
from .serializers import SubjectCombinationSerializer

class SubjectByClassView(generics.ListAPIView):
    serializer_class = SubjectCombinationSerializer

    def get_queryset(self):
        class_name = self.request.query_params.get('class_name')
        if class_name:
            queryset = SubjectCombination.objects.filter(select_class__class_name=class_name)
            return queryset
        return SubjectCombination.objects.none()
