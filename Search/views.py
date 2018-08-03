from astroquery.utils import TableList
from django.http import HttpResponse
from django.template import loader
from query.find_astrosource import FindAstroSource
from Search.models import Catalog
from Search.serializers import CatalogSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from frastro import SAMPManager
from frastro import LiverPoolObsservation
import json


import numpy
from django.contrib.staticfiles.templatetags.staticfiles import static




# Create your views here.



@api_view(['GET','POST'])
@renderer_classes((JSONRenderer,))
def index(request):


    context = {}
    result = FindAstroSource()
    radius = 1
    if request.POST.__contains__('coordinates'):
        coordinates = request.POST['coordinates']
        #print(request.POST['coordinates'])


    elif "coordinates" in request.data:
        coordinates = request.data["coordinates"]
    elif "coordinates" in request.query_params:
        coordinates = request.query_params["coordinates"]
    else:
        template = loader.get_template('Search/index.html')
        return HttpResponse(template.render(context, request))


    if request.POST.__contains__('radius'):
        radius = request.POST['radius']

    elif "radius" in request.data:
        radius = request.data["radius"]

    r = result.searchSources(coordinates=coordinates,radius=radius)

    return Response(r)


@api_view(['GET','POST'])
@renderer_classes((JSONRenderer,))
def sourceList(request):
    finder = FindAstroSource()
    sources=finder.getAllSource()
    return Response(sources)

@api_view(['GET','POST'])
@renderer_classes((JSONRenderer,))
def sampList(request):
    sampMg = SAMPManager()
    list = sampMg.getRegisteredClients()
    sampMg.disconnect()
    return Response(list)


@api_view(['GET','POST'])
@renderer_classes((JSONRenderer,))
def sampMessage(request):
    client=coordinates=""
    if request.POST.__contains__('coordinates'):
        coordinates = request.POST['coordinates']
        client = request.POST['client']
        localfiles = request.data["local"]
    elif "coordinates" in request.data:
        coordinates = request.data["coordinates"]
        client = request.data["client"]
        localfiles = request.data["local"]

    if coordinates != "":
        fs = FindAstroSource()
        fs.sendSourceToSAMP(source=coordinates,client=client)
        status={"status":"send"}
    else:
        status = {"status": "error"}

    return Response(status)

@api_view(['GET','POST'])
@renderer_classes((JSONRenderer,))
def observationList(request):
    lvSn = LiverPoolObsservation()
    list=lvSn.getObservations()

    return Response(list)


@api_view(['GET','POST'])
@renderer_classes((JSONRenderer,))
def sampSEDMessage(request):
    client=coordinates=""
    if request.POST.__contains__('coordinates'):
        coordinates = request.POST['coordinates']
        client = request.POST['client']
    elif "coordinates" in request.data:
        coordinates = request.data["coordinates"]
        client = request.data["client"]

    if coordinates != "":
        fs = FindAstroSource()
        fs.sendSEDToSAMP(source=coordinates,client=client)
        status={"status":"send"}
    else:
        status = {"status": "error"}

    return Response(status)

