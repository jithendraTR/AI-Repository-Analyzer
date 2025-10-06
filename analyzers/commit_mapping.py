"""
Commits Mapping Analyzer
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

from .base_analyzer import BaseAnalyzer, OperationCancelledException

class ExpertiseMapper(BaseAnalyzer):
    """Analyzes developer expertise based on git history and code contributions"""
    
    def analyze(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Analyze developer expertise across the codebase with cancellation support"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("expertise_mapping")
        if cached_result:
            return cached_result
        
        if not self.repo:
            return {"error": "Git repository required for expertise mapping"}
        
        try:
            total_steps = 5
            current_step = 0
            
            # Step 1: Get commits
            if progress_callback:
                progress_callback(current_step, total_steps, "Loading git history...")
            
            # Check for cancellation
            if token:
                token.check_cancellation()
            
            # Get all commits with cancellation support
            commits = self.get_git_history_cancellable(max_commits=1000, token=token)
            current_step += 1
            
            # Step 2: Analyze file expertise
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing file-level expertise...")
            
            # Check for cancellation
            if token:
                token.check_cancellation()
            
            # Analyze file-level expertise
            file_expertise = self._analyze_file_expertise(token)
            current_step += 1
            
            # Step 3: Analyze technology expertise
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing technology expertise...")
            
            # Check for cancellation
            if token:
                token.check_cancellation()
            
            # Analyze technology expertise
            tech_expertise = self._analyze_technology_expertise(token)
            current_step += 1
            
            # Step 4: Analyze commit patterns
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing commit patterns...")
            
            # Check for cancellation
            if token:
                token.check_cancellation()
            
            # Analyze commit patterns
            commit_patterns = self._analyze_commit_patterns(commits, token)
            current_step += 1
            
            # Step 5: Get recent activity
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing recent activity...")
            
            # Check for cancellation
            if token:
                token.check_cancellation()
            
            # Get recent activity
            recent_activity = self._get_recent_activity(commits)
            current_step += 1
            
            if progress_callback:
                progress_callback(current_step, total_steps, "Finalizing expertise analysis...")
            
            result = {
                "file_expertise": file_expertise,
                "tech_expertise": tech_expertise,
                "commit_patterns": commit_patterns,
                "recent_activity": recent_activity,
                "total_contributors": len(set(commit['author'] for commit in commits))
            }
            
            # Cache the result
            self.cache_analysis("expertise_mapping", result)
            
            return result
            
        except OperationCancelledException:
            return {"error": "Analysis was cancelled by user"}
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_file_expertise(self, token=None) -> Dict[str, Dict[str, int]]:
        """Analyze which developers have worked on which files with cancellation support"""
        file_expertise = defaultdict(lambda: defaultdict(int))
        
        # Get all source code files with cancellation support
        code_files = self.get_file_list_cancellable(['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rb', '.php'], token)
        
        for i, file_path in enumerate(code_files):
            # Check for cancellation every 10 files
            if token and i % 10 == 0:
                token.check_cancellation()
                
            relative_path = str(file_path.relative_to(self.repo_path))
            contributors = self.get_file_contributors(relative_path)
            
            for author, commit_count in contributors.items():
                file_expertise[relative_path][author] = commit_count
        
        return dict(file_expertise)
    
    def _analyze_technology_expertise(self, token=None) -> Dict[str, Dict[str, int]]:
        """Analyze developer expertise by technology/language with cancellation support"""
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
        
        # Analyze each technology
        for tech_name, extensions in tech_patterns.items():
            # Check for cancellation
            if token:
                token.check_cancellation()
                
            files = []
            for ext in extensions:
                if ext.startswith('.'):
                    files.extend(self.get_file_list_cancellable([ext], token))
                else:
                    # Handle special files like Dockerfile
                    files.extend(self.find_files_by_pattern(f"**/{ext}"))
            
            for i, file_path in enumerate(files):
                # Check for cancellation every 20 files
                if token and i % 20 == 0:
                    token.check_cancellation()
                    
                relative_path = str(file_path.relative_to(self.repo_path))
                contributors = self.get_file_contributors(relative_path)
                
                for author, commit_count in contributors.items():
                    tech_expertise[tech_name][author] += commit_count
        
        return dict(tech_expertise)
    
    def _analyze_commit_patterns(self, commits: List[Dict], token=None) -> Dict[str, Any]:
        """Analyze commit patterns by developer with cancellation support"""
        patterns = defaultdict(lambda: {
            'total_commits': 0,
            'avg_files_per_commit': 0,
            'commit_messages': [],
            'commit_types': defaultdict(int)
        })
        
        # Commit type patterns
        commit_type_patterns = {
            'feature': r'(feat|feature|add)',
            'fix': r'(fix|bug|patch)',
            'refactor': r'(refactor|refact|clean)',
            'docs': r'(doc|docs|documentation)',
            'test': r'(test|spec)',
            'style': r'(style|format)',
            'chore': r'(chore|maintenance|update)'
        }
        
        for i, commit in enumerate(commits):
            # Check for cancellation every 50 commits
            if token and i % 50 == 0:
                token.check_cancellation()
                
            author = commit['author']
            patterns[author]['total_commits'] += 1
            patterns[author]['avg_files_per_commit'] += commit['files_changed']
            patterns[author]['commit_messages'].append(commit['message'])
            
            # Classify commit type
            message_lower = commit['message'].lower()
            classified = False
            
            for commit_type, pattern in commit_type_patterns.items():
                if re.search(pattern, message_lower):
                    patterns[author]['commit_types'][commit_type] += 1
                    classified = True
                    break
            
            if not classified:
                patterns[author]['commit_types']['other'] += 1
        
        # Calculate averages
        for author in patterns:
            if patterns[author]['total_commits'] > 0:
                patterns[author]['avg_files_per_commit'] /= patterns[author]['total_commits']
        
        return dict(patterns)
    
    def _get_recent_activity(self, commits: List[Dict], days: int = 30) -> Dict[str, Any]:
        """Get recent activity by developers"""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_commits = [c for c in commits if c['date'].replace(tzinfo=None) > cutoff_date]
        
        activity = defaultdict(int)
        for commit in recent_commits:
            activity[commit['author']] += 1
        
        return {
            'recent_commits': dict(activity),
            'active_developers': len(activity),
            'total_recent_commits': len(recent_commits)
        }
    
    def render(self):
        """Render the commits mapping analysis"""
        st.header("👥 Developer Commits Mapping")
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
