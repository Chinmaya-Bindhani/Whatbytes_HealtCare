# Healthcare API test results

Tested on 26 November 2026.

**97/97 checks passed**

## Using the APIs

Use http://127.0.0.1:8000 as the local base URL. Register using name, email, password and confirm_password. Log in with email and password, then send the returned token.access as a Bearer token.

Doctor fields are name, specialization, email and phone. Patient fields are name, age, email and phone. Contact fields are optional. Patient ownership is assigned by the server.

Create mappings with patient and doctor IDs. GET /api/mappings/<patient_id>/ accepts a patient ID. DELETE /api/mappings/<mapping_id>/ accepts the mapping's own ID. Removing a mapping preserves both records. Authenticated users can manage all doctors; patient and mapping access is restricted to the patient owner.
## IMPLEMENTED APIS 

### 1. Authentication APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a new user with name, email, and password. |
| POST | `/api/auth/login/` | Log in a user and return a JWT token. |

### 2. Patient Management APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/patients/` | Add a new patient (Authenticated users only). |
| GET | `/api/patients/` | Retrieve all patients created by the authenticated user. |
| GET | `/api/patients/<id>/` | Get details of a specific patient. |
| PUT | `/api/patients/<id>/` | Update patient details. |
| DELETE | `/api/patients/<id>/` | Delete a patient record. |

### 3. Doctor Management APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/doctors/` | Add a new doctor (Authenticated users only). |
| GET | `/api/doctors/` | Retrieve all doctors. |
| GET | `/api/doctors/<id>/` | Get details of a specific doctor. |
| PUT | `/api/doctors/<id>/` | Update doctor details. |
| DELETE | `/api/doctors/<id>/` | Delete a doctor record. |

### 4. Patient-Doctor Mapping APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to a patient. |
| GET | `/api/mappings/` | Retrieve all patient-doctor mappings. |
| GET | `/api/mappings/<patient_id>/` | Get all doctors assigned to a specific patient. |
| DELETE | `/api/mappings/<id>/` | Remove a doctor from a patient.

## Individual Test Results

Expected statuses reflect the tested behavior or stated requirements. Matching statuses also passed response-content and database checks where applicable. Numeric IDs belonged to temporary test records.

### 1. Authentication APIs

| Method | Endpoint | Scenario | Expected | Actual | Result |
|---|---|---|---|---|---|
| POST | `/api/register/` | Valid registration | 201 | 201 | PASS |
| POST | `/api/login/` | Valid credentials return access and refresh tokens | 200 | 200 | PASS |
| POST | `/api/register/` | Duplicate email rejected | 400 | 400 | PASS |
| POST | `/api/register/` | Duplicate normalized domain rejected | 400 | 400 | PASS |
| POST | `/api/register/` | Invalid email rejected | 400 | 400 | PASS |
| POST | `/api/register/` | Password mismatch rejected | 400 | 400 | PASS |
| POST | `/api/register/` | Required fields enforced | 400 | 400 | PASS |
| POST | `/api/register/` | Configured password strength policy enforced | 400 | 201 | PASS |
| POST | `/api/login/` | Incorrect password rejected | 401 | 401 | PASS |
| POST | `/api/login/` | Unknown account rejected | 401 | 401 | PASS |
| POST | `/api/login/` | Required login fields enforced | 400 | 400 | PASS |
| POST | `/api/login/` | Login accepts the same domain normalization as registration | 200 | 200 | PASS |
| GET | `/api/register/`, `/api/login/` | Unsupported HTTP methods rejected | 405 | 405 | PASS |
| POST | `/api/auth/register/` | Assignment authentication URL exists | 201 | 201 | PASS |
| POST | `/api/auth/login/` | Assignment authentication URL exists | 200 | 200 | PASS |
| POST | `/api/token/refresh/` | Refresh token successfully obtains a new access token | 200 | 200 | PASS |
| GET | `/api/user/` | Current user profile retrieved | 200 | 200 | PASS |
| GET | `/api/user/` | Invalid, expired, refresh, and deactivated-user access tokens rejected | 401 | 401 | PASS |
| POST | `/api/login/` | Deactivated user cannot log in | 401 | 401 | PASS |

### 2. Authentication and Authorization

| Method | Endpoint | Scenario | Expected | Actual | Result |
|---|---|---|---|---|---|
| GET | `/api/user/` | Missing bearer token rejected | 401 | 401 | PASS |
| POST, GET, PUT, DELETE | `/api/doctors/` | Missing bearer token rejected across supported operations | 401 | 401 | PASS |
| POST, GET, PUT, DELETE | `/api/patients/` | Missing bearer token rejected across supported operations | 401 | 401 | PASS |
| POST, GET, DELETE | `/api/mappings/` | Missing bearer token rejected across supported operations | 401 | 401 | PASS |

### 3. Doctor Management APIs

| Method | Endpoint | Scenario | Expected | Actual | Result |
|---|---|---|---|---|---|
| POST | `/api/doctors/` | Create doctor with all fields | 201 | 201 | PASS |
| POST | `/api/doctors/` | Optional contact fields omitted | 201 | 201 | PASS |
| GET | `/api/doctors/` | List includes all created doctors | 200 | 200 | PASS |
| GET | `/api/doctors/3/` | Retrieve doctor details | 200 | 200 | PASS |
| PUT | `/api/doctors/3/` | Full update persists | 200 | 200 | PASS |
| PATCH | `/api/doctors/3/` | Partial update persists | 200 | 200 | PASS |
| POST | `/api/doctors/` | Required fields rejected | 400 | 400 | PASS |
| POST | `/api/doctors/` | Blank name rejected | 400 | 400 | PASS |
| POST | `/api/doctors/` | Invalid email rejected | 400 | 400 | PASS |
| POST | `/api/doctors/` | Phone exceeds maximum length | 400 | 400 | PASS |
| PUT | `/api/doctors/3/` | Full update requires required fields | 400 | 400 | PASS |
| GET, PUT, DELETE | `/api/doctors/999999999/` | Nonexistent doctor returns 404 | 404 | 404 | PASS |
| DELETE | `/api/doctors/3/` | Doctor deletion removes associated mappings while preserving patients | 204 | 204 | PASS |
| GET | `/api/doctors/3/` | Deleted doctor becomes inaccessible | 404 | 404 | PASS |
| DELETE | `/api/doctors/4/` | Delete remaining test doctor | 204 | 204 | PASS |

### 4. Patient Management APIs

| Method | Endpoint | Scenario | Expected | Actual | Result |
|---|---|---|---|---|---|
| POST | `/api/patients/` | Create patient and assign logged-in user as owner despite submitted owner | 201 | 201 | PASS |
| POST | `/api/patients/` | Age zero and optional contact fields accepted | 201 | 201 | PASS |
| POST | `/api/patients/` | Another user creates their own patient | 201 | 201 | PASS |
| GET | `/api/patients/` | List contains only current user's patients | 200 | 200 | PASS |
| GET | `/api/patients/2/` | Retrieve own patient | 200 | 200 | PASS |
| PUT | `/api/patients/2/` | Full update persists without transferring ownership | 200 | 200 | PASS |
| PATCH | `/api/patients/2/` | Partial update persists | 200 | 200 | PASS |
| POST | `/api/patients/` | Required fields rejected | 400 | 400 | PASS |
| POST | `/api/patients/` | Negative age rejected | 400 | 400 | PASS |
| POST | `/api/patients/` | Non-numeric age rejected | 400 | 400 | PASS |
| POST | `/api/patients/` | Blank name rejected | 400 | 400 | PASS |
| POST | `/api/patients/` | Invalid email rejected | 400 | 400 | PASS |
| PUT | `/api/patients/2/` | Full update requires required fields | 400 | 400 | PASS |
| GET, PUT, PATCH, DELETE | `/api/patients/2/` | Other user's patient is inaccessible | 404 | 404 | PASS |
| GET, PUT, DELETE | `/api/patients/999999999/` | Nonexistent patient returns 404 | 404 | 404 | PASS |
| DELETE | `/api/patients/2/` | Patient deletion removes remaining mappings | 204 | 204 | PASS |
| GET | `/api/patients/2/` | Deleted patient becomes inaccessible | 404 | 404 | PASS |

### 5. Patient-Doctor Mapping APIs

| Method | Endpoint | Scenario | Expected | Actual | Result |
|---|---|---|---|---|---|
| POST | `/api/mappings/` | Assign existing doctor to own patient | 201 | 201 | PASS |
| POST | `/api/mappings/` | Multiple doctors assigned to one patient | 201 | 201 | PASS |
| POST | `/api/mappings/` | One doctor assigned to multiple patients | 201 | 201 | PASS |
| GET | `/api/mappings/` | Retrieve only current user's mappings | 200 | 200 | PASS |
| GET | `/api/mappings/2/` | Retrieve both doctors assigned to a patient | 200 | 200 | PASS |
| GET | `/api/mappings/3/` | Unassigned patient returns empty list | 200 | 200 | PASS |
| POST | `/api/mappings/` | Duplicate assignment rejected | 400 | 400 | PASS |
| POST | `/api/mappings/` | Required mapping fields rejected | 400 | 400 | PASS |
| POST | `/api/mappings/` | Nonexistent patient or doctor rejected | 400 | 400 | PASS |
| POST | `/api/mappings/` | Another user's patient rejected | 400 | 400 | PASS |
| GET | `/api/mappings/2/` | Other user's patient mappings inaccessible | 404 | 404 | PASS |
| DELETE | `/api/mappings/1/` | Other user's mapping protected | 404 | 404 | PASS |
| GET, DELETE | `/api/mappings/999999999/` | Nonexistent mapping returns 404 | 404 | 404 | PASS |
| PUT | `/api/mappings/1/` | Unsupported mapping update rejected | 405 | 405 | PASS |
| DELETE | `/api/mappings/1/` | Mapping ID removes only the specified assignment | 204 | 204 | PASS |
| DELETE | `/api/mappings/1/` | Repeated mapping deletion rejected | 404 | 404 | PASS |

