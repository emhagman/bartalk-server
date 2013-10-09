from tools.database import Database
import re
import hashlib
from sqlalchemy.exc import SQLAlchemyError
from django.views.decorators.csrf import csrf_exempt
from dateutil.parser import *
from django.http import HttpResponse
import json

@csrf_exempt
def list(request):
    return HttpResponse(json.loads([{"name": "Kelly's Tap House", "address": "Heaven"}]), content_type="application/json")