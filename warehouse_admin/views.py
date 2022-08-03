from bson.objectid import ObjectId
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import mongo
import re

db = mongo.mongo_handle.db
mongo_utils = mongo.mongo_utils

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the warehouse_admin index.")

@api_view(["GET"])
def package_list(request, format=None):
    if request.method == "GET":
        package_name = request.GET.get('name', '')

        query_dict = {}
        if len(package_name) > 0:
            rgx = re.compile('.*{}.*'.format(package_name))
            query_dict["name"] = rgx

        packages = mongo_utils.find(db.get_collection("packages"), query_dict, sort=["name", 0])
        response = {"packages": packages}
        return JsonResponse(response)


@api_view(["GET"])
def package_details(request, id, format=None):
    if request.method == "GET":
        package = mongo_utils.find_one_by_id(db.get_collection("packages"), id)
        if len(package) == 0:
            return HttpResponseNotFound()
        return JsonResponse(package)


@api_view(["GET"])
def inspection_list(request, format=None):
    if request.method == "GET":
        inspections = mongo_utils.find(db.get_collection("inspections"), {}, sort=["time", 1])
        response = {"inspections": inspections}
        return JsonResponse(response)


@api_view(["GET"])
def inspection_details(request, id, format=None):
    if request.method == "GET":
        inspection = mongo_utils.find_one_by_id(db.get_collection("inspections"), id)
        if len(inspection) == 0:
            return HttpResponseNotFound()
        return JsonResponse(inspection)


@api_view(["GET"])
def package_inspection_list(request, format=None):
    if request.method == "GET":
        package_id = request.GET.get('package_id', '')
        inspection_id = request.GET.get('inspection_id', '')
        position = request.GET.get('position', '')
        status = request.GET.get('status', '')
        package_name = request.GET.get('package_name', '')

        query_dict = {}
        if len(package_id) > 0:
            query_dict["_package_id"] = ObjectId(package_id)
        if len(inspection_id) > 0:
            query_dict["_inspection_id"] = ObjectId(inspection_id)
        if len(position) > 0:
            query_dict["position"] = position
        if len(package_name) > 0:
            rgx = re.compile('.*{}.*'.format(package_name))
            query_dict["name"] = rgx
        if len(status) > 0:
            status = status.lower()
            if status == "true":
                query_dict["status"] = True
            elif status == "false":
                query_dict["status"] = False

        print(query_dict)
        package_inspections = mongo_utils.find(db.get_collection("packageinspections"), query_dict, sort=["timestamp", 1])
        response = {"packageInspections": package_inspections}
        return JsonResponse(response)


@api_view(["GET"])
def package_inspection_details(request, id, format=None):
    if request.method == "GET":
        package_inspection = mongo_utils.find_one_by_id(db.get_collection("packageinspections"), id)
        if len(package_inspection) == 0:
            return HttpResponseNotFound()
        return JsonResponse(package_inspection)
