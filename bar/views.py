from tools.database import Database
import re
import hashlib
from sqlalchemy.exc import SQLAlchemyError
from django.views.decorators.csrf import csrf_exempt
from dateutil.parser import *
from django.http import HttpResponse
import simplejson as json

@csrf_exempt
def list(request):
    return HttpResponse(json.dumps([{"name": "Kelly's Tap House", "address": "Heaven", "image": "http://drunkdevs.com/images/test.png"}]), content_type="application/json")