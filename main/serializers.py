from rest_framework import serializers
from .models import CV

class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = ['id', 'first_name', 'last_name', 'skills', 'projects', 'bio', 'contacts'] 