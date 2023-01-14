# import modules for Function Based Api views
from rest_framework.decorators import api_view
from .models import PropertyDetail
from .serializers import PropertyDetailSerializer
from rest_framework.response import Response
# from django.shortcuts import redirect
from rest_framework import status
from django.http import HttpResponseRedirect


# This view returns property details.
'''If city is mentioned then it filter properties for these cities otherwise fatches all the data''' 
@api_view(["GET"])
def FatchPropertyDetails(request):
    if request.method == "GET":
        city_data = request.data.get("city")
        if city_data is not None:
            prop_dtl = PropertyDetail.objects.filter(city=city_data)
            serializer = PropertyDetailSerializer(prop_dtl, many=True)
            return Response(serializer.data)

        prop_dtl = PropertyDetail.objects.all()
        serializer = PropertyDetailSerializer(prop_dtl, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


'''this view returns all the property details 
after creation of new property.'''
@api_view(["POST"])
def CreateNewProperty(request):
    if request.method == "POST":
        serializer = PropertyDetailSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(redirect_to="http://127.0.0.1:8000/fetch_property_details/")
            # return redirect("fetchproperty")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''This view updates the existing details and returns new updated list. we need to provide every field for update.'''
'''we also can partially update data for that we need following changes in UpdatePropertyDetails view
1 ---> @api_view(["PATCH"])   put this decorator in view
2 ---> partial=True    add this in PropertyDetailSerializer'''
@api_view(["PUT"])
def UpdatePropertyDetails(request):
    if request.method == "PUT":
        id = request.data.get("id")
        if id is not None:
            prop_dtl = PropertyDetail.objects.get(id=id)
            serializer = PropertyDetailSerializer(prop_dtl, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponseRedirect(redirect_to="http://127.0.0.1:8000/fetch_property_details/")
        res = {"id":["This field is required."]}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


'''This view returns the list of all the cities those are belongs to
the provided state name'''
@api_view(["GET"])
def FindCitiesByState(request):
    if request.method == "GET":
        state_name = request.data.get("state")
        if state_name is not None:
            cities_list = []
            prop_dtl = PropertyDetail.objects.filter(state=state_name)
            serializer = PropertyDetailSerializer(prop_dtl, many=True)
            for dict in serializer.data:
                cities_list.append(dict["city"])
            res = {"cities":cities_list}
            return Response(res, status=status.HTTP_404_NOT_FOUND)
        res = {"state":"Please enter state name"}
        return Response(res, status=status.HTTP_404_NOT_FOUND)


'''This view returns the list of properties those are belongs to the same cities
with mentioned property'''
@api_view(["GET"])
def FindSimilarProperties(request):
    if request.method == "GET":
        prop_id = request.data.get("id")
        if prop_id is not None:
            prop_dtl = PropertyDetail.objects.get(id=prop_id)
            similar_prop = PropertyDetail.objects.filter(city=prop_dtl.city)
            serializer = PropertyDetailSerializer(similar_prop, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        res = {"msg":["Please mention property id for getting similar results."]}
        return Response(res)