from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', profile_view, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),

    path('', HomeView.as_view(), name='home'),
    path('tests/', TestsListView.as_view(), name='tests_list'),
    path('test/<test_slug_name>/', TestDetailView.as_view(), name='test_detail'),
    path('test/<test_slug_name>/questions/', TestQuestionsView.as_view(), name='test_questions'),
    path('test/<test_slug_name>/results/', TestResultsView.as_view(), name='results'),
    path('add_comment/', CommentCreateView.as_view(), name='add_comment'),
    path('test_create/', TestCreateView.as_view(), name='test_create'),
    path('test_create/add_questions/', QuestionsCreateView.as_view(), name='add_questions'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
