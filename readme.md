# Zarity Assignment : BE (Intern)

## **The Goal**

To understand your technical, code hygiene & creative approach.

## **Assignment**

<aside>
🟢

Create a Django REST API that processes and analyses sample medical test results

</aside>

### 🎯 **Core task**

Build an API that manages blood test results with these key features:

1. **A single model to store blood test records with fields:**
    1. patient_id (integer)
    2. test_name (string)
    3. value (decimal)
    4. unit (string)
    5. test_date (datetime)
    6. is_abnormal (boolean)
2. **Implement these specific API endpoints**:
    1. POST /api/tests/ - Create a new test record
    2. GET /api/tests/?patient_id=123 - Get all tests for a patient
    3. GET /api/tests/stats/ - Get basic statistics (min, max, avg) for each test type
3. **Implement ONE of these advanced features (candidate's choice):**
    1. Batch upload of test results via CSV
    2. Caching of statistics with Redis
    3. Custom filtering with complex queries

### ⚙️ **Technical Requirements**

1. Use class-based views
2. Implement proper serializer validation
3. Write at least 3 unit tests
4. Use appropriate status codes and error handling
5. Document your API using function/class docstrings

### ⭐ **Evaluation Points**

1. Proper use of Django REST Framework features
2. Serialiser implementation and validation
3. Query optimisation
4. Error handling
5. Code organisation and style
6. Test quality
7. Documentation clarity

### 💿 **Sample Model**

```python
```
from django.db import models
from django.core.validators import MinValueValidator

class TestResult(models.Model):
    patient_id = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    test_name = models.CharField(
        max_length=100,
        choices=[
            ('GLUCOSE', 'Blood Glucose'),
            ('HB', 'Hemoglobin'),
            ('CHOL', 'Cholesterol')
        ]
    )
    value = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    unit = models.CharField(max_length=10)
    test_date = models.DateTimeField()
    is_abnormal = models.BooleanField()

    class Meta:
        indexes = [
            models.Index(fields=['patient_id', 'test_name'])
        ]
```
**Sample API Response**
```
{
    "test_stats": {
        "GLUCOSE": {
            "min_value": 70.0,
            "max_value": 180.0,
            "avg_value": 98.5,
            "total_tests": 150,
            "abnormal_count": 15
        }
    }
}
```

```

### 💬 **Hints**

- Use Django's aggregation functions for statistics
- Consider using select_related() or prefetch_related() if you add related models
- Remember to validate incoming data properly
- Think about handling edge cases in your statistics endpoint

## 🚀 **How to submit**

- Step 1: GitHub Repository Setup
    1. Create a new **private** repository on GitHub
    2. Name it appropriately (e.g., "healthcare-api-assignment" or "django-test-analysis")
    3. Make sure to include:
        - README.md
        - .gitignore (for Python/Django)
        - All your project files
- Step 2: Final Code Push
    1. Ensure all your code is committed
    2. Push your final changes to the main/master branch
    3. Double-check that all files are properly uploaded
- Step 3: Add Collaborator (Required for Access)
    1. Go to your repository settings on GitHub
    2. Navigate to "Collaborators and teams" section
    3. Click "Add people" button
    4. Add collaborator username: `rupesh-zarity`
    5. Confirm the invitation
        - This step is crucial as it's the only way we can access your private repository
- Step 4: Submission
    1. Fill the submission form below:
    
- Important Notes
    - Your repository MUST be private
    - Ensure collaborator access is granted before submitting the form
    - Double-check that all code is pushed before sharing
    - Verify that the GitHub repository link is correct
    - Submit before the deadline

### 💎 **Shortlisting**

- Shortlisted candidates for the live case study round will hear back via Email & Internshala
- Make sure you monitor your inbox/spam folder - within 3-5 working days of your submission.
- Because of the volume of candidates, we will not be able to give a personal feedback to each candidate.
    - Please be rest-assured, we go through each and every assignment in detail.



# Blood Test Management API

This is a Django-based REST API for managing blood test records. The API supports operations for registering users, managing blood test records, and viewing test statistics. The application also includes permissions for different user roles such as doctors and patients.


There is a postman file attached with the repository in which I have tested all the API Endpoint.
And a CSV file for testing.

## Features

- **User Authentication:** Allows user registration and login via JWT tokens.
- **Blood Test Records:**
 - Create blood test records (accessible only by doctors).
 - List blood test records for a patient with optional filtering (test name, abnormal tests, and date range).
 - Upload multiple blood test records in bulk using CSV files (accessible only by doctors).
 - View statistical data on blood test records (min, max, average values).
- **Role-based Permissions:** Different permissions for doctors and patients.

## Prerequisites

Ensure that the following are installed:

- **Python 3.10+**
- **Django 4.0+**
- **Django REST Framework 3.12+**
- **Django Filter 2.4+**
- **Django Rest Framework Simple JWT 4.7+**

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/kunalarya873/zarity.git
   cd blood_tests_project

2.  **Create and Activate Virtual Environment:**
    
    `python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate` 
    
3.  **Install Dependencies:**
    
    `pip install -r requirements.txt` 
    
4.  **Setup Database:**
    
    Make sure to set up the database and apply migrations.
    
    `python manage.py migrate` 
    
5.  **Create Superuser (Optional for Admin Access):**
    
    `python manage.py createsuperuser` 
    
6.  **Run the Server:**
    
    Start the development server.
    
    `python manage.py runserver` 
    

API Endpoints
-------------

### Authentication Endpoints

*   **POST** `/api/register/`  
    Register a new user (Doctor or Patient).
    
    **Payload:**
    
    `{
      "username": "john_doe",
      "password": "securepassword123",
      "email": "john@example.com",
      "user_type": "patient"
    }` 
    
*   **POST** `/api/token/`  
    Obtain JWT access token.
    
    **Payload:**
    
    `{
      "username": "john_doe",
      "password": "securepassword123"
    }` 
    
*   **POST** `/api/token/refresh/`  
    Refresh the JWT token.
    

### Blood Test Endpoints

*   **POST** `/api/tests/`  
    Create a new blood test record (Only accessible by Doctors).
    
    **Payload:**
    
    `{
      "patient_id": 2,
      "test_name": "Hemoglobin",
      "value": "13.50",
      "unit": "g/dL",
      "test_date": "2024-11-27T10:00:00Z",
      "is_abnormal": false
    }` 
    
*   **GET** `/api/tests/list/`  
    List blood test records for a patient (Only accessible by Patients).
    
    **Query Parameters:**
    
    *   `start_date`: Start date of the range (Optional, format: YYYY-MM-DD)
    *   `end_date`: End date of the range (Optional, format: YYYY-MM-DD)
    *   `is_abnormal`: Filter abnormal tests (Optional, values: "true", "false")
    
    **Example:**
    
    `GET /api/tests/list/?start_date=2024-11-01&end_date=2024-11-30&is_abnormal=true` 
    
*   **GET** `/api/tests/stats/`  
    View statistical data (min, max, average) for blood test records (Only accessible by Doctors).
    
*   **POST** `/api/tests/upload/`  
    Bulk upload of blood test records from a CSV file (Only accessible by Doctors).
    
    **CSV Format:**
    
    `patient_id,test_name,value,unit,test_date,is_abnormal
    2,Hemoglobin,13.50,g/dL,2024-11-27T10:00:00Z,false
    3,Cholesterol,180.00,mg/dL,2024-11-26T10:00:00Z,true` 
    

Permissions
-----------

### IsAuthenticated

*   Ensures that the user is authenticated.

### IsDoctor

*   Custom permission to ensure that only doctors can access certain views like creating test records or viewing test statistics.

### IsPatient

*   Custom permission to ensure that only patients can access their own blood test records.

Troubleshooting
---------------

1.  **Database Issues:** If you encounter the error `no such table: tests_app_customuser`, make sure you have run the migrations:
    
    `python manage.py migrate` 
    
2.  **CORS Issues:** If you're testing the API from a different domain and encounter CORS issues, make sure to install and configure `django-cors-headers`:
    
    `pip install django-cors-headers` 
    
    Add it to `INSTALLED_APPS` and middleware in `settings.py`.
    
3.  **Permissions Error:** Ensure that you're logged in as the correct user (doctor or patient) when making requests, especially for endpoints that have role-based restrictions.
    

Development
-----------

1.  **To add a new feature:**
    
    *   Create a new migration (if modifying models):
        
        `python manage.py makemigrations` 
        
    *   Apply migrations:
        
        `python manage.py migrate` 
        
    *   Add the feature to the views, serializers, and URLs.
2.  **To run tests:**
    
    `python manage.py test` 
    

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.

 ### Instructions Summary:

- **Installation:** The README provides clear steps to install dependencies, set up a virtual environment, and migrate the database.
- **API Documentation:** It includes details about the endpoints, request/response formats, and required parameters.
- **Permissions and Troubleshooting:** It covers the role-based permissions (`IsDoctor`, `IsPatient`, etc.) and how to resolve common errors like migration issues or CORS problems.
- **Development Guidelines:** Instructions for adding new features and running tests.

You can create a `README.md` file with this content in your project's root directory to help others understand how to work with your API.
