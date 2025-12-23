import requests

from agents import function_tool


# e.g. https://www.reddit.com/r/UMD/search.json?q=Clyde%20kruskal&restrict_sr=1
@function_tool
def search_umd_reddit(query: str, limit: int = 20):
    """
    Search UMD Reddit for information about courses and professors.
    Supports boolean operators (AND, OR, NOT) which must be UPPERCASE.
    Use parentheses for grouping.

    :param query: The search query. Examples: "Kruskal OR 351", "(Justin OR Huerter) AND 140"
    :param limit: Maximum number of records to return.
    """

    # sort by comments by default since we would expect them to have the most information about a certain professor
    url = f"https://www.reddit.com/r/UMD/search.json?q={query}&restrict_sr=1&sort=comments&limit={limit}"

    data = requests.get(url, headers={"User-agent": "PlanetTerp Agent 0.1 (u/kiesoma)"})
    json_data = data.json()

    results = []
    for post in json_data.get("data", {}).get("children", []):
        p = post.get("data", {})
        results.append(
            {
                "title": p.get("title"),
                "selftext": p.get("selftext"),
                "score": p.get("score"),
                "num_comments": p.get("num_comments"),
                "upvote_ratio": p.get("upvote_ratio"),
                "link_flair_text": p.get("link_flair_text"),
                "permalink": f"https://reddit.com{p.get('permalink')}",
                "author_flair": p.get("author_flair_text"),
            }
        )

    return results
