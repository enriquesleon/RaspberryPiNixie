#!/usr/bin/python
import nixiedisplay
import shift595
import urllib2
import json
import time

def select_game():
    # print out weeks for user prompt
    print "Select a week:"
    for i in range (0, 15):
        print (i + 1)

    # loop until user enters valid week
    week_loop = True
    while (week_loop):
        print "\nWeek Selection: ",
        num = raw_input()
        if num.isdigit() and int(num) > 0 and int(num) < 16:
            week_loop = False
        else:
            print "Invalid selection, try again"

    # Build and call API to get game data for selected week
    week_url = 'http://api.sportradar.us/nfl-ot1/games/2015/REG/' + num + '/schedule.json?api_key=sjs8f4b2uj34ea39cmhjcu44'
    week_request = urllib2.urlopen(week_url).read()
    week_data = json.loads(week_request)

    # print out games for user prompt
    print "Select game:"
    game_counter = 0
    for game in week_data['week']['games']:
        home = game['home']['name']
        away = game['away']['name']
        print "%d: %s vs %s" % (game_counter+1, home, away)
        game_counter += 1

    # loop until user selects valid game
    game_loop = True
    while (game_loop):
        print "Game Selection: ",
        game = raw_input()
        if game.isdigit() and int(game) > 0 and int(game) <= len(week_data['week']['games']) :
            game_id = week_data['week']['games'][int(game)-1]['id']
            game_loop = False
        else:
            print "Invalid selection, try again"

    return game_id

# Utilize SportsRadar API to grab live NFL score data
# Prompts user twice, first to get week number, and second
# to select game. Returns home score and away score as a tuple
def display_scores(game_id):
    # build and call API to get score data for selected game
    game_url = "http://api.sportradar.us/nfl-ot1/games/" + game_id + "/statistics.json?api_key=sjs8f4b2uj34ea39cmhjcu44"
    shift = shift595.Shift595()
    display = nixiedisplay.NixieDisplay(6,shift)

    while True:
        game_request = urllib2.urlopen(game_url).read()
        game_data = json.loads(game_request)

        # If game has not taken place yet, set scores to 0
        try:
            home_score = game_data['summary']['home']['points']
            away_score = game_data['summary']['away']['points']
        except:
            home_score = 0
            away_score = 0

        
        bridge_scores = "%d00%d" % (home_score, away_score)
        display.string_display(bridge_scores)
        display.update()
        time.sleep(5)

# Main program
# Todo: after getting scores from the get_score function as a tuple,
# pass those values onto be displayed on the tubes
def main():
    game = select_game()
    display_scores(game)

if __name__ == '__main__':
    main()

