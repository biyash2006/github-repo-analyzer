import requests

# This function gets info about a GitHub repo
def analyze_repo():
    url = "https://api.github.com/repos/facebook/react"
    response = requests.get(url)
    data = response.json()

    # Print some basic details
    print("📘 Repository:", data["full_name"])
    print("⭐ Stars:", data["stargazers_count"])
    print("🍴 Forks:", data["forks_count"])
    print("🐞 Open Issues:", data["open_issues_count"])

# Run the function
analyze_repo()