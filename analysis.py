import sqlite3
import numpy
import time
import pandas as pd

conn = sqlite3.connect("data.db")

def numberOfCourses():
    c = conn.cursor()
    sql = """ 
    SELECT COUNT(DISTINCT course) AS number FROM coursedata ORDER BY number desc
    """
    c.execute(sql)
    results = c.fetchall()
    results = results[0]
    results = results[0]
    return results

# Find the number of events hosted per course
def numberEachCourse():
    c = conn.cursor()
    sql = """ 
    SELECT course, COUNT(*) as number FROM coursedata GROUP BY course ORDER BY number DESC
    """
    c.execute(sql)
    results = c.fetchall()
    list = []
    for x in results:
        list.append(x)
    return list

# Find the highest score to make the cut and return the name. Ensure the contains only numbers.
def highestScoreMadeCut():
    c = conn.cursor()
    sql = """ 
    select place from scoreboard where place REGEXP '^-?[0-9]+$' order by finalscore
    """
    c.execute(sql)
    results = c.fetchall()
    list = []
    for x in results:
        list.append(x)
    return list


# Find the lowest score at a particular place. Allow tournament and place as a parameters
def Winners(place, tournament):
    c = conn.cursor()
    sql = """
    SELECT 
    s.playername, 
    s.roundone, 
    s.roundtwo, 
    s.roundthree, 
    s.roundfour, 
    s.finalscore, 
    c.par*4, 
    s.winnings, 
    s.year, 
    c.course, 
    c.purse,
    s.finalscore - c.par*4
    FROM scoreboard s LEFT JOIN coursedata c ON s.ending = c.ending
    WHERE place = '{}' and s.titleString = '{}' ORDER BY s.year DESC 
    """.format(place, tournament)
    c.execute(sql)
    results = c.fetchall()
    list = []
    for x in results:
        list.append(x)
    return list

#Find the average four round score and course par for each tournament.
def AverageFourRoundScore():
    c = conn.cursor()
    sql = """ 
    SELECT 
        s.titlestring, 
        round(avg(s.finalscore), 2) as number, 
        round(avg(c.par*4), 2),
        round(avg(s.finalscore) - avg(c.par*4), 2)
        FROM scoreboard s 
        LEFT JOIN coursedata c ON s.titleString = c.titlestring
        WHERE s.roundfour != '' and s.place != 'W/D' and s.place != 'CUT' 
        GROUP BY s.titleString 
        ORDER BY number DESC;
    """
    c.execute(sql)
    results = c.fetchall()
    list = []
    for x in results:
        list.append(x)
        
    return list

#Find player total winnings from the scoreboard table. Add up the total winnings based on the records returned
def PlayerWinnings(player):
        c = conn.cursor()
        sql = """ 
        SELECT playername, winnings FROM scoreboard WHERE winnings !='' and playername = '{}'
        """.format(player)
        c.execute(sql)
        results = c.fetchall()
        list = []
        for x in results:
                list.append(x)
        total = 0
        for i in list:
                some = i[1].replace(',', '')
                total = total + float(some)
        total = int(total)
                
        return total