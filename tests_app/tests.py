from rest_framework.test import APITestCase
from rest_framework import status
from .models import BloodTestRecord, CustomUser
from io import BytesIO
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken

class BloodTestAPITests(APITestCase):

    def setUp(self):
        # Create a test doctor user and obtain JWT token for authentication
        self.doctor_user = CustomUser.objects.create_user(username='doctoruser', password='testpassword', user_type='doctor')
        self.patient_user = CustomUser.objects.create_user(username='patientuser', password='testpassword', user_type='patient')

        # Generate JWT tokens for both doctor and patient
        self.doctor_refresh = RefreshToken.for_user(self.doctor_user)
        self.patient_refresh = RefreshToken.for_user(self.patient_user)

        self.doctor_access_token = str(self.doctor_refresh.access_token)
        self.patient_access_token = str(self.patient_refresh.access_token)

    def get_auth_header(self, user_type='doctor'):
        if user_type == 'doctor':
            return {'Authorization': f'Bearer {self.doctor_access_token}'}
        else:
            return {'Authorization': f'Bearer {self.patient_access_token}'}

    def test_create_test_record(self):
        data = {
            "patient_id": 123,
            "test_name": "Hemoglobin",
            "value": 13.5,
            "unit": "g/dL",
            "test_date": "2024-11-27T10:00:00Z",
            "is_abnormal": False
        }
        response = self.client.post('/api/tests/', data, HTTP_AUTHORIZATION=f'Bearer {self.doctor_access_token}' )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tests_for_patient(self):
        # Create a test record for the authenticated patient
        BloodTestRecord.objects.create(
            patient_id=self.patient_user.id,  # Ensure patient ID is correct
            test_name="Hemoglobin", 
            value=13.5, 
            unit="g/dL", 
            test_date="2024-11-27T10:00:00Z", 
            is_abnormal=False
        )
        # Send the GET request to fetch the test records for the patient
        response = self.client.get(f'/api/tests/list/?patient_id={self.patient_user.id}', HTTP_AUTHORIZATION=f'Bearer {self.patient_access_token}')
        # Ensure the response is OK and contains the expected data
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_statistics(self):
        BloodTestRecord.objects.create(
            patient_id=123, test_name="Hemoglobin", value=13.5, unit="g/dL", test_date="2024-11-27T10:00:00Z", is_abnormal=False
        )
        response = self.client.get('/api/tests/list/?patient_id=123', HTTP_AUTHORIZATION=f'Bearer {self.doctor_access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_batch_upload(self):
        csv_content = b"patient_id,test_name,value,unit,test_date,is_abnormal\n123,Hemoglobin,13.5,g/dL,2024-11-27T10:00:00Z,False\n"
        response = self.client.post(
            '/api/tests/upload/',
            {'file': BytesIO(csv_content)},
            format='multipart',
            HTTP_AUTHORIZATION=f'Bearer {self.doctor_access_token}' 
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BloodTestRecord.objects.count(), 1)

    def test_caching_stats(self):
        # Clear cache before testing
        cache.clear()

        # Populate data
        BloodTestRecord.objects.create(patient_id=123, test_name="Hemoglobin", value=13.5, unit="g/dL", test_date="2024-11-27T10:00:00Z", is_abnormal=False)
        BloodTestRecord.objects.create(patient_id=124, test_name="Hemoglobin", value=15.0, unit="g/dL", test_date="2024-11-28T10:00:00Z", is_abnormal=False)

        response = self.client.get('/api/tests/stats/', HTTP_AUTHORIZATION=f'Bearer {self.doctor_access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure caching is working
        cached_stats = cache.get('blood_test_stats')
        self.assertIsNotNone(cached_stats)
        self.assertEqual(len(cached_stats), 1)

    def test_custom_filtering(self):
        # Create test records with the correct patient_id and abnormal status
        BloodTestRecord.objects.create(patient_id=self.patient_user.id, test_name="Hemoglobin", value=13.5, unit="g/dL", test_date="2024-11-27T10:00:00Z", is_abnormal=False)
        BloodTestRecord.objects.create(patient_id=self.patient_user.id, test_name="Hemoglobin", value=15.0, unit="g/dL", test_date="2024-11-28T10:00:00Z", is_abnormal=True)

        # Use the patient access token instead of the doctor's token
        response = self.client.get('/api/tests/list/?test_name=Hemoglobin&is_abnormal=true', HTTP_AUTHORIZATION=f'Bearer {self.patient_access_token}')

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Ensure records are returned
        self.assertEqual(response.data[0]['value'], '15.00')  # Ensure the correct record is returned (with is_abnormal=True)

