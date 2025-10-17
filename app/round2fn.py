# # Updated Round 2 Function with Correct Pydantic Models
# # This function works with the actual task format and FileContext models

# import json
# # import re
# from typing import Dict, List, Optional, Any
# from pydantic import BaseModel
# from pydantic_ai import Agent, RunContext
# from .models import FileContext,TaskRequest
# import logging

# import os
# from dotenv import load_dotenv
# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)


# # Pydantic models matching the provided format
# # class FileContext(BaseModel):
# #     file_name: str
# #     file_content: str

# class TaskObject(BaseModel):
#     email: str
#     secret: str
#     task: str
#     round: int
#     nonce: str
#     brief: str
#     checks: List[Dict[str, str]]
#     evaluation_url: str
#     attachments: List[str]

# class ValidationCheck(BaseModel):
#     js: str

# class CodeAnalysisContext(BaseModel):
#     original_files: List[FileContext]
#     task_brief: str
#     validation_checks: List[ValidationCheck]
#     attachments: List[str]

# class ModificationResult(BaseModel):
#     """Pydantic model for the complete modification result"""
#     modified_files: List[FileContext]
#     validation_status: Dict[str, bool]
#     summary: str

# def simulate_js_validation(html_content: str, js_content: str, check: ValidationCheck) -> bool:
#     """
#     Simulate JavaScript validation by analyzing code patterns
#     This is a simplified version - in production you'd use a proper JS engine
#     """
#     combined_content = html_content + "\n" + js_content
    
#     try:
#         check_code = check.js
        
#         # Check for element existence with tagName
#         if "document.querySelector" in check_code and ".tagName" in check_code:
#             selector_match = re.search(r'document\.querySelector\("([^"]+)"\)', check_code)
#             tag_match = re.search(r'tagName === "([^"]+)"', check_code)
            
#             if selector_match and tag_match:
#                 selector = selector_match.group(1)
#                 expected_tag = tag_match.group(1)
                
#                 # Check if HTML contains element with that ID and tag
#                 pattern = rf'<{expected_tag.lower()}[^>]*id=["\']?{re.escape(selector.replace("#", ""))}'
#                 return bool(re.search(pattern, combined_content, re.IGNORECASE))
        
#         # Check for text content includes
#         if ".textContent.includes" in check_code:
#             selector_match = re.search(r'document\.querySelector\("([^"]+)"\)', check_code)
#             text_match = re.search(r'textContent\.includes\("([^"]+)"\)', check_code)
            
#             if selector_match and text_match:
#                 expected_text = text_match.group(1)
#                 return expected_text in combined_content
        
#         # Check for script content includes
#         if "script" in check_code.lower() and "textContent.includes" in check_code:
#             url_match = re.search(r'textContent\.includes\("([^"]+)"\)', check_code)
#             if url_match:
#                 expected_content = url_match.group(1)
#                 return expected_content in combined_content
        
#         # Check for attributes (like aria-live)
#         if ".getAttribute" in check_code:
#             selector_match = re.search(r'document\.querySelector\("([^"]+)"\)', check_code)
#             attr_match = re.search(r'getAttribute\("([^"]+)"\)', check_code)
#             value_match = re.search(r'=== "([^"]+)"', check_code)
            
#             if selector_match and attr_match and value_match:
#                 selector = selector_match.group(1).replace("#", "")
#                 attr_name = attr_match.group(1)
#                 expected_value = value_match.group(1)
                
#                 # Look for element with ID and attribute
#                 id_pattern = rf'id=["\']?{re.escape(selector)}["\']?'
#                 attr_pattern = rf'{re.escape(attr_name)}=["\']?{re.escape(expected_value)}["\']?'
                
#                 # Check if both ID and attribute exist in the content
#                 has_id = bool(re.search(id_pattern, combined_content, re.IGNORECASE))
#                 has_attr = bool(re.search(attr_pattern, combined_content, re.IGNORECASE))
                
#                 return has_id and has_attr
        
#         # Check for double negation patterns (!!expression)
#         if check_code.startswith("!!"):
#             inner_check = check_code[2:]  # Remove !!
#             # Recursively check the inner expression
#             inner_validation = ValidationCheck(js=inner_check)
#             return simulate_js_validation(html_content, js_content, inner_validation)
        
#         return False
        
#     except Exception as e:
#         print(f"Validation error: {e}")
#         return False

# def analyze_existing_codebase(files: List[FileContext]) -> Dict[str, Any]:
#     """Analyze the existing codebase to understand its structure and functionality"""
#     analysis = {
#         "html_files": [],
#         "css_files": [],
#         "js_files": [],
#         "other_files": [],
#         "existing_elements": [],
#         "scripts_and_apis": []
#     }
    
#     for file in files:
#         file_ext = file.file_name.split('.')[-1].lower()
        
#         if file_ext == 'html':
#             analysis["html_files"].append(file)
#             # Extract form elements, IDs, classes
#             ids = re.findall(r'id=["\']([^"\']+)["\']', file.file_content)
#             analysis["existing_elements"].extend([f"#{id_val}" for id_val in ids])
            
#         elif file_ext == 'css':
#             analysis["css_files"].append(file)
            
#         elif file_ext == 'js':
#             analysis["js_files"].append(file)
#             # Extract API calls and functions
#             api_calls = re.findall(r'https://[^\s"\']+', file.file_content)
#             analysis["scripts_and_apis"].extend(api_calls)
            
#         else:
#             analysis["other_files"].append(file)
    
#     return analysis

# # Initialize Pydantic AI Agent
# code_modification_agent = Agent(
#     "openai:gpt-5-nano",
#     deps_type=CodeAnalysisContext,
#     result_type=ModificationResult,
#     system_prompt="""You are an expert web developer tasked with making minimal, targeted modifications to an existing GitHub Pages codebase.

# Your responsibilities:
# 1. Analyze the existing code structure and functionality thoroughly
# 2. Make ONLY the minimal changes needed to implement the new brief requirements
# 3. Do NOT rewrite entire files or change the overall structure
# 4. Ensure all modifications will pass the provided JavaScript validation checks
# 5. Update files to include new functionality while preserving existing features
# 6. Focus on GitHub Pages compatibility (static HTML, CSS, JS only)

# Guidelines:
# - Add new elements, functions, or styles incrementally
# - Modify existing code only when absolutely necessary
# - Test your changes against validation checks mentally before finalizing
# - Keep the same coding style and patterns as the original code
# - If checks require specific elements or attributes, ensure they are added
# - Pay special attention to accessibility attributes like aria-live when required"""
# )

# @code_modification_agent.tool
# async def analyze_codebase_structure(ctx: RunContext[CodeAnalysisContext]) -> str:
#     """Analyze the structure and functionality of the existing codebase"""
#     analysis = analyze_existing_codebase(ctx.deps.original_files)
    
#     summary = []
#     summary.append(f"Found {len(analysis['html_files'])} HTML files")
#     summary.append(f"Found {len(analysis['css_files'])} CSS files")  
#     summary.append(f"Found {len(analysis['js_files'])} JavaScript files")
#     summary.append(f"Existing elements: {', '.join(analysis['existing_elements'][:10])}")
#     summary.append(f"API endpoints used: {', '.join(analysis['scripts_and_apis'][:3])}")
    
#     return "\n".join(summary)

# @code_modification_agent.tool
# async def get_task_requirements(ctx: RunContext[CodeAnalysisContext]) -> str:
#     """Get the new task requirements and brief"""
#     brief = f"Task Brief: {ctx.deps.task_brief}"
    
#     if ctx.deps.attachments:
#         brief += f"\nAttachments: {', '.join(ctx.deps.attachments)}"
    
#     brief += "\n\nValidation checks that MUST pass:"
#     for i, check in enumerate(ctx.deps.validation_checks):
#         brief += f"\n{i+1}. {check.js}"
        
#     return brief

# @code_modification_agent.tool
# async def validate_against_checks(ctx: RunContext[CodeAnalysisContext], modified_files: List[FileContext]) -> Dict[str, bool]:
#     """Validate modified files against the JavaScript validation checks"""
#     results = {}
    
#     # Combine all HTML and JS content for validation
#     html_content = ""
#     js_content = ""
    
#     for file in modified_files:
#         if file.file_name.endswith('.html'):
#             html_content += file.file_content + "\n"
#         elif file.file_name.endswith('.js'):
#             js_content += file.file_content + "\n"
    
#     for i, check in enumerate(ctx.deps.validation_checks):
#         try:
#             is_valid = simulate_js_validation(html_content, js_content, check)
#             results[f"check_{i}"] = is_valid
#         except Exception as e:
#             results[f"check_{i}"] = False
            
#     return results

# @code_modification_agent.tool
# async def suggest_file_modifications(ctx: RunContext[CodeAnalysisContext]) -> str:
#     """Analyze what modifications are needed for each file based on the task brief and checks"""
    
#     brief = ctx.deps.task_brief.lower()
#     suggestions = []
    
#     # Analyze what the checks require
#     required_elements = set()
#     required_attributes = {}
#     required_content = []
    
#     for check in ctx.deps.validation_checks:
#         check_js = check.js
        
#         # Extract required selectors
#         selector_matches = re.findall(r'document\.querySelector\("([^"]+)"\)', check_js)
#         for selector in selector_matches:
#             required_elements.add(selector)
        
#         # Extract required attributes
#         if ".getAttribute" in check_js:
#             attr_match = re.search(r'getAttribute\("([^"]+)"\).*?=== "([^"]+)"', check_js)
#             if attr_match:
#                 attr_name, attr_value = attr_match.groups()
#                 selector_match = re.search(r'querySelector\("([^"]+)"\)', check_js)
#                 if selector_match:
#                     element_selector = selector_match.group(1)
#                     required_attributes[element_selector] = (attr_name, attr_value)
        
#         # Extract required content
#         if "textContent.includes" in check_js:
#             content_match = re.search(r'textContent\.includes\("([^"]+)"\)', check_js)
#             if content_match:
#                 required_content.append(content_match.group(1))
    
#     suggestions.append(f"Brief requires: {brief}")
#     suggestions.append(f"Required elements: {', '.join(required_elements)}")
#     suggestions.append(f"Required attributes: {required_attributes}")
#     suggestions.append(f"Required content: {', '.join(required_content)}")
    
#     return "\n".join(suggestions)

# async def round2_code_modification_function(
#     files: List[FileContext],
#     task_object: Dict[str, Any]
# ) -> List[FileContext]:
#     """
#     Round 2 function that modifies existing GitHub repository files using Pydantic AI
    
#     Args:
#         files: List of FileContext objects from GitHub repository
#         task_object: Dictionary containing brief, checks, attachments, etc.
    
#     Returns:
#         List[FileContext]: Modified files ready for GitHub Pages deployment
#     """
#     print("call is here")
#     try:
#         # Parse task object
#         task = task_object
        
#         # Convert checks to ValidationCheck objects
#         validation_checks = [ValidationCheck(js=check['js']) for check in task.checks]
        
#         # Create context for the AI agent
#         context = CodeAnalysisContext(
#             original_files=files,
#             task_brief=task.brief,
#             validation_checks=validation_checks,
#             attachments=task.attachments
#         )
        
#         # Create the prompt for the AI agent
#         prompt = f"""Analyze the existing codebase and implement the following requirement with minimal changes:

# BRIEF: {task.brief}

# VALIDATION CHECKS that must pass:
# {chr(10).join([f"- {check['js']}" for check in task.checks])}

# REQUIREMENTS:
# 1. Make only targeted modifications to implement the new functionality
# 2. Do not rewrite entire files - add incrementally to existing code
# 3. Ensure ALL JavaScript validation checks pass
# 4. Maintain GitHub Pages compatibility
# 5. Preserve all existing functionality
# 6. Add new elements/attributes/functionality as required by the checks

# Please analyze the code, understand the requirements, and provide the modified files that will pass all validation checks."""

#         # Run the Pydantic AI agent
#         result =await code_modification_agent.run(prompt, deps=context)
#         print("Raw LLM output:", result.raw_output)
#         print("Parsed data:", result.data)
#         # Return the modified files in the required format
#         return result.data.modified_files
        
#     except Exception as e:
#         # Fallback: return original files if modification fails
#         print(f"Error in code modification: {str(e)}")
#         # return files

# # Example usage matching the provided format
# if __name__ == "__main__":
#     # Example files in FileContext format
#     example_files = [
#         FileContext(
#             file_name="index.html",
#             file_content='''<!DOCTYPE html>
# <html>
# <head>
#     <title>GitHub User Info</title>
#     <link rel="stylesheet" href="style.css">
# </head>
# <body>
#     <form id="github-user-123">
#         <input type="text" id="username" placeholder="Enter GitHub username">
#         <button type="submit">Get User Info</button>
#     </form>
#     <div id="github-created-at"></div>
#     <script src="script.js"></script>
# </body>
# </html>'''
#         ),
#         FileContext(
#             file_name="script.js",
#             file_content='''document.getElementById('github-user-123').addEventListener('submit', async function(e) {
#     e.preventDefault();
#     const username = document.getElementById('username').value;
#     const response = await fetch(`https://api.github.com/users/${username}`);
#     const user = await response.json();
#     document.getElementById('github-created-at').textContent = user.created_at.split('T')[0];
# });'''
#         ),
#         FileContext(
#             file_name="style.css",
#             file_content='''body {
#     font-family: Arial, sans-serif;
#     margin: 20px;
# }

# form {
#     margin-bottom: 20px;
# }

# input, button {
#     padding: 10px;
#     margin: 5px;
# }'''
#         )
#     ]
    
#     # Example task object matching the provided format
#     example_task = {
#         "email": "student@example.com",
#         "secret": "shamil", 
#         "task": "test-round2-1",
#         "round": 2,
#         "nonce": "ab12-...",
#         "brief": "Display the account age in whole years inside #github-account-age alongside the creation date.",
#         "checks": [
#             {
#                 "js": "document.querySelector(\"#github-status\").getAttribute(\"aria-live\") === \"polite\""
#             },
#             {
#                 "js": "!!document.querySelector(\"script\").textContent.includes(\"github-status\")"
#             }
#         ],
#         "evaluation_url": "http://0.0.0.0:8001/notify",
#         "attachments": []
#     }
    
#     # Run the function
#     modified_files = round2_code_modification_function(
#         files=example_files,
#         task_object=example_task
#     )
    
#     print("Modified Files:")
#     for file in modified_files:
#         print(f"\n--- {file.file_name} ---")
#         print(file.file_content[:300] + "..." if len(file.file_content) > 300 else file.file_content)





# This version removes most complexity to prevent loops

from typing import Dict, List, Any
from pydantic import BaseModel
from pydantic_ai import Agent
from .models import FileContext
import json

# Minimal agent setup









        # prompt = f"""Analyze the existing codebase and implement the following requirement with minimal changes:

        # FILES TO MODIFY: {json.dumps(files_info, indent=2)}

        # BRIEF: {brief}

        # attachments (if any): {attachments_text}

        # CHECKS (for reference): {checks}

        # REQUIREMENTS:
        # 1. Make only targeted modifications to implement the new functionality
        # 2. Do not rewrite entire files - add incrementally to existing code
        # 3. Ensure ALL JavaScript validation checks pass
        # 4. Maintain GitHub Pages compatibility
        # 5. Preserve all existing functionality
        # 6. update/add  elements/attributes/functionality as required by the checks
        # 7. update the readme file with the changes made
        # 8. Do not include text explanations in the output; only return the code files and README as specified
        # 9. code should be ready to deploy in Github pages
        # 10. Output format:
        #     Return only a JSON array of objects where each object has:
        #     - "file_name": string
        #     - "file_content": string

        # Please analyze the code, understand the requirements, and provide the modified files that will pass all validation checks."""
