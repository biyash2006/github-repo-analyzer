import requests
import click
import pandas as pd

BASE_URL = "https://api.github.com"

def fetch_repo_data(owner, repo):
    url = f"{BASE_URL}/repos/{owner}/{repo}"
    response = requests.get(url)

    if response.status_code == 404:
        raise ValueError(f"❌ Repository '{owner}/{repo}' not found.")
    if response.status_code == 403:
        raise RuntimeError("❌ GitHub API rate limit exceeded. Please try again later.")

    return response.json()

def fetch_contributors(owner, repo):
    url = f"{BASE_URL}/repos/{owner}/{repo}/contributors"
    response = requests.get(url)
    if response.status_code == 403:
        raise RuntimeError("❌ GitHub API rate limit exceeded. Try again later.")
    return response.json()

def fetch_issue_stats(owner, repo):
    open_url = f"{BASE_URL}/repos/{owner}/{repo}/issues?state=open&per_page=1"
    closed_url = f"{BASE_URL}/repos/{owner}/{repo}/issues?state=closed&per_page=1"

    open_response = requests.get(open_url)
    closed_response = requests.get(closed_url)

    # Rate limit check
    if open_response.status_code == 403 or closed_response.status_code == 403:
        raise RuntimeError("❌ GitHub API rate limit exceeded. Please try again later.")

    open_issues = open_response.links.get('last', {}).get('url', '')
    closed_issues = closed_response.links.get('last', {}).get('url', '')

    open_count = int(open_issues.split('page=')[-1]) if open_issues else 0
    closed_count = int(closed_issues.split('page=')[-1]) if closed_issues else 0

    return open_count, closed_count


def fetch_pr_stats(owner, repo):
    open_url = f"{BASE_URL}/repos/{owner}/{repo}/pulls?state=open&per_page=1"
    closed_url = f"{BASE_URL}/repos/{owner}/{repo}/pulls?state=closed&per_page=1"

    open_response = requests.get(open_url)
    closed_response = requests.get(closed_url)

    # Handle API rate limiting
    if open_response.status_code == 403 or closed_response.status_code == 403:
        raise RuntimeError("❌ GitHub API rate limit exceeded. Please try again later.")

    open_prs = open_response.links.get('last', {}).get('url', '')
    closed_prs = closed_response.links.get('last', {}).get('url', '')

    open_count = int(open_prs.split('page=')[-1]) if open_prs else 0
    closed_count = int(closed_prs.split('page=')[-1]) if closed_prs else 0

    return open_count, closed_count

def export_to_csv(repo_data, contributors, issue_stats, pr_stats, filename="repo_stats.csv"):
    rows = []

    # Add basic repo info
    rows.append({
        "Metric": "Repository",
        "Value": repo_data["full_name"]
    })
    rows.append({
        "Metric": "Stars",
        "Value": repo_data["stargazers_count"]
    })
    rows.append({
        "Metric": "Forks",
        "Value": repo_data["forks_count"]
    })
    rows.append({
        "Metric": "Open Issues (Raw)",
        "Value": repo_data["open_issues_count"]
    })

    # Add issue stats
    rows.append({
        "Metric": "Open Issues",
        "Value": issue_stats[0]
    })
    rows.append({
        "Metric": "Closed Issues",
        "Value": issue_stats[1]
    })

    # Add PR stats
    rows.append({
        "Metric": "Open PRs",
        "Value": pr_stats[0]
    })
    rows.append({
        "Metric": "Closed/Merged PRs",
        "Value": pr_stats[1]
    })

    # Add contributor info
    for contributor in contributors[:5]:
        rows.append({
            "Metric": f"Contributor - {contributor['login']}",
            "Value": contributor["contributions"]
        })

    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False)
    print(f"\n📁 Data exported to {filename}")

def analyze_repo(owner, repo, export=False):
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

    if export:
        export_to_csv(
            repo_data,
            contributors,
            (open_issues, closed_issues),
            (open_prs, closed_prs)
        )


@click.command()
@click.option('--owner', prompt='GitHub Owner', help='The username or organization that owns the repo')
@click.option('--repo', prompt='Repository Name', help='The name of the GitHub repository')
@click.option('--export', is_flag=True, help='Export the results to CSV')


def main(owner, repo, export):
    analyze_repo(owner, repo, export)


if __name__ == "__main__":
    main()