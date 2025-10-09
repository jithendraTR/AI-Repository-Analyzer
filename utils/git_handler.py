"""
Git Repository Handler
Handles cloning, validation, and cleanup of Git repositories
"""

import os
import re
import shutil
import subprocess
import tempfile
import urllib.parse
from typing import Dict, Any, Optional, Tuple


class GitHandler:
    """Handles Git repository operations with non-interactive mode"""
    
    def __init__(self):
        self.temp_dirs = []  # Track temporary directories for cleanup
    
    def parse_git_url(self, url: str) -> Dict[str, Any]:
        """
        Parse various Git URL formats and extract components
        
        Supported formats:
        - https://github.com/owner/repo
        - https://github.com/owner/repo.git
        - git@github.com:owner/repo.git
        - https://github.com/owner/repo/tree/branch/subfolder
        - https://github.com/owner/repo?ref=branch
        """
        result = {
            'is_git_url': False,
            'url': url,
            'clean_url': None,
            'ref': None,
            'subfolder': None,
            'protocol': None,
            'host': None,
            'owner': None,
            'repo': None,
            'error': None
        }
        
        try:
            # Check for SSH format first
            ssh_pattern = r'^git@([^:]+):([^/]+)/([^/]+?)(?:\.git)?(?:/.*)?$'
            ssh_match = re.match(ssh_pattern, url)
            
            if ssh_match:
                result['is_git_url'] = True
                result['protocol'] = 'ssh'
                result['host'] = ssh_match.group(1)
                result['owner'] = ssh_match.group(2)
                result['repo'] = ssh_match.group(3)
                result['clean_url'] = f"git@{result['host']}:{result['owner']}/{result['repo']}.git"
                return result
            
            # Parse HTTPS URLs
            if url.startswith('https://') or url.startswith('http://'):
                # Handle query parameters (e.g., ?ref=branch)
                if '?' in url:
                    base_url, query_string = url.split('?', 1)
                    params = urllib.parse.parse_qs(query_string)
                    if 'ref' in params:
                        result['ref'] = params['ref'][0]
                else:
                    base_url = url
                
                # Parse the base URL
                parsed = urllib.parse.urlparse(base_url)
                result['host'] = parsed.netloc
                path_parts = parsed.path.strip('/').split('/')
                
                if len(path_parts) >= 2:
                    result['is_git_url'] = True
                    result['protocol'] = 'https'
                    result['owner'] = path_parts[0]
                    result['repo'] = path_parts[1]
                    
                    # Remove .git suffix if present
                    if result['repo'].endswith('.git'):
                        result['repo'] = result['repo'][:-4]
                    
                    # Handle GitHub tree URLs (e.g., /tree/branch/subfolder)
                    if len(path_parts) >= 4 and path_parts[2] == 'tree':
                        if not result['ref']:  # Don't override query param ref
                            result['ref'] = path_parts[3]
                        if len(path_parts) > 4:
                            result['subfolder'] = '/'.join(path_parts[4:])
                    
                    # Build clean clone URL
                    if result['host'] in ['github.com', 'gitlab.com', 'bitbucket.org']:
                        result['clean_url'] = f"https://{result['host']}/{result['owner']}/{result['repo']}.git"
                    else:
                        result['clean_url'] = f"{parsed.scheme}://{result['host']}{parsed.path}"
                        if not result['clean_url'].endswith('.git'):
                            result['clean_url'] += '.git'
                
        except Exception as e:
            result['error'] = f"Failed to parse Git URL: {str(e)}"
        
        return result
    
    def detect_git_credentials(self) -> Dict[str, Any]:
        """
        Detect available Git credentials without user interaction
        """
        creds = {
            'has_token': False,
            'has_ssh': False,
            'has_git_config': False,
            'git_config_user': None,
            'methods': []
        }
        
        try:
            # Check for Git auth token in environment
            if os.getenv('GIT_AUTH_TOKEN') or os.getenv('GITHUB_TOKEN') or os.getenv('GITLAB_TOKEN'):
                creds['has_token'] = True
                creds['methods'].append('token')
            
            # Check for SSH keys
            ssh_dir = os.path.expanduser('~/.ssh')
            if os.path.exists(ssh_dir):
                for key_file in ['id_rsa', 'id_ed25519', 'id_ecdsa']:
                    if os.path.exists(os.path.join(ssh_dir, key_file)):
                        creds['has_ssh'] = True
                        creds['methods'].append('ssh')
                        break
            
            # Check Git configuration
            try:
                result = subprocess.run(['git', 'config', '--global', 'user.name'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0 and result.stdout.strip():
                    creds['has_git_config'] = True
                    creds['git_config_user'] = result.stdout.strip()
                    creds['methods'].append('git-config')
            except Exception:
                pass
                
        except Exception as e:
            pass  # Silent failure for credential detection
        
        return creds
    
    def setup_git_environment(self) -> bool:
        """
        Setup Git environment for non-interactive operation
        """
        try:
            # Configure Git for long paths on Windows
            if os.name == 'nt':
                subprocess.run(['git', 'config', '--global', 'core.longpaths', 'true'], 
                             capture_output=True, timeout=10)
            
            # Configure Git for non-interactive mode
            os.environ['GIT_TERMINAL_PROMPT'] = '0'
            os.environ['GIT_ASKPASS'] = 'echo'
            
            # Set up token-based authentication if available
            token = os.getenv('GIT_AUTH_TOKEN') or os.getenv('GITHUB_TOKEN') or os.getenv('GITLAB_TOKEN')
            if token:
                # Configure Git credential helper for this session
                subprocess.run(['git', 'config', '--global', 'credential.helper', ''], 
                             capture_output=True, timeout=10)
                
            return True
        except Exception:
            return False
    
    def clone_repository(self, url: str, target_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Clone Git repository to temporary or specified directory
        """
        result = {
            'success': False,
            'local_path': None,
            'temp_dir': None,
            'error': None,
            'info': ''
        }
        
        try:
            # Parse the Git URL
            parsed = self.parse_git_url(url)
            if not parsed['is_git_url']:
                result['error'] = f"Not a valid Git URL: {url}"
                return result
            
            if parsed['error']:
                result['error'] = parsed['error']
                return result
            
            # Setup Git environment
            self.setup_git_environment()
            
            # Create temporary directory if target not specified
            if target_dir is None:
                temp_dir = tempfile.mkdtemp(prefix='git_clone_')
                self.temp_dirs.append(temp_dir)
                result['temp_dir'] = temp_dir
                clone_path = temp_dir
            else:
                clone_path = target_dir
                if os.path.exists(clone_path):
                    shutil.rmtree(clone_path)
                os.makedirs(clone_path, exist_ok=True)
            
            # Prepare clone command with optimizations
            cmd = ['git', 'clone']
            
            # Add specific branch/tag if specified
            if parsed['ref']:
                cmd.extend(['--branch', parsed['ref']])
            
            # For analysis purposes, we need full history and all branches
            # Don't use --single-branch as it limits history analysis
            
            # Add URL and target directory
            cmd.extend([parsed['clean_url'], clone_path])
            
            # Execute clone command
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd=os.getcwd()
            )
            
            if process.returncode != 0:
                error_msg = process.stderr.strip() if process.stderr else "Unknown clone error"
                
                # Provide specific error messages for common issues
                if 'authentication failed' in error_msg.lower() or 'permission denied' in error_msg.lower():
                    creds = self.detect_git_credentials()
                    if not any([creds['has_token'], creds['has_ssh'], creds['has_git_config']]):
                        result['error'] = (
                            "Authentication failed - No credentials detected.\n"
                            "For private repositories, set up one of:\n"
                            "• GIT_AUTH_TOKEN environment variable\n"
                            "• SSH keys in ~/.ssh/\n"
                            "• Git credential helper"
                        )
                    else:
                        result['error'] = f"Authentication failed: {error_msg}"
                elif 'repository not found' in error_msg.lower():
                    result['error'] = f"Repository not found: {parsed['clean_url']}"
                elif 'could not resolve host' in error_msg.lower():
                    result['error'] = f"Network error - could not resolve host: {parsed['host']}"
                else:
                    result['error'] = f"Git clone failed: {error_msg}"
                
                return result
            
            # Handle subfolder if specified
            if parsed['subfolder']:
                subfolder_path = os.path.join(clone_path, parsed['subfolder'])
                if os.path.exists(subfolder_path):
                    result['local_path'] = subfolder_path
                    result['info'] = f"Cloned with subfolder: {parsed['subfolder']}"
                else:
                    result['error'] = f"Subfolder not found: {parsed['subfolder']}"
                    return result
            else:
                result['local_path'] = clone_path
            
            # Verify the cloned repository
            if not os.path.exists(result['local_path']):
                result['error'] = "Clone completed but directory not found"
                return result
            
            # Add repository info
            info_parts = []
            if parsed['ref']:
                info_parts.append(f"branch/tag: {parsed['ref']}")
            if parsed['subfolder']:
                info_parts.append(f"subfolder: {parsed['subfolder']}")
            if info_parts:
                result['info'] = f"Cloned {' | '.join(info_parts)}"
            
            result['success'] = True
            return result
            
        except subprocess.TimeoutExpired:
            result['error'] = "Git clone operation timed out (5 minutes)"
            return result
        except Exception as e:
            result['error'] = f"Unexpected error during clone: {str(e)}"
            return result
    
    def cleanup_repository(self, path: str) -> bool:
        """
        Clean up temporary repository directory
        """
        try:
            if os.path.exists(path) and os.path.isdir(path):
                # On Windows, handle long paths and readonly files
                if os.name == 'nt':
                    # Use Windows rmdir command for better long path support
                    subprocess.run(['cmd', '/c', 'rmdir', '/s', '/q', path], 
                                 capture_output=True, timeout=30)
                else:
                    shutil.rmtree(path)
                
                # Remove from tracking list
                if path in self.temp_dirs:
                    self.temp_dirs.remove(path)
                
                return True
        except Exception:
            pass
        return False
    
    def cleanup_all(self):
        """
        Clean up all tracked temporary directories
        """
        for temp_dir in self.temp_dirs.copy():
            self.cleanup_repository(temp_dir)


# Global instance
git_handler = GitHandler()


def validate_and_prepare_repository(path: str) -> Dict[str, Any]:
    """
    Validate repository path or Git URL and prepare for analysis
    """
    result = {
        'success': False,
        'type': 'unknown',
        'path': path,
        'info': '',
        'error': None
    }
    
    try:
        # Check if it's a Git URL
        parsed_git = git_handler.parse_git_url(path)
        
        if parsed_git['is_git_url']:
            result['type'] = 'git_url'
            result['success'] = True
            info_parts = []
            if parsed_git['ref']:
                info_parts.append(f"ref: {parsed_git['ref']}")
            if parsed_git['subfolder']:
                info_parts.append(f"subfolder: {parsed_git['subfolder']}")
            result['info'] = ' | '.join(info_parts) if info_parts else 'Git URL validated'
            return result
        
        # Check if it's a local path
        if os.path.exists(path) and os.path.isdir(path):
            result['type'] = 'local_path'
            result['success'] = True
            result['path'] = os.path.abspath(path)
            return result
        
        # Path doesn't exist
        result['error'] = f"Path does not exist: {path}"
        return result
        
    except Exception as e:
        result['error'] = f"Validation error: {str(e)}"
        return result


def cleanup_on_exit():
    """
    Cleanup function to be called on application exit
    """
    git_handler.cleanup_all()


# Register cleanup function
import atexit
atexit.register(cleanup_on_exit)
