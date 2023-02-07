from git import Repo

def parse_json(data):
    try:
        clone_url = data["repository"]["clone_url"]
        branch = data["ref"].replace("refs/heads/", "")
        return clone_url, branch
    except:
        return "invalid json"

def clone_repo(git_url, repo_dir, branch):
    try:
        repo = Repo.clone_from(git_url, repo_dir, branch=branch)
        return 'clone succeded'
    except:
        return 'clone failed'