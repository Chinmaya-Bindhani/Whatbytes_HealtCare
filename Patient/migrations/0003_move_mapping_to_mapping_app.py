from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Patient", "0002_patientdoctormapping"),
    ]

    operations = [
        # Transfer model ownership while keeping the existing table and records.
        migrations.SeparateDatabaseAndState(
            state_operations=[migrations.DeleteModel(name="PatientDoctorMapping")],
            database_operations=[],
        ),
    ]
