from django.urls import path
from django.conf.urls import url
from recommender.views import RecommenderView, RecommenderThankYouView
from recommender.views import ChatBotAppView


app_name = "recommender"

urlpatterns = [
    path('', RecommenderView.as_view(), name="recommender"),
    path('thank-you/', RecommenderThankYouView.as_view(), name="thank_you"),
]

