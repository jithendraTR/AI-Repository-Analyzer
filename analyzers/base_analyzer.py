"""
Base Analyzer Class
Common functionality for all repository analyzers
"""

import os
import git
import streamlit as st
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pathlib import Path
import subprocess
import json
import pandas as pd
from datetime import datetime
import threading
import time
from utils.ai_client import OpenArenaClient

class CancellationToken:
    """Thread-safe cancellation token for stopping long-running operations"""
    
    def __init__(self, token_id: str):
        self.token_id = token_id
        self._cancelled = threading.Event()
        self._start_time = time.time()
    
    def cancel(self):
        """Cancel the operation"""
        self._cancelled.set()
        # Update session state
        if f"cancelled_{self.token_id}" not in st.session_state:
            st.session_state[f"cancelled_{self.token_id}"] = True
    
    def is_cancelled(self) -> bool:
        """Check if the operation has been cancelled"""
        # Check both the event and session state
        session_cancelled = st.session_state.get(f"cancelled_{self.token_id}", False)
        return self._cancelled.is_set() or session_cancelled
    
    def check_cancellation(self):
        """Raise an exception if cancelled"""
        if self.is_cancelled():
            raise OperationCancelledException(f"Operation {self.token_id} was cancelled")
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time since token creation"""
        return time.time() - self._start_time
    
    def cleanup(self):
        """Clean up session state"""
        keys_to_remove = [
            f"cancelled_{self.token_id}",
            f"running_{self.token_id}",
            f"progress_{self.token_id}"
        ]
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]

class OperationCancelledException(Exception):
    """Exception raised when an operation is cancelled"""
    pass

class BaseAnalyzer(ABC):
    """Base class for all repository analyzers"""
    
    def __init__(self, repo_path: str):
        # Validate repository path
        if not repo_path or not repo_path.strip():
            raise ValueError("Repository path cannot be empty")
        
        if repo_path in ["/path/to/your/repo", "C:\\path\\to\\your\\repo"]:
            raise ValueError("Please provide a valid repository path, not the placeholder text")
        
        if not os.path.exists(repo_path):
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        self.repo_path = Path(repo_path)
        self.ai_client = OpenArenaClient()
        
        # Initialize git repository if it exists
        try:
            self.repo = git.Repo(repo_path)
        except git.exc.InvalidGitRepositoryError:
            self.repo = None
            st.warning("Not a git repository - some features may be limited")
    
    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """Perform the specific analysis - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def render(self):
        """Render the analysis results in Streamlit - must be implemented by subclasses"""
        pass
    
    def get_file_list(self, extensions: List[str] = None) -> List[Path]:
        """
        Get list of files in the repository
        
        Args:
            extensions: List of file extensions to filter by (e.g., ['.py', '.js'])
            
        Returns:
            List of file paths
        """
        files = []
        for root, dirs, filenames in os.walk(self.repo_path):
            # Skip common directories that shouldn't be analyzed
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in 
                      ['node_modules', '__pycache__', 'venv', 'env', 'build', 'dist']]
            
            for filename in filenames:
                file_path = Path(root) / filename
                if extensions:
                    if file_path.suffix.lower() in extensions:
                        files.append(file_path)
                else:
                    files.append(file_path)
        
        return files
    
    def read_file_content(self, file_path: Path) -> Optional[str]:
        """
        Read content of a file safely
        
        Args:
            file_path: Path to the file
            
        Returns:
            File content or None if error
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            st.warning(f"Could not read file {file_path}: {str(e)}")
            return None
    
    def get_git_history(self, file_path: str = None, max_commits: int = 100) -> List[Dict]:
        """
        Get git commit history
        
        Args:
            file_path: Specific file to get history for (optional)
            max_commits: Maximum number of commits to retrieve
            
        Returns:
            List of commit information dictionaries
        """
        if not self.repo:
            return []
        
        try:
            commits = []
            commit_iter = self.repo.iter_commits(paths=file_path, max_count=max_commits)
            
            for commit in commit_iter:
                commits.append({
                    'hash': commit.hexsha,
                    'author': commit.author.name,
                    'email': commit.author.email,
                    'date': commit.committed_datetime,
                    'message': commit.message.strip(),
                    'files_changed': len(commit.stats.files)
                })
            
            return commits
        except Exception as e:
            st.warning(f"Could not retrieve git history: {str(e)}")
            return []
    
    def get_file_contributors(self, file_path: str) -> Dict[str, int]:
        """
        Get contributors to a specific file with their commit counts
        
        Args:
            file_path: Path to the file relative to repo root
            
        Returns:
            Dictionary of author -> commit count
        """
        if not self.repo:
            return {}
        
        try:
            contributors = {}
            commits = list(self.repo.iter_commits(paths=file_path))
            
            for commit in commits:
                author = commit.author.name
                contributors[author] = contributors.get(author, 0) + 1
            
            return contributors
        except Exception as e:
            st.warning(f"Could not get contributors for {file_path}: {str(e)}")
            return {}
    
    def find_files_by_pattern(self, pattern: str) -> List[Path]:
        """
        Find files matching a specific pattern
        
        Args:
            pattern: Glob pattern to match
            
        Returns:
            List of matching file paths
        """
        return list(self.repo_path.glob(pattern))
    
    def get_project_structure(self, max_depth: int = 3) -> str:
        """
        Get a string representation of the project structure
        
        Args:
            max_depth: Maximum directory depth to traverse
            
        Returns:
            String representation of project structure
        """
        structure = []
        
        def add_to_structure(path: Path, depth: int, prefix: str = ""):
            if depth > max_depth:
                return
            
            items = sorted([p for p in path.iterdir() if not p.name.startswith('.')])
            
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                structure.append(f"{prefix}{current_prefix}{item.name}")
                
                if item.is_dir() and item.name not in ['node_modules', '__pycache__', 'venv', 'env']:
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    add_to_structure(item, depth + 1, next_prefix)
        
        structure.append(self.repo_path.name)
        add_to_structure(self.repo_path, 0)
        
        return "\n".join(structure)
    
    def run_command(self, command: List[str]) -> Optional[str]:
        """
        Run a command in the repository directory
        
        Args:
            command: Command to run as list of strings
            
        Returns:
            Command output or None if error
        """
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout if result.returncode == 0 else None
        except Exception as e:
            st.warning(f"Command failed: {' '.join(command)} - {str(e)}")
            return None
    
    def cache_analysis(self, analysis_type: str, data: Any):
        """
        Cache analysis results
        
        Args:
            analysis_type: Type of analysis
            data: Data to cache
        """
        cache_key = f"{analysis_type}_{hash(str(self.repo_path))}"
        st.session_state[cache_key] = data
    
    def get_cached_analysis(self, analysis_type: str) -> Optional[Any]:
        """
        Get cached analysis results
        
        Args:
            analysis_type: Type of analysis
            
        Returns:
            Cached data or None if not found
        """
        cache_key = f"{analysis_type}_{hash(str(self.repo_path))}"
        return st.session_state.get(cache_key)
    
    def clear_cache(self, analysis_type: str = None):
        """
        Clear cached analysis results
        
        Args:
            analysis_type: Specific analysis type to clear, or None to clear all
        """
        if analysis_type:
            cache_key = f"{analysis_type}_{hash(str(self.repo_path))}"
            if cache_key in st.session_state:
                del st.session_state[cache_key]
        else:
            # Clear all cache for this repository
            repo_hash = hash(str(self.repo_path))
            keys_to_delete = [key for key in st.session_state.keys() 
                            if key.endswith(f"_{repo_hash}")]
            for key in keys_to_delete:
                del st.session_state[key]
    
    def create_cancellation_token(self, operation_name: str) -> CancellationToken:
        """
        Create a new cancellation token for an operation
        
        Args:
            operation_name: Name of the operation
            
        Returns:
            CancellationToken instance
        """
        token_id = f"{operation_name}_{hash(str(self.repo_path))}_{int(time.time())}"
        token = CancellationToken(token_id)
        
        # Mark operation as running
        st.session_state[f"running_{token.token_id}"] = True
        
        return token
    
    def display_cancellable_operation(self, token: CancellationToken, message: str, progress: float = None):
        """
        Display a cancellable operation with stop button
        
        Args:
            token: Cancellation token
            message: Status message
            progress: Progress value (0-100) if available
        """
        col1, col2 = st.columns([4, 1])
        
        with col1:
            if progress is not None:
                st.progress(progress / 100.0)
            st.text(f"{message} (Elapsed: {token.get_elapsed_time():.1f}s)")
        
        with col2:
            if st.button("🛑 Stop", key=f"stop_{token.token_id}"):
                token.cancel()
                st.warning("Stopping operation...")
                st.rerun()
    
    def get_file_list_cancellable(self, extensions: List[str] = None, token: CancellationToken = None) -> List[Path]:
        """
        Get list of files in the repository with cancellation support
        
        Args:
            extensions: List of file extensions to filter by
            token: Cancellation token
            
        Returns:
            List of file paths
        """
        files = []
        processed_dirs = 0
        
        for root, dirs, filenames in os.walk(self.repo_path):
            if token:
                token.check_cancellation()
            
            # Skip common directories that shouldn't be analyzed
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in 
                      ['node_modules', '__pycache__', 'venv', 'env', 'build', 'dist']]
            
            for filename in filenames:
                if token and processed_dirs % 10 == 0:  # Check every 10 files
                    token.check_cancellation()
                
                file_path = Path(root) / filename
                if extensions:
                    if file_path.suffix.lower() in extensions:
                        files.append(file_path)
                else:
                    files.append(file_path)
            
            processed_dirs += 1
        
        return files
    
    def get_git_history_cancellable(self, file_path: str = None, max_commits: int = 100, token: CancellationToken = None) -> List[Dict]:
        """
        Get git commit history with cancellation support
        
        Args:
            file_path: Specific file to get history for (optional)
            max_commits: Maximum number of commits to retrieve
            token: Cancellation token
            
        Returns:
            List of commit information dictionaries
        """
        if not self.repo:
            return []
        
        try:
            commits = []
            commit_iter = self.repo.iter_commits(paths=file_path, max_count=max_commits)
            
            for i, commit in enumerate(commit_iter):
                if token and i % 10 == 0:  # Check every 10 commits
                    token.check_cancellation()
                
                commits.append({
                    'hash': commit.hexsha,
                    'author': commit.author.name,
                    'email': commit.author.email,
                    'date': commit.committed_datetime,
                    'message': commit.message.strip(),
                    'files_changed': len(commit.stats.files)
                })
            
            return commits
        except OperationCancelledException:
            raise
        except Exception as e:
            st.warning(f"Could not retrieve git history: {str(e)}")
            return []
    
    def add_rerun_button(self, analysis_type: str):
        """
        Add a rerun button that clears cache and reruns analysis
        
        Args:
            analysis_type: Type of analysis to rerun
        """
        col1, col2 = st.columns([3, 1])
        with col2:
            # Only show rerun button if analysis is not currently running
            analysis_running = st.session_state.get('analysis_running', False)
            if not analysis_running:
                if st.button("🔄 Rerun Analysis", key=f"rerun_{analysis_type}"):
                    # Only rerun if we're not in the middle of a selection change
                    if not st.session_state.get('selection_changing', False):
                        self.clear_cache(analysis_type)
                        st.rerun()
    
    def get_analysis_with_control(self, analysis_type: str, loading_message: str):
        """
        Get analysis results with proper control flow - only runs when appropriate
        
        Args:
            analysis_type: Type of analysis
            loading_message: Message to show while loading
            
        Returns:
            Analysis results or None if analysis should not run
        """
        # Check if we should run analysis automatically or wait for user action
        analysis_running = st.session_state.get('analysis_running', False)
        
        # Check if this specific analyzer is running during parallel analysis
        analyzer_progress = st.session_state.get('analyzer_progress', {})
        is_analyzer_running = (analysis_type in analyzer_progress and 
                              analyzer_progress[analysis_type].get('status') == 'Running')
        
        # Check if analysis results are already available from parallel analysis
        if 'analysis_results' in st.session_state and analysis_type in st.session_state.analysis_results:
            result = st.session_state.analysis_results[analysis_type]
            if result.get('success', False) and 'analysis_data' in result:
                return result['analysis_data']
        
        # Only auto-analyze if analysis is explicitly running OR this analyzer is running in parallel
        if (analysis_running and st.session_state.get('analysis_started', False)) or is_analyzer_running:
            with self.display_loading_message(loading_message):
                return self.analyze()
        else:
            # Check for cached results first
            analysis = self.get_cached_analysis(analysis_type)
            
            if not analysis:
                # Show a button to run analysis manually
                st.info(f"Click 'Run Analysis' to {loading_message.lower()}.")
                if st.button("🚀 Run Analysis", key=f"run_{analysis_type}"):
                    with self.display_loading_message(loading_message):
                        return self.analyze()
                else:
                    return None  # Don't run analysis
            else:
                return analysis
    
    def display_parallel_ai_insights(self, analysis_type: str):
        """
        Display AI insights from parallel analysis if available
        
        Args:
            analysis_type: Type of analysis to show insights for
        """
        if 'parallel_ai_results' in st.session_state:
            results = st.session_state.parallel_ai_results
            
            # Map analysis types to result keys
            type_mapping = {
                'expertise_mapping': 'expertise',
                'timeline_analysis': 'timeline',
                'api_contracts': 'api_contracts',
                'ai_context': 'ai_context',
                'risk_analysis': 'risk_analysis',
                'development_patterns': 'development_patterns',
                'version_governance': 'version_governance',
                'tech_debt_detection': 'tech_debt',
                'design_patterns': 'design_patterns'
            }
            
            result_key = type_mapping.get(analysis_type, analysis_type)
            
            if result_key in results:
                result = results[result_key]
                
                st.subheader("🤖 AI Insights (From Parallel Analysis)")
                
                if result.get('success', False) and result.get('insight'):
                    st.markdown("**AI-Generated Insights:**")
                    st.markdown(result['insight'])
                    
                    # Add timestamp
                    st.caption("Generated from parallel AI analysis")
                else:
                    st.error(f"AI analysis failed: {result.get('error', 'Unknown error')}")
                    
                return True  # Insights were displayed
        
        return False  # No insights available
    
    def display_loading_message(self, message: str):
        """Display a loading message"""
        return st.spinner(message)
    
    def display_error(self, message: str):
        """Display an error message"""
        st.error(message)
    
    def display_success(self, message: str):
        """Display a success message"""
        st.success(message)
    
    def display_info(self, message: str):
        """Display an info message"""
        st.info(message)
    
    def add_save_options(self, analysis_type: str, analysis_data: Dict[str, Any]):
        """
        Add save/export options for analysis results
        
        Args:
            analysis_type: Type of analysis
            analysis_data: Analysis data to save
        """
        st.subheader("💾 Save & Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Save as JSON
            if st.button("📄 Save as JSON", key=f"save_json_{analysis_type}"):
                json_data = self._prepare_json_export(analysis_type, analysis_data)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{analysis_type}_report_{timestamp}.json"
                
                st.download_button(
                    label="⬇️ Download JSON Report",
                    data=json.dumps(json_data, indent=2, default=str),
                    file_name=filename,
                    mime="application/json",
                    key=f"download_json_{analysis_type}"
                )
        
        with col2:
            # Save as CSV (for tabular data)
            if st.button("📊 Save as CSV", key=f"save_csv_{analysis_type}"):
                csv_data = self._prepare_csv_export(analysis_type, analysis_data)
                if csv_data:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{analysis_type}_report_{timestamp}.csv"
                    
                    st.download_button(
                        label="⬇️ Download CSV Report",
                        data=csv_data,
                        file_name=filename,
                        mime="text/csv",
                        key=f"download_csv_{analysis_type}"
                    )
                else:
                    st.warning("No tabular data available for CSV export")
        
        with col3:
            # Save comprehensive report
            if st.button("📋 Save Full Report", key=f"save_full_{analysis_type}"):
                report_data = self._prepare_full_report(analysis_type, analysis_data)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{analysis_type}_full_report_{timestamp}.md"
                
                st.download_button(
                    label="⬇️ Download Full Report",
                    data=report_data,
                    file_name=filename,
                    mime="text/markdown",
                    key=f"download_full_{analysis_type}"
                )
    
    def _prepare_json_export(self, analysis_type: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for JSON export"""
        export_data = {
            "report_metadata": {
                "analysis_type": analysis_type,
                "repository_path": str(self.repo_path),
                "generated_at": datetime.now().isoformat(),
                "analyzer_version": "1.0.0"
            },
            "analysis_results": analysis_data
        }
        
        # Add AI insights if available
        if 'parallel_ai_results' in st.session_state:
            type_mapping = {
                'expertise_mapping': 'expertise',
                'timeline_analysis': 'timeline',
                'api_contracts': 'api_contracts',
                'ai_context': 'ai_context',
                'risk_analysis': 'risk_analysis',
                'development_patterns': 'development_patterns',
                'version_governance': 'version_governance',
                'tech_debt_detection': 'tech_debt',
                'design_patterns': 'design_patterns'
            }
            
            result_key = type_mapping.get(analysis_type, analysis_type)
            results = st.session_state.parallel_ai_results
            
            if result_key in results and results[result_key].get('success', False):
                export_data["ai_insights"] = results[result_key].get('insight', '')
        
        return export_data
    
    def _prepare_csv_export(self, analysis_type: str, analysis_data: Dict[str, Any]) -> Optional[str]:
        """Prepare data for CSV export"""
        try:
            # Convert analysis data to DataFrame based on analysis type
            df = None
            
            if analysis_type == "expertise_mapping":
                if "file_expertise" in analysis_data:
                    rows = []
                    for file_path, experts in analysis_data["file_expertise"].items():
                        for expert, commits in experts.items():
                            rows.append({
                                "file_path": file_path,
                                "expert": expert,
                                "commits": commits
                            })
                    df = pd.DataFrame(rows)
            
            elif analysis_type == "timeline_analysis":
                if "timeline_data" in analysis_data and "monthly_commits" in analysis_data["timeline_data"]:
                    monthly_data = analysis_data["timeline_data"]["monthly_commits"]
                    df = pd.DataFrame([
                        {"month": month, "commits": commits}
                        for month, commits in monthly_data.items()
                    ])
            
            elif analysis_type == "risk_analysis":
                if "test_coverage" in analysis_data:
                    coverage_data = analysis_data["test_coverage"]
                    rows = []
                    for file_path, coverage in coverage_data.items():
                        rows.append({
                            "file_path": file_path,
                            "has_tests": coverage.get("has_tests", False),
                            "test_files": len(coverage.get("test_files", []))
                        })
                    df = pd.DataFrame(rows)
            
            # Add more analysis types as needed
            
            if df is not None and not df.empty:
                return df.to_csv(index=False)
            
            return None
            
        except Exception as e:
            st.warning(f"Could not prepare CSV export: {str(e)}")
            return None
    
    def _prepare_full_report(self, analysis_type: str, analysis_data: Dict[str, Any]) -> str:
        """Prepare comprehensive markdown report"""
        report_lines = []
        
        # Header
        report_lines.append(f"# {analysis_type.replace('_', ' ').title()} Report")
        report_lines.append("")
        report_lines.append(f"**Repository:** {self.repo_path}")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**Analysis Type:** {analysis_type}")
        report_lines.append("")
        
        # Executive Summary
        report_lines.append("## Executive Summary")
        report_lines.append("")
        
        # Add AI insights if available
        if 'parallel_ai_results' in st.session_state:
            type_mapping = {
                'expertise_mapping': 'expertise',
                'timeline_analysis': 'timeline',
                'api_contracts': 'api_contracts',
                'ai_context': 'ai_context',
                'risk_analysis': 'risk_analysis',
                'development_patterns': 'development_patterns',
                'version_governance': 'version_governance',
                'tech_debt_detection': 'tech_debt',
                'design_patterns': 'design_patterns'
            }
            
            result_key = type_mapping.get(analysis_type, analysis_type)
            results = st.session_state.parallel_ai_results
            
            if result_key in results and results[result_key].get('success', False):
                report_lines.append("### AI-Generated Insights")
                report_lines.append("")
                report_lines.append(results[result_key].get('insight', ''))
                report_lines.append("")
        
        # Detailed Analysis Results
        report_lines.append("## Detailed Analysis Results")
        report_lines.append("")
        
        # Convert analysis data to markdown
        self._add_analysis_to_markdown(report_lines, analysis_data)
        
        # Footer
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("*Report generated by AI-Powered Codebase Analyzer*")
        
        return "\n".join(report_lines)
    
    def _add_analysis_to_markdown(self, report_lines: List[str], data: Any, level: int = 3):
        """Recursively add analysis data to markdown report"""
        if isinstance(data, dict):
            for key, value in data.items():
                if key in ['error']:  # Skip error keys
                    continue
                    
                header = "#" * level + f" {key.replace('_', ' ').title()}"
                report_lines.append(header)
                report_lines.append("")
                
                if isinstance(value, (dict, list)):
                    self._add_analysis_to_markdown(report_lines, value, level + 1)
                else:
                    report_lines.append(f"{value}")
                    report_lines.append("")
        
        elif isinstance(data, list):
            if data and isinstance(data[0], dict):
                # Create a table for list of dictionaries
                if len(data) > 0:
                    headers = list(data[0].keys())
                    report_lines.append("| " + " | ".join(headers) + " |")
                    report_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
                    
                    for item in data[:20]:  # Limit to first 20 items
                        row = []
                        for header in headers:
                            value = str(item.get(header, ""))
                            # Escape pipe characters
                            value = value.replace("|", "\\|")
                            row.append(value)
                        report_lines.append("| " + " | ".join(row) + " |")
                    
                    if len(data) > 20:
                        report_lines.append(f"*... and {len(data) - 20} more items*")
                    
                    report_lines.append("")
            else:
                # Simple list
                for item in data[:50]:  # Limit to first 50 items
                    report_lines.append(f"- {item}")
                
                if len(data) > 50:
                    report_lines.append(f"*... and {len(data) - 50} more items*")
                
                report_lines.append("")
        
        else:
            report_lines.append(f"{data}")
            report_lines.append("")
