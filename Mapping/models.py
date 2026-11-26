from django.db import models


class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(
        "Patient.Patient", on_delete=models.CASCADE, related_name="doctor_mappings"
    )
    doctor = models.ForeignKey(
        "Doctor.Doctor", on_delete=models.CASCADE, related_name="patient_mappings"
    )

    class Meta:
        db_table = "Patient_patientdoctormapping"
        constraints = [
            models.UniqueConstraint(
                fields=["patient", "doctor"], name="unique_patient_doctor"
            )
        ]
