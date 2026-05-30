import requests
from config import STEAM_API_KEY


def resolve_vanity_url(vanity_name):
    url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={vanity_name}"
    try:
        response = requests.get(url, timeout=3).json()
        if response.get("response", {}).get("success") == 1:
            return response["response"]["steamid"]
    except Exception as e:
        print(f'Error: {e}')
    return None


def get_steam_friends_stats(steam_id):
    url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={STEAM_API_KEY}&steamid={steam_id}&relationship=friend"
    try:
        res = requests.get(url, timeout=5).json()
        friends = res.get('friendslist', {}).get('friends', [])
        if not friends: return []
    except Exception:
        return []

    friend_ids = [f['steamid'] for f in friends]
    players_data = []

    for i in range(0, len(friend_ids), 100):
        chunk = friend_ids[i:i + 100]
        chunk_str = ",".join(chunk)
        summary_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={chunk_str}"
        try:
            s_res = requests.get(summary_url, timeout=5).json()
            players_data.extend(s_res.get('response', {}).get('players', []))
        except Exception:
            pass

    rust_players = []
    online_players = []

    for p in players_data:
        game = p.get('gameextrainfo', '')
        state = p.get('personastate', 0)
        if game == 'Rust':
            rust_players.append(p)
        elif state != 0:
            online_players.append(p)

    top_players = rust_players + online_players
    return top_players[:10]


def get_rust_hours(steam_id):
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}"
    try:
        response = requests.get(url, timeout=10).json()
        games = response.get('response', {}).get('games', [])
        for game in games:
            if game.get('appid') == 252490:
                hours = int(game.get('playtime_forever', 0) / 60)
                return str(hours)
    except Exception as e:
        print(f'Error: {e}')
    return "Скрыто / 0.00"