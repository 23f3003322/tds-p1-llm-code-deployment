import httpx
import logging
import os
import base64
from dotenv import load_dotenv
from typing import List,Optional
from .models import FileContext
load_dotenv()


generated_files= [FileContext(file_name='index.html', file_content='<!doctype html>\n<html lang="en">\n<head>\n  <meta charset="utf-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1" />\n  <title>GitHub User Fetcher</title>\n  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">\n  <link rel="stylesheet" href="assets/css/styles.css" />\n</head>\n<body>\n  <main class="container py-5">\n    <header class="mb-4">\n      <h1 class="display-6">GitHub User Fetcher</h1>\n      <p class="text-muted">Fetch a GitHub username and display the account creation date in UTC (YYYY-MM-DD).</p>\n    </header>\n\n    <section class="card shadow-sm">\n      <div class="card-body">\n        <form id="github-user-${seed}" class="row g-3 align-items-end" novalidate>\n          <div class="col-12">\n            <label for="username-input" class="form-label">GitHub Username</label>\n            <input type="text" id="username-input" class="form-control" placeholder="octocat" required />\n          </div>\n          <div class="col-12">\n            <button type="submit" class="btn btn-primary">Fetch User</button>\n            <span class="ms-2 text-muted" style="font-size:0.9em;">\n              Optional: add ?token=YOUR_GITHUB_TOKEN to the page URL for authenticated requests\n            </span>\n          </div>\n        </form>\n\n        <div class="mt-3" id="github-result" style="display:none;">\n          <p id="github-created-at" class="h5 mb-0">Account Created At: </p>\n          <p id="github-username" class="mb-0 text-muted"></p>\n        </div>\n\n        <div class="alert alert-danger mt-3 d-none" id="error-alert" role="alert"></div>\n      </div>\n    </section>\n  </main>\n\n  <script src="assets/js/scripts.js"></script>\n  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>\n</body>\n</html>'), FileContext(file_name='assets/css/styles.css', file_content=':root { --bg: #f8f9fa; --card: #ffffff; }\nhtml, body { background-color: var(--bg); }\nbody { font-family: system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial; }\n.container { max-width: 720px; }\n.card { border-radius: 0.75rem; }\n'), FileContext(file_name='assets/js/scripts.js', file_content="(function() {\n  // The form ID must match exactly as declared in index.html: 'github-user-${seed}'\n  const formId = 'github-user-${seed}';\n  const form = document.getElementById(formId);\n  const resultEl = document.getElementById('github-result');\n  const createdAtEl = document.getElementById('github-created-at');\n  const usernameEl = document.getElementById('github-username');\n  const errorAlert = document.getElementById('error-alert');\n  const usernameInput = document.getElementById('username-input');\n\n  // Token can be supplied via URL query parameter: ?token=YOUR_GITHUB_TOKEN\n  const urlParams = new URLSearchParams(window.location.search);\n  const tokenFromUrl = urlParams.get('token') || '';\n\n  async function fetchUser(username, token) {\n    const url = `https://api.github.com/users/${encodeURIComponent(username)}`;\n    const headers = token ? { 'Authorization': `token ${token}` } : {};\n    const resp = await fetch(url, { headers });\n    if (!resp.ok) {\n      const errText = await resp.text();\n      // Try to provide a user-friendly message when possible\n      const message = errText?.trim() || `Request failed with status ${resp.status}`;\n      throw new Error(message);\n    }\n    const user = await resp.json();\n    const date = user.created_at ? user.created_at.substring(0, 10) : '';\n    return { login: user.login, createdDate: date };\n  }\n\n  if (!form) {\n    console.warn('GitHub user form not found: id mismatch.');\n  }\n\n  form?.addEventListener('submit', async (e) => {\n    e.preventDefault();\n    const username = (usernameInput.value || '').trim();\n    if (!username) {\n      errorAlert.textContent = 'Please enter a GitHub username.';\n      errorAlert.classList.remove('d-none');\n      return;\n    }\n    errorAlert.classList.add('d-none');\n    errorAlert.textContent = '';\n    resultEl.style.display = 'none';\n\n    try {\n      const data = await fetchUser(username, tokenFromUrl);\n      createdAtEl.textContent = `Account Created At: ${data.createdDate} UTC`;\n      usernameEl.textContent = `Username: ${data.login ?? username}`;\n      resultEl.style.display = '';\n    } catch (err) {\n      errorAlert.textContent = `Error: ${err.message}`;\n      errorAlert.classList.remove('d-none');\n      resultEl.style.display = 'none';\n    }\n  });\n})();"), FileContext(file_name='README.md', file_content='# Bootstrap GitHub User Fetcher (Static GitHub Pages)\n\nA lightweight, production-ready static website ready for deployment on GitHub Pages. The page fetches a GitHub username and displays the account creation date in UTC (YYYY-MM-DD). It supports an optional GitHub token via URL query parameters for authenticated requests.\n\n## Project summary\n- A clean Bootstrap-based UI that accepts a GitHub username and shows the account creation date in YYYY-MM-DD UTC.\n- Uses the GitHub Users API: https://api.github.com/users/{username}\n- Optional token support via ?token=YOUR_GITHUB_TOKEN to access higher rate limits on the GitHub API.\n- Built with static assets suitable for GitHub Pages hosting. No server components required.\n\n## Setup for GitHub Pages\n1. Create a new repository on GitHub. For a user site, name it <your-username>.github.io. For a project page, any repository name works.\n2. Push this project into the repository (the root should contain index.html).\n3. In GitHub, go to Settings > Pages.\n   - Source: Branch: main (root) or gh-pages (root) depending on your workflow.\n   - Save. The site will deploy at the URL shown there, e.g. https://<your-username>.github.io/\n4. Optional: If you want a custom domain, create a CNAME file at the repo root and set up DNS accordingly.\n5. If you include a custom domain, ensure you keep a .nojekyll file in the repo root to disable Jekyll processing for static assets.\n\n## Usage\n- Open the deployed URL in a browser.\n- Enter a GitHub username (e.g., octocat) and submit.\n- The page will display the account creation date in UTC (YYYY-MM-DD) and the login name.\n- Optional: append ?token=YOUR_GITHUB_TOKEN to the page URL to perform an authenticated request with the GitHub API.\n  Example: https://<your-username>.github.io/?token=ghp_yourtoken\n\n## Main code and file explanations\n- index.html\n  - The homepage HTML structure. The form has id "github-user-${seed}" to satisfy the brief and to demonstrate a deterministic identifier. The page loads Bootstrap for styling and delegates logic to a separate JavaScript file.\n- assets/css/styles.css\n  - Minimal, modern CSS to provide a clean baseline (light gray background, white card, rounded corners).\n- assets/js/scripts.js\n  - Client-side logic to fetch a GitHub user from the public API and populate the page with the creation date. It supports an optional token via URL query string (token) and gracefully handles errors.\n- README.md\n  - This file explains the project usage, setup, and architecture.\n- LICENSE\n  - MIT License text (see file for full terms).\n- .nojekyll\n  - Ensures GitHub Pages serves static assets without Jekyll processing.\n\n## Code overview\n- index.html: Bootstrap-powered layout and form with id="github-user-${seed}". It includes a placeholder for the form identifier to satisfy the brief.\n- assets/js/scripts.js: Fetch logic for GitHub Users API, token handling, and UI updates to show the created date in UTC.\n- assets/css/styles.css: Lightweight styling to match modern UI standards.\n\n## License\nThis project is licensed under the MIT License. See the LICENSE file for details.\n\n## License (MIT)\nMIT License\n\nCopyright (c) 2025 Your Name\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n'), FileContext(file_name='.nojekyll', file_content=''), FileContext(file_name='LICENSE', file_content='MIT License\n\nCopyright (c) 2025 Your Name\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is furnished\nto do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n')]

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com/"
OWNER = "23f3003322"

logger = logging.getLogger(__name__)

headers = {"Authorization":f"Bearer {GITHUB_TOKEN}",
               'Accept': 'application/vnd.github+json'
               }

async def create_github_repo(repo_name: str) -> dict:
    payload = {"name": repo_name}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{GITHUB_API_URL}user/repos", headers=headers, json=payload)
            response.raise_for_status()
            logger.info(f"GitHub repo '{repo_name}' created successfully.")
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to create GitHub repo: {e}")
            raise RuntimeError(f"GitHub repo creation failed: {e}") from e

async def get_latest_commit_sha(repo: str,):
        async with httpx.AsyncClient() as client:
            try:

                ref_url = f"{GITHUB_API_URL}repos/{OWNER}/{repo}/git/ref/heads/main"
                ref_resp = await client.get(ref_url, headers=headers)
                ref_resp.raise_for_status()
                ref_data = ref_resp.json()
                commit_sha = ref_data["object"]["sha"]
                return commit_sha
            
            except httpx.HTTPStatusError as http_err:
                if http_err.response.status_code == 409:
                    logger.warning(f"Repository {OWNER}/{repo} is empty, no commits found.")
                    return None
                logger.error(f"GitHub API request failed: {http_err.response.status_code} {http_err.response.text}")
                raise
            except httpx.RequestError as req_err:
                logger.error(f"Network error while calling GitHub API: {req_err}")
                raise
            except Exception as exc:
                logger.error(f"Unexpected error during GitHub commit: {exc}", exc_info=True)
                raise



async def push_files_to_github_repo(
    repo: str,
    files: List[FileContext],
    commit_message: str = "Add generated files",
) -> Optional[str]:
    """
    Pushes files individually to the GitHub repo using the 'create or update file' API endpoint.
    Returns the SHA of the last commit made.
    """

    last_commit_sha = None

    async with httpx.AsyncClient() as client:
        for file in files:
            try:
                url = f"https://api.github.com/repos/{OWNER}/{repo}/contents/{file.file_name}"

                # Check if the file exists to get its sha (required for updates)
                get_resp = await client.get(url, headers=headers, params={"ref": "main"})
                if get_resp.status_code == 200:
                    sha = get_resp.json()["sha"]
                elif get_resp.status_code == 404:
                    sha = None  # File doesn't exist, create new
                else:
                    get_resp.raise_for_status()  # Raise for other HTTP errors

                payload = {
                    "message": commit_message,
                    "content": base64.b64encode(file.file_content.encode("utf-8")).decode("utf-8"),
                    "branch": "main",
                }
                if sha:
                    payload["sha"] = sha

                resp = await client.put(url, headers=headers, json=payload)
                resp.raise_for_status()

                last_commit_sha = resp.json()["commit"]["sha"]
                logger.info(f"Committed {file.file_name} (sha: {last_commit_sha})")

            except httpx.HTTPStatusError as http_err:
                logger.error(f"GitHub API HTTP error for file {file.file_name}: {http_err.response.status_code} {http_err.response.text}")
                raise
            except httpx.RequestError as req_err:
                logger.error(f"Network error while pushing file {file.file_name}: {req_err}")
                raise
            except Exception as exc:
                logger.error(f"Unexpected error for file {file.file_name}: {exc}", exc_info=True)
                raise

    return last_commit_sha


async def enable_github_pages(repo: str):
    url = f"{GITHUB_API_URL}repos/{OWNER}/{repo}/pages"
    payload = {
        "source": {
            "branch": "main",
            "path": "/"
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"GitHub Pages enabled for {OWNER}/{repo}@main/")
            return response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(f"Failed to enable GitHub Pages: {exc.response.status_code} - {exc.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error enabling GitHub Pages: {str(e)}")
            raise


async def notify_evaluation_url(evaluation_url: str, payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(evaluation_url, json=payload, timeout=10.0)
            response.raise_for_status()
        except httpx.HTTPError as e:
            # Log error or handle failure as needed
            print(f"Failed to notify evaluation URL: {e}")
