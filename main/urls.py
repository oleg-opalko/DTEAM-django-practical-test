from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cvs', views.CVViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('cv/<int:cv_id>/', views.cv_detail, name='cv_detail'),
    path('cv/<int:cv_id>/pdf/', views.render_pdf_view, name='cv_pdf'),
    path('api/', include(router.urls)),
] 