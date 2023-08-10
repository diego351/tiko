from django.db.models import Prefetch
from drf_spectacular.settings import spectacular_settings
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import AUTHENTICATION_CLASSES
from rest_framework.authentication import get_user_model
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from tiko.models import Event, Participant
from tiko.serializers import (
    EventSerializer,
    UpdateCreateParticipationSerializer,
    UpdateEventSerializer,
    UserRegistrationSerializer,
)

User = get_user_model()


class SpectacularElementsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = spectacular_settings.SERVE_PERMISSIONS
    authentication_classes = AUTHENTICATION_CLASSES
    url_name = 'schema'
    url = None
    template_name = 'elements.html'
    title = spectacular_settings.TITLE

    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        return Response(
            data={
                'title': self.title,
                'js_dist': 'https://unpkg.com/@stoplight/elements/web-components.min.js',
                'css_dist': 'https://unpkg.com/@stoplight/elements/styles.min.css',
                'schema_url': 'schema',
            },
            template_name=self.template_name,
        )


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = []


class MyEventsView(ListCreateAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        qs = Event.objects
        qs = qs.filter(creator=self.request.user)
        qs = qs.prefetch_related(
            Prefetch('participants', queryset=Participant.objects.filter(status=Participant.ParticipantStatus.GOING))
        )
        qs = qs.prefetch_related('participants__user')
        return qs.all()


class AllEventsView(ListAPIView):
    serializer_class = EventSerializer
    filterset_fields = ('name', 'starting_at')

    def get_queryset(self):
        qs = Event.objects
        qs = qs.prefetch_related(
            Prefetch('participants', queryset=Participant.objects.filter(status=Participant.ParticipantStatus.GOING))
        )
        qs = qs.prefetch_related('participants__user')
        return qs.all()


class ParticipationCreateUpdateView(CreateAPIView):
    serializer_class = UpdateCreateParticipationSerializer


class UpdateEventView(RetrieveUpdateAPIView):
    serializer_class = UpdateEventSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Event.objects.filter(id=event_id)

    def get_object(self):
        queryset = self.get_queryset()
        event_id = self.kwargs['event_id']
        event = queryset.filter(pk=event_id).first()

        if not event:
            raise NotFound('Not such event')

        return event

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        return obj.creator == request.user
