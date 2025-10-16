import logging
from typing import List
from pydantic_ai import Agent
from .models import TaskRequest,FileContext

# Configure module-level logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



async def genereate_code_with_llm(request: TaskRequest) -> List[FileContext]:
    prompt = f"""
Generate a complete static website project that is deployable on GitHub Pages.

Brief: {request.brief}

Requirements:
- Provide all files necessary for deployment including at least an index.html.
- Write a thorough README.md that includes:
  - Project summary
  - Setup instructions for GitHub Pages
  - Usage guide
  - Explanation of the main code/files
  - License information (use MIT)
- The project must follow industry standards for static GitHub Pages hosting.
- Return the project as a list of files with filenames and file contents.
- All code should be modern and ready to deploy without modification.
Output format:
Return only a JSON array of objects where each object has:
- "file_name": string
- "file_content": string
"""

    system_prompt = """
You are a highly experienced senior developer specializing in creating GitHub Pages-ready static websites.

Your task is to generate a production-ready, modern, and industry-standard static website project based on the user’s brief.

Specifically, ensure you do the following:

1. Create all necessary files to fully deploy a static website on GitHub Pages, including but not limited to:
   - index.html (the homepage)
   - any required CSS, JS, or asset files
   - configuration files (e.g., CNAME, if needed)
2. Write a complete, professional README.md file containing:
   - A clear project summary describing what the site does
   - Setup instructions to deploy the project on GitHub Pages step-by-step
   - Usage instructions, explaining how to use the website
   - Explanation of the key code files and their purpose
   - License information, applying the MIT license in standard format
3. Ensure all source code and resources are clean, properly structured, and follow modern best practices
4. Format your output as a list of files, with each containing a file_name and file_content field
5. Do not include text explanations in the output; only return the code files and README as specified
6. Output format:
Return only a JSON array of objects where each object has:
- "file_name": string
- "file_content": string

The user will provide a brief describing the site functionality. Use that to guide your file generation.

Focus on quality, clarity, and correctness to deliver a ready-to-use GitHub Pages static website project.
"""

    try:
        agent = Agent(
            "openai:gpt-5-nano",
            result_type=List[FileContext],
            system_prompt=system_prompt
        )
        result = await agent.run(prompt)
        logger.info("Successfully generated code with LLM")
        # print(result.data)
        return result.data
    except Exception as e:
        # Log the error with traceback
        logger.error(f"Error generating code with LLM: {e}", exc_info=True)
        # Raise runtime error to caller or optionally return empty list/fallback output
        raise RuntimeError(f"LLM code generation failed: {e}") from e
