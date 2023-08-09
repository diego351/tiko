from django.db.models import PROTECT, DateTimeField, ForeignKey, ManyToManyField, Model, TextField
from django.utils import timezone
from rest_framework.authentication import get_user_model
from tiko.helpers import EnumType

User = get_user_model()


class BaseModel(Model):
    updated_at = DateTimeField(null=True)
    created_at = DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()

        return super().save()

    class Meta:
        abstract = True


class Participant(BaseModel):
    class ParticipantStatus(EnumType):
        GOING = 'GOING'
        NOT_GOING = 'NOT_GOING'

    user = ForeignKey(User, related_name='as_participant', on_delete=PROTECT)
    joined_at = DateTimeField(null=False)
    status = TextField(choices=ParticipantStatus.choices())


class Event(BaseModel):
    name = TextField(null=False)
    starting_at = DateTimeField(null=False)
    participants = ManyToManyField(Participant)
    creator = ForeignKey(User, related_name='as_creator', null=False, on_delete=PROTECT)
