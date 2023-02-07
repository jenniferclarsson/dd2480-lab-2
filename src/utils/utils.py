def parse_json(data):
    try:
        clone_url = data["repository"]["clone_url"]
        branch = data["ref"].replace("refs/heads/", "")
        return clone_url, branch
    except:
        return "invalid json"