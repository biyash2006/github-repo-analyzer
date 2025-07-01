import requests
import click

BASE_URL = "https://api.github.com"

def fetch_repo_data(owner, repo):
    url = f"{BASE_URL}/repos/{owner}/{repo}"
    response = requests.get(url)
    return response.json()

def fetch_contributors(owner, repo):
    url = f"{BASE_URL}/repos/{owner}/{repo}/contributors"
    response = requests.get(url)
    return response.json()

def analyze_repo(owner, repo):
    repo_data = fetch_repo_data(owner, repo)
    contributors = fetch_contributors(owner, repo)

    print(f"\n📘 Repository: {repo_data['full_name']}")
    print(f"⭐ Stars: {repo_data['stargazers_count']}")
    print(f"🍴 Forks: {repo_data['forks_count']}")
    print(f"🐞 Open Issues: {repo_data['open_issues_count']}")
    print("\n👥 Top Contributors:")
    for user in contributors[:5]:
        print(f"- {user['login']}: {user['contributions']} commits")

# 👇 This part is new!
@click.command()
@click.option('--owner', prompt='GitHub Owner', help='The username or organization that owns the repo')
@click.option('--repo', prompt='Repository Name', help='The name of the GitHub repository')
def main(owner, repo):
    analyze_repo(owner, repo)

if __name__ == "__main__":
    main()