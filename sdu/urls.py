from django.urls import include, path
from rest_framework import routers
from sdu.main import views
from rest_framework import permissions
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r"profile", views.ProfilePageView)
router.register(r"projects", views.ProjectsViewSet)
router.register(r"tasks", views.TasksViewSet)
router.register(r"dashboard", views.DashboardView)
router.register(r"analytics", views.AnalyticsPageViewSet)
router.register(r"courses", views.CoursesViewSet)
router.register(r"search_users", views.UsersSearchViewSet)
router.register(r"subtasks", views.SubtasksViewSet)
router.register(r"supervisor", views.StudentSupervisorViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="SDU API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    patterns=router.urls,
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("login/", views.MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.RegisterView.as_view(), name="auth_register"),
    path(
        "schema/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
