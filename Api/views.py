# import modules for Function Based Api views
from rest_framework.decorators import api_view
from .models import PropertyDetail
from .serializers import PropertyDetailSerializer
from rest_framework.response import Response
# from django.shortcuts import redirect
from rest_framework import status
from django.http import HttpResponseRedirect
from django.http import JsonResponse


@api_view(["GET"])
def FatchPropertyDetails(request):
    if request.method == "GET":
        city_data = request.data.get("city")
        if city_data is not None:
            prop_dtl = PropertyDetail.objects.filter(city=city_data)
            serializer = PropertyDetailSerializer(prop_dtl, many=True)
            print(serializer)
            return Response(serializer.data)

        prop_dtl = PropertyDetail.objects.all()
        serializer = PropertyDetailSerializer(prop_dtl, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def CreateNewProperty(request):
    if request.method == "POST":
        state = request.data.get("state")
        serializer = PropertyDetailSerializer(data = request.data)
        if serializer.is_valid():
            # serializer.save()
            return HttpResponseRedirect(redirect_to="http://127.0.0.1:8000/fetch_property_details/")
            # return redirect("fetchproperty")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def UpdatePropertyDetails(request):
    if request.method == "PUT":
        id = request.data.get("id")
        if id is not None:
            prop_dtl = PropertyDetail.objects.get(id=id)
            serializer = PropertyDetailSerializer(prop_dtl, data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return HttpResponseRedirect(redirect_to="http://127.0.0.1:8000/fetch_property_details/")
        res = {"id":["This field is required."]}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


STATE_IDS = (
    ("an", "andaman and nicobar islands"),
    ("ap", "andhra pradesh"),
    ("ar", "arunachal pradesh"),
    ("uk", "uttarakhand"),
)

@api_view(["GET"])
def FindCitiesByState(request):
    if request.method == "GET":
        state_id = request.data.get("state_id")
        state_name = request.data.get("state")
        print(state_id)
        print(state_name)
        cities = []
        for tup in STATE_IDS:
            if state_id == tup[0]:
                state_name = tup[1]
                prop_dtl = list(PropertyDetail.objects.filter(state_id=state_name))
                for prop in prop_dtl:
                    cities.append(prop.city)
                break
        # serializer = PropertyDetailSerializer(prop_dtl, many=True)
        return JsonResponse(cities, safe=False)

        # if state_name is not None:
        #     prop_dtl = PropertyDetail.objects.filter(state=state_name)
        #     find_serializer = PropertyDetailSerializer(prop_dtl, many=True)
        #     return Response(find_serializer.data)

        # else:
        # #     return Response({"msg":"please provide state id or state name."})


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