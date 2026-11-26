import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Doctor", "0001_initial"),
        ("Patient", "0003_move_mapping_to_mapping_app"),
    ]

    operations = [
        # The Patient migrations already created this table.
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name="PatientDoctorMapping",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("patient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="doctor_mappings", to="Patient.patient")),
                        ("doctor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="patient_mappings", to="Doctor.doctor")),
                    ],
                    options={
                        "db_table": "Patient_patientdoctormapping",
                        "constraints": [models.UniqueConstraint(fields=("patient", "doctor"), name="unique_patient_doctor")],
                    },
                ),
            ],
        ),
    ]
