import os
import requests

class ApiUnavailable(Exception): ...
class SeriesNotSupported(Exception): ...

def _base_url():
    return os.getenv("ERGAST_BASE_URL", "https://ergast.com/api/f1")

def _http_get(url: str, params: dict | None = None):
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code >= 500:
            raise ApiUnavailable(f"Server error: {r.status_code}")
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        raise ApiUnavailable(str(e)) from e

def get_f1_calendar(year: int | None = None):
    base = _base_url()
    path = f"{base}/{year}.json" if year else f"{base}/current.json"
    data = _http_get(path)
    races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
    return races

def get_f1_results_by_round(round_num: int, year: int | None = None):
    base = _base_url()
    if year:
        path = f"{base}/{year}/{round_num}/results.json"
    else:
        path = f"{base}/current/{round_num}/results.json"
    data = _http_get(path)
    res = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
    if not res:
        return []
    return res[0].get("Results", [])

def get_f1_standings(drivers: bool = True, year: int | None = None):
    base = _base_url()
    path = f"{base}/{year}/driverStandings.json" if drivers else f"{base}/{year}/constructorStandings.json"
    if year is None:
        path = f"{base}/current/driverStandings.json" if drivers else f"{base}/current/constructorStandings.json"
    data = _http_get(path)
    if drivers:
        st = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
        return st[0].get("DriverStandings", []) if st else []
    else:
        st = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
        return st[0].get("ConstructorStandings", []) if st else []
