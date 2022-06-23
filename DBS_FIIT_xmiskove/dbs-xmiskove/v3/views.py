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

#load_dotenv


def function1(request, match_id):
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
                        subq.match_id as match_id,
                        subq.hero_id as hero_id,
                        subq.hero_name as hero_name,
                        subq.item_id as item_id,
                        subq.item_name as item_name,
                        subq.itemcount as itemcount
                        FROM
                        (SELECT
                        m.id as match_id,
                        h.id as hero_id,
                        h.localized_name as hero_name,
                        i.id as item_id,
                        i.name as item_name,
                        --m.duration as dur,
                        COUNT(i.name) as itemcount,
                        ROW_NUMBER() OVER (PARTITION BY h.localized_name ORDER BY COUNT(i.name) DESC, i.name) as rownum
                        FROM matches as m
                        JOIN matches_players_details as mpd ON 
                        m.id=mpd.match_id
                        AND ((m.radiant_win=true AND mpd.player_slot>=0 AND mpd.player_slot<=4)
                        OR (m.radiant_win=false AND mpd.player_slot>=128 AND mpd.player_slot<=132))
                        JOIN heroes as h ON
                        mpd.hero_id=h.id
                        JOIN purchase_logs as pl ON 
                        pl.match_player_detail_id=mpd.id
                        JOIN items as i ON
                        i.id=pl.item_id
                        WHERE m.id={}
                        GROUP BY m.id, h.localized_name, i.name, h.id, i.id
                        ORDER BY h.id ASC, itemcount DESC, item_name) as subq
                        WHERE subq.rownum<=5 AND subq.rownum>=0
                        """.format(match_id)
                )
                output = cursor1.fetchall()
                match_id=output[0][0]

                heroes = []
                i=0
                x=0
                while(i<len(output)):
                        heroes.append({})
                        heroes[x]["id"]=output[i][1]
                        heroes[x]["name"]=output[i][2]
                        heroes[x]["top_purchases"]=[]
                        k=0
                        for j in range(i,len(output)):
                                heroes[x]["top_purchases"].append({})
                                heroes[x]["top_purchases"][k]["id"]=output[j][3]
                                heroes[x]["top_purchases"][k]["name"]=output[j][4]
                                heroes[x]["top_purchases"][k]["count"]=output[j][5]
                                k+=1
                                if (j+1==len(output) or output[j+1][2]!=output[j][2]):
                                        i=j
                                        break
                        x+=1
                        i+=1
                        if(i==len(output)):
                                break

                dict= {"id":match_id,"heroes":heroes}


                JsonResponse.status_code=200
                return JsonResponse(dict,content_type = "application/json",json_dumps_params={'indent': 1})
        except (Exception, Error) as error:
                print("Error while connecting to PostgreSQL", error)
        finally:
                if conn:
                        cursor1.close()
                        conn.close()
                        print("connection minus")

def function2(request, ability_id):
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
            realvsetko.ability_id,
            realvsetko.ability_name,
            realvsetko.hero_id,
            realvsetko.hero_name,
            realvsetko.bucketwin,
            realvsetko.countwin,
            realvsetko.bucketloss,
            realvsetko.countloss
            FROM
            (
            SELECT
            vsetko.ability_id as ability_id,
            vsetko.ability_name as ability_name,
            vsetko.hero_id as hero_id,
            vsetko.hero_name as hero_name,
            GREATEST(vsetko."count0",vsetko."count1",vsetko."count2",vsetko."count3",
                    vsetko."count4",vsetko."count5",vsetko."count6",vsetko."count7",
                    vsetko."count8",vsetko."count9",vsetko."count10") as countwin,
            CASE
            WHEN vsetko."count0"=GREATEST(vsetko."count0",vsetko."count1",vsetko."count2",vsetko."count3",
                    vsetko."count4",vsetko."count5",vsetko."count6",vsetko."count7",
                    vsetko."count8",vsetko."count9",vsetko."count10") THEN '0-9'
            WHEN vsetko."count1"=GREATEST(vsetko."count0",vsetko."count1",vsetko."count2",vsetko."count3",
                    vsetko."count4",vsetko."count5",vsetko."count6",vsetko."count7",
                    vsetko."count8",vsetko."count9",vsetko."count10") THEN '10-19'
            WHEN vsetko."count2"=GREATEST(vsetko."count0",vsetko."count1",vsetko."count2",vsetko."count3",
                    vsetko."count4",vsetko."count5",vsetko."count6",vsetko."count7",
                    vsetko."count8",vsetko."count9",vsetko."count10") THEN '20-29'
            WHEN vsetko."count3"=GREATEST(vsetko."count0",vsetko."count1",vsetko."count2",vsetko."count3",
                    vsetko."count4",vsetko."count5",vsetko."count6",vsetko."count7",
                    vsetko."count8",vsetko."count9",vsetko."count10") THEN '30-39'
            WHEN vsetko."count4"=GREATEST(vsetko."count0",vsetko."count1",vsetko."count2",vsetko."count3",
                    vsetko."count4",vsetko."count5",vsetko."count6",vsetko."count7",
                    vsetko."count8",vsetko."count9",vsetko."count10") THEN '40-49'
            WHEN vsetko."count5"=GREATEST(vsetko."count0",vsetko."count1",vsetko."count2",vsetko."count3",
                    vsetko."count4",vsetko."count5",vsetko."count6",vsetko."count7",
                    vsetko."count8",vsetko."count9",vsetko."count10") THEN '50-59'
            WHEN vsetko."count6"=GREATEST(vsetko."count0",vsetko."count1",vsetko."count2",vsetko."count3",
                    vsetko."count4",vsetko."count5",vsetko."count6",vsetko."count7",
                    vsetko."count8",vsetko."count9",vsetko."count10") THEN '60-69'
            WHEN vsetko."count7"=GREATEST(vsetko."count0",vsetko."count1",vsetko."count2",vsetko."count3",
                    vsetko."count4",vsetko."count5",vsetko."count6",vsetko."count7",
                    vsetko."count8",vsetko."count9",vsetko."count10") THEN '70-79'
            WHEN vsetko."count8"=GREATEST(vsetko."count0",vsetko."count1",vsetko."count2",vsetko."count3",
                    vsetko."count4",vsetko."count5",vsetko."count6",vsetko."count7",
                    vsetko."count8",vsetko."count9",vsetko."count10") THEN '80-89'
            WHEN vsetko."count9"=GREATEST(vsetko."count0",vsetko."count1",vsetko."count2",vsetko."count3",
                    vsetko."count4",vsetko."count5",vsetko."count6",vsetko."count7",
                    vsetko."count8",vsetko."count9",vsetko."count10") THEN '90-99'
            ELSE '100-109'
            END as bucketwin,
            CASE
            WHEN vsetko."xcount0"=GREATEST(vsetko."xcount0",vsetko."xcount1",vsetko."xcount2",vsetko."xcount3",
                    vsetko."xcount4",vsetko."xcount5",vsetko."xcount6",vsetko."xcount7",
                    vsetko."xcount8",vsetko."xcount9",vsetko."xcount10") THEN '0-9'
            WHEN vsetko."xcount1"=GREATEST(vsetko."xcount0",vsetko."xcount1",vsetko."xcount2",vsetko."xcount3",
                    vsetko."xcount4",vsetko."xcount5",vsetko."xcount6",vsetko."xcount7",
                    vsetko."xcount8",vsetko."xcount9",vsetko."xcount10") THEN '10-19'
            WHEN vsetko."xcount2"=GREATEST(vsetko."xcount0",vsetko."xcount1",vsetko."xcount2",vsetko."xcount3",
                    vsetko."xcount4",vsetko."xcount5",vsetko."xcount6",vsetko."xcount7",
                    vsetko."xcount8",vsetko."xcount9",vsetko."xcount10") THEN '20-29'
            WHEN vsetko."xcount3"=GREATEST(vsetko."xcount0",vsetko."xcount1",vsetko."xcount2",vsetko."xcount3",
                    vsetko."xcount4",vsetko."xcount5",vsetko."xcount6",vsetko."xcount7",
                    vsetko."xcount8",vsetko."xcount9",vsetko."xcount10") THEN '30-39'
            WHEN vsetko."xcount4"=GREATEST(vsetko."xcount0",vsetko."xcount1",vsetko."xcount2",vsetko."xcount3",
                    vsetko."xcount4",vsetko."xcount5",vsetko."xcount6",vsetko."xcount7",
                    vsetko."xcount8",vsetko."xcount9",vsetko."xcount10") THEN '40-49'
            WHEN vsetko."xcount5"=GREATEST(vsetko."xcount0",vsetko."xcount1",vsetko."xcount2",vsetko."xcount3",
                    vsetko."xcount4",vsetko."xcount5",vsetko."xcount6",vsetko."xcount7",
                    vsetko."xcount8",vsetko."xcount9",vsetko."xcount10") THEN '50-59'
            WHEN vsetko."xcount6"=GREATEST(vsetko."xcount0",vsetko."xcount1",vsetko."xcount2",vsetko."xcount3",
                    vsetko."xcount4",vsetko."xcount5",vsetko."xcount6",vsetko."xcount7",
                    vsetko."xcount8",vsetko."xcount9",vsetko."xcount10") THEN '60-69'
            WHEN vsetko."xcount7"=GREATEST(vsetko."xcount0",vsetko."xcount1",vsetko."xcount2",vsetko."xcount3",
                    vsetko."xcount4",vsetko."xcount5",vsetko."xcount6",vsetko."xcount7",
                    vsetko."xcount8",vsetko."xcount9",vsetko."xcount10") THEN '70-79'
            WHEN vsetko."xcount8"=GREATEST(vsetko."xcount0",vsetko."xcount1",vsetko."xcount2",vsetko."xcount3",
                    vsetko."xcount4",vsetko."xcount5",vsetko."xcount6",vsetko."xcount7",
                    vsetko."xcount8",vsetko."xcount9",vsetko."xcount10") THEN '80-89'
            WHEN vsetko."xcount9"=GREATEST(vsetko."xcount0",vsetko."xcount1",vsetko."xcount2",vsetko."xcount3",
                    vsetko."xcount4",vsetko."xcount5",vsetko."xcount6",vsetko."xcount7",
                    vsetko."xcount8",vsetko."xcount9",vsetko."xcount10") THEN '90-99'
            ELSE '100-109'
            END as bucketloss,
            GREATEST(vsetko."xcount0",vsetko."xcount1",vsetko."xcount2",vsetko."xcount3",
                    vsetko."xcount4",vsetko."xcount5",vsetko."xcount6",vsetko."xcount7",
                    vsetko."xcount8",vsetko."xcount9",vsetko."xcount10") as countloss
            FROM
            (
            SELECT DISTINCT
            --m.id,
            a.id as ability_id,
            a.name as ability_name,
            h.id as hero_id,
            COUNT(CASE WHEN subq1."0-9"=1 THEN subq1.sub_match_id END) as "count0",
            COUNT(CASE WHEN subq1."10-19"=1 THEN subq1.sub_match_id END) as "count1",
            COUNT(CASE WHEN subq1."20-29"=1 THEN subq1.sub_match_id END) as "count2",
            COUNT(CASE WHEN subq1."30-39"=1 THEN subq1.sub_match_id END) as "count3",
            COUNT(CASE WHEN subq1."40-49"=1 THEN subq1.sub_match_id END) as "count4",
            COUNT(CASE WHEN subq1."50-59"=1 THEN subq1.sub_match_id END) as "count5",
            COUNT(CASE WHEN subq1."60-69"=1 THEN subq1.sub_match_id END) as "count6",
            COUNT(CASE WHEN subq1."70-79"=1 THEN subq1.sub_match_id END) as "count7",
            COUNT(CASE WHEN subq1."80-89"=1 THEN subq1.sub_match_id END) as "count8",
            COUNT(CASE WHEN subq1."90-99"=1 THEN subq1.sub_match_id END) as "count9",
            COUNT(CASE WHEN subq1."100-109"=1 THEN subq1.sub_match_id END) as "count10",
            COUNT(CASE WHEN subq1."0-9"=2 THEN subq1.sub_match_id END) as "xcount0",
            COUNT(CASE WHEN subq1."10-19"=2 THEN subq1.sub_match_id END) as "xcount1",
            COUNT(CASE WHEN subq1."20-29"=2 THEN subq1.sub_match_id END) as "xcount2",
            COUNT(CASE WHEN subq1."30-39"=2 THEN subq1.sub_match_id END) as "xcount3",
            COUNT(CASE WHEN subq1."40-49"=2 THEN subq1.sub_match_id END) as "xcount4",
            COUNT(CASE WHEN subq1."50-59"=2 THEN subq1.sub_match_id END) as "xcount5",
            COUNT(CASE WHEN subq1."60-69"=2 THEN subq1.sub_match_id END) as "xcount6",
            COUNT(CASE WHEN subq1."70-79"=2 THEN subq1.sub_match_id END) as "xcount7",
            COUNT(CASE WHEN subq1."80-89"=2 THEN subq1.sub_match_id END) as "xcount8",
            COUNT(CASE WHEN subq1."90-99"=2 THEN subq1.sub_match_id END) as "xcount9",
            COUNT(CASE WHEN subq1."100-109"=2 THEN subq1.sub_match_id END) as "xcount10",
            h.localized_name as hero_name
            --ROUND((CAST(au.time AS FLOAT)/60)::numeric,2) as upgrade_time,
            --ROUND((CAST(m.duration AS FLOAT)/60)::numeric,2) as match_duration
            FROM abilities as a
            JOIN ability_upgrades as au ON au.ability_id=a.id
            JOIN matches_players_details as mpd ON au.match_player_detail_id=mpd.id
            JOIN matches as m ON mpd.match_id=m.id
            JOIN heroes as h ON mpd.hero_id=h.id
            JOIN(
            SELECT DISTINCT
            sub_m.id as sub_match_id,
            ROUND((CAST(sub_au.time AS FLOAT)/60)::numeric,2) as sub_upgrade_time,
            CASE
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=0 AND FLOOR((100*sub_au.time/sub_m.duration))<=9)AND 
            ((sub_m.radiant_win=true AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=false AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 1
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=0 AND FLOOR((100*sub_au.time/sub_m.duration))<=9)AND 
            ((sub_m.radiant_win=false AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=true AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 2
            ELSE 0
            END as "0-9",
            CASE
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=10 AND FLOOR((100*sub_au.time/sub_m.duration))<=19)AND 
            ((sub_m.radiant_win=true AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=false AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 1
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=10 AND FLOOR((100*sub_au.time/sub_m.duration))<=19)AND 
            ((sub_m.radiant_win=false AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=true AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 2
            ELSE 0
            END as "10-19",
            CASE
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=20 AND FLOOR((100*sub_au.time/sub_m.duration))<=29)AND 
            ((sub_m.radiant_win=true AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=false AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 1
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=20 AND FLOOR((100*sub_au.time/sub_m.duration))<=29)AND 
            ((sub_m.radiant_win=false AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=true AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 2
            ELSE 0
            END as "20-29",
            CASE
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=30 AND FLOOR((100*sub_au.time/sub_m.duration))<=39)AND 
            ((sub_m.radiant_win=true AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=false AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 1
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=30 AND FLOOR((100*sub_au.time/sub_m.duration))<=39)AND 
            ((sub_m.radiant_win=false AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=true AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 2
            ELSE 0
            END as "30-39",
            CASE
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=40 AND FLOOR((100*sub_au.time/sub_m.duration))<=49)AND 
            ((sub_m.radiant_win=true AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=false AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 1
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=40 AND FLOOR((100*sub_au.time/sub_m.duration))<=49)AND 
            ((sub_m.radiant_win=false AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=true AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 2
            ELSE 0
            END as "40-49",
            CASE
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=50 AND FLOOR((100*sub_au.time/sub_m.duration))<=59)AND 
            ((sub_m.radiant_win=true AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=false AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 1
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=50 AND FLOOR((100*sub_au.time/sub_m.duration))<=59)AND 
            ((sub_m.radiant_win=false AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=true AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 2
            ELSE 0
            END as "50-59",
            CASE
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=60 AND FLOOR((100*sub_au.time/sub_m.duration))<=69)AND 
            ((sub_m.radiant_win=true AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=false AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 1
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=60 AND FLOOR((100*sub_au.time/sub_m.duration))<=69)AND 
            ((sub_m.radiant_win=false AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=true AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 2
            ELSE 0
            END as "60-69",
            CASE
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=70 AND FLOOR((100*sub_au.time/sub_m.duration))<=79)AND 
            ((sub_m.radiant_win=true AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=false AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 1
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=70 AND FLOOR((100*sub_au.time/sub_m.duration))<=79)AND 
            ((sub_m.radiant_win=false AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=true AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 2
            ELSE 0
            END as "70-79",
            CASE
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=80 AND FLOOR((100*sub_au.time/sub_m.duration))<=89)AND 
            ((sub_m.radiant_win=true AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=false AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 1
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=80 AND FLOOR((100*sub_au.time/sub_m.duration))<=89)AND 
            ((sub_m.radiant_win=false AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=true AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 2
            ELSE 0
            END as "80-89",
            CASE
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=90 AND FLOOR((100*sub_au.time/sub_m.duration))<=99)AND 
            ((sub_m.radiant_win=true AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=false AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 1
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=90 AND FLOOR((100*sub_au.time/sub_m.duration))<=99)AND 
            ((sub_m.radiant_win=false AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=true AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 2
            ELSE 0
            END as "90-99",
            CASE
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=100)AND 
            ((sub_m.radiant_win=true AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=false AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 1
            WHEN (FLOOR((100*sub_au.time/sub_m.duration))>=100)AND 
            ((sub_m.radiant_win=false AND sub_mpd.player_slot>=0 AND sub_mpd.player_slot<=4) OR (sub_m.radiant_win=true AND sub_mpd.player_slot>=128 AND sub_mpd.player_slot<=132)) THEN 2
            ELSE 0
            END as "100-109"
            FROM abilities as sub_a
            JOIN ability_upgrades as sub_au ON sub_au.ability_id=sub_a.id
            JOIN matches_players_details as sub_mpd ON sub_au.match_player_detail_id=sub_mpd.id
            JOIN matches as sub_m ON sub_mpd.match_id=sub_m.id
            JOIN heroes as sub_h ON sub_mpd.hero_id=sub_h.id
            WHERE sub_a.id=5004
            ) as subq1 ON subq1.sub_match_id=m.id AND subq1.sub_upgrade_time=ROUND((CAST(au.time AS FLOAT)/60)::numeric,2)
            WHERE a.id=5004
            GROUP BY a.id, a.name, h.id, h.localized_name) as vsetko) as realvsetko
            ORDER BY hero_id;
            """.format(ability_id)
        )
        output = cursor1.fetchall()
        ability_id=output[0][0]
        ability_name=output[0][1]
        heroes=[]
        for i in range(0,len(output)):
            heroes.append({})
            heroes[i]["id"]=output[i][2]
            heroes[i]["name"]=output[i][3]
            if(output[i][5]>0):
                heroes[i]["usage_winners"]={"bucket":output[i][4],"count":output[i][5]}
            if(output[i][7]>0):
                heroes[i]["usage_loosers"]={"bucket":output[i][6],"count":output[i][7]}
        

        dict= {"id":ability_id,"name":ability_name,"heroes":heroes}


        JsonResponse.status_code=200
        return JsonResponse(dict,content_type = "application/json",json_dumps_params={'indent': 1})
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor1.close()
            conn.close()
            print("connection minus")


def function3(request):
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
                SELECT DISTINCT
                anothersubq.heroid as heroid,
                anothersubq.heroname as hero_name,
                MAX(anothersubq.sequencecount) OVER (PARTITION BY anothersubq.heroname) as maxseqcount
                FROM
                (SELECT
                subq.heroid as heroid,
                subq.heroname as heroname,
                COUNT(subq.*) as sequencecount
                FROM
                (SELECT
                row_number() over(order by mpd.match_id, go.time) as rownum,
                mpd.match_id as m_id,
                --go.subtype,
                h.id as heroid,
                h.localized_name as heroname,
                -- row_number() over (partition by mpd.match_id) as num1,
                -- row_number() over (partition by h.localized_name order by mpd.match_id, go.time) as num2,
                row_number() over (partition by mpd.match_id) - row_number() over (partition by h.localized_name order by mpd.match_id, go.time) as vysledok
                FROM game_objectives as go
                JOIN matches_players_details as mpd ON mpd.id=go.match_player_detail_id_1
                JOIN heroes as h ON h.id=mpd.hero_id
                WHERE go.subtype='CHAT_MESSAGE_TOWER_KILL'
                ORDER BY rownum) as subq
                GROUP BY subq.heroname,subq.m_id, subq.vysledok,subq.heroid
                ORDER BY subq.heroname) as anothersubq
                ORDER BY maxseqcount DESC, hero_name ASC
                """
        )
        output = cursor1.fetchall()
        heroes = []
        for i in range(0,len(output)):
            heroes.append({})
            heroes[i]["id"]=output[i][0]
            heroes[i]["name"]=output[i][1]
            heroes[i]["tower_kills"]=output[i][2]

        dict= {"heroes":heroes}


        JsonResponse.status_code=200
        return JsonResponse(dict,content_type = "application/json",json_dumps_params={'indent': 1})
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor1.close()
            conn.close()
            print("connection minus")