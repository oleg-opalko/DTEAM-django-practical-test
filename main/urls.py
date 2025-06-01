from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cv/<int:cv_id>/', views.cv_detail, name='cv_detail'),
    path('cv/<int:cv_id>/pdf/', views.render_pdf_view, name='cv_pdf'),
] 