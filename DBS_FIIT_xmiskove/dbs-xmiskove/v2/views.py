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

#load_dotenv()




def patch3s(request):
    try:
        conn = psycopg2.connect(
        host=os.getenv("DBHOST"),
        port=os.getenv("DBPORT"),
        database=os.getenv("DBNAME"),
        user=os.getenv("DBUSER"),
        password=os.getenv("DBPASS"),
        )
        cursor1 = conn.cursor()
        cursor1.execute(
            """
            SELECT p1.name as patch_version,
            EXTRACT(EPOCH FROM p1.release_date) as patch_start_date,
            EXTRACT(EPOCH FROM p2.release_date) as patch_end_date,
            m.id as match_id,
            ROUND((CAST(m.duration AS FLOAT)/60)::numeric,2) as match_duration
            FROM patches as p1
            LEFT JOIN patches as p2 ON p2.id-p1.id=1
            LEFT JOIN(
            SELECT m.id,
            m.start_time,
            m.duration
            FROM matches as m
            ) as m ON m.start_time>=EXTRACT(EPOCH FROM p1.release_date)
            AND m.start_time<COALESCE(EXTRACT(EPOCH FROM p2.release_date),EXTRACT(EPOCH FROM timestamp '2022-03-15'))
            ORDER BY p1.name,m.id;
            """
        )
        output = cursor1.fetchall()
        patches = []
        i=0
        j=0
        while(i<len(output)):
            patches.append({})
            patches[j]["patch_version"]=output[i][0]
            patches[j]["patch_start_date"]=int(output[i][1])
            if(isinstance(output[i][2],float)):
                patches[j]["patch_end_date"]=int(output[i][2])
            else:
                patches[j]["patch_end_date"]=output[i][2]
            if(patches[j]["patch_end_date"]==1647302400):
                patches[j]["patch_end_date"]="null"
            patches[j]["matches"]=[]
            y=j
            temp=0
            if(isinstance(output[i][3],int)==False):
                j+=1
                i+=1
                continue
            while(i+1<len(output) and output[i+1][0]==output[i][0]):
                patches[y]["matches"].append({})
                patches[y]["matches"][temp]["match_id"]=output[i][3]
                patches[y]["matches"][temp]["duration"]=float(output[i][4])
                i+=1
                temp+=1
            patches[y]["matches"].append({})
            patches[y]["matches"][temp]["match_id"]=output[i][3]
            patches[y]["matches"][temp]["duration"]=float(output[i][4])
            temp+=1
            i+=1
            j+=1

        
        dict= {"patches":patches}

        JsonResponse.status_code=200
        return JsonResponse(dict,content_type = "application/json",json_dumps_params={'indent': 1})
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor1.close()
            conn.close()
            print("it go byebye")

def funct1on(request, player_id):
    try:
        conn = psycopg2.connect(
        host=os.getenv("DBHOST"),
        port=os.getenv("DBPORT"),
        database=os.getenv("DBNAME"),
        user=os.getenv("DBUSER"),
        password=os.getenv("DBPASS"),
        )
        cursor1 = conn.cursor()
        cursor1.execute(
            """
            SELECT 
            p.id, 
            COALESCE(p.nick,'unknown') as player_nick,
            m.id as match_id,
            h.localized_name as hero_localized_name,
            ROUND((CAST(m.duration AS FLOAT)/60)::numeric,2) as match_duration_minutes,
            (COALESCE(mpd.xp_hero,0)+COALESCE(mpd.xp_creep,0)+COALESCE(mpd.xp_other,0)+COALESCE(mpd.xp_roshan,0)) as experience_gained,
            mpd.level as level_gained,
            CASE 
            WHEN (mpd.player_slot>=0 AND mpd.player_slot<=4 AND m.radiant_win=True) THEN True
            WHEN (mpd.player_slot>=128 AND mpd.player_slot<=132 AND m.radiant_win=False) THEN True
            ELSE False 
            END as winner
            FROM players as p
            JOIN matches_players_details as mpd ON p.id=mpd.player_id
            JOIN matches as m ON m.id=mpd.match_id
            JOIN heroes as h ON h.id=mpd.hero_id
            WHERE p.id={}
            ORDER BY m.id;
            """.format(player_id)
        )
        output = cursor1.fetchall()
        player_id=output[0][0]
        player_nick=output[0][1]
        matches = []
        for i in range(0,len(output)):
            matches.append({})
            matches[i]["match_id"]=output[i][2]
            matches[i]["hero_localized_name"]=output[i][3]
            matches[i]["match_duration_minutes"]=float(output[i][4])
            matches[i]["experiences_gained"]=output[i][5]
            matches[i]["level_gained"]=output[i][6]
            matches[i]["winner"]=output[i][7]

        dict= {"id":player_id,"player_nick":player_nick,"matches":matches}


        JsonResponse.status_code=200
        return JsonResponse(dict,content_type = "application/json",json_dumps_params={'indent': 1})
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor1.close()
            conn.close()
            print("it go byebye")

def funct2on(request,player_id):
    try:
        conn = psycopg2.connect(
        host=os.getenv("DBHOST"),
        port=os.getenv("DBPORT"),
        database=os.getenv("DBNAME"),
        user=os.getenv("DBUSER"),
        password=os.getenv("DBPASS"),
        )
        cursor1 = conn.cursor()
        cursor1.execute(
            """
            SELECT
            p.id, 
            COALESCE(p.nick,'unknown') as player_nick,
            m.id as match_id,
            h.localized_name as hero_localized_name,
            COALESCE(go.subtype,'NO_ACTION') as hero_action,
            COUNT(*) as count
            FROM players as p
            JOIN matches_players_details as mpd ON p.id=mpd.player_id
            JOIN matches as m ON m.id=mpd.match_id
            JOIN heroes as h ON h.id=mpd.hero_id
            LEFT JOIN game_objectives as go ON go.match_player_detail_id_1=mpd.id
            WHERE p.id={}
            GROUP BY p.id,m.id,hero_localized_name,hero_action
            ORDER BY m.id ASC;
            """.format(player_id)
        )
        output = cursor1.fetchall()
        player_id=output[0][0]
        player_nick=output[0][1]
        matches = []
        i=0
        j=0
        while(i<len(output)):
            matches.append({})
            matches[j]["match_id"]=output[i][2]
            matches[j]["hero_localized_name"]=output[i][3]
            matches[j]["actions"]=[]
            y=j
            temp=0
            while(i+1<len(output) and output[i+1][2]==output[i][2]):
                matches[y]["actions"].append({})
                matches[y]["actions"][temp]["hero_action"]=output[i][4]
                matches[y]["actions"][temp]["count"]=output[i][5]
                i+=1
                temp+=1
            matches[y]["actions"].append({})
            matches[y]["actions"][temp]["hero_action"]=output[i][4]
            matches[y]["actions"][temp]["count"]=output[i][5]
            temp+=1
            i+=1
            j+=1

        
        dict= {"id":player_id,"player_nick":player_nick,"matches":matches}

        JsonResponse.status_code=200
        return JsonResponse(dict,content_type = "application/json",json_dumps_params={'indent': 1})
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor1.close()
            conn.close()
            print("it go byebye")


def funct3on(request,player_id):
    try:
        conn = psycopg2.connect(
        host=os.getenv("DBHOST"),
        port=os.getenv("DBPORT"),
        database=os.getenv("DBNAME"),
        user=os.getenv("DBUSER"),
        password=os.getenv("DBPASS"),
        )
        cursor1 = conn.cursor()
        cursor1.execute(
            """
            SELECT 
            p.id, 
            COALESCE(p.nick,'unknown') as player_nick,
            m.id as match_id,
            h.localized_name as hero_localized_name,
            a.name as ability_name,
            COUNT(a.name) as count,
            MAX(aup.level) as upgrade_level
            FROM players as p
            JOIN matches_players_details as mpd ON p.id=mpd.player_id
            JOIN matches as m ON m.id=mpd.match_id
            JOIN heroes as h ON h.id=mpd.hero_id
            JOIN ability_upgrades as aup ON mpd.id=aup.match_player_detail_id
            JOIN abilities as a ON aup.ability_id=a.id
            WHERE p.id={}
            GROUP BY p.id,h.localized_name,m.id,a.name,p.nick
            ORDER BY m.id,a.name ASC;
            """.format(player_id)
        )
        output = cursor1.fetchall()
        player_id=output[0][0]
        player_nick=output[0][1]
        matches = []
        i=0
        j=0
        while(i<len(output)):
            matches.append({})
            matches[j]["match_id"]=output[i][2]
            matches[j]["hero_localized_name"]=output[i][3]
            matches[j]["abilities"]=[]
            y=j
            temp=0
            while(i+1<len(output) and output[i+1][2]==output[i][2]):
                matches[y]["abilities"].append({})
                matches[y]["abilities"][temp]["ability_name"]=output[i][4]
                matches[y]["abilities"][temp]["count"]=output[i][5]
                matches[y]["abilities"][temp]["upgrade_level"]=output[i][6]
                i+=1
                temp+=1
            matches[y]["abilities"].append({})
            matches[y]["abilities"][temp]["ability_name"]=output[i][4]
            matches[y]["abilities"][temp]["count"]=output[i][5]
            matches[y]["abilities"][temp]["upgrade_level"]=output[i][6]
            temp+=1
            i+=1
            j+=1
            
    
        
        dict= {"id":player_id,"player_nick":player_nick,"matches":matches}

        JsonResponse.status_code=200
        return JsonResponse(dict,content_type = "application/json",json_dumps_params={'indent': 1})
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor1.close()
            conn.close()
            print("it go byebye")