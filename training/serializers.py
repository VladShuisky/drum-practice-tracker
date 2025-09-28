from rest_framework.serializers import ModelSerializer

from training.models import TrainingSession

class TrainingSessionSerializer(ModelSerializer):

    class Meta:
        model = TrainingSession

        fields = ('user',
            'date', 'duration_minutes',
            'exercise_type', 'notes',
        )

# class CreateTrainingSessionSerializer(ModelSerializer):
