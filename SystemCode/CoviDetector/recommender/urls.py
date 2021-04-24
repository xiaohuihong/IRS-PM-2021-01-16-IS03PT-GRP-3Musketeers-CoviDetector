from django.urls import path

from recommender.views import RecommenderView, RecommenderThankYouView, RecommenderWelcomeView,RecommenderPositiveView,RecommenderNegativeView,RecommenderAboutView


app_name = "recommender"

urlpatterns = [
    #path('', RecommenderView.as_view(), name="recommender"),
    path('', RecommenderWelcomeView.as_view(), name="welcome"),
    path('thank_you/', RecommenderThankYouView.as_view(), name="thank_you"),
    path('positive/', RecommenderPositiveView.as_view(), name="positive"),
    path('negative/', RecommenderNegativeView.as_view(), name="negative"),
    path('about/', RecommenderAboutView.as_view(), name="about"),
    path('questionnaire/', RecommenderView.as_view(), name="recommender")
]

