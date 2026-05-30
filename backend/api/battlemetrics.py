import requests


def search_bm_players_by_name(nickname):
    url = f"https://api.battlemetrics.com/players?filter[search]={nickname}"
    try:
        response = requests.get(url, timeout=10).json()
        data = response.get("data", [])

        player_ids = []
        for p in data:
            if p["attributes"]["name"].lower() == nickname.lower():
                player_ids.insert(0, p["attributes"]["id"])
            else:
                player_ids.append(p["attributes"]["id"])

        unique_ids = []
        for pid in player_ids:
            if pid not in unique_ids:
                unique_ids.append(pid)

        return unique_ids[:5]
    except Exception as e:
        print(f"Error searching BM player: {e}")
        return []


def get_bm_player_servers(player_id):
    url = f"https://api.battlemetrics.com/players/{player_id}?include=server,identifier"
    try:
        response = requests.get(url, timeout=10).json()
        included = response.get("included", [])
        servers = []
        for item in included:
            if item.get("type") == "server":
                if item.get("relationships", {}).get("game", {}).get("data", {}).get("id") == "rust":
                    servers.append(item.get("attributes", {}))
        return servers[:20]
    except Exception as e:
        print(f"Error getting BM servers: {e}")
    return []