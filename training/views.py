from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from training.models import TrainingSession
from training.serializers import TrainingSessionSerializer


class TrainingSessionViewSet(mixins.CreateModelMixin, mixins.ListModelMixin ,viewsets.GenericViewSet):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TrainingSessionSerializer
    queryset = TrainingSession.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        return super().create(request, *args, **kwargs)
