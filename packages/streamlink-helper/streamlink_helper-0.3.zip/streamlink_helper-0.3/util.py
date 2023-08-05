import requests
import subprocess

HEADERS = {
    'Client-ID': "zjcbgrilhcnzx1mt3fbcrpn7vekw64"
}


def followscraper(user_id):
    params = {
        'from_id': user_id,
        'first': 100
    }
    follows_api_url = "https://api.twitch.tv/helix/users/follows"
    followed_response = requests.get(follows_api_url, params=params, headers=HEADERS)
    followed_list = followed_response.json()["data"]
    return create_stream_urls(followed_list)


def create_stream_urls(follow_list):
    # TODO: Add game name, stream title
    live_api_url = "https://api.twitch.tv/helix/streams"
    game_api_url = "https://api.twitch.tv/helix/games"
    base_url = "twitch.tv/"
    streams = []
    for follow_relation in follow_list:
        streams.append(follow_relation["to_id"])
    params = {
        "user_id": streams
    }
    online_streams_response = requests.get(live_api_url, params=params, headers=HEADERS)
    online_streams = {}
    for online_relation in online_streams_response.json()["data"]:
        params = {
            "id": online_relation["game_id"]
        }
        game_response = requests.get(game_api_url, params=params, headers=HEADERS)
        try:
            game = game_response.json()["data"][0]["name"]
        except IndexError:
            game = "N/A"
        online_streams["{user} - {title} \n Streaming {game} to {viewer_count} viewers \n".format(
            user=online_relation["user_name"],
            title=online_relation["title"],
            game=game,
            viewer_count=online_relation["viewer_count"])] = base_url + online_relation["user_name"]
    return online_streams


def execute_streamlink_command(stream_url, configuration):
    for quality in reversed(configuration.quality_order_of_preference):
        try:
            subprocess.check_output("streamlink " + stream_url + " " + quality, shell=True)
            break
        except subprocess.CalledProcessError:
            pass
