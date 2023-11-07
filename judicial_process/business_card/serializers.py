
# from drf_extra_fields.fields import Base64ImageField
# from djoser.serializers import UserCreateSerializer, UserSerializer
# from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework import serializers

from .models import (FamiliarizationCase, SidesCase, ReceivedCase, Petitions,
                     Decisions, ConsideredCase, Appeal, BusinessCard)
from django.contrib.auth import get_user_model

User = get_user_model()


class FamiliarizationCaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = FamiliarizationCase
        fields = ('petition', 'start_date', 'end_date',
                  'number_days', 'amount_one_day', 'total_amount')


class SidesCaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = SidesCase
        fields = ('sides_case', 'name', 'date_sending_agenda',
                  'familiarization_case', 'notation')


class ReceivedCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceivedCase
        fields = ('date_issue', 'name_action', 'sides_case', 'notation')


class PetitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petitions
        fields = ('name_petition', 'sides_case', 'date_application',
                  'decision_rendered', 'date_decision', 'notation')
