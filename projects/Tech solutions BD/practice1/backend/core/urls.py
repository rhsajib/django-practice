from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('tution/', include('tution.urls', namespace='tution')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
