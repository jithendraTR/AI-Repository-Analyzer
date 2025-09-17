"""
Thomson Reuters Open Arena AI Client
Handles API communication with the Thomson Reuters AI Arena
"""

import requests
import os
from typing import Dict, Any, Optional
import logging

class OpenArenaClient:
    """Client for Thomson Reuters Open Arena AI API"""
    
    def __init__(self):
        self.base_url = os.getenv('OPEN_ARENA_THOMSON_REUTERS_URL', 
                                 'https://aiopenarena.gcs.int.thomsonreuters.com/v1/inference')
        self.workflow_id = os.getenv('AI_ARENA_WORKFLOW_ID', 
                                   'eded8958-bd45-4cbf-bf44-5de6c0b00c7c')
        self.esso_token = os.getenv('ESSO_TOKEN')
        
        if not self.esso_token:
            raise ValueError("ESSO_TOKEN environment variable is required")
        
        self.headers = {
            "Authorization": f"Bearer {self.esso_token}",
            "Content-Type": "application/json"
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def query(self, prompt: str, is_persistence_allowed: bool = False, timeout: int = 120) -> Optional[str]:
        """
        Send a query to the Thomson Reuters AI Arena
        
        Args:
            prompt: The query/prompt to send to the AI
            is_persistence_allowed: Whether to allow persistence of the query
            timeout: Request timeout in seconds (default: 120)
            
        Returns:
            The AI response or None if error occurred
        """
        payload = {
            "workflow_id": self.workflow_id,
            "query": prompt,
            "is_persistence_allowed": is_persistence_allowed
        }
        
        try:
            self.logger.info(f"Sending query to AI Arena: {prompt[:100]}...")
            
            # Add timeout and retry logic
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                json=payload,
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("answer", "")
                self.logger.info("Successfully received AI response")
                return answer
            elif response.status_code == 429:
                self.logger.warning("Rate limit exceeded, retrying after delay...")
                import time
                time.sleep(2)  # Wait 2 seconds before retry
                # Retry once
                response = requests.post(
                    self.base_url, 
                    headers=self.headers, 
                    json=payload,
                    timeout=timeout
                )
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("answer", "")
                    self.logger.info("Successfully received AI response on retry")
                    return answer
                else:
                    self.logger.error(f"API Error on retry: {response.status_code} - {response.text}")
                    return None
            else:
                self.logger.error(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            self.logger.error(f"Request timed out after {timeout} seconds")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return None
    
    def analyze_code(self, code_snippet: str, analysis_type: str) -> Optional[str]:
        """
        Analyze code snippet with specific analysis type
        
        Args:
            code_snippet: The code to analyze
            analysis_type: Type of analysis (e.g., 'tech_debt', 'patterns', 'risks')
            
        Returns:
            Analysis result or None if error occurred
        """
        prompt = f"""
        Please analyze the following code for {analysis_type}:
        
        ```
        {code_snippet}
        ```
        
        Provide detailed insights about:
        - Key findings
        - Recommendations
        - Potential issues
        - Best practices
        """
        
        return self.query(prompt)
    
    def get_architectural_insights(self, file_structure: str, code_samples: str) -> Optional[str]:
        """
        Get architectural insights from file structure and code samples
        
        Args:
            file_structure: String representation of project structure
            code_samples: Representative code samples
            
        Returns:
            Architectural insights or None if error occurred
        """
        prompt = f"""
        Analyze this codebase structure and provide architectural insights:
        
        File Structure:
        {file_structure}
        
        Code Samples:
        {code_samples}
        
        Please provide insights on:
        - Architecture patterns used
        - Integration points
        - Potential areas for new features
        - System boundaries
        - Technical constraints
        """
        
        return self.query(prompt)
    
    def analyze_dependencies(self, dependencies: str) -> Optional[str]:
        """
        Analyze project dependencies for governance and risk assessment
        
        Args:
            dependencies: String representation of project dependencies
            
        Returns:
            Dependency analysis or None if error occurred
        """
        prompt = f"""
        Analyze these project dependencies for version governance and risks:
        
        {dependencies}
        
        Please provide:
        - Outdated dependencies
        - Security vulnerabilities
        - Version conflicts
        - Upgrade recommendations
        - Maintenance risks
        """
        
        return self.query(prompt)
    
    def detect_patterns(self, code_files: Dict[str, str]) -> Optional[str]:
        """
        Detect development patterns across multiple files
        
        Args:
            code_files: Dictionary of filename -> code content
            
        Returns:
            Pattern analysis or None if error occurred
        """
        files_content = "\n\n".join([f"File: {filename}\n{content}" 
                                   for filename, content in code_files.items()])
        
        prompt = f"""
        Analyze these code files to identify development patterns:
        
        {files_content}
        
        Please identify:
        - Design patterns used
        - Coding conventions
        - Framework usage patterns
        - Anti-patterns
        - Consistency issues
        """
        
        return self.query(prompt)
