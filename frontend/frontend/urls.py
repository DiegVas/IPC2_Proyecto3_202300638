
from django.contrib import admin
from django.urls import path
from mainPage.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home , name='home'),
    path('upload/', upload_xml, name='upload_xml'),
    path('query/', query_data, name='query_data'),
    path('date-summary/', date_summary, name='date_summary'),
    path('range-summary/', range_summary, name='range_summary'),
    path('generate-pdf/', generate_pdf, name='generate_pdf'),
    path('test-message/', test_message, name='test_message'),
]
