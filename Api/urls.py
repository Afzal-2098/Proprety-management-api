from django.urls import path
from . import views

urlpatterns = [
    path("fetch_property_details/", views.FatchPropertyDetails, name="fetchproperty"),
    path("create_new_property/", views.CreateNewProperty, name="createproperty"),
    path("update_property_details/", views.UpdatePropertyDetails, name="updateproperty"),
    path("find_cities_by_state/", views.FindCitiesByState, name="findcities"),
    path("find_similar_properties/", views.FindSimilarProperties, name="similarpropertis"),
]
