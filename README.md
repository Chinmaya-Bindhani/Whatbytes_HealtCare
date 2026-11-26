# Healthcare API test results

Tested on 26 November 2026.

**96/97 checks passed. 1 check failed.**

The original run passed 92 checks. Targeted reruns passed the previously failing email-normalization, assignment registration URL, assignment login URL and refresh-token checks after their fixes. The other original results are retained from that run.

Requests ran through Django REST Framework's API client, the actual URL configuration, JWT authentication and the configured PostgreSQL database. Synthetic records were created inside a transaction and rolled back after the run. Login-issued tokens were used for authenticated requests.

These checks cover application behavior in-process. They do not verify the running HTTP server, concurrent requests, load, or production deployment.

## Findings

- The implemented doctor, patient and mapping operations passed the tested success, validation, authentication and ownership scenarios.
- Registration accepts the password '1' even though password validators are configured. The serializer does not invoke Django password validation.
- Login now uses the same user-manager email normalization as registration. Lowercase, uppercase and mixed-case domains passed targeted PostgreSQL checks. Incorrect passwords still return 401 and invalid email syntax returns 400. Normalization lowercases the domain and preserves the part before @.
- The assignment authentication paths /api/auth/register/ and /api/auth/login/ now return 201 and 200 for valid requests. The existing /api/register/ and /api/login/ routes also passed regression checks.
- POST /api/token/refresh/ and POST /api/auth/token/refresh/ accept a JSON refresh field and return a new access token. Both passed tests for profile access with the new token, missing refresh input (400), and invalid, expired or wrong-type tokens (401).
- DEFAULT_PERMISSION_CLASSES is configured as a string because its single-item tuple has no trailing comma. Existing views declare their permissions explicitly, so the tested routes work. This configuration should be corrected before relying on default permissions.

## Using the APIs

Use http://127.0.0.1:8000 as the local base URL. Register using name, email, password and confirm_password. Log in with email and password, then send the returned token.access as a Bearer token.

Doctor fields are name, specialization, email and phone. Patient fields are name, age, email and phone. Contact fields are optional. Patient ownership is assigned by the server.

Create mappings with patient and doctor IDs. GET /api/mappings/<patient_id>/ accepts a patient ID. DELETE /api/mappings/<mapping_id>/ accepts the mapping's own ID. Removing a mapping preserves both records. Authenticated users can manage all doctors; patient and mapping access is restricted to the patient owner.

## Individual results

Expected statuses reflect the tested behavior or stated requirement. A matching status also had to pass any response-content or database checks for that case. Numeric IDs below belonged to temporary test records.

| Method | Endpoint | Scenario | Expected | Actual | Result |
|---|---|---|---|---|---|
| POST | /api/register/ | Valid registration | 201 | 201 | PASS |
| POST | /api/register/ | Valid registration | 201 | 201 | PASS |
| POST | /api/login/ | Valid credentials return access and refresh tokens | 200 | 200 | PASS |
| POST | /api/login/ | Valid credentials return access and refresh tokens | 200 | 200 | PASS |
| POST | /api/register/ | Duplicate email rejected | 400 | 400 | PASS |
| POST | /api/register/ | Duplicate normalized domain rejected | 400 | 400 | PASS |
| POST | /api/register/ | Invalid email rejected | 400 | 400 | PASS |
| POST | /api/register/ | Password mismatch rejected | 400 | 400 | PASS |
| POST | /api/register/ | Required fields enforced | 400 | 400 | PASS |
| POST | /api/register/ | Configured password strength policy enforced | 400 | 201 | FAIL |
| POST | /api/login/ | Incorrect password rejected | 401 | 401 | PASS |
| POST | /api/login/ | Unknown account rejected | 401 | 401 | PASS |
| POST | /api/login/ | Required login fields enforced | 400 | 400 | PASS |
| POST | /api/login/ | Login accepts the same domain normalization as registration | 200 | 200 | PASS |
| GET | /api/register/ | Unsupported method rejected | 405 | 405 | PASS |
| GET | /api/login/ | Unsupported method rejected | 405 | 405 | PASS |
| POST | /api/auth/register/ | Assignment authentication URL exists | 201 | 201 | PASS |
| POST | /api/auth/login/ | Assignment authentication URL exists | 200 | 200 | PASS |
| POST | /api/token/refresh/ | Returned refresh token can obtain new access token | 200 | 200 | PASS |
| GET | /api/user/ | Missing bearer token rejected | 401 | 401 | PASS |
| POST | /api/doctors/ | Missing bearer token rejected | 401 | 401 | PASS |
| GET | /api/doctors/ | Missing bearer token rejected | 401 | 401 | PASS |
| GET | /api/doctors/999999999/ | Missing bearer token rejected | 401 | 401 | PASS |
| PUT | /api/doctors/999999999/ | Missing bearer token rejected | 401 | 401 | PASS |
| DELETE | /api/doctors/999999999/ | Missing bearer token rejected | 401 | 401 | PASS |
| POST | /api/patients/ | Missing bearer token rejected | 401 | 401 | PASS |
| GET | /api/patients/ | Missing bearer token rejected | 401 | 401 | PASS |
| GET | /api/patients/999999999/ | Missing bearer token rejected | 401 | 401 | PASS |
| PUT | /api/patients/999999999/ | Missing bearer token rejected | 401 | 401 | PASS |
| DELETE | /api/patients/999999999/ | Missing bearer token rejected | 401 | 401 | PASS |
| POST | /api/mappings/ | Missing bearer token rejected | 401 | 401 | PASS |
| GET | /api/mappings/ | Missing bearer token rejected | 401 | 401 | PASS |
| GET | /api/mappings/999999999/ | Missing bearer token rejected | 401 | 401 | PASS |
| DELETE | /api/mappings/999999999/ | Missing bearer token rejected | 401 | 401 | PASS |
| GET | /api/user/ | Invalid token rejected | 401 | 401 | PASS |
| GET | /api/user/ | Expired token rejected | 401 | 401 | PASS |
| GET | /api/user/ | Refresh token rejected as access token | 401 | 401 | PASS |
| GET | /api/user/ | Current user profile | 200 | 200 | PASS |
| POST | /api/doctors/ | Create doctor with all fields | 201 | 201 | PASS |
| POST | /api/doctors/ | Optional contact fields omitted | 201 | 201 | PASS |
| GET | /api/doctors/ | List includes both created doctors | 200 | 200 | PASS |
| GET | /api/doctors/3/ | Retrieve doctor | 200 | 200 | PASS |
| PUT | /api/doctors/3/ | Full update persists | 200 | 200 | PASS |
| PATCH | /api/doctors/3/ | Partial update persists | 200 | 200 | PASS |
| POST | /api/doctors/ | Required fields rejected | 400 | 400 | PASS |
| POST | /api/doctors/ | Blank name rejected | 400 | 400 | PASS |
| POST | /api/doctors/ | Invalid email rejected | 400 | 400 | PASS |
| POST | /api/doctors/ | Phone exceeds max length rejected | 400 | 400 | PASS |
| PUT | /api/doctors/3/ | Full update requires required fields | 400 | 400 | PASS |
| GET | /api/doctors/999999999/ | Missing doctor | 404 | 404 | PASS |
| PUT | /api/doctors/999999999/ | Missing doctor | 404 | 404 | PASS |
| DELETE | /api/doctors/999999999/ | Missing doctor | 404 | 404 | PASS |
| POST | /api/patients/ | Create assigns logged-in owner despite submitted owner | 201 | 201 | PASS |
| POST | /api/patients/ | Age zero and optional contact fields accepted | 201 | 201 | PASS |
| POST | /api/patients/ | Second user creates own patient | 201 | 201 | PASS |
| GET | /api/patients/ | List contains only current user's patients | 200 | 200 | PASS |
| GET | /api/patients/2/ | Retrieve own patient | 200 | 200 | PASS |
| PUT | /api/patients/2/ | Update persists and cannot transfer ownership | 200 | 200 | PASS |
| PATCH | /api/patients/2/ | Partial update persists | 200 | 200 | PASS |
| POST | /api/patients/ | Required fields rejected | 400 | 400 | PASS |
| POST | /api/patients/ | Negative age rejected | 400 | 400 | PASS |
| POST | /api/patients/ | Non-numeric age rejected | 400 | 400 | PASS |
| POST | /api/patients/ | Blank name rejected | 400 | 400 | PASS |
| POST | /api/patients/ | Invalid email rejected | 400 | 400 | PASS |
| PUT | /api/patients/2/ | Full update requires required fields | 400 | 400 | PASS |
| GET | /api/patients/2/ | Other user's patient inaccessible | 404 | 404 | PASS |
| PUT | /api/patients/2/ | Other user's patient inaccessible | 404 | 404 | PASS |
| PATCH | /api/patients/2/ | Other user's patient inaccessible | 404 | 404 | PASS |
| DELETE | /api/patients/2/ | Other user's patient inaccessible | 404 | 404 | PASS |
| GET | /api/patients/999999999/ | Missing patient | 404 | 404 | PASS |
| PUT | /api/patients/999999999/ | Missing patient | 404 | 404 | PASS |
| DELETE | /api/patients/999999999/ | Missing patient | 404 | 404 | PASS |
| POST | /api/mappings/ | Assign existing doctor to own patient | 201 | 201 | PASS |
| POST | /api/mappings/ | Multiple doctors per patient | 201 | 201 | PASS |
| POST | /api/mappings/ | Doctor can serve multiple patients | 201 | 201 | PASS |
| GET | /api/mappings/ | Lists own mappings only | 200 | 200 | PASS |
| GET | /api/mappings/2/ | Patient ID returns both assigned doctors | 200 | 200 | PASS |
| GET | /api/mappings/3/ | Unassigned patient returns empty list | 200 | 200 | PASS |
| POST | /api/mappings/ | Duplicate assignment rejected | 400 | 400 | PASS |
| POST | /api/mappings/ | Required mapping fields rejected | 400 | 400 | PASS |
| POST | /api/mappings/ | Missing patient rejected | 400 | 400 | PASS |
| POST | /api/mappings/ | Missing doctor rejected | 400 | 400 | PASS |
| POST | /api/mappings/ | Another user's patient rejected | 400 | 400 | PASS |
| GET | /api/mappings/2/ | Other user's patient mappings inaccessible | 404 | 404 | PASS |
| DELETE | /api/mappings/1/ | Other user's mapping protected | 404 | 404 | PASS |
| GET | /api/mappings/999999999/ | Missing record | 404 | 404 | PASS |
| DELETE | /api/mappings/999999999/ | Missing record | 404 | 404 | PASS |
| PUT | /api/mappings/1/ | Unsupported mapping update rejected | 405 | 405 | PASS |
| DELETE | /api/mappings/1/ | Mapping ID removes only assignment | 204 | 204 | PASS |
| DELETE | /api/mappings/1/ | Repeated mapping deletion | 404 | 404 | PASS |
| DELETE | /api/patients/2/ | Patient deletion removes its remaining mappings | 204 | 204 | PASS |
| GET | /api/patients/2/ | Deleted patient inaccessible | 404 | 404 | PASS |
| DELETE | /api/doctors/3/ | Doctor deletion removes its mappings and preserves patients | 204 | 204 | PASS |
| GET | /api/doctors/3/ | Deleted doctor inaccessible | 404 | 404 | PASS |
| DELETE | /api/doctors/4/ | Delete remaining test doctor | 204 | 204 | PASS |
| GET | /api/user/ | Deactivated user access token rejected | 401 | 401 | PASS |
| POST | /api/login/ | Deactivated user cannot log in | 401 | 401 | PASS |

## Project checks

- Django system check passed.
- Migration consistency check passed with no model changes detected.
- Synthetic test account cleanup verified after transaction rollback.
- OPTIONS and HEAD metadata behavior, browser UI, Django Admin workflows and concurrency were outside this API test run.
