from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cvs', views.CVViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('cv/<int:cv_id>/', views.cv_detail, name='cv_detail'),
    path('cv/<int:cv_id>/pdf/', views.cv_pdf, name='cv_pdf'),
    path('cv/<int:cv_id>/send-email/', views.send_cv_email, name='send_cv_email'),
    path('settings/', views.settings_view, name='settings'),
    path('api/', include(router.urls)),
] 