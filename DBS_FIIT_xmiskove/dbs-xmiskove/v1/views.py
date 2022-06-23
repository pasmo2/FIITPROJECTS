from pickletools import string1
from textwrap import indent
from xmlrpc.client import ProtocolError
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from dotenv import load_dotenv
import os
import psycopg2
import json

# Create your views here.

load_dotenv()


conn = psycopg2.connect(
     host=os.getenv("DBHOST"),
     port=os.getenv("DBPORT"),
     database=os.getenv("DBNAME"),
     user=os.getenv("DBUSER"),
     password=os.getenv("DBPASS"),
)



cursor1 = conn.cursor()
cursor1.execute(
    "SELECT VERSION();"
)
output1 = cursor1.fetchone()

cursor2 = conn.cursor()
cursor2.execute(
    "SELECT pg_database_size('dota2')/1024/1024 as dota2_db_size;"
)
output2 = cursor2.fetchone()


def func1(request):

    str1=output1[0]
    str2=output2[0]

    dict = {"pgsql":{"version": str1, "dota2_db_size": str2}}
    return JsonResponse(dict,json_dumps_params={'indent': 1})


cursor1.close()    
cursor2.close()
conn.close()















