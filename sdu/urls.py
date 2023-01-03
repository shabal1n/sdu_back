from django.urls import include, path
from rest_framework import routers
from sdu.main import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenRefreshView
)


router = routers.DefaultRouter()
router.register(r'profile', views.ProfileViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="SDU API",
      default_version='v1',
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
   path('', include(router.urls)),
   path('login/', views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
   path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('register/', views.RegisterView.as_view(), name='auth_register'),
   path('schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
