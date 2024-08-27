from rest_framework import viewsets
from .models import TeacherProfile, Blog
from .serializers import TeacherProfileSerializer, BlogSerializer
from rest_framework import filters

class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned blogs to published only
        by filtering against a `published` query parameter.
        """
        queryset = Blog.objects.all()
        published = self.request.query_params.get('published', None)
        if published is not None:
            published = published.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(published=published)
        return queryset
