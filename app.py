from flask import Flask, render_template
import requests

app = Flask(__name__)

# Docker Registry URL
DOCKER_REGISTRY_URL = "http://localhost:5000"

@app.route("/")
def list_repositories():
    # Get the repositories from registiry
    catalog_url = f"{DOCKER_REGISTRY_URL}/v2/_catalog"
    response = requests.get(catalog_url)
    if response.status_code != 200:
        return f"Can't reach to Registry API: {response.status_code}"

    repositories = response.json().get("repositories", [])

    # Get all the tags of the repositories
    repo_tags = []
    for repo in repositories:
        tags_url = f"{DOCKER_REGISTRY_URL}/v2/{repo}/tags/list"
        tags_response = requests.get(tags_url)
        if tags_response.status_code == 200:
            tags = tags_response.json().get("tags", [])
            repo_tags.append({"repository": repo, "tags": tags})

    return render_template("index.html", repo_tags=repo_tags)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
