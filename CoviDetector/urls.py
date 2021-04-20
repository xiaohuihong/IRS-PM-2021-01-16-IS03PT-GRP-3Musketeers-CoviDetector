"""CoviDetector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from recommender.views import RecommenderView, RecommenderThankYouView, RecommenderWelcomeView,RecommenderPositiveView,RecommenderNegativeView, RecommenderAboutView


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', RedirectView.as_view(url=reverse_lazy('recommender:recommender'))),
    path('', RedirectView.as_view(url=reverse_lazy('recommender:welcome'))),
    path('thank_you/', RecommenderThankYouView.as_view(), name="thank_you"),
    path('positive/', RecommenderPositiveView.as_view(), name="positive"),
    path('negative/', RecommenderNegativeView.as_view(), name="negative"),
    path('about/', RecommenderAboutView.as_view(), name="about"),
    path('recommender/', include('recommender.urls', namespace='recommender'))
]

urlpatterns += staticfiles_urlpatterns()