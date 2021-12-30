import sqlite3
import seleniumwebscraper

def courses():
  theopen = "https://www.pgatour.com/tournaments/the-open-championship/past-results.html"
  themasters = "https://www.pgatour.com/tournaments/masters-tournament/past-results.html"
  thepga = "https://www.pgatour.com/tournaments/pga-championship/past-results.html"
  theusopen = "https://www.pgatour.com/tournaments/us-open/past-results.html"
  tlist = [theopen, themasters, thepga, theusopen]
  return tlist

#Create a table to insert table scraping data into from seleniumwebscraper
def scorescraper():
  #build connection to database
  conn = sqlite3.connect("data.db")
  c = conn.cursor()

  #create a table
  # c.execute("DROP TABLE IF EXISTS scoreboard")
  sql = """
  CREATE TABLE scoreboard (
    id INTEGER PRIMARY KEY,
    playername VARCHAR(20),
    place VARCHAR(20),
    roundOne VARCHAR(20),
    roundTwo VARCHAR(20),
    roundThree VARCHAR(20),
    roundFour VARCHAR(20),
    finalScore VARCHAR(20),
    winnings money(20),
    points VARCHAR(20),
    titleString VARCHAR(30),
    ending VARCHAR(12),
    year VARCHAR(5)
  ) """
  c.execute(sql)

  #insert records into the table
  tlist = courses()
  for x in tlist:
      for i in range(1,40):
          data = seleniumwebscraper.playerscore(i, x)
          for i in range(0,len(data)):
              dataString = data[i]

              print(dataString)
              c.execute("INSERT INTO scoreboard VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (dataString))

  #view the results
  c.execute("SELECT * FROM scoreboard")
  results = c.fetchall()
  for x in results:
    print(x)

  #make changes permanent
  conn.commit()
  c.close()

#Create a table to insert course data into from seleniumwebscraper
def coursescraper():
 #build connection to database
  conn = sqlite3.connect("data.db")
  c = conn.cursor()
  
  #create a table
  # c.execute("DROP TABLE IF EXISTS coursedata")
  sql = """
  CREATE TABLE coursedata (
    id INTEGER PRIMARY KEY,
    titleString VARCHAR(20),
    year VARCHAR(5),
    ending VARCHAR(12),
    par VARCHAR(2),
    course VARCHAR(40),
    purse money(20)
  ) """
  c.execute(sql)

  #insert records into the table
  tlist = courses()
  for x in tlist:
    for i in range(1,40):
        data = seleniumwebscraper.webscrapeCourse(i, x)
        print(data)
        print("")
        print(x, i)
        c.execute("INSERT INTO coursedata VALUES (null, ?, ?, ?, ?, ?, ?)",
            (data))

  #view the results
  c.execute("SELECT * FROM coursedata")
  results = c.fetchall()
  for x in results:
    print(x)

  #make changes permanent
  conn.commit()
  c.close()

def main():
    scorescraper()
    coursescraper()

main()
#Yay! we now have database.db that we can use.