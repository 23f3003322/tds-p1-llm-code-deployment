from .models import TaskRequest
from .deployer import create_github_repo,notify_evaluation_url


def round2():
    print("inside round 2")


async def  round1(request: TaskRequest):
    try:
        repo_response = await create_github_repo(repo_name=request.task)
        repo_url = repo_response.get("html_url", "")
        # Temporary placeholders for commit_sha and pages_url
        commit_sha = ""
        pages_url = ""

        # Prepare payload
        payload = {
            "email": request.email,
            "task": request.task,
            "round": request.round,
            "nonce": request.nonce,
            "repo_url": repo_url,
            "commit_sha": commit_sha,
            "pages_url": pages_url,
        }
        await notify_evaluation_url(request.evaluation_url, payload)
    except Exception as e:
        print(f"Error in background task: {e}")
