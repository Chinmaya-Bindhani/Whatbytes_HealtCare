from rest_framework import serializers

from .models import PatientDoctorMapping


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "patient", "doctor"]

    def validate_patient(self, patient):
        if patient.created_by_id != self.context["request"].user.pk:
            raise serializers.ValidationError("Select one of your own patients.")
        return patient

    def create(self, validated_data):
        mapping, created = PatientDoctorMapping.objects.get_or_create(**validated_data)
        if not created:
            raise serializers.ValidationError("This doctor is already assigned to this patient.")
        return mapping
