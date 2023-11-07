from django.contrib import admin
from django.urls import include, path
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('', include('business_card.urls', namespace='business_card')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
]
