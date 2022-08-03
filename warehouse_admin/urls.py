from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('packages/', views.package_list),
    path('packages/<str:id>', views.package_details),
    path('inspections/', views.inspection_list),
    path('inspections/<str:id>', views.inspection_details),
    path('package_inspections/', views.package_inspection_list),
    path('package_inspections/<str:id>', views.package_inspection_details),
]

urlpatterns = format_suffix_patterns(urlpatterns)