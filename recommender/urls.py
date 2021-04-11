from django.urls import path

from recommender.views import RecommenderView, RecommenderThankYouView


app_name = "recommender"

urlpatterns = [
    path('', RecommenderView.as_view(), name="recommender"),
    path('thank-you/', RecommenderThankYouView.as_view(), name="thank_you"),
]

