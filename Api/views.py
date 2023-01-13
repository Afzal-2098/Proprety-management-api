# import modules for Function Based Api views
from rest_framework.decorators import api_view
from .models import PropertyDetail
from .serializers import PropertyDetailSerializer
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework import status
from django.http import HttpResponseRedirect


@api_view(["GET"])
def FatchPropertyDetails(request):
    if request.method == "GET":
        city_data = request.data.get("city_name")
        if city_data is not None:
            prop_dtl = PropertyDetail.objects.filter(city=city_data)
            get_serializer = PropertyDetailSerializer(prop_dtl, many=True)
            return Response(get_serializer.data)

        prop_dtl = PropertyDetail.objects.all()
        get_serializer = PropertyDetailSerializer(prop_dtl, many=True)
        return Response(get_serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def CreateNewProperty(request):
    if request.method == "POST":
        post_serializer = PropertyDetailSerializer(data = request.data)
        print(post_serializer)
        if post_serializer.is_valid():
            print(post_serializer)
            post_serializer.save()
            return HttpResponseRedirect(redirect_to="http://127.0.0.1:8000/fetch_property_details/")
            # return redirect("fetchproperty")
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def UpdatePropertyDetails(request):
    if request.method == "PUT":
        id = request.data.get("property_id")
        if id is not None:
            prop_dtl = PropertyDetail.objects.get(id=id)
            put_serializer = PropertyDetailSerializer(prop_dtl, data=request.data)
            if put_serializer.is_valid():
                put_serializer.save()
                return HttpResponseRedirect(redirect_to="http://127.0.0.1:8000/fetch_property_details/")
            return Response(put_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def FindCitiesByState(request):
    if request.method == "GET":
        state_id = request.data.get("state_id")
        state_name = request.data.get("state")
        print(state_id)
        print(state_name)
        # if state_id is not None:
        #     prop_dtl = PropertyDetail.objects.filter(state_id=state_id)
        #     print(type(prop_dtl))
        #     print(prop_dtl)
        #     # find_serializer = PropertyDetailSerializer(prop_dtl, many=True)
        #     # return Response(find_serializer.data)

        if state_name is not None:
            prop_dtl = PropertyDetail.objects.filter(state=state_name)
            find_serializer = PropertyDetailSerializer(prop_dtl, many=True)
            return Response(find_serializer.data)

        else:
            return Response({"msg":"please provide state id or state name."})
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def FindSimilarProperties(request):
    if request.method == "GET":
        prop_id = request.data.get("property_id")
        prop_dtl = PropertyDetail.objects.get(id=prop_id)
        similar_prop = PropertyDetail.objects.filter(city=prop_dtl.city)
        sim_serializer = PropertyDetailSerializer(similar_prop, many=True)
        return Response(sim_serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)