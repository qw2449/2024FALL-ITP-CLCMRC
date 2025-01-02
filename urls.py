from django.conf.urls import include
from django.urls import path, re_path
from django.contrib import admin
from TextToArt import views
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.text_to_art_home, name='text_to_art_home'),  # Home page
    path('search/', views.text_to_art_search, name='text_to_art_search'),  # Search functionality
    path('select/<int:image_id>/', views.select_image, name='select_image'),  # Image selection
    path('image/<int:image_id>/', views.text_to_art_image_page, name='text_to_art_image_page'),
]
