from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Min, Max, Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from io import StringIO
import csv

from .models import BloodTestRecord
from .serializers import BloodTestRecordSerializer
from .permissions import IsDoctor


class BloodTestCreateView(generics.CreateAPIView):
    """
    View to create a blood test record.
    Only accessible by doctors.
    """
    queryset = BloodTestRecord.objects.all()
    serializer_class = BloodTestRecordSerializer
    permission_classes = [IsAuthenticated, IsDoctor]  # Ensure only authenticated doctors


class BloodTestListView(generics.ListAPIView):
    """
    View to list blood test records for a patient.
    Only accessible by patients.
    """
    queryset = BloodTestRecord.objects.all()
    serializer_class = BloodTestRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['test_name', 'is_abnormal']
    ordering_fields = ['test_date', 'value']

    def get_queryset(self):
        """
        Filters test records for the authenticated patient within an optional date range.
        """
        queryset = super().get_queryset().filter(patient_id=self.request.user.id)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        is_abnormal = self.request.query_params.get('is_abnormal')

        if start_date and end_date:
            queryset = queryset.filter(test_date__range=[start_date, end_date])
        
        if is_abnormal:
            queryset = queryset.filter(is_abnormal=is_abnormal.lower() == 'true')

        return queryset


class BloodTestStatsView(APIView):
    """
    View to provide statistical data (min, max, avg) for test records.
    Only accessible by doctors.
    """
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        """
        Retrieves cached statistics if available, or calculates and caches them.
        """
        stats = cache.get('blood_test_stats')
        if not stats:
            stats = BloodTestRecord.objects.values('test_name').annotate(
                min_value=Min('value'),
                max_value=Max('value'),
                avg_value=Avg('value'),
            )
            cache.set('blood_test_stats', list(stats), timeout=3600)  # Cache for 1 hour

        return Response(stats, status=status.HTTP_200_OK)


class BatchUploadView(APIView):
    """
    View to batch upload blood test records from a CSV file.
    Only accessible by doctors.
    """
    permission_classes = [IsAuthenticated, IsDoctor]

    def post(self, request):
        """
        Processes a CSV file and creates multiple blood test records.
        """
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "CSV file is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_file = file.read().decode('utf-8')
            data = csv.DictReader(StringIO(decoded_file))
        except Exception:
            return Response({"error": "Invalid CSV file"}, status=status.HTTP_400_BAD_REQUEST)

        records = []
        for row in data:
            try:
                records.append(BloodTestRecord(
                    patient_id=row['patient_id'],
                    test_name=row['test_name'],
                    value=row['value'],
                    unit=row['unit'],
                    test_date=row['test_date'],
                    is_abnormal=row['is_abnormal'].lower() == 'true',
                ))
            except KeyError as e:
                return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        BloodTestRecord.objects.bulk_create(records)
        return Response({"message": "Batch upload successful"}, status=status.HTTP_201_CREATED)
