import httpx
import os
import logging
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com/"
logger = logging.getLogger(__name__)

async def create_github_repo(repo_name: str) -> dict:
    headers = {"Authorization":f"Bearer {GITHUB_TOKEN}",
               'Accept': 'application/vnd.github+json'
               }
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

def push_to_repo():
    return

def get_latest_sha():
    return

def enable_github_pages():
    pass


async def notify_evaluation_url(evaluation_url: str, payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(evaluation_url, json=payload, timeout=10.0)
            response.raise_for_status()
        except httpx.HTTPError as e:
            # Log error or handle failure as needed
            print(f"Failed to notify evaluation URL: {e}")
