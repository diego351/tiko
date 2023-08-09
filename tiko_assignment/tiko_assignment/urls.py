from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from tiko.views import (
    AllEventsView,
    MyEventsView,
    ParticipationCreateUpdateView,
    SpectacularElementsView,
    UpdateEventView,
    UserRegistrationView,
)

api_urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_paidawr'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('schema', SpectacularAPIView.as_view(), name="schema"),
    path('docs', SpectacularElementsView.as_view(), name='docs'),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('events/my', MyEventsView.as_view(), name='my-events'),
    path('events', AllEventsView.as_view(), name='events'),
    path(
        'events/<int:event_id>/participation',
        ParticipationCreateUpdateView.as_view(),
        name='update-create-participation',
    ),
    path('events/<int:event_id>', UpdateEventView.as_view(), name='update-event'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
]
