import requests
import matplotlib.pyplot as plt
from operator import itemgetter
from datetime import datetime


def get_user_input():
    # User input
    player_input = input("What player do you want to get stats for? (Enter Full Name) ")
    player_input = player_input.replace(" ", "_")
    return player_input


player_url = get_user_input()


def player_general_info(url_endpoint):
    """Gets the api containing general player data"""
    url = f'https://www.balldontlie.io/api/v1/players?search={url_endpoint}'
    api_request = requests.get(url)
    print(f"Status Code: {api_request.status_code}")
    return api_request


# The api link that we use to generate the json file with data provided by api
accepted_api = player_general_info(player_url)


def extract_data():
    """Converts the api request into json and converts into a dictionary"""
    # Convert the api request to a json file containing player info
    player_data = accepted_api.json()

    # Get the part of the data containing relevant data
    player_specifics = player_data['data']

    # Convert the dictionary inside the list for easier extraction of data
    player_dictionary = {}
    for line in player_specifics:
        player_dictionary.update(line)
    return player_dictionary


# Returns a clean dictionary in which we can pull off data
player_information = extract_data()


def get_id():
    """Returns player ID of the player searched"""
    return player_information['id']


# We need the id to got to line api link that contains stats
player_id = get_id()


def get_player_season_avgs(url_endpoint):
    """API request to get player stats. DIFFERENT URL THAN PREVIOUS"""
    url = f'https://www.balldontlie.io/api/v1/season_averages?season=2020&player_ids[]={player_id}'
    api_request = requests.get(url)
    print(f"Status Code: {api_request.status_code}")
    return api_request


# Returns the api request of player stats
player_stats_accepted_api = get_player_season_avgs(player_id)


def extra_stats():
    """Contains season average stats"""
    """Converts request into json file and converts into a dictionary."""
    # Store player stats in json
    player_stats_data = player_stats_accepted_api.json()

    # Just the stats part
    player_stats = player_stats_data['data']

    # Convert the dictionary inside the list for easier extraction of data

    player_stats_dict = {}
    for line in player_stats:
        player_stats_dict.update(line)
    return player_stats_dict


player_stats = extra_stats()


def output():
    """Output messages"""
    player_name = player_information['first_name']
    player_last_name = player_information['last_name']
    player_team = player_information['team']['full_name']

    player_ppg = player_stats['pts']
    player_fga = player_stats['fga']
    print(f"The player you chose is {player_name} {player_last_name} he plays for the {player_team}")
    print(f"He averages {player_ppg} points per game on {player_fga} attempts")


def get_player_name():
    name = ''
    name = player_information['first_name'] + " " + player_information['last_name']
    return name


player_name = get_player_name()


def get_last_five_games(url_endpoint):
    """API request to get player stats. DIFFERENT URL THAN PREVIOUS"""
    end_date = datetime.now().strftime('%Y-%m-%d')
    url = f'https://www.balldontlie.io/api/v1/stats?&start_date=2021-01-01&end_date={end_date}&player_ids[]={player_id}'

    api_request = requests.get(url)
    print(f"Status Code: {api_request.status_code}")
    return api_request


player_last_five_api = get_last_five_games(player_id)

output()


def last_five_game_stats():
    last_five_stats = player_last_five_api.json()

    last_five = last_five_stats['data']
    return last_five


last_five = last_five_game_stats()
print(last_five)

sorted_data = sorted(last_five, key=itemgetter('id'))
myList = sorted_data[-5:]
print(myList)
first_dict = (myList[0])
second_dict = (myList[1])
third_dict = (myList[2])
fourth_dict = (myList[3])
fifth_dict = (myList[4])

first_game_data = {'Date: ': first_dict['game']['date'], 'Points: ': first_dict['pts']}
second_game_data = {'Date: ': second_dict['game']['date'], 'Points: ': second_dict['pts']}
third_game_data = {'Date: ': third_dict['game']['date'], 'Points: ': third_dict['pts']}
fourth_game_data = {'Date: ': fourth_dict['game']['date'], 'Points: ': fourth_dict['pts']}
fifth_game_data = {'Date: ': fifth_dict['game']['date'], 'Points: ': fifth_dict['pts']}

points = [first_game_data['Points: '], second_game_data['Points: '], third_game_data['Points: '],
          fourth_game_data['Points: '], fifth_game_data['Points: ']]

date_pt = [first_game_data['Date: '][:10], second_game_data['Date: '][:10], third_game_data['Date: '][:10],
           fourth_game_data['Date: '][:10], fifth_game_data['Date: '][:10]]
date = ['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5']

y_values = [0, 10, 20, 30, 40]

# plt.style.use('dark_background')
fig, ax = plt.subplots()

fig.patch.set_facecolor('#333333')
ax.patch.set_facecolor('#333333')

ax.spines['bottom'].set_color('#F7F7F2')
ax.spines['left'].set_color('#F7F7F2')
# ax.yaxis.set_ticks_position('bottom')
# ax.xaxis.set_ticks_position('left')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# ax.plot(date, points, color='blue', linestyle='-', marker='o')

sc = plt.scatter(date, points, c='#B41212')
plt.plot(date, points, c='#B41212')

annot = ax.annotate("", xy=(0, 0), xytext=(-30, 10), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle='-'))
annot.set_visible(False)


def update_annot(ind):
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "Points Scored: {} \nGame Date: {} ".format(" ".join(str(points[n]) for n in ind["ind"]),
                                                       " ".join([date_pt[n] for n in ind["ind"]]))
    annot.set_text(text)
    # annot.get_bbox_patch().set_facecolor(points(date))
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", hover)

plt.title("{} P.P.G (Last FIVE)".format(player_name), fontsize=24, pad=20, c='#F7F7F2')
# plt.xlabel('Game Dates', fontsize=12, c='blue')
fig.autofmt_xdate()
# plt.ylabel('Points', fontsize=16, c='#F7F7F2')
plt.tick_params(axis='both', which='both', labelsize=16, color='#F7F7F2', labelcolor='#F7F7F2')
ax.spines['top'].set_color('orange')
plt.show()
