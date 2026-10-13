import json
import urllib.parse
import urllib.request

API = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "claim-checker-student-project/0.1"}


def _get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_wikipedia(query, limit=3):
    data = _get({
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "format": "json",
    })
    titles = [item["title"] for item in data["query"]["search"]]
    if not titles:
        return []

    pages = _get({
        "action": "query",
        "prop": "extracts",
        "exintro": 1,
        "explaintext": 1,
        "exsentences": 4,
        "titles": "|".join(titles),
        "format": "json",
    })["query"]["pages"]

    results = []
    for page in pages.values():
        title = page["title"]
        results.append({
            "title": title,
            "extract": page.get("extract", ""),
            "url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
        })

    order = {t: i for i, t in enumerate(titles)}
    results.sort(key=lambda r: order.get(r["title"], 99))
    return results


if __name__ == "__main__":
    with open("results.json", encoding="utf-8") as f:
        results = json.load(f)

    for entry in results:
        for claim in entry["claims"]:
            if claim["statement_type"] != "fact":
                continue
            print("\nCLAIM:", claim["normalized_claim"])
            for r in search_wikipedia(claim["normalized_claim"], limit=2):
                print("  -", r["title"], "|", r["url"])
                print("   ", r["extract"][:200].replace("\n", " "))