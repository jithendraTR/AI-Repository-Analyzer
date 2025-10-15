"""
Timeline Analysis Analyzer - Optimized Version
Analyzes project timeline and latest additions for understanding project evolution
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict, Counter
from typing import Dict, List, Any
from datetime import datetime, timedelta
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .base_analyzer import BaseAnalyzer, OperationCancelledException

class TimelineAnalyzer(BaseAnalyzer):
    """Analyzes project timeline and recent changes - Ultra-optimized for performance"""
    
    # Pre-compile regex patterns at class level for maximum performance
    _COMMIT_PATTERNS = {
        'feature': re.compile(r'(feat|feature|add|new|implement)', re.IGNORECASE),
        'fix': re.compile(r'(fix|bug|patch|resolve)', re.IGNORECASE),
        'refactor': re.compile(r'(refactor|refact|clean|improve)', re.IGNORECASE),
        'docs': re.compile(r'(doc|docs|documentation|readme)', re.IGNORECASE),
        'initialization': re.compile(r'(initial|init|start)', re.IGNORECASE),
        'testing': re.compile(r'(test|spec)', re.IGNORECASE)
    }
    
    def analyze(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Ultra-optimized timeline analysis for sub-5-minute performance"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("timeline_analysis")
        if cached_result:
            return cached_result
        
        if not self.repo:
            return {"error": "Git repository required for timeline analysis"}
        
        try:
            total_steps = 9  # Increased steps for enhanced analysis
            current_step = 0
            
            # Step 1: Get minimal commit history for speed
            if progress_callback:
                progress_callback(current_step, total_steps, "Loading commit history (limited for performance)...")
            
            if token:
                token.check_cancellation()
            
            # Significantly reduce commit limit for speed (300 instead of 800)
            commits_data = self._get_ultra_optimized_timeline_data(token, max_commits=300)
            commits = commits_data['commits']
            
            if not commits:
                return {"error": "No commit history found"}
            current_step += 1
            
            # Step 2: Fast timeline patterns analysis
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing timeline patterns (fast mode)...")
            
            if token:
                token.check_cancellation()
            
            timeline_data = self._analyze_timeline_patterns_ultra_fast(commits, token)
            current_step += 1
            
            # Step 3: Quick recent changes analysis
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing recent changes (optimized)...")
            
            if token:
                token.check_cancellation()
            
            recent_changes = self._analyze_recent_changes_ultra_fast(commits, token)
            current_step += 1
            
            # Step 4: Simplified development phases
            if progress_callback:
                progress_callback(current_step, total_steps, "Identifying key development phases...")
            
            if token:
                token.check_cancellation()
            
            development_phases = self._identify_development_phases_ultra_fast(commits, token)
            current_step += 1
            
            # Step 5: Enhanced Feature Addition Patterns Analysis
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing feature addition patterns...")
            
            if token:
                token.check_cancellation()
            
            feature_patterns = self._analyze_feature_addition_patterns(commits, token)
            current_step += 1
            
            # Step 6: Enhanced Architecture Migration History Analysis
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing architecture migration history...")
            
            if token:
                token.check_cancellation()
            
            architecture_migration = self._analyze_architecture_migration_history(commits, token)
            current_step += 1
            
            # Step 7: Enhanced Performance Evolution Analysis
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing performance evolution...")
            
            if token:
                token.check_cancellation()
            
            performance_evolution = self._analyze_performance_evolution(commits, token)
            current_step += 1
            
            # Step 8: Enhanced Security Evolution Analysis
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing security evolution...")
            
            if token:
                token.check_cancellation()
            
            security_evolution = self._analyze_security_evolution(commits, token)
            current_step += 1
            
            # Step 9: Quick file evolution (skip if too many files)
            if progress_callback:
                progress_callback(current_step, total_steps, "Finalizing analysis...")
            
            if token:
                token.check_cancellation()
            
            # Skip complex file evolution for speed, provide simple summary
            file_evolution = self._get_simple_file_stats(commits_data)
            
            # Skip release patterns if they take too long, provide minimal data
            release_patterns = self._get_quick_release_info()
            
            current_step += 1
            
            result = {
                "timeline_data": timeline_data,
                "recent_changes": recent_changes,
                "development_phases": development_phases,
                "file_evolution": file_evolution,
                "release_patterns": release_patterns,
                "project_age": self._calculate_project_age_fast(commits),
                "total_commits": len(commits),
                # Enhanced Analysis Results
                "feature_patterns": feature_patterns,
                "architecture_migration": architecture_migration,
                "performance_evolution": performance_evolution,
                "security_evolution": security_evolution
            }
            
            # Cache the result
            self.cache_analysis("timeline_analysis", result)
            
            return result
            
        except OperationCancelledException:
            return {"error": "Analysis was cancelled by user"}
        except Exception as e:
            return {"error": f"Timeline analysis failed: {str(e)}"}
    
    def _get_optimized_timeline_data(self, token=None, max_commits=800) -> Dict[str, Any]:
        """Get timeline data efficiently using direct git commands"""
        try:
            # Use git log to get commit and file data in one efficient command
            cmd = [
                'git', 'log', '--name-only', '--pretty=format:%H|%an|%ae|%ci|%s', 
                f'-{max_commits}', '--no-merges'
            ]
            
            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True, timeout=120
            )
            
            if result.returncode != 0:
                # Fallback to original method
                return {'commits': self.get_git_history_cancellable(max_commits=max_commits, token=token), 'file_data': {}}
            
            # Parse the output efficiently
            commits = []
            file_data = defaultdict(lambda: defaultdict(list))
            
            current_commit = None
            lines = result.stdout.strip().split('\n')
            
            for line in lines:
                if token and len(commits) % 100 == 0:
                    token.check_cancellation()
                
                if '|' in line and len(line.split('|')) == 5:
                    # New commit line
                    if current_commit:
                        commits.append(current_commit)
                    
                    parts = line.split('|')
                    commit_hash, author, email, date, message = parts
                    
                    current_commit = {
                        'hash': commit_hash,
                        'author': author,
                        'email': email,
                        'date': pd.to_datetime(date),
                        'message': message.strip(),
                        'files': []
                    }
                elif line.strip() and current_commit and not line.startswith('.git/'):
                    # File path
                    file_path = line.strip()
                    if file_path:
                        current_commit['files'].append(file_path)
                        file_data[file_path]['commits'].append(current_commit['hash'])
                        file_data[file_path]['authors'].add(current_commit['author'])
            
            # Add the last commit
            if current_commit:
                commits.append(current_commit)
            
            # Convert sets to lists for JSON serialization
            for file_path in file_data:
                file_data[file_path]['authors'] = list(file_data[file_path]['authors'])
            
            return {
                'commits': commits,
                'file_data': dict(file_data)
            }
            
        except Exception as e:
            # Fallback to original method if git command fails
            commits = self.get_git_history_cancellable(max_commits=max_commits, token=token)
            return {'commits': commits, 'file_data': {}}
    
    def _analyze_timeline_patterns_optimized(self, commits: List[Dict], token=None) -> Dict[str, Any]:
        """Optimized timeline patterns analysis with parallel processing"""
        
        # Pre-allocate collections for better performance
        daily_commits = defaultdict(int)
        weekly_commits = defaultdict(int)
        monthly_commits = defaultdict(int)
        hourly_commits = defaultdict(int)
        
        # Process commits in batches for better performance
        batch_size = 200
        for i in range(0, len(commits), batch_size):
            if token:
                token.check_cancellation()
            
            batch = commits[i:i+batch_size]
            for commit in batch:
                date = commit['date']
                daily_key = date.strftime('%Y-%m-%d')
                weekly_key = date.strftime('%Y-W%U')
                monthly_key = date.strftime('%Y-%m')
                hourly_key = date.hour
                
                daily_commits[daily_key] += 1
                weekly_commits[weekly_key] += 1
                monthly_commits[monthly_key] += 1
                hourly_commits[hourly_key] += 1
        
        # Process additional analysis in parallel
        def analyze_velocity():
            return self._calculate_velocity_trend_optimized(commits)
        
        def analyze_developer_timeline():
            return self._analyze_developer_timeline_optimized(commits)
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            velocity_future = executor.submit(analyze_velocity)
            timeline_future = executor.submit(analyze_developer_timeline)
            
            velocity_trend = velocity_future.result()
            developer_timeline = timeline_future.result()
        
        return {
            "daily_commits": dict(daily_commits),
            "weekly_commits": dict(weekly_commits),
            "monthly_commits": dict(monthly_commits),
            "hourly_commits": dict(hourly_commits),
            "velocity_trend": velocity_trend,
            "developer_timeline": developer_timeline
        }
    
    def _analyze_recent_changes_optimized(self, commits: List[Dict], token=None, days: int = 30) -> Dict[str, Any]:
        """Optimized recent changes analysis with compiled patterns"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter recent commits efficiently
        recent_commits = [c for c in commits if c['date'].replace(tzinfo=None) > cutoff_date]
        
        if not recent_commits:
            return {
                "total_recent_commits": 0,
                "feature_commits": [],
                "bug_fixes": [],
                "refactoring": [],
                "documentation": [],
                "other_commits": [],
                "recent_file_changes": {},
                "most_active_recent_authors": []
            }
        
        # Pre-compile regex patterns for better performance
        import re as regex_lib
        compiled_patterns = {
            'feature': regex_lib.compile(r'(feat|feature|add|new|implement)', regex_lib.IGNORECASE),
            'fix': regex_lib.compile(r'(fix|bug|patch|resolve)', regex_lib.IGNORECASE),
            'refactor': regex_lib.compile(r'(refactor|refact|clean|improve)', regex_lib.IGNORECASE),
            'docs': regex_lib.compile(r'(doc|docs|documentation|readme)', regex_lib.IGNORECASE),
        }
        
        # Pre-allocate lists
        categorized_commits = {
            'feature': [],
            'fix': [],
            'refactor': [],
            'docs': [],
            'other': []
        }
        
        # Categorize commits efficiently
        for commit in recent_commits:
            if token:
                token.check_cancellation()
            
            message = commit['message']
            categorized = False
            
            for category, pattern in compiled_patterns.items():
                if pattern.search(message):
                    categorized_commits[category].append(commit)
                    categorized = True
                    break
            
            if not categorized:
                categorized_commits['other'].append(commit)
        
        # Analyze file changes using existing data
        recent_file_changes = self._analyze_recent_file_changes_optimized(recent_commits)
        
        return {
            "total_recent_commits": len(recent_commits),
            "feature_commits": categorized_commits['feature'],
            "bug_fixes": categorized_commits['fix'],
            "refactoring": categorized_commits['refactor'],
            "documentation": categorized_commits['docs'],
            "other_commits": categorized_commits['other'],
            "recent_file_changes": recent_file_changes,
            "most_active_recent_authors": self._get_most_active_authors(recent_commits)
        }
    
    def _identify_development_phases_optimized(self, commits: List[Dict], token=None) -> List[Dict]:
        """Optimized development phases identification with batch processing"""
        
        if len(commits) < 10:
            return []
        
        # Sort commits by date efficiently
        sorted_commits = sorted(commits, key=lambda x: x['date'])
        
        # Pre-compile regex patterns
        import re as regex_lib
        phase_patterns = {
            'initialization': regex_lib.compile(r'(initial|init|start)', regex_lib.IGNORECASE),
            'feature_development': regex_lib.compile(r'(feat|feature|add|new)', regex_lib.IGNORECASE),
            'bug_fixing': regex_lib.compile(r'(fix|bug|patch)', regex_lib.IGNORECASE),
            'refactoring': regex_lib.compile(r'(refactor|clean|improve)', regex_lib.IGNORECASE),
            'testing': regex_lib.compile(r'(test|spec)', regex_lib.IGNORECASE)
        }
        
        # Analyze commit velocity in chunks
        chunk_size = max(10, len(commits) // 10)
        phases = []
        
        for i in range(0, len(sorted_commits), chunk_size):
            if token:
                token.check_cancellation()
            
            chunk = sorted_commits[i:i + chunk_size]
            if len(chunk) < 5:
                continue
            
            start_date = chunk[0]['date']
            end_date = chunk[-1]['date']
            duration = (end_date - start_date).days
            
            # Analyze commit types in this phase efficiently
            commit_types = defaultdict(int)
            authors = set()
            
            for commit in chunk:
                authors.add(commit['author'])
                message = commit['message']
                
                # Use compiled patterns for better performance
                classified = False
                for phase_type, pattern in phase_patterns.items():
                    if pattern.search(message):
                        commit_types[phase_type] += 1
                        classified = True
                        break
                
                if not classified:
                    commit_types['maintenance'] += 1
            
            # Determine phase type
            if commit_types:
                dominant_type = max(commit_types.items(), key=lambda x: x[1])[0]
            else:
                dominant_type = 'maintenance'
            
            phases.append({
                'start_date': start_date,
                'end_date': end_date,
                'duration_days': duration,
                'commit_count': len(chunk),
                'author_count': len(authors),
                'dominant_activity': dominant_type,
                'commit_types': dict(commit_types),
                'velocity': len(chunk) / max(1, duration) if duration > 0 else len(chunk)
            })
        
        return phases
    
    def _analyze_file_evolution_optimized(self, commits_data: Dict, token=None) -> Dict[str, Any]:
        """Optimized file evolution analysis using existing commit data"""
        
        file_data = commits_data.get('file_data', {})
        if not file_data:
            return {}
        
        file_stats = {}
        commits = commits_data.get('commits', [])
        
        # Create commit lookup for performance
        commit_lookup = {commit['hash']: commit for commit in commits}
        
        # Process file data efficiently
        for file_path, data in file_data.items():
            if token:
                token.check_cancellation()
            
            # Skip non-source code files for performance
            if not any(file_path.endswith(ext) for ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rb', '.php']):
                continue
            
            file_commits = data.get('commits', [])
            if not file_commits:
                continue
            
            # Get commit dates efficiently
            commit_dates = []
            for commit_hash in file_commits[:50]:  # Limit for performance
                if commit_hash in commit_lookup:
                    commit_dates.append(commit_lookup[commit_hash]['date'])
            
            if commit_dates:
                commit_dates.sort()
                recent_activity = sum(1 for date in commit_dates 
                                    if (datetime.now() - date.replace(tzinfo=None)).days <= 30)
                
                file_stats[file_path] = {
                    'total_commits': len(file_commits),
                    'first_commit': commit_dates[0] if commit_dates else None,
                    'last_commit': commit_dates[-1] if commit_dates else None,
                    'contributors': len(data.get('authors', [])),
                    'recent_activity': recent_activity
                }
        
        return file_stats
    
    def _analyze_release_patterns_optimized(self, token=None) -> Dict[str, Any]:
        """Optimized release patterns analysis"""
        
        if not self.repo:
            return {}
        
        try:
            # Use git command for better performance
            cmd = ['git', 'tag', '-l', '--sort=-version:refname']
            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True, timeout=30
            )
            
            if result.returncode != 0:
                return {}
            
            tag_names = [tag.strip() for tag in result.stdout.strip().split('\n') if tag.strip()]
            
            if not tag_names:
                return {}
            
            # Get tag details in batch
            releases = []
            for tag_name in tag_names[:50]:  # Limit for performance
                if token:
                    token.check_cancellation()
                
                try:
                    tag = self.repo.tag(tag_name)
                    releases.append({
                        'name': tag_name,
                        'date': tag.commit.committed_datetime,
                        'commit': tag.commit.hexsha
                    })
                except:
                    continue
            
            # Sort by date
            releases.sort(key=lambda x: x['date'])
            
            # Calculate release intervals
            intervals = []
            for i in range(1, len(releases)):
                interval = (releases[i]['date'] - releases[i-1]['date']).days
                intervals.append(interval)
            
            return {
                'total_releases': len(releases),
                'releases': releases,
                'avg_release_interval': sum(intervals) / len(intervals) if intervals else 0,
                'release_intervals': intervals
            }
        
        except Exception as e:
            return {"error": f"Could not analyze releases: {str(e)}"}
    
    def _calculate_velocity_trend_optimized(self, commits: List[Dict]) -> List[Dict]:
        """Optimized commit velocity trend calculation"""
        
        # Group commits by week efficiently using Counter
        weekly_data = Counter()
        
        for commit in commits:
            week_key = commit['date'].strftime('%Y-W%U')
            weekly_data[week_key] += 1
        
        # Convert to trend data sorted by week
        return [
            {'week': week, 'commits': count}
            for week, count in sorted(weekly_data.items())
        ]
    
    def _analyze_developer_timeline_optimized(self, commits: List[Dict]) -> Dict[str, List[Dict]]:
        """Optimized developer timeline analysis"""
        
        # Use nested defaultdict for better performance
        developer_activity = defaultdict(lambda: defaultdict(int))
        
        # Process all commits in single pass
        for commit in commits:
            author = commit['author']
            month_key = commit['date'].strftime('%Y-%m')
            developer_activity[author][month_key] += 1
        
        # Convert to required format
        result = {}
        for author, months_data in developer_activity.items():
            result[author] = [
                {'month': month, 'commits': count}
                for month, count in sorted(months_data.items())
            ]
        
        return result
    
    def _analyze_recent_file_changes_optimized(self, recent_commits: List[Dict]) -> Dict[str, int]:
        """Optimized recent file changes analysis using commit file data"""
        
        file_mentions = Counter()
        
        # Extract file information from commits if available
        for commit in recent_commits:
            # Use files data if available in commit
            if 'files' in commit and commit['files']:
                for file_path in commit['files']:
                    if any(file_path.endswith(ext) for ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rb', '.php', '.html', '.css']):
                        file_mentions[file_path] += 1
            else:
                # Fallback to message parsing
                message = commit['message'].lower()
                
                # Pre-compiled patterns for performance
                import re as regex_lib
                patterns = [
                    regex_lib.compile(r'(\w+\.py)', regex_lib.IGNORECASE),
                    regex_lib.compile(r'(\w+\.js)', regex_lib.IGNORECASE),
                    regex_lib.compile(r'(\w+\.ts)', regex_lib.IGNORECASE),
                    regex_lib.compile(r'(\w+\.java)', regex_lib.IGNORECASE),
                    regex_lib.compile(r'(\w+\.cpp)', regex_lib.IGNORECASE),
                    regex_lib.compile(r'(\w+\.c)', regex_lib.IGNORECASE),
                    regex_lib.compile(r'(\w+\.cs)', regex_lib.IGNORECASE),
                    regex_lib.compile(r'(\w+\.go)', regex_lib.IGNORECASE),
                    regex_lib.compile(r'(\w+\.rb)', regex_lib.IGNORECASE),
                    regex_lib.compile(r'(\w+\.php)', regex_lib.IGNORECASE),
                    regex_lib.compile(r'(\w+\.html)', regex_lib.IGNORECASE),
                    regex_lib.compile(r'(\w+\.css)', regex_lib.IGNORECASE)
                ]
                
                for pattern in patterns:
                    matches = pattern.findall(message)
                    for match in matches:
                        file_mentions[match] += 1
        
        return dict(file_mentions)
    
    def _calculate_velocity_trend(self, commits: List[Dict]) -> List[Dict]:
        """Calculate commit velocity trend over time"""
        
        # Group commits by week
        weekly_data = defaultdict(int)
        
        for commit in commits:
            week_key = commit['date'].strftime('%Y-W%U')
            weekly_data[week_key] += 1
        
        # Convert to trend data
        trend_data = []
        for week, count in sorted(weekly_data.items()):
            trend_data.append({
                'week': week,
                'commits': count
            })
        
        return trend_data
    
    def _analyze_developer_timeline(self, commits: List[Dict]) -> Dict[str, List[Dict]]:
        """Analyze when each developer was active"""
        
        developer_activity = defaultdict(list)
        
        for commit in commits:
            author = commit['author']
            month_key = commit['date'].strftime('%Y-%m')
            
            # Find existing month entry or create new one
            month_entry = None
            for entry in developer_activity[author]:
                if entry['month'] == month_key:
                    month_entry = entry
                    break
            
            if month_entry:
                month_entry['commits'] += 1
            else:
                developer_activity[author].append({
                    'month': month_key,
                    'commits': 1
                })
        
        return dict(developer_activity)
    
    def _analyze_recent_file_changes(self, recent_commits: List[Dict]) -> Dict[str, int]:
        """Analyze which files have been changed recently"""
        
        # This is a simplified version - in a real implementation,
        # you'd parse the actual file changes from git diff
        file_mentions = defaultdict(int)
        
        for commit in recent_commits:
            # Simple heuristic: look for file extensions in commit messages
            message = commit['message'].lower()
            
            # Common file patterns
            patterns = [
                r'(\w+\.py)', r'(\w+\.js)', r'(\w+\.ts)', r'(\w+\.java)',
                r'(\w+\.cpp)', r'(\w+\.c)', r'(\w+\.cs)', r'(\w+\.go)',
                r'(\w+\.rb)', r'(\w+\.php)', r'(\w+\.html)', r'(\w+\.css)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, message)
                for match in matches:
                    file_mentions[match] += 1
        
        return dict(file_mentions)
    
    def _get_most_active_authors(self, commits: List[Dict]) -> List[Dict]:
        """Get most active authors in given commits"""
        
        author_stats = defaultdict(int)
        for commit in commits:
            author_stats[commit['author']] += 1
        
        return [
            {"author": author, "commits": count}
            for author, count in sorted(author_stats.items(), key=lambda x: x[1], reverse=True)
        ]
    
    def _calculate_project_age(self, commits: List[Dict]) -> Dict[str, Any]:
        """Calculate project age and milestones"""
        
        if not commits:
            return {}
        
        sorted_commits = sorted(commits, key=lambda x: x['date'])
        first_commit = sorted_commits[0]
        last_commit = sorted_commits[-1]
        
        age_days = (last_commit['date'] - first_commit['date']).days
        
        return {
            'first_commit_date': first_commit['date'],
            'last_commit_date': last_commit['date'],
            'age_days': age_days,
            'age_months': age_days / 30.44,
            'age_years': age_days / 365.25
        }
    
    def render(self):
        """Render the timeline analysis"""
        # Add rerun button
        self.add_rerun_button("timeline_analysis")
        
        with self.display_loading_message("Analyzing project timeline..."):
            analysis = self.analyze()
        
        if "error" in analysis:
            self.display_error(analysis["error"])
            return
        
        # Project overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Commits", analysis["total_commits"])
        
        with col2:
            age_data = analysis["project_age"]
            if age_data:
                st.metric("Project Age", f"{age_data['age_years']:.1f} years")
        
        with col3:
            recent_data = analysis["recent_changes"]
            st.metric("Recent Commits (30d)", recent_data["total_recent_commits"])
        
        with col4:
            if analysis["release_patterns"] and "total_releases" in analysis["release_patterns"]:
                st.metric("Total Releases", analysis["release_patterns"]["total_releases"])
            else:
                st.metric("Total Releases", "N/A")
        
        # Timeline visualization
        st.subheader("📈 Commit Timeline")
        
        timeline_data = analysis["timeline_data"]
        
        # Monthly commit trend
        if timeline_data["monthly_commits"]:
            monthly_df = pd.DataFrame([
                {"Month": month, "Commits": count}
                for month, count in sorted(timeline_data["monthly_commits"].items())
            ])
            
            fig_monthly = px.line(
                monthly_df,
                x='Month',
                y='Commits',
                title="Monthly Commit Activity",
                markers=True
            )
            fig_monthly.update_xaxes(tickangle=45)
            st.plotly_chart(fig_monthly, use_container_width=True)
        
        # Weekly velocity trend
        if timeline_data["velocity_trend"]:
            velocity_df = pd.DataFrame(timeline_data["velocity_trend"])
            
            fig_velocity = px.line(
                velocity_df,
                x='week',
                y='commits',
                title="Weekly Commit Velocity",
                markers=True
            )
            fig_velocity.update_xaxes(tickangle=45)
            st.plotly_chart(fig_velocity, use_container_width=True)
        
        # Hourly commit patterns
        if timeline_data["hourly_commits"]:
            hourly_df = pd.DataFrame([
                {"Hour": hour, "Commits": count}
                for hour, count in sorted(timeline_data["hourly_commits"].items())
            ])
            
            fig_hourly = px.bar(
                hourly_df,
                x='Hour',
                y='Commits',
                title="Commit Activity by Hour of Day"
            )
            st.plotly_chart(fig_hourly, use_container_width=True)
        
        # Recent changes analysis
        st.subheader("🆕 Recent Changes (Last 30 Days)")
        
        recent_data = analysis["recent_changes"]
        
        if recent_data["total_recent_commits"] > 0:
            # Recent activity breakdown
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Features", len(recent_data["feature_commits"]))
            with col2:
                st.metric("Bug Fixes", len(recent_data["bug_fixes"]))
            with col3:
                st.metric("Refactoring", len(recent_data["refactoring"]))
            with col4:
                st.metric("Documentation", len(recent_data["documentation"]))
            
            # Recent commit types chart
            commit_type_data = [
                {"Type": "Features", "Count": len(recent_data["feature_commits"])},
                {"Type": "Bug Fixes", "Count": len(recent_data["bug_fixes"])},
                {"Type": "Refactoring", "Count": len(recent_data["refactoring"])},
                {"Type": "Documentation", "Count": len(recent_data["documentation"])},
                {"Type": "Other", "Count": len(recent_data["other_commits"])}
            ]
            
            commit_type_df = pd.DataFrame(commit_type_data)
            fig_recent_types = px.pie(
                commit_type_df,
                values='Count',
                names='Type',
                title="Recent Commit Types Distribution"
            )
            st.plotly_chart(fig_recent_types, use_container_width=True)
            
            # Most active recent authors
            if recent_data["most_active_recent_authors"]:
                st.write("**Most Active Recent Contributors:**")
                recent_authors_df = pd.DataFrame(recent_data["most_active_recent_authors"][:10])
                
                fig_recent_authors = px.bar(
                    recent_authors_df,
                    x='author',
                    y='commits',
                    title="Most Active Contributors (Last 30 Days)"
                )
                fig_recent_authors.update_xaxes(tickangle=45)
                st.plotly_chart(fig_recent_authors, use_container_width=True)
            
            # Recent commits details
            st.write("**Recent Feature Commits:**")
            for commit in recent_data["feature_commits"][:5]:
                with st.expander(f"{commit['message'][:60]}... - {commit['author']}"):
                    st.write(f"**Author:** {commit['author']}")
                    st.write(f"**Date:** {commit['date'].strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Hash:** {commit['hash'][:8]}")
                    st.write(f"**Message:** {commit['message']}")
        else:
            st.info("No recent commits found in the last 30 days")
        
        # Development phases
        st.subheader("🔄 Development Phases")
        
        phases = analysis["development_phases"]
        if phases:
            phases_df = pd.DataFrame([
                {
                    "Phase": f"Phase {i+1}",
                    "Start": phase['start_date'].strftime('%Y-%m-%d'),
                    "End": phase['end_date'].strftime('%Y-%m-%d'),
                    "Duration (days)": phase['duration_days'],
                    "Commits": phase['commit_count'],
                    "Authors": phase['author_count'],
                    "Dominant Activity": phase['dominant_activity'],
                    "Velocity": round(phase['velocity'], 2)
                }
                for i, phase in enumerate(phases)
            ])
            
            st.dataframe(phases_df, use_container_width=True)
            
            # Phase velocity chart
            fig_phases = px.bar(
                phases_df,
                x='Phase',
                y='Velocity',
                title="Development Phase Velocity (Commits per Day)",
                color='Dominant Activity'
            )
            st.plotly_chart(fig_phases, use_container_width=True)
        else:
            st.info("Not enough commit history to identify development phases")
        
        # File evolution
        st.subheader("📁 File Evolution")
        
        file_evolution = analysis.get("file_evolution", {})
        
        # Defensive check - ensure file_evolution is always a dictionary
        if not isinstance(file_evolution, dict):
            st.info(f"File evolution data format issue - got {type(file_evolution).__name__} instead of dict")
        elif not file_evolution:
            st.info("No file evolution data available")
        elif 'total_files_analyzed' in file_evolution:
            # New simplified format - show basic stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Files Analyzed", file_evolution.get('total_files_analyzed', 0))
            with col2:
                st.metric("Most Common Extension", file_evolution.get('most_common_extension', 'unknown'))
            with col3:
                extensions = file_evolution.get('file_extensions', {})
                st.metric("Extension Types", len(extensions))
            
            # Show file extensions breakdown
            if extensions:
                ext_df = pd.DataFrame([
                    {"Extension": ext, "Mentions": count}
                    for ext, count in extensions.items()
                ])
                
                fig_ext = px.bar(
                    ext_df,
                    x='Extension',
                    y='Mentions',
                    title="File Extensions in Commit Messages"
                )
                st.plotly_chart(fig_ext, use_container_width=True)
        
        elif any('total_commits' in str(v) for v in file_evolution.values() if isinstance(v, dict)):
            # Old detailed format - keep original logic
            try:
                active_files = sorted(
                    [(path, stats) for path, stats in file_evolution.items() 
                     if isinstance(stats, dict) and isinstance(stats.get('total_commits'), (int, float))],
                    key=lambda x: x[1].get('total_commits', 0),
                    reverse=True
                )[:20]
            except (KeyError, TypeError, AttributeError):
                active_files = []
            
            if active_files:
                files_df = pd.DataFrame([
                    {
                        "File": path,
                        "Total Commits": stats['total_commits'],
                        "Contributors": stats.get('contributors', 0),
                        "Recent Activity": stats.get('recent_activity', 0),
                        "Age (days)": (datetime.now() - stats['first_commit'].replace(tzinfo=None)).days if stats.get('first_commit') else 0
                    }
                    for path, stats in active_files
                ])
                
                st.write("**Most Active Files:**")
                st.dataframe(files_df, use_container_width=True)
                
                # File activity visualization
                fig_files = px.scatter(
                    files_df.head(15),
                    x='Age (days)',
                    y='Total Commits',
                    size='Contributors',
                    hover_name='File',
                    title="File Activity vs Age"
                )
                st.plotly_chart(fig_files, use_container_width=True)
            else:
                st.info("No detailed file evolution data available")
        else:
            st.info("File evolution data format not recognized")
        
        # Release patterns
        st.subheader("🚀 Release Patterns")
        
        release_data = analysis["release_patterns"]
        if release_data and "releases" in release_data and release_data["releases"]:
            releases_df = pd.DataFrame([
                {
                    "Release": release['name'],
                    "Date": release['date'].strftime('%Y-%m-%d'),
                    "Commit": release['commit'][:8]
                }
                for release in release_data["releases"]
            ])
            
            st.dataframe(releases_df, use_container_width=True)
            
            if release_data["avg_release_interval"] > 0:
                st.metric("Average Release Interval", f"{release_data['avg_release_interval']:.1f} days")
            
            # Release timeline
            if len(release_data["releases"]) > 1:
                releases_timeline_df = pd.DataFrame([
                    {"Release": r['name'], "Date": r['date']}
                    for r in release_data["releases"]
                ])
                
                fig_releases = px.scatter(
                    releases_timeline_df,
                    x='Date',
                    y=[1] * len(releases_timeline_df),
                    hover_name='Release',
                    title="Release Timeline"
                )
                fig_releases.update_yaxes(visible=False)
                st.plotly_chart(fig_releases, use_container_width=True)
        else:
            st.info("No release tags found in the repository")
        
        # Enhanced Analysis Sections
        st.header("🚀 Enhanced Historical Evolution Analysis")
        st.markdown("Advanced insights into project evolution patterns and trends")
        
        # Feature Addition Patterns
        st.subheader("📊 Feature Addition Patterns")
        feature_data = analysis.get("feature_patterns", {})
        
        if feature_data and feature_data.get("total_feature_commits", 0) > 0:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Feature Commits", feature_data["total_feature_commits"])
            with col2:
                most_common_type = max(feature_data["feature_categories"].items(), key=lambda x: x[1]) if feature_data["feature_categories"] else ("N/A", 0)
                st.metric("Most Common Feature Type", most_common_type[0])
            with col3:
                st.metric("Integration Approaches", len(feature_data.get("integration_approaches", {})))
            with col4:
                developer_insights = feature_data.get("developer_insights", {})
                st.metric("Avg Files per Feature", f"{developer_insights.get('avg_files_per_feature', 0):.1f}")
            
            # Feature categories distribution
            if feature_data["feature_categories"]:
                categories_df = pd.DataFrame([
                    {"Category": category, "Count": count}
                    for category, count in feature_data["feature_categories"].items()
                ])
                
                fig_feature_categories = px.pie(
                    categories_df,
                    values='Count',
                    names='Category',
                    title="Feature Categories Distribution"
                )
                st.plotly_chart(fig_feature_categories, use_container_width=True)
            
            # Feature velocity over time
            if feature_data.get("feature_velocity"):
                velocity_df = pd.DataFrame([
                    {"Quarter": quarter, "Features": count}
                    for quarter, count in sorted(feature_data["feature_velocity"].items())
                ])
                
                fig_feature_velocity = px.line(
                    velocity_df,
                    x='Quarter',
                    y='Features',
                    title="Feature Addition Velocity Over Time",
                    markers=True
                )
                st.plotly_chart(fig_feature_velocity, use_container_width=True)
            
            # Best practices and insights
            if feature_data.get("best_practices"):
                st.write("**🎯 Identified Best Practices:**")
                for practice in feature_data["best_practices"]:
                    st.write(f"• {practice}")
            
            # Recent features highlights
            if feature_data.get("recent_features"):
                st.write("**🆕 Recent Feature Highlights:**")
                for feature in feature_data["recent_features"][:5]:
                    with st.expander(f"🔧 {feature['type'].title()} Feature - {feature['hash']} ({feature['date']})"):
                        st.write(f"**Message:** {feature['message']}")
                        st.write(f"**Author:** {feature['author']}")
                        st.write(f"**Files Impacted:** {feature['files_impacted']}")
        else:
            st.info("No feature addition patterns found in the commit history")
        
        # Architecture Migration History
        st.subheader("🏗️ Architecture Migration History")
        arch_data = analysis.get("architecture_migration", {})
        
        if arch_data and arch_data.get("total_migration_commits", 0) > 0:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Migration Commits", arch_data["total_migration_commits"])
            with col2:
                trends = arch_data.get("migration_trends", {})
                st.metric("Migration Velocity", f"{trends.get('migration_velocity', 0):.1f}%")
            with col3:
                st.metric("Technology Adoptions", len(arch_data.get("technology_adoptions", {})))
            with col4:
                debt_indicators = arch_data.get("architectural_debt_indicators", {})
                st.metric("Debt Risk Level", debt_indicators.get("risk_level", "Unknown"))
            
            # Architecture evolution timeline
            if arch_data.get("architecture_evolution"):
                evolution_data = []
                for category, commits in arch_data["architecture_evolution"].items():
                    for commit in commits:
                        evolution_data.append({
                            "Date": commit["date"],
                            "Category": category.replace("_", " ").title(),
                            "Message": commit["message"][:60] + "...",
                            "Author": commit["author"],
                            "Hash": commit["hash"]
                        })
                
                if evolution_data:
                    evolution_df = pd.DataFrame(evolution_data)
                    
                    fig_arch_timeline = px.scatter(
                        evolution_df,
                        x='Date',
                        y='Category',
                        color='Category',
                        hover_data=['Message', 'Author', 'Hash'],
                        title="Architecture Evolution Timeline"
                    )
                    fig_arch_timeline.update_xaxes(tickangle=45)
                    st.plotly_chart(fig_arch_timeline, use_container_width=True)
            
            # Migration phases
            if arch_data.get("migration_phases"):
                st.write("**📅 Major Migration Phases:**")
                for phase in arch_data["migration_phases"]:
                    with st.expander(f"📆 {phase['period']} - {phase['dominant_type'].replace('_', ' ').title()} ({phase['commits_count']} commits)"):
                        st.write(f"**Complexity Score:** {phase['complexity_avg']:.1f}/10")
                        st.write("**Key Changes:**")
                        for highlight in phase["highlights"]:
                            st.write(f"• {highlight}")
            
            # Technology adoptions
            if arch_data.get("technology_adoptions"):
                tech_df = pd.DataFrame([
                    {"Technology": tech, "Mentions": count}
                    for tech, count in arch_data["technology_adoptions"].items()
                ])
                
                fig_tech = px.bar(
                    tech_df,
                    x='Technology',
                    y='Mentions',
                    title="Technology Adoption Frequency"
                )
                st.plotly_chart(fig_tech, use_container_width=True)
            
            # Maturity indicators
            maturity = arch_data.get("maturity_indicators", {})
            if maturity:
                st.write("**🎯 Architecture Maturity Indicators:**")
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.write("🔄 Microservices:", "✅" if maturity.get("microservices") else "❌")
                with col2:
                    st.write("📦 Containerization:", "✅" if maturity.get("containerization") else "❌")
                with col3:
                    st.write("☁️ Cloud Native:", "✅" if maturity.get("cloud_native") else "❌")
                with col4:
                    st.write("🚀 CI/CD:", "✅" if maturity.get("ci_cd") else "❌")
                with col5:
                    st.write("📊 Monitoring:", "✅" if maturity.get("monitoring") else "❌")
        else:
            st.info("No architecture migration history found in the commit history")
        
        # Performance Evolution
        st.subheader("⚡ Performance Evolution")
        perf_data = analysis.get("performance_evolution", {})
        
        if perf_data and perf_data.get("total_performance_commits", 0) > 0:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Performance Commits", perf_data["total_performance_commits"])
            with col2:
                trends = perf_data.get("performance_trends", {})
                st.metric("Improvement Velocity", f"{trends.get('improvement_velocity', 0):.1f}%")
            with col3:
                st.metric("Regressions", len(perf_data.get("performance_regressions", [])))
            with col4:
                developer_insights = perf_data.get("developer_insights", {})
                st.metric("Avg Impact Score", f"{developer_insights.get('avg_impact_per_commit', 0):.1f}")
            
            # Performance optimization types
            if perf_data.get("optimization_types"):
                opt_df = pd.DataFrame([
                    {"Type": opt_type.replace("_", " ").title(), "Count": count}
                    for opt_type, count in perf_data["optimization_types"].items()
                ])
                
                fig_perf_types = px.bar(
                    opt_df,
                    x='Type',
                    y='Count',
                    title="Performance Optimization Types"
                )
                fig_perf_types.update_xaxes(tickangle=45)
                st.plotly_chart(fig_perf_types, use_container_width=True)
            
            # Quarterly performance improvements
            if perf_data.get("quarterly_improvements"):
                quarterly_data = []
                for quarter, data in perf_data["quarterly_improvements"].items():
                    quarterly_data.append({
                        "Quarter": quarter,
                        "Count": data["count"],
                        "Avg Impact": data["avg_impact"]
                    })
                
                if quarterly_data:
                    quarterly_df = pd.DataFrame(quarterly_data)
                    
                    fig_quarterly_perf = px.line(
                        quarterly_df,
                        x='Quarter',
                        y='Count',
                        title="Quarterly Performance Improvements",
                        markers=True
                    )
                    st.plotly_chart(fig_quarterly_perf, use_container_width=True)
            
            # Key optimizations
            if perf_data.get("key_optimizations"):
                st.write("**🚀 Key Performance Optimizations:**")
                for optimization in perf_data["key_optimizations"][:5]:
                    with st.expander(f"⚡ {optimization['type'].replace('_', ' ').title()} - {optimization['hash']} (Impact: {optimization['impact_estimate']}/10)"):
                        st.write(f"**Date:** {optimization['date']}")
                        st.write(f"**Author:** {optimization['author']}")
                        st.write(f"**Message:** {optimization['message']}")
            
            # Performance champions
            champions = perf_data.get("developer_insights", {}).get("performance_champions", [])
            if champions:
                st.write("**🏆 Performance Champions:**")
                champions_df = pd.DataFrame([
                    {"Developer": champ[0], "Contributions": champ[1]}
                    for champ in champions[:5]
                ])
                
                fig_champions = px.bar(
                    champions_df,
                    x='Developer',
                    y='Contributions',
                    title="Top Performance Contributors"
                )
                st.plotly_chart(fig_champions, use_container_width=True)
        else:
            st.info("No performance evolution data found in the commit history")
        
        # Security Evolution
        st.subheader("🔒 Security Evolution")
        sec_data = analysis.get("security_evolution", {})
        
        if sec_data and sec_data.get("total_security_commits", 0) > 0:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Security Commits", sec_data["total_security_commits"])
            with col2:
                maturity = sec_data.get("security_maturity", {})
                st.metric("Security Maturity", maturity.get("maturity_level", "Unknown"))
            with col3:
                st.metric("Vulnerability Responses", len(sec_data.get("vulnerability_responses", [])))
            with col4:
                trends = sec_data.get("security_trends", {})
                avg_response_time = trends.get("vulnerability_response_avg", 0)
                st.metric("Avg Response Time", f"{avg_response_time:.0f} days")
            
            # Security domains distribution
            if sec_data.get("security_domains"):
                domains_df = pd.DataFrame([
                    {"Domain": domain.replace("_", " ").title(), "Count": count}
                    for domain, count in sec_data["security_domains"].items()
                ])
                
                fig_sec_domains = px.pie(
                    domains_df,
                    values='Count',
                    names='Domain',
                    title="Security Domains Focus"
                )
                st.plotly_chart(fig_sec_domains, use_container_width=True)
            
            # Security maturity assessment
            maturity = sec_data.get("security_maturity", {})
            if maturity.get("indicators"):
                st.write("**🛡️ Security Maturity Assessment:**")
                indicators = maturity["indicators"]
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write("🔐 Modern Auth:", "✅" if indicators.get("modern_authentication") else "❌")
                with col2:
                    st.write("🔒 Encryption:", "✅" if indicators.get("encryption_practices") else "❌")
                with col3:
                    st.write("🛡️ Validation:", "✅" if indicators.get("input_validation") else "❌")
                with col4:
                    st.write("📋 Headers:", "✅" if indicators.get("security_headers") else "❌")
            
            # Framework adoptions timeline
            if sec_data.get("framework_adoptions"):
                st.write("**📚 Security Framework Adoptions:**")
                for adoption in sec_data["framework_adoptions"][:5]:
                    st.write(f"• **{adoption['framework'].upper()}** adopted on {adoption['date']} (Commit: {adoption['hash']})")
            
            # Security recommendations
            if maturity.get("recommendations"):
                st.write("**💡 Security Recommendations:**")
                for recommendation in maturity["recommendations"]:
                    st.write(f"• {recommendation}")
            
            # Recent security work
            if sec_data.get("recent_security_work"):
                st.write("**🔒 Recent Security Work:**")
                for work in sec_data["recent_security_work"][:5]:
                    with st.expander(f"🔐 {work['type'].replace('_', ' ').title()} - {work['hash']} (Severity: {work['severity']}/5)"):
                        st.write(f"**Date:** {work['date']}")
                        st.write(f"**Author:** {work['author']}")
                        st.write(f"**Message:** {work['message']}")
        else:
            st.info("No security evolution data found in the commit history")
        
        
        # Add save options
        self.add_save_options("timeline_analysis", analysis)
    
    def _get_ultra_optimized_timeline_data(self, token=None, max_commits=300) -> Dict[str, Any]:
        """Ultra-optimized timeline data retrieval with minimal processing"""
        try:
            # Use fastest git command possible
            cmd = [
                'git', 'log', '--oneline', '--pretty=format:%H|%an|%ci|%s', 
                f'-{max_commits}', '--no-merges'
            ]
            
            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True, timeout=60
            )
            
            if result.returncode != 0:
                # Quick fallback
                commits = self.get_git_history_cancellable(max_commits=max_commits//2, token=token)
                return {'commits': commits, 'file_data': {}}
            
            # Fast parsing without file data collection
            commits = []
            lines = result.stdout.strip().split('\n')
            
            for line in lines:
                if token and len(commits) % 100 == 0:
                    token.check_cancellation()
                
                if '|' in line:
                    parts = line.split('|', 3)  # Limit splits for speed
                    if len(parts) >= 4:
                        commit_hash, author, date, message = parts
                        commits.append({
                            'hash': commit_hash,
                            'author': author,
                            'email': '',  # Skip email for speed
                            'date': pd.to_datetime(date),
                            'message': message.strip(),
                            'files': []  # Skip files for speed
                        })
            
            return {'commits': commits, 'file_data': {}}
            
        except Exception as e:
            # Ultra-quick fallback
            commits = self.get_git_history_cancellable(max_commits=100, token=token)
            return {'commits': commits[:100], 'file_data': {}}
    
    def _analyze_timeline_patterns_ultra_fast(self, commits: List[Dict], token=None) -> Dict[str, Any]:
        """Ultra-fast timeline patterns analysis"""
        
        # Pre-allocate for speed
        monthly_commits = Counter()
        hourly_commits = Counter()
        
        # Single pass through commits
        for commit in commits:
            if token:
                token.check_cancellation()
            
            date = commit['date']
            monthly_commits[date.strftime('%Y-%m')] += 1
            hourly_commits[date.hour] += 1
        
        # Simplified velocity calculation
        velocity_trend = []
        if monthly_commits:
            for month, count in sorted(monthly_commits.items())[-12:]:  # Last 12 months only
                velocity_trend.append({'week': month, 'commits': count})
        
        return {
            "daily_commits": {},  # Skip for speed
            "weekly_commits": {},  # Skip for speed  
            "monthly_commits": dict(monthly_commits),
            "hourly_commits": dict(hourly_commits),
            "velocity_trend": velocity_trend,
            "developer_timeline": {}  # Skip for speed
        }
    
    def _analyze_recent_changes_ultra_fast(self, commits: List[Dict], token=None, days: int = 30) -> Dict[str, Any]:
        """Ultra-fast recent changes analysis"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_commits = [c for c in commits if c['date'].replace(tzinfo=None) > cutoff_date]
        
        if not recent_commits:
            return {
                "total_recent_commits": 0,
                "feature_commits": [],
                "bug_fixes": [],
                "refactoring": [],
                "documentation": [],
                "other_commits": [],
                "recent_file_changes": {},
                "most_active_recent_authors": []
            }
        
        # Use pre-compiled class patterns for maximum speed
        categorized_commits = {
            'feature': [],
            'fix': [],
            'refactor': [],
            'docs': [],
            'other': []
        }
        
        # Fast categorization using class-level patterns
        for commit in recent_commits:
            if token:
                token.check_cancellation()
            
            message = commit['message']
            categorized = False
            
            if self._COMMIT_PATTERNS['feature'].search(message):
                categorized_commits['feature'].append(commit)
                categorized = True
            elif self._COMMIT_PATTERNS['fix'].search(message):
                categorized_commits['fix'].append(commit)
                categorized = True
            elif self._COMMIT_PATTERNS['refactor'].search(message):
                categorized_commits['refactor'].append(commit)
                categorized = True
            elif self._COMMIT_PATTERNS['docs'].search(message):
                categorized_commits['docs'].append(commit)
                categorized = True
            
            if not categorized:
                categorized_commits['other'].append(commit)
        
        # Quick author stats
        author_count = Counter(commit['author'] for commit in recent_commits)
        most_active = [
            {"author": author, "commits": count}
            for author, count in author_count.most_common(5)
        ]
        
        return {
            "total_recent_commits": len(recent_commits),
            "feature_commits": categorized_commits['feature'],
            "bug_fixes": categorized_commits['fix'],
            "refactoring": categorized_commits['refactor'],
            "documentation": categorized_commits['docs'],
            "other_commits": categorized_commits['other'],
            "recent_file_changes": {},  # Skip for speed
            "most_active_recent_authors": most_active
        }
    
    def _identify_development_phases_ultra_fast(self, commits: List[Dict], token=None) -> List[Dict]:
        """Ultra-fast development phases identification"""
        
        if len(commits) < 20:  # Require more commits for meaningful phases
            return []
        
        # Simple chunking approach
        sorted_commits = sorted(commits, key=lambda x: x['date'])
        chunk_size = max(20, len(commits) // 5)  # Max 5 phases for speed
        phases = []
        
        for i in range(0, min(len(sorted_commits), chunk_size * 5), chunk_size):
            if token:
                token.check_cancellation()
            
            chunk = sorted_commits[i:i + chunk_size]
            if len(chunk) < 10:
                continue
            
            start_date = chunk[0]['date']
            end_date = chunk[-1]['date']
            duration = (end_date - start_date).days
            
            # Fast activity classification using pre-compiled patterns
            activity_counts = Counter()
            authors = set()
            
            for commit in chunk:
                authors.add(commit['author'])
                message = commit['message']
                
                # Quick classification using class patterns
                if self._COMMIT_PATTERNS['initialization'].search(message):
                    activity_counts['initialization'] += 1
                elif self._COMMIT_PATTERNS['feature'].search(message):
                    activity_counts['feature_development'] += 1
                elif self._COMMIT_PATTERNS['fix'].search(message):
                    activity_counts['bug_fixing'] += 1
                elif self._COMMIT_PATTERNS['refactor'].search(message):
                    activity_counts['refactoring'] += 1
                else:
                    activity_counts['maintenance'] += 1
            
            # Quick dominant activity determination
            dominant_type = activity_counts.most_common(1)[0][0] if activity_counts else 'maintenance'
            
            phases.append({
                'start_date': start_date,
                'end_date': end_date,
                'duration_days': duration,
                'commit_count': len(chunk),
                'author_count': len(authors),
                'dominant_activity': dominant_type,
                'commit_types': dict(activity_counts),
                'velocity': len(chunk) / max(1, duration) if duration > 0 else len(chunk)
            })
        
        return phases
    
    def _get_simple_file_stats(self, commits_data: Dict) -> Dict[str, Any]:
        """Simple file statistics without complex analysis - guaranteed to return dict"""
        
        # Default return structure to avoid any TypeError issues
        default_result = {
            'total_files_analyzed': 0,
            'file_extensions': {},
            'most_common_extension': 'unknown'
        }
        
        # Just return basic file count info for speed
        commits = commits_data.get('commits', [])
        if not commits:
            return default_result
        
        try:
            # Simple file extension analysis from commit messages
            file_extensions = Counter()
            total_files_mentioned = 0
            
            for commit in commits[:100]:  # Limit for speed
                message = commit['message'].lower()
                
                # Quick regex for common extensions
                for ext in ['.py', '.js', '.ts', '.java', '.cpp', '.html', '.css']:
                    if ext in message:
                        file_extensions[ext] += 1
                        total_files_mentioned += 1
            
            result = {
                'total_files_analyzed': total_files_mentioned,
                'file_extensions': dict(file_extensions),
                'most_common_extension': file_extensions.most_common(1)[0][0] if file_extensions else 'unknown'
            }
            
            # Ensure we always return a valid dictionary
            return result if isinstance(result, dict) else default_result
            
        except Exception:
            # Return safe default on any error
            return default_result
    
    def _get_quick_release_info(self) -> Dict[str, Any]:
        """Quick release information without detailed analysis"""
        
        try:
            # Quick git tag count
            cmd = ['git', 'tag', '--list']
            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                tags = [tag.strip() for tag in result.stdout.strip().split('\n') if tag.strip()]
                return {
                    'total_releases': len(tags),
                    'releases': [],  # Skip detailed release info for speed
                    'avg_release_interval': 0,
                    'release_intervals': []
                }
            
        except Exception:
            pass
        
        return {'total_releases': 0, 'releases': [], 'avg_release_interval': 0, 'release_intervals': []}
    
    def _calculate_project_age_fast(self, commits: List[Dict]) -> Dict[str, Any]:
        """Fast project age calculation"""
        
        if not commits:
            return {}
        
        # Just use first and last commits from the already sorted list
        dates = [commit['date'] for commit in commits]
        first_date = min(dates)
        last_date = max(dates)
        
        age_days = (last_date - first_date).days
        
        return {
            'first_commit_date': first_date,
            'last_commit_date': last_date,
            'age_days': age_days,
            'age_months': age_days / 30.44,
            'age_years': age_days / 365.25
        }
    
    def _analyze_feature_addition_patterns(self, commits: List[Dict], token=None) -> Dict[str, Any]:
        """Analyze how new features and capabilities have been integrated over time"""
        
        # Feature identification patterns
        feature_patterns = {
            'api_features': re.compile(r'(api|endpoint|route|service)', re.IGNORECASE),
            'ui_features': re.compile(r'(ui|component|page|form|button|modal)', re.IGNORECASE),
            'database_features': re.compile(r'(database|table|schema|migration|model)', re.IGNORECASE),
            'auth_features': re.compile(r'(auth|login|signup|permission|role)', re.IGNORECASE),
            'integration_features': re.compile(r'(integration|external|third.party|webhook)', re.IGNORECASE),
            'performance_features': re.compile(r'(cache|optimize|performance|speed)', re.IGNORECASE)
        }
        
        feature_commits = []
        feature_categories = Counter()
        feature_timeline = defaultdict(list)
        integration_approaches = Counter()
        
        for commit in commits:
            if token:
                token.check_cancellation()
            
            message = commit['message'].lower()
            
            # Check if it's a feature commit
            if self._COMMIT_PATTERNS['feature'].search(commit['message']):
                # Categorize the feature
                feature_type = 'general'
                for category, pattern in feature_patterns.items():
                    if pattern.search(message):
                        feature_type = category
                        break
                
                feature_categories[feature_type] += 1
                
                # Track integration approaches
                if any(keyword in message for keyword in ['module', 'class', 'function']):
                    integration_approaches['modular'] += 1
                elif any(keyword in message for keyword in ['config', 'setting', 'parameter']):
                    integration_approaches['configurable'] += 1
                elif any(keyword in message for keyword in ['extend', 'inherit', 'override']):
                    integration_approaches['extensible'] += 1
                else:
                    integration_approaches['direct'] += 1
                
                # Timeline tracking
                quarter = f"{commit['date'].year}-Q{(commit['date'].month-1)//3 + 1}"
                feature_timeline[quarter].append({
                    'type': feature_type,
                    'message': commit['message'][:100],
                    'hash': commit['hash'][:8],
                    'date': commit['date'].strftime('%Y-%m-%d'),
                    'author': commit['author']
                })
                
                feature_commits.append({
                    'hash': commit['hash'][:8],
                    'message': commit['message'],
                    'author': commit['author'],
                    'date': commit['date'].strftime('%Y-%m-%d'),
                    'type': feature_type,
                    'files_impacted': len(commit.get('files', [])) if commit.get('files') else 0
                })
        
        # Identify best practices and patterns
        best_practices = []
        if integration_approaches['modular'] > len(feature_commits) * 0.3:
            best_practices.append("Strong modular design approach in feature development")
        if integration_approaches['configurable'] > len(feature_commits) * 0.2:
            best_practices.append("Configuration-driven feature implementation")
        if len(set(fc['author'] for fc in feature_commits)) > len(feature_commits) * 0.5:
            best_practices.append("Collaborative feature development across team")
        
        # Calculate feature velocity
        feature_velocity = {}
        for quarter, features in feature_timeline.items():
            feature_velocity[quarter] = len(features)
        
        return {
            'total_feature_commits': len(feature_commits),
            'feature_categories': dict(feature_categories),
            'feature_timeline': dict(feature_timeline),
            'integration_approaches': dict(integration_approaches),
            'best_practices': best_practices,
            'feature_velocity': feature_velocity,
            'recent_features': feature_commits[:10],  # Last 10 features
            'feature_complexity_trend': self._analyze_feature_complexity(feature_commits),
            'developer_insights': {
                'most_prolific_feature_developer': max(Counter(fc['author'] for fc in feature_commits).items(), key=lambda x: x[1])[0] if feature_commits else None,
                'avg_files_per_feature': sum(fc['files_impacted'] for fc in feature_commits) / len(feature_commits) if feature_commits else 0
            }
        }
    
    def _analyze_architecture_migration_history(self, commits: List[Dict], token=None) -> Dict[str, Any]:
        """Analyze major architectural changes, migrations, and system evolution decisions"""
        
        # Architecture change patterns
        architecture_patterns = {
            'framework_migration': re.compile(r'(migrate|upgrade|framework|library|version)', re.IGNORECASE),
            'database_migration': re.compile(r'(database|db|migration|schema|table)', re.IGNORECASE),
            'infrastructure_changes': re.compile(r'(deploy|docker|container|cloud|server|infrastructure)', re.IGNORECASE),
            'api_evolution': re.compile(r'(api|rest|graphql|endpoint|service)', re.IGNORECASE),
            'security_hardening': re.compile(r'(security|auth|ssl|tls|encrypt|secure)', re.IGNORECASE),
            'performance_optimization': re.compile(r'(optimize|performance|cache|speed|memory)', re.IGNORECASE)
        }
        
        migration_commits = []
        architecture_evolution = defaultdict(list)
        technology_adoptions = Counter()
        migration_phases = []
        
        sorted_commits = sorted(commits, key=lambda x: x['date'])
        
        for commit in sorted_commits:
            if token:
                token.check_cancellation()
            
            message = commit['message'].lower()
            
            # Check for architectural changes
            for category, pattern in architecture_patterns.items():
                if pattern.search(commit['message']):
                    period = f"{commit['date'].year}-{commit['date'].month:02d}"
                    
                    # Track technology adoptions
                    tech_keywords = ['react', 'angular', 'vue', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'mongodb', 'postgresql', 'redis']
                    for tech in tech_keywords:
                        if tech in message:
                            technology_adoptions[tech] += 1
                    
                    architecture_evolution[category].append({
                        'hash': commit['hash'][:8],
                        'message': commit['message'],
                        'date': commit['date'].strftime('%Y-%m-%d'),
                        'author': commit['author'],
                        'period': period,
                        'files_impacted': len(commit.get('files', [])) if commit.get('files') else 0
                    })
                    
                    migration_commits.append({
                        'hash': commit['hash'][:8],
                        'message': commit['message'],
                        'date': commit['date'].strftime('%Y-%m-%d'),
                        'author': commit['author'],
                        'category': category,
                        'complexity_score': self._calculate_migration_complexity(commit['message'])
                    })
                    break
        
        # Identify major migration phases
        if migration_commits:
            # Group migrations by time periods
            period_groups = defaultdict(list)
            for commit in migration_commits:
                year_month = commit['date'][:7]  # YYYY-MM
                period_groups[year_month].append(commit)
            
            # Identify major phases (periods with multiple migrations)
            for period, commits_in_period in period_groups.items():
                if len(commits_in_period) >= 3:
                    dominant_category = Counter(c['category'] for c in commits_in_period).most_common(1)[0]
                    migration_phases.append({
                        'period': period,
                        'commits_count': len(commits_in_period),
                        'dominant_type': dominant_category[0],
                        'complexity_avg': sum(c['complexity_score'] for c in commits_in_period) / len(commits_in_period),
                        'highlights': [c['message'][:80] + '...' for c in commits_in_period[:3]]
                    })
        
        # Architecture maturity assessment
        maturity_indicators = {
            'microservices': any('microservice' in c['message'].lower() for c in migration_commits),
            'containerization': any(keyword in c['message'].lower() for c in migration_commits for keyword in ['docker', 'container']),
            'cloud_native': any(keyword in c['message'].lower() for c in migration_commits for keyword in ['cloud', 'aws', 'azure', 'gcp']),
            'ci_cd': any(keyword in c['message'].lower() for c in migration_commits for keyword in ['ci', 'cd', 'pipeline', 'deploy']),
            'monitoring': any(keyword in c['message'].lower() for c in migration_commits for keyword in ['monitor', 'log', 'metric', 'alert'])
        }
        
        return {
            'total_migration_commits': len(migration_commits),
            'architecture_evolution': dict(architecture_evolution),
            'technology_adoptions': dict(technology_adoptions),
            'migration_phases': migration_phases,
            'maturity_indicators': maturity_indicators,
            'recent_migrations': migration_commits[:10],
            'migration_trends': {
                'most_active_migration_type': max(architecture_evolution.keys(), key=lambda k: len(architecture_evolution[k])) if architecture_evolution else None,
                'migration_velocity': len(migration_commits) / max(1, len(commits)) * 100,  # Percentage
                'complexity_trend': [c['complexity_score'] for c in migration_commits[-10:]]
            },
            'architectural_debt_indicators': self._identify_architectural_debt(migration_commits)
        }
    
    def _analyze_performance_evolution(self, commits: List[Dict], token=None) -> Dict[str, Any]:
        """Track how system performance metrics have changed across releases and refactors"""
        
        # Performance-related patterns
        performance_patterns = {
            'optimization': re.compile(r'(optimize|performance|speed|fast|efficient)', re.IGNORECASE),
            'caching': re.compile(r'(cache|redis|memcache|cdn)', re.IGNORECASE),
            'database_perf': re.compile(r'(index|query|database|db.*perf|slow.*query)', re.IGNORECASE),
            'memory_management': re.compile(r'(memory|leak|garbage|allocation)', re.IGNORECASE),
            'concurrency': re.compile(r'(async|concurrent|parallel|thread|worker)', re.IGNORECASE),
            'network_perf': re.compile(r'(network|bandwidth|compression|gzip)', re.IGNORECASE)
        }
        
        performance_commits = []
        performance_timeline = defaultdict(list)
        optimization_types = Counter()
        performance_regressions = []
        
        for commit in commits:
            if token:
                token.check_cancellation()
            
            message = commit['message'].lower()
            
            # Check for performance-related commits
            perf_type = None
            for category, pattern in performance_patterns.items():
                if pattern.search(commit['message']):
                    perf_type = category
                    optimization_types[category] += 1
                    break
            
            # Also check for regression fixes
            if any(keyword in message for keyword in ['slow', 'timeout', 'bottleneck', 'regression']):
                if any(keyword in message for keyword in ['fix', 'resolve', 'improve']):
                    perf_type = 'regression_fix'
                    optimization_types['regression_fix'] += 1
                    performance_regressions.append({
                        'hash': commit['hash'][:8],
                        'message': commit['message'],
                        'date': commit['date'].strftime('%Y-%m-%d'),
                        'author': commit['author']
                    })
            
            if perf_type:
                quarter = f"{commit['date'].year}-Q{(commit['date'].month-1)//3 + 1}"
                performance_timeline[quarter].append({
                    'type': perf_type,
                    'message': commit['message'][:100],
                    'hash': commit['hash'][:8],
                    'date': commit['date'].strftime('%Y-%m-%d'),
                    'author': commit['author'],
                    'impact_estimate': self._estimate_performance_impact(commit['message'])
                })
                
                performance_commits.append({
                    'hash': commit['hash'][:8],
                    'message': commit['message'],
                    'date': commit['date'].strftime('%Y-%m-%d'),
                    'author': commit['author'],
                    'type': perf_type,
                    'impact_estimate': self._estimate_performance_impact(commit['message'])
                })
        
        # Calculate performance improvement trends
        quarterly_improvements = {}
        for quarter, improvements in performance_timeline.items():
            quarterly_improvements[quarter] = {
                'count': len(improvements),
                'avg_impact': sum(imp['impact_estimate'] for imp in improvements) / len(improvements) if improvements else 0,
                'types': Counter(imp['type'] for imp in improvements)
            }
        
        # Identify key optimizations
        key_optimizations = sorted(performance_commits, key=lambda x: x['impact_estimate'], reverse=True)[:10]
        
        return {
            'total_performance_commits': len(performance_commits),
            'optimization_types': dict(optimization_types),
            'performance_timeline': dict(performance_timeline),
            'quarterly_improvements': quarterly_improvements,
            'performance_regressions': performance_regressions,
            'key_optimizations': key_optimizations,
            'performance_trends': {
                'improvement_velocity': len(performance_commits) / max(1, len(commits)) * 100,
                'regression_rate': len(performance_regressions) / max(1, len(performance_commits)) * 100 if performance_commits else 0,
                'most_common_optimization': optimization_types.most_common(1)[0] if optimization_types else None
            },
            'architecture_correlation': self._correlate_performance_with_architecture(performance_commits),
            'developer_insights': {
                'performance_champions': Counter(pc['author'] for pc in performance_commits).most_common(5),
                'avg_impact_per_commit': sum(pc['impact_estimate'] for pc in performance_commits) / len(performance_commits) if performance_commits else 0
            }
        }
    
    def _analyze_security_evolution(self, commits: List[Dict], token=None) -> Dict[str, Any]:
        """Map the development and improvement of security patterns and practices"""
        
        # Security-related patterns
        security_patterns = {
            'authentication': re.compile(r'(auth|login|signup|oauth|jwt|session)', re.IGNORECASE),
            'authorization': re.compile(r'(permission|role|access|authorize|rbac)', re.IGNORECASE),
            'cryptography': re.compile(r'(encrypt|decrypt|hash|crypto|ssl|tls)', re.IGNORECASE),
            'validation': re.compile(r'(validate|sanitize|escape|xss|sql.*injection)', re.IGNORECASE),
            'vulnerability_fixes': re.compile(r'(vulnerability|security.*fix|cve|exploit)', re.IGNORECASE),
            'security_headers': re.compile(r'(header|cors|csp|security.*policy)', re.IGNORECASE)
        }
        
        security_commits = []
        security_timeline = defaultdict(list)
        security_domains = Counter()
        vulnerability_responses = []
        framework_adoptions = []
        
        for commit in commits:
            if token:
                token.check_cancellation()
            
            message = commit['message'].lower()
            
            # Check for security-related commits
            sec_type = None
            for category, pattern in security_patterns.items():
                if pattern.search(commit['message']):
                    sec_type = category
                    security_domains[category] += 1
                    break
            
            # Check for framework adoptions
            security_frameworks = ['oauth2', 'jwt', 'passport', 'spring.security', 'helmet', 'csrf']
            for framework in security_frameworks:
                if framework.replace('.', ' ') in message or framework in message:
                    framework_adoptions.append({
                        'framework': framework,
                        'hash': commit['hash'][:8],
                        'date': commit['date'].strftime('%Y-%m-%d'),
                        'message': commit['message']
                    })
            
            # Check for vulnerability responses
            if sec_type == 'vulnerability_fixes' or any(keyword in message for keyword in ['security fix', 'vulnerability', 'cve']):
                response_time = self._estimate_vulnerability_response_time(commit)
                vulnerability_responses.append({
                    'hash': commit['hash'][:8],
                    'message': commit['message'],
                    'date': commit['date'].strftime('%Y-%m-%d'),
                    'author': commit['author'],
                    'estimated_response_time': response_time,
                    'severity_estimate': self._estimate_vulnerability_severity(commit['message'])
                })
            
            if sec_type:
                quarter = f"{commit['date'].year}-Q{(commit['date'].month-1)//3 + 1}"
                security_timeline[quarter].append({
                    'type': sec_type,
                    'message': commit['message'][:100],
                    'hash': commit['hash'][:8],
                    'date': commit['date'].strftime('%Y-%m-%d'),
                    'author': commit['author'],
                    'severity': self._estimate_vulnerability_severity(commit['message'])
                })
                
                security_commits.append({
                    'hash': commit['hash'][:8],
                    'message': commit['message'],
                    'date': commit['date'].strftime('%Y-%m-%d'),
                    'author': commit['author'],
                    'type': sec_type,
                    'severity': self._estimate_vulnerability_severity(commit['message'])
                })
        
        # Security maturity progression
        security_maturity = self._assess_security_maturity(security_commits, framework_adoptions)
        
        # Calculate security improvement trends
        quarterly_security = {}
        for quarter, improvements in security_timeline.items():
            quarterly_security[quarter] = {
                'count': len(improvements),
                'types': Counter(imp['type'] for imp in improvements),
                'avg_severity': sum(imp['severity'] for imp in improvements) / len(improvements) if improvements else 0
            }
        
        return {
            'total_security_commits': len(security_commits),
            'security_domains': dict(security_domains),
            'security_timeline': dict(security_timeline),
            'quarterly_security': quarterly_security,
            'vulnerability_responses': vulnerability_responses,
            'framework_adoptions': framework_adoptions,
            'security_maturity': security_maturity,
            'recent_security_work': security_commits[:10],
            'security_trends': {
                'improvement_velocity': len(security_commits) / max(1, len(commits)) * 100,
                'vulnerability_response_avg': sum(vr['estimated_response_time'] for vr in vulnerability_responses) / len(vulnerability_responses) if vulnerability_responses else 0,
                'most_active_security_domain': security_domains.most_common(1)[0] if security_domains else None
            },
            'developer_insights': {
                'security_champions': Counter(sc['author'] for sc in security_commits).most_common(5),
                'framework_adoption_timeline': sorted(framework_adoptions, key=lambda x: x['date'])
            }
        }
    
    # Helper methods for enhanced analysis
    def _analyze_feature_complexity(self, feature_commits: List[Dict]) -> List[Dict]:
        """Analyze feature complexity trends over time"""
        complexity_data = []
        
        for commit in feature_commits[-20:]:  # Last 20 features
            # Simple complexity estimation based on commit message length and keywords
            complexity_score = 1
            message = commit['message'].lower()
            
            # Complexity indicators
            if any(keyword in message for keyword in ['refactor', 'migrate', 'rewrite']):
                complexity_score += 3
            if any(keyword in message for keyword in ['integration', 'api', 'database']):
                complexity_score += 2
            if any(keyword in message for keyword in ['config', 'setting', 'parameter']):
                complexity_score += 1
            
            # Length-based complexity
            if len(commit['message']) > 100:
                complexity_score += 2
            elif len(commit['message']) > 50:
                complexity_score += 1
            
            complexity_data.append({
                'date': commit['date'],
                'complexity': min(complexity_score, 10),  # Cap at 10
                'type': commit['type']
            })
        
        return complexity_data
    
    def _calculate_migration_complexity(self, message: str) -> int:
        """Calculate migration complexity score based on commit message"""
        complexity = 1
        message_lower = message.lower()
        
        # High complexity indicators
        if any(keyword in message_lower for keyword in ['breaking', 'major', 'rewrite']):
            complexity += 5
        if any(keyword in message_lower for keyword in ['database', 'schema', 'migration']):
            complexity += 3
        if any(keyword in message_lower for keyword in ['framework', 'library', 'dependency']):
            complexity += 2
        if any(keyword in message_lower for keyword in ['config', 'environment', 'deployment']):
            complexity += 1
        
        return min(complexity, 10)
    
    def _identify_architectural_debt(self, migration_commits: List[Dict]) -> Dict[str, Any]:
        """Identify indicators of architectural debt"""
        debt_indicators = {
            'frequent_migrations': len([c for c in migration_commits if 'migration' in c['message'].lower()]) > len(migration_commits) * 0.3,
            'emergency_fixes': len([c for c in migration_commits if any(keyword in c['message'].lower() for keyword in ['hotfix', 'urgent', 'critical'])]) > 0,
            'inconsistent_patterns': len(set(c['category'] for c in migration_commits[-10:])) > 3,  # Too many different types recently
            'high_complexity_trend': sum(c['complexity_score'] for c in migration_commits[-5:]) / 5 > 5 if len(migration_commits) >= 5 else False
        }
        
        debt_score = sum(1 for indicator in debt_indicators.values() if indicator)
        
        return {
            'debt_indicators': debt_indicators,
            'debt_score': debt_score,
            'risk_level': 'High' if debt_score >= 3 else 'Medium' if debt_score >= 2 else 'Low'
        }
    
    def _estimate_performance_impact(self, message: str) -> int:
        """Estimate performance impact based on commit message"""
        impact = 1
        message_lower = message.lower()
        
        # High impact indicators
        if any(keyword in message_lower for keyword in ['optimization', 'performance', 'speed']):
            impact += 3
        if any(keyword in message_lower for keyword in ['cache', 'index', 'query']):
            impact += 2
        if any(keyword in message_lower for keyword in ['memory', 'cpu', 'resource']):
            impact += 2
        if any(keyword in message_lower for keyword in ['async', 'parallel', 'concurrent']):
            impact += 1
        
        return min(impact, 10)
    
    def _correlate_performance_with_architecture(self, performance_commits: List[Dict]) -> Dict[str, Any]:
        """Correlate performance changes with architectural changes"""
        architecture_keywords = ['migrate', 'framework', 'refactor', 'restructure']
        performance_architecture_correlation = []
        
        for commit in performance_commits:
            message_lower = commit['message'].lower()
            has_architecture_keywords = any(keyword in message_lower for keyword in architecture_keywords)
            
            if has_architecture_keywords:
                performance_architecture_correlation.append({
                    'hash': commit['hash'],
                    'date': commit['date'],
                    'message': commit['message'],
                    'type': commit['type'],
                    'impact': commit['impact_estimate']
                })
        
        return {
            'correlated_commits': performance_architecture_correlation,
            'correlation_strength': len(performance_architecture_correlation) / len(performance_commits) if performance_commits else 0
        }
    
    def _estimate_vulnerability_response_time(self, commit: Dict) -> int:
        """Estimate vulnerability response time (simplified heuristic)"""
        message_lower = commit['message'].lower()
        
        # Urgency indicators suggest faster response
        if any(keyword in message_lower for keyword in ['critical', 'urgent', 'hotfix']):
            return 1  # 1 day
        elif any(keyword in message_lower for keyword in ['high', 'important', 'security']):
            return 3  # 3 days
        else:
            return 7  # 1 week
    
    def _estimate_vulnerability_severity(self, message: str) -> int:
        """Estimate vulnerability severity based on commit message"""
        severity = 1
        message_lower = message.lower()
        
        # Severity indicators
        if any(keyword in message_lower for keyword in ['critical', 'severe']):
            severity = 5
        elif any(keyword in message_lower for keyword in ['high', 'important']):
            severity = 4
        elif any(keyword in message_lower for keyword in ['medium', 'moderate']):
            severity = 3
        elif any(keyword in message_lower for keyword in ['low', 'minor']):
            severity = 2
        elif any(keyword in message_lower for keyword in ['injection', 'xss', 'csrf', 'cve']):
            severity = 5
        
        return severity
    
    def _assess_security_maturity(self, security_commits: List[Dict], framework_adoptions: List[Dict]) -> Dict[str, Any]:
        """Assess overall security maturity"""
        
        # Security maturity indicators
        has_modern_auth = any(framework in str(framework_adoptions) for framework in ['oauth2', 'jwt'])
        has_encryption = any('encrypt' in commit['message'].lower() for commit in security_commits)
        has_validation = any(commit['type'] == 'validation' for commit in security_commits)
        has_security_headers = any(commit['type'] == 'security_headers' for commit in security_commits)
        
        maturity_score = sum([has_modern_auth, has_encryption, has_validation, has_security_headers])
        
        maturity_levels = {
            0: 'Basic',
            1: 'Developing', 
            2: 'Intermediate',
            3: 'Advanced',
            4: 'Mature'
        }
        
        return {
            'maturity_level': maturity_levels[maturity_score],
            'maturity_score': maturity_score,
            'indicators': {
                'modern_authentication': has_modern_auth,
                'encryption_practices': has_encryption,
                'input_validation': has_validation,
                'security_headers': has_security_headers
            },
            'recommendations': self._get_security_recommendations(maturity_score)
        }
    
    def _get_security_recommendations(self, maturity_score: int) -> List[str]:
        """Get security recommendations based on maturity score"""
        recommendations = []
        
        if maturity_score < 4:
            recommendations.append("Implement comprehensive security headers (CSP, HSTS, etc.)")
        if maturity_score < 3:
            recommendations.append("Enhance input validation and sanitization practices")
        if maturity_score < 2:
            recommendations.append("Implement modern authentication mechanisms (OAuth2, JWT)")
        if maturity_score < 1:
            recommendations.append("Establish basic encryption for sensitive data")
        
        if maturity_score >= 4:
            recommendations.append("Maintain current security practices and stay updated with latest threats")
        
        return recommendations
