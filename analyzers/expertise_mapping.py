"""
Expertise Mapping Analyzer - Optimized Version
Analyzes who has worked on what parts of the codebase to map developer expertise
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict, Counter
from typing import Dict, List, Any
from pathlib import Path
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

from .base_analyzer import BaseAnalyzer, OperationCancelledException

class ExpertiseMapper(BaseAnalyzer):
    """Analyzes developer expertise based on git history and code contributions"""
    
    def analyze(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Optimized analyze method for faster performance"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("expertise_mapping")
        if cached_result:
            return cached_result
        
        if not self.repo:
            return {"error": "Git repository required for expertise mapping"}
        
        try:
            total_steps = 6
            current_step = 0
            
            # Step 1: Get commit data efficiently using git log
            if progress_callback:
                progress_callback(current_step, total_steps, "Loading git history efficiently...")
            
            if token:
                token.check_cancellation()
            
            # Use optimized git log parsing instead of GitPython iteration
            commits_data = self._get_optimized_git_data(token, max_commits=500)
            current_step += 1
            
            # Step 2: Analyze file expertise using bulk operations
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing file expertise with bulk operations...")
            
            if token:
                token.check_cancellation()
            
            file_expertise = self._analyze_file_expertise_optimized(commits_data['file_stats'], token)
            current_step += 1
            
            # Step 3: Analyze technology expertise using parallel processing
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing technology expertise in parallel...")
            
            if token:
                token.check_cancellation()
            
            tech_expertise = self._analyze_technology_expertise_optimized(file_expertise, token)
            current_step += 1
            
            # Step 4: Process commit patterns efficiently
            if progress_callback:
                progress_callback(current_step, total_steps, "Processing commit patterns...")
            
            if token:
                token.check_cancellation()
            
            commit_patterns = self._analyze_commit_patterns_optimized(commits_data['commits'], token)
            current_step += 1
            
            # Step 5: Calculate recent activity from existing data
            if progress_callback:
                progress_callback(current_step, total_steps, "Computing recent activity...")
            
            if token:
                token.check_cancellation()
            
            recent_activity = self._get_recent_activity_optimized(commits_data['commits'])
            current_step += 1
            
            # Step 6: Finalize results
            if progress_callback:
                progress_callback(current_step, total_steps, "Finalizing expertise analysis...")
            
            result = {
                "file_expertise": file_expertise,
                "tech_expertise": tech_expertise,
                "commit_patterns": commit_patterns,
                "recent_activity": recent_activity,
                "total_contributors": commits_data['total_contributors']
            }
            
            # Cache the result
            self.cache_analysis("expertise_mapping", result)
            
            return result
            
        except OperationCancelledException:
            return {"error": "Analysis was cancelled by user"}
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _get_optimized_git_data(self, token=None, max_commits=500) -> Dict[str, Any]:
        """Get git data efficiently using direct git commands"""
        try:
            # Use git log to get commit and file stats in one go
            cmd = [
                'git', 'log', '--name-only', '--pretty=format:%H|%an|%ae|%ci|%s', 
                f'-{max_commits}', '--no-merges'
            ]
            
            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True, timeout=60
            )
            
            if result.returncode != 0:
                return {'commits': [], 'file_stats': {}, 'total_contributors': 0}
            
            # Parse the output efficiently
            commits = []
            file_stats = defaultdict(lambda: defaultdict(int))
            contributors = set()
            
            current_commit = None
            lines = result.stdout.strip().split('\n')
            
            for line in lines:
                if token and len(commits) % 50 == 0:
                    token.check_cancellation()
                
                if '|' in line and len(line.split('|')) == 5:
                    # New commit line
                    if current_commit:
                        commits.append(current_commit)
                    
                    parts = line.split('|')
                    commit_hash, author, email, date, message = parts
                    contributors.add(author)
                    
                    current_commit = {
                        'hash': commit_hash,
                        'author': author,
                        'email': email,
                        'date': pd.to_datetime(date),
                        'message': message.strip(),
                        'files': []
                    }
                elif line.strip() and current_commit:
                    # File path
                    file_path = line.strip()
                    if file_path and not file_path.startswith('.git/'):
                        current_commit['files'].append(file_path)
                        file_stats[file_path][current_commit['author']] += 1
            
            # Add the last commit
            if current_commit:
                commits.append(current_commit)
            
            # Add files_changed count to commits
            for commit in commits:
                commit['files_changed'] = len(commit['files'])
            
            return {
                'commits': commits,
                'file_stats': dict(file_stats),
                'total_contributors': len(contributors)
            }
            
        except Exception as e:
            # Fallback to original method if git command fails
            commits = self.get_git_history_cancellable(max_commits=max_commits, token=token)
            return {
                'commits': commits,
                'file_stats': {},
                'total_contributors': len(set(commit['author'] for commit in commits))
            }
    
    def _analyze_file_expertise_optimized(self, file_stats: Dict[str, Dict[str, int]], token=None) -> Dict[str, Dict[str, int]]:
        """Optimized file expertise analysis using pre-computed stats"""
        if not file_stats:
            # Fallback to original method
            return self._analyze_file_expertise_fallback(token)
        
        # Filter to only source code files
        source_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rb', '.php', '.jsx', '.tsx'}
        
        filtered_stats = {}
        for file_path, contributors in file_stats.items():
            if token:
                token.check_cancellation()
            
            # Check if it's a source code file
            if any(file_path.endswith(ext) for ext in source_extensions):
                filtered_stats[file_path] = contributors
        
        return filtered_stats
    
    def _analyze_file_expertise_fallback(self, token=None) -> Dict[str, Dict[str, int]]:
        """Fallback method for file expertise analysis"""
        file_expertise = defaultdict(lambda: defaultdict(int))
        
        # Get only the most important source code files (limit to 200 for performance)
        code_files = self.get_file_list_cancellable(['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go'], token)
        
        # Sort by file size/importance and limit
        important_files = []
        for file_path in code_files[:200]:  # Limit to first 200 files
            if token and len(important_files) % 20 == 0:
                token.check_cancellation()
            
            try:
                file_size = file_path.stat().st_size
                if file_size > 100 and file_size < 1000000:  # Skip very small and very large files
                    important_files.append(file_path)
            except:
                continue
        
        # Process files in parallel batches
        def process_file_batch(files_batch):
            batch_results = {}
            for file_path in files_batch:
                relative_path = str(file_path.relative_to(self.repo_path))
                contributors = self.get_file_contributors(relative_path)
                if contributors:  # Only include files with contributors
                    batch_results[relative_path] = contributors
            return batch_results
        
        # Process in batches of 10 files
        batch_size = 10
        batches = [important_files[i:i+batch_size] for i in range(0, len(important_files), batch_size)]
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(process_file_batch, batch) for batch in batches]
            
            for future in as_completed(futures):
                if token:
                    token.check_cancellation()
                
                batch_result = future.result()
                file_expertise.update(batch_result)
        
        return dict(file_expertise)
    
    def _analyze_technology_expertise_optimized(self, file_expertise: Dict[str, Dict[str, int]], token=None) -> Dict[str, Dict[str, int]]:
        """Optimized technology expertise analysis using pre-computed file expertise"""
        tech_expertise = defaultdict(lambda: defaultdict(int))
        
        # Technology patterns
        tech_patterns = {
            'Python': ['.py'],
            'JavaScript': ['.js', '.jsx'],
            'TypeScript': ['.ts', '.tsx'],
            'Java': ['.java'],
            'C++': ['.cpp', '.cc', '.cxx'],
            'C': ['.c'],
            'C#': ['.cs'],
            'Go': ['.go'],
            'Ruby': ['.rb'],
            'PHP': ['.php'],
            'HTML': ['.html', '.htm'],
            'CSS': ['.css', '.scss', '.sass'],
            'SQL': ['.sql'],
            'Shell': ['.sh', '.bash'],
            'Docker': ['Dockerfile', '.dockerfile'],
            'YAML': ['.yml', '.yaml'],
            'JSON': ['.json'],
            'XML': ['.xml']
        }
        
        # Process files in parallel by grouping by technology
        def process_tech_files(tech_name_and_patterns):
            tech_name, patterns = tech_name_and_patterns
            tech_stats = defaultdict(int)
            
            for file_path, contributors in file_expertise.items():
                # Check if file matches this technology
                file_matches = False
                for pattern in patterns:
                    if pattern.startswith('.'):
                        if file_path.endswith(pattern):
                            file_matches = True
                            break
                    else:
                        if pattern in file_path:
                            file_matches = True
                            break
                
                if file_matches:
                    for author, commit_count in contributors.items():
                        tech_stats[author] += commit_count
            
            return tech_name, dict(tech_stats)
        
        # Process technologies in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(process_tech_files, (tech_name, patterns))
                for tech_name, patterns in tech_patterns.items()
            ]
            
            for future in as_completed(futures):
                if token:
                    token.check_cancellation()
                
                tech_name, tech_stats = future.result()
                if tech_stats:  # Only include technologies with activity
                    tech_expertise[tech_name] = tech_stats
        
        return dict(tech_expertise)
    
    def _analyze_commit_patterns_optimized(self, commits: List[Dict], token=None) -> Dict[str, Any]:
        """Optimized commit patterns analysis"""
        patterns = defaultdict(lambda: {
            'total_commits': 0,
            'avg_files_per_commit': 0,
            'commit_messages': [],
            'commit_types': defaultdict(int)
        })
        
        # Commit type patterns (compiled for better performance)
        import re as regex_lib
        commit_type_patterns = {
            'feature': regex_lib.compile(r'(feat|feature|add)', regex_lib.IGNORECASE),
            'fix': regex_lib.compile(r'(fix|bug|patch)', regex_lib.IGNORECASE),
            'refactor': regex_lib.compile(r'(refactor|refact|clean)', regex_lib.IGNORECASE),
            'docs': regex_lib.compile(r'(doc|docs|documentation)', regex_lib.IGNORECASE),
            'test': regex_lib.compile(r'(test|spec)', regex_lib.IGNORECASE),
            'style': regex_lib.compile(r'(style|format)', regex_lib.IGNORECASE),
            'chore': regex_lib.compile(r'(chore|maintenance|update)', regex_lib.IGNORECASE)
        }
        
        # Process commits in batches for better performance
        batch_size = 100
        for i in range(0, len(commits), batch_size):
            if token:
                token.check_cancellation()
            
            batch = commits[i:i+batch_size]
            
            for commit in batch:
                author = commit['author']
                patterns[author]['total_commits'] += 1
                patterns[author]['avg_files_per_commit'] += commit.get('files_changed', 0)
                
                # Only keep recent commit messages to avoid memory issues
                if len(patterns[author]['commit_messages']) < 10:
                    patterns[author]['commit_messages'].append(commit['message'])
                
                # Classify commit type using compiled regexes
                message = commit['message']
                classified = False
                
                for commit_type, pattern in commit_type_patterns.items():
                    if pattern.search(message):
                        patterns[author]['commit_types'][commit_type] += 1
                        classified = True
                        break
                
                if not classified:
                    patterns[author]['commit_types']['other'] += 1
        
        # Calculate averages efficiently
        for author in patterns:
            if patterns[author]['total_commits'] > 0:
                patterns[author]['avg_files_per_commit'] /= patterns[author]['total_commits']
            # Convert defaultdict to regular dict for JSON serialization
            patterns[author]['commit_types'] = dict(patterns[author]['commit_types'])
        
        return dict(patterns)
    
    def _get_recent_activity_optimized(self, commits: List[Dict], days: int = 30) -> Dict[str, Any]:
        """Optimized recent activity calculation"""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Use list comprehension for better performance
        activity = defaultdict(int)
        recent_count = 0
        
        for commit in commits:
            commit_date = commit['date']
            # Handle different date formats
            if hasattr(commit_date, 'replace'):
                commit_date = commit_date.replace(tzinfo=None)
            
            if commit_date > cutoff_date:
                activity[commit['author']] += 1
                recent_count += 1
        
        return {
            'recent_commits': dict(activity),
            'active_developers': len(activity),
            'total_recent_commits': recent_count
        }
    
    
    def render(self):
        """Render the expertise mapping analysis"""
        st.header("👥 Developer Expertise Mapping")
        st.markdown("Understanding who has worked on what parts of the codebase")
        
        # Add rerun button
        self.add_rerun_button("expertise_mapping")
        
        with self.display_loading_message("Analyzing team expertise and knowledge distribution..."):
            analysis = self.analyze()
        
        if "error" in analysis:
            self.display_error(analysis["error"])
            return
        
        # Overview metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Contributors", analysis["total_contributors"])
        with col2:
            st.metric("Active Developers (30 days)", analysis["recent_activity"]["active_developers"])
        with col3:
            st.metric("Recent Commits (30 days)", analysis["recent_activity"]["total_recent_commits"])
        
        # Technology expertise visualization
        st.subheader("🔧 Technology Expertise")
        
        if analysis["tech_expertise"]:
            # Create technology expertise heatmap data
            tech_data = []
            for tech, developers in analysis["tech_expertise"].items():
                for dev, commits in developers.items():
                    tech_data.append({
                        'Technology': tech,
                        'Developer': dev,
                        'Commits': commits
                    })
            
            if tech_data:
                df_tech = pd.DataFrame(tech_data)
                
                # Create pivot table for heatmap
                pivot_tech = df_tech.pivot(index='Developer', columns='Technology', values='Commits').fillna(0)
                
                # Create heatmap
                fig_heatmap = px.imshow(
                    pivot_tech.values,
                    x=pivot_tech.columns,
                    y=pivot_tech.index,
                    color_continuous_scale='Blues',
                    title="Developer Technology Expertise Heatmap"
                )
                fig_heatmap.update_layout(height=400)
                st.plotly_chart(fig_heatmap, use_container_width=True)
                
                # Top technologies by total commits
                tech_totals = df_tech.groupby('Technology')['Commits'].sum().sort_values(ascending=False)
                fig_tech_bar = px.bar(
                    x=tech_totals.index,
                    y=tech_totals.values,
                    title="Most Active Technologies",
                    labels={'x': 'Technology', 'y': 'Total Commits'}
                )
                st.plotly_chart(fig_tech_bar, use_container_width=True)
        
        # File expertise analysis
        st.subheader("📁 File-Level Expertise")
        
        if analysis["file_expertise"]:
            # Get top files by activity
            file_activity = {}
            for file_path, contributors in analysis["file_expertise"].items():
                file_activity[file_path] = sum(contributors.values())
            
            top_files = sorted(file_activity.items(), key=lambda x: x[1], reverse=True)[:20]
            
            if top_files:
                st.write("**Most Active Files:**")
                for file_path, total_commits in top_files[:10]:
                    with st.expander(f"{file_path} ({total_commits} commits)"):
                        contributors = analysis["file_expertise"][file_path]
                        contrib_df = pd.DataFrame([
                            {"Developer": dev, "Commits": commits}
                            for dev, commits in sorted(contributors.items(), key=lambda x: x[1], reverse=True)
                        ])
                        st.dataframe(contrib_df, use_container_width=True)
        
        # Commit patterns analysis
        st.subheader("📊 Commit Patterns")
        
        if analysis["commit_patterns"]:
            # Developer activity overview
            dev_stats = []
            for dev, stats in analysis["commit_patterns"].items():
                dev_stats.append({
                    'Developer': dev,
                    'Total Commits': stats['total_commits'],
                    'Avg Files/Commit': round(stats['avg_files_per_commit'], 2)
                })
            
            df_dev_stats = pd.DataFrame(dev_stats).sort_values('Total Commits', ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_commits = px.bar(
                    df_dev_stats.head(10),
                    x='Developer',
                    y='Total Commits',
                    title="Top Contributors by Commit Count"
                )
                fig_commits.update_xaxes(tickangle=45)
                st.plotly_chart(fig_commits, use_container_width=True)
            
            with col2:
                fig_files = px.bar(
                    df_dev_stats.head(10),
                    x='Developer',
                    y='Avg Files/Commit',
                    title="Average Files per Commit"
                )
                fig_files.update_xaxes(tickangle=45)
                st.plotly_chart(fig_files, use_container_width=True)
            
            # Commit type analysis
            st.write("**Commit Type Distribution:**")
            commit_type_data = []
            for dev, stats in analysis["commit_patterns"].items():
                for commit_type, count in stats['commit_types'].items():
                    commit_type_data.append({
                        'Developer': dev,
                        'Commit Type': commit_type,
                        'Count': count
                    })
            
            if commit_type_data:
                df_commit_types = pd.DataFrame(commit_type_data)
                fig_commit_types = px.bar(
                    df_commit_types,
                    x='Commit Type',
                    y='Count',
                    color='Developer',
                    title="Commit Types by Developer"
                )
                st.plotly_chart(fig_commit_types, use_container_width=True)
        
        # Recent activity
        st.subheader("🕒 Recent Activity (Last 30 Days)")
        
        if analysis["recent_activity"]["recent_commits"]:
            recent_df = pd.DataFrame([
                {"Developer": dev, "Recent Commits": commits}
                for dev, commits in sorted(
                    analysis["recent_activity"]["recent_commits"].items(),
                    key=lambda x: x[1], reverse=True
                )
            ])
            
            fig_recent = px.bar(
                recent_df.head(10),
                x='Developer',
                y='Recent Commits',
                title="Most Active Developers (Last 30 Days)"
            )
            fig_recent.update_xaxes(tickangle=45)
            st.plotly_chart(fig_recent, use_container_width=True)
        else:
            st.info("No recent activity found in the last 30 days")
        
        # AI-powered insights
        st.subheader("🤖 AI Insights")
        
        if st.button("Generate Expertise Insights"):
            with self.display_loading_message("Generating AI insights..."):
                # Prepare data for AI analysis
                expertise_summary = {
                    "total_contributors": analysis["total_contributors"],
                    "top_technologies": list(analysis["tech_expertise"].keys())[:5],
                    "most_active_files": [f[0] for f in sorted(
                        [(f, sum(c.values())) for f, c in analysis["file_expertise"].items()],
                        key=lambda x: x[1], reverse=True
                    )[:5]],
                    "recent_activity": analysis["recent_activity"]
                }
                
                prompt = f"""
                Analyze this developer expertise data and provide insights:
                
                {expertise_summary}
                
                Please provide:
                1. Key expertise areas in the team
                2. Potential knowledge silos or bus factor risks
                3. Recommendations for knowledge sharing
                4. Areas that might need more expertise
                5. Team collaboration patterns
                """
                
                insights = self.ai_client.query(prompt)
                
                if insights:
                    st.markdown("**AI-Generated Insights:**")
                    st.markdown(insights)
                else:
                    st.error("Failed to generate AI insights")
        
        # Add save options
        self.add_save_options("expertise_mapping", analysis)
