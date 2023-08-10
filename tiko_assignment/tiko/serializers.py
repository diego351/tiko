from asyncio import events
from tkinter import EventType

from django.utils import timezone
from rest_framework.authentication import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer
from tiko.models import Event, Participant

User = get_user_model()


class UserRegistrationSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        # TODO: in normal flow we need to do email validation

        if User.objects.filter(email=validated_data['email']).exists():
            raise ValidationError('Given email already exists')

        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class ParticipantSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Participant
        fields = ('id', 'joined_at', 'user')


class EventSerializer(ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'starting_at', 'participants')

    def create(self, validated_data):
        starting_at = validated_data['starting_at']

        now = timezone.now()
        if starting_at <= now:
            raise ValidationError("Can't create event starting in past")

        user = Event.objects.create(
            name=validated_data['name'],
            starting_at=starting_at,
            creator=self.context['request'].user,
        )

        return user


class UpdateCreateParticipationSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = ('status',)

    def create(self, validated_data):
        event_id = self.context['view'].kwargs['event_id']

        if not Event.objects.filter(id=event_id).exists():
            raise ValidationError("Not such event")

        event = Event.objects.get(id=event_id)

        if event.starting_at <= timezone.now():
            raise ValidationError("Can't attend past events")

        participation, created = Participant.objects.update_or_create(
            event=event,
            user=self.context['request'].user,
            defaults={
                'status': validated_data['status'],
                'joined_at': timezone.now(),
            },
        )

        return participation


class UpdateEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'starting_at')
