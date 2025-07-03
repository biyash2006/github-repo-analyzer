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

def fetch_issue_stats(owner, repo):
    open_url = f"{BASE_URL}/repos/{owner}/{repo}/issues?state=open&per_page=1"
    closed_url = f"{BASE_URL}/repos/{owner}/{repo}/issues?state=closed&per_page=1"

    open_issues = requests.get(open_url).links.get('last', {}).get('url', '')
    closed_issues = requests.get(closed_url).links.get('last', {}).get('url', '')

    open_count = int(open_issues.split('page=')[-1]) if open_issues else 0
    closed_count = int(closed_issues.split('page=')[-1]) if closed_issues else 0

    return open_count, closed_count


def fetch_pr_stats(owner, repo):
    open_url = f"{BASE_URL}/repos/{owner}/{repo}/pulls?state=open&per_page=1"
    closed_url = f"{BASE_URL}/repos/{owner}/{repo}/pulls?state=closed&per_page=1"

    open_prs = requests.get(open_url).links.get('last', {}).get('url', '')
    closed_prs = requests.get(closed_url).links.get('last', {}).get('url', '')

    open_count = int(open_prs.split('page=')[-1]) if open_prs else 0
    closed_count = int(closed_prs.split('page=')[-1]) if closed_prs else 0

    return open_count, closed_count

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
    open_issues, closed_issues = fetch_issue_stats(owner, repo)
    open_prs, closed_prs = fetch_pr_stats(owner, repo)

    print(f"\n📊 Issue Stats:")
    print(f"🟢 Open Issues: {open_issues}")
    print(f"🔴 Closed Issues: {closed_issues}")

    print(f"\n🔁 Pull Request Stats:")
    print(f"🟢 Open PRs: {open_prs}")
    print(f"🔴 Closed/Merged PRs: {closed_prs}")

# 👇 This part is new!
@click.command()
@click.option('--owner', prompt='GitHub Owner', help='The username or organization that owns the repo')
@click.option('--repo', prompt='Repository Name', help='The name of the GitHub repository')
def main(owner, repo):
    analyze_repo(owner, repo)

if __name__ == "__main__":
    main()