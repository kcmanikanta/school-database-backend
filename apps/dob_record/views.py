from rest_framework import generics
from .models import PDFRecord
from .serializers import PDFRecordSerializer
import io
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from .models import PDFRecord
from .serializers import PDFRecordSerializer
from pdf2image import convert_from_bytes
from PIL import Image
import cloudinary.uploader
from django.db.models import Q



class PDFRecordCreateView(generics.CreateAPIView):
    queryset = PDFRecord.objects.all()
    serializer_class = PDFRecordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        pdf_record = serializer.instance

        pdf_file = request.FILES.get('pdf_file')
        if pdf_file:
            try:
                images = convert_from_bytes(pdf_file.read())
                image_urls = []
                for image in images:
                    buffer = io.BytesIO()
                    image.save(buffer, format="PNG")
                    buffer.seek(0)
                    response = cloudinary.uploader.upload(buffer, folder="pdf_images")
                    image_urls.append(response['url'])

                pdf_record.image_url = image_urls[0]  # Save the first image's URL
                pdf_record.save()

                return Response(PDFRecordSerializer(pdf_record).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "PDF file not provided"}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import generics
from .models import PDFRecord
from .serializers import PDFRecordSerializer
from django.db.models import Q

class PDFRecordListView(generics.ListAPIView):
    queryset = PDFRecord.objects.all()
    serializer_class = PDFRecordSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)

        if search_query:
            queryset = queryset.filter(
                Q(student__student_roll__icontains=search_query) |
                Q(student__firstname__icontains=search_query) |
                Q(student__lastname__icontains=search_query)
            )
        return queryset

    

class PDFRecordDetailView(generics.RetrieveAPIView):
    queryset = PDFRecord.objects.all()
    serializer_class = PDFRecordSerializer
    lookup_field = 'id'



