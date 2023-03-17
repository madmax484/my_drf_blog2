from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("api/", include('core.urls')),
                  path("api/v1/", include('core.urls')),
                  path("api/token/", TokenObtainPairView.as_view(), name="token"),
                  path("api/refresh_token/", TokenRefreshView.as_view(), name="refresh_token"),
                  path("ckeditor/", include('ckeditor_uploader.urls')),
                  path('', include('social_django.urls', namespace='social')),
                  path('__debug__/', include('debug_toolbar.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
