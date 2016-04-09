from bs4 import BeautifulSoup
from datetime import datetime
import requests
import os

team_list = [['ATL', 'STL', 'MLH', 'TRI'], ['BOS'], ['BRK', 'NJN', 'NYN', 'NYA', 'NJA'], ['CHA', 'CHH', 'CHO'], ['CHI'], ['CLE'], ['DAL'], ['DEN', 'DNA', 'DNR'], ['DET', 'FTW'], ['GSW', 'SFW', 'PHW'], ['HOU', 'SDR'], ['IND', 'INA'], ['LAC', 'SDC', 'BUF'], ['LAL', 'MNL'], ['MEM', 'VAN'], ['MIA'], ['MIL'], ['MIN'], ['NOP', 'NOH', 'NOK'], ['NYK'], ['OKC', 'SEA'], ['ORL'], ['PHI', 'SYR'], ['PHO'], ['POR'], ['SAC', 'KCK', 'KCO', 'CIN', 'ROC'], ['SAS', 'SAA', 'TEX', 'DLC'], ['TOR'], ['UTA', 'NOJ'], ['WAS', 'WSB', 'CAP', 'BAL', 'CHZ', 'CHP']]

if not os.path.exists('NBA_Stats'):
    os.makedirs('NBA_Stats')

def get_date_time(): 
    date_time =  datetime.now()

    month = date_time.month
    month = str(month)

    day = date_time.day
    day = str(day)

    year = date_time.year
    year = str(year)
    
    hour = date_time.hour
    am_pm = hour/12
    hour = hour%12
    hour = str(hour)

    num_minute = date_time.minute
    minute = str(num_minute)
    if num_minute < 10: # Makes it more consistent with the numbers
        minute = "0"+minute

    if am_pm == 0: # setup an am/pm system
        get_date_time.date_for_saving = hour + "_" + minute + "_AM_" + month + "-" + day + "-" + year  
        time_now = hour+"-"+minute+"-AM-"+month+"-"+day+"-"+year
    else:
        get_date_time.date_for_saving = hour + "_" + minute + "_PM_" + month + "-" + day + "-" + year  
        time_now = hour+"-"+minute+"-PM-"+month+"-"+day+"-"+year
    return time_now

def nba_stats_big(url, header_print, curr_team):
    ids = ['per_game', 'per_minute', 'totals', 'advanced']
    stat_types = ["Per_Game", "Per_36min", "Year_Total", "Advanced"]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    tables = []
    for id in ids:
        table = soup.find("table", {"id":id})
        tables.append(table)
    if tables[0] is None:
        return [header_print, True]
    per_game_rows = tables[0].find_all('tr')
    per36_rows = tables[1].find_all('tr')
    year_total_rows = tables[2].find_all('tr')
    advanced_rows = tables[3].find_all('tr')


    get_date_time()
    team_year = url[42:45]+"_"+url[46:50]
    team = url[42:45]
    year = url[46:50]
    file_name = "./NBA_Stats/NBA_Data.csv"
    print file_name, team, year, team_year
    nba_stats_per_game = open(file_name, "a")
    
    for index in range(0, len(per_game_rows)):
        each_row = ""
        row = per_game_rows[index]
        if header_print == False:
            header_print = True
            each_row = "Year,Team,Current_Team"
            # header: first table, per game
            header = row.find_all('th')
            for th in header:
                stat = th['data-stat'] # gets whatever statistic we are looking at (i.e. steals, blocks, points, etc)
                # write onto file. 
                if len(each_row) > 0:
                    each_row = each_row + ","
                each_row = each_row + stat
            # header: second table
            row = per36_rows[index]
            header = row.find_all('th')
            for th_index in range(5, len(header)):
                th = header[th_index]
                stat = th['data-stat'] # gets whatever statistic we are looking at (i.e. steals, blocks, points, etc)
                # write onto file. 
                if len(each_row) > 0:
                    each_row = each_row + ","
                each_row = each_row + stat
            # header: 3rd table
            row = year_total_rows[index]
            header = row.find_all('th')
            for th_index in range(6, len(header)):
                th = header[th_index]
                stat = th['data-stat'] # gets whatever statistic we are looking at (i.e. steals, blocks, points, etc)
                # write onto file. 
                if len(each_row) > 0:
                    each_row = each_row + ","
                each_row = each_row + stat
            # header: 4th table
            row = advanced_rows[index]
            header = row.find_all('th')
            for th_index in range(5, len(header)):
                th = header[th_index]
                stat = th['data-stat'] # gets whatever statistic we are looking at (i.e. steals, blocks, points, etc)
                # write onto file. 
                if len(each_row) > 0:
                    each_row = each_row + ","
                each_row = each_row + stat
            each_row = each_row+"\n"

        else:
            data = row.find_all('td')
            if len(data) > 0:
                each_row = year+","+team+","+curr_team
            
            for td in data:
                if td.a:
                    stats = td.a.text
                else:
                    stats = td.text
                # write onto file. 
                if len(each_row) > 0:
                    each_row = each_row + ","
                each_row = each_row + stats
            # data: second table
            row = per36_rows[index]
            data = row.find_all('td')
            for td_index in range(5, len(data)):
                td = data[td_index]
                if td.a:
                    stats = td.a.text
                else:
                    stats = td.text # gets whatever statistic we are looking at (i.e. steals, blocks, points, etc)
                # write onto file. 
                if len(each_row) > 0:
                    each_row = each_row + ","
                each_row = each_row + stats
            # data: third table
            row = year_total_rows[index]
            data = row.find_all('td')
            for td_index in range(6, len(data)):
                td = data[td_index]
                if td.a:
                    stats = td.a.text
                else:
                    stats = td.text # gets whatever statistic we are looking at (i.e. steals, blocks, points, etc)
                # write onto file. 
                if len(each_row) > 0:
                    each_row = each_row + ","
                each_row = each_row + stats            
            # data: fourth table
            row = advanced_rows[index]
            data = row.find_all('td')
            for td_index in range(5, len(data)):
                td = data[td_index]
                if td.a:
                    stats = td.a.text
                else:
                    stats = td.text # gets whatever statistic we are looking at (i.e. steals, blocks, points, etc)
                # write onto file. 
                if len(each_row) > 0:
                    each_row = each_row + ","
                each_row = each_row + stats
            if len(data) > 0:
                each_row = each_row + "\n"

        #print each_row
        nba_stats_per_game.write(each_row)
    nba_stats_per_game.close()
    
    return [header_print, False]
        
def files_creator(teams, header_print):
    num_year = 1949
    str_year = "1949"
    while num_year < 2017:
        print num_year
        for team in teams:
            print team
            team_url = "http://www.basketball-reference.com/teams/"+team+"/"+str_year+".html"
            data = nba_stats_big(team_url, header_print, teams[0])
            header_print = data[0]
            cont = data[1]
            if cont is False:
                break
        str_year = str(num_year + 1)
        num_year = num_year + 1
    return header_print

year = 1947
header_print = False
for teams in team_list:
    header_print = files_creator(teams, header_print)
    
