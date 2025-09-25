"""
Timeline Analysis Analyzer
Analyzes project timeline and latest additions for understanding project evolution
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
from typing import Dict, List, Any
from datetime import datetime, timedelta
import re

from .base_analyzer import BaseAnalyzer

class TimelineAnalyzer(BaseAnalyzer):
    """Analyzes project timeline and recent changes"""
    
    def analyze(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Analyze project timeline and evolution"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("timeline_analysis")
        if cached_result:
            return cached_result
        
        if not self.repo:
            return {"error": "Git repository required for timeline analysis"}
        
        try:
            total_steps = 6
            current_step = 0
            
            # Step 1: Get commit history
            if progress_callback:
                progress_callback(current_step, total_steps, "Loading commit history...")
            
            # Get comprehensive commit history
            commits = self.get_git_history(max_commits=2000)
            
            if not commits:
                return {"error": "No commit history found"}
            current_step += 1
            
            # Step 2: Analyze timeline patterns
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing timeline patterns...")
            
            # Analyze timeline patterns
            timeline_data = self._analyze_timeline_patterns(commits)
            current_step += 1
            
            # Step 3: Analyze recent changes
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing recent changes...")
            
            # Get recent additions and changes
            recent_changes = self._analyze_recent_changes(commits)
            current_step += 1
            
            # Step 4: Identify development phases
            if progress_callback:
                progress_callback(current_step, total_steps, "Identifying development phases...")
            
            # Analyze development phases
            development_phases = self._identify_development_phases(commits)
            current_step += 1
            
            # Step 5: Analyze file evolution
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing file evolution...")
            
            # Get file evolution
            file_evolution = self._analyze_file_evolution()
            current_step += 1
            
            # Step 6: Analyze release patterns
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing release patterns...")
            
            # Analyze release patterns
            release_patterns = self._analyze_release_patterns()
            current_step += 1
            
            if progress_callback:
                progress_callback(current_step, total_steps, "Finalizing timeline analysis...")
            
            result = {
                "timeline_data": timeline_data,
                "recent_changes": recent_changes,
                "development_phases": development_phases,
                "file_evolution": file_evolution,
                "release_patterns": release_patterns,
                "project_age": self._calculate_project_age(commits),
                "total_commits": len(commits)
            }
            
            # Cache the result
            self.cache_analysis("timeline_analysis", result)
            
            return result
            
        except Exception as e:
            return {"error": f"Timeline analysis failed: {str(e)}"}
    
    def _analyze_timeline_patterns(self, commits: List[Dict]) -> Dict[str, Any]:
        """Analyze commit patterns over time"""
        
        # Group commits by time periods
        daily_commits = defaultdict(int)
        weekly_commits = defaultdict(int)
        monthly_commits = defaultdict(int)
        hourly_commits = defaultdict(int)
        
        for commit in commits:
            date = commit['date']
            daily_key = date.strftime('%Y-%m-%d')
            weekly_key = date.strftime('%Y-W%U')
            monthly_key = date.strftime('%Y-%m')
            hourly_key = date.hour
            
            daily_commits[daily_key] += 1
            weekly_commits[weekly_key] += 1
            monthly_commits[monthly_key] += 1
            hourly_commits[hourly_key] += 1
        
        # Analyze commit velocity trends
        velocity_trend = self._calculate_velocity_trend(commits)
        
        # Analyze developer activity over time
        developer_timeline = self._analyze_developer_timeline(commits)
        
        return {
            "daily_commits": dict(daily_commits),
            "weekly_commits": dict(weekly_commits),
            "monthly_commits": dict(monthly_commits),
            "hourly_commits": dict(hourly_commits),
            "velocity_trend": velocity_trend,
            "developer_timeline": developer_timeline
        }
    
    def _analyze_recent_changes(self, commits: List[Dict], days: int = 30) -> Dict[str, Any]:
        """Analyze recent changes and additions"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_commits = [c for c in commits if c['date'].replace(tzinfo=None) > cutoff_date]
        
        # Categorize recent changes
        feature_commits = []
        bug_fixes = []
        refactoring = []
        documentation = []
        other_commits = []
        
        patterns = {
            'feature': r'(feat|feature|add|new|implement)',
            'fix': r'(fix|bug|patch|resolve)',
            'refactor': r'(refactor|refact|clean|improve)',
            'docs': r'(doc|docs|documentation|readme)',
        }
        
        for commit in recent_commits:
            message_lower = commit['message'].lower()
            categorized = False
            
            for category, pattern in patterns.items():
                if re.search(pattern, message_lower):
                    if category == 'feature':
                        feature_commits.append(commit)
                    elif category == 'fix':
                        bug_fixes.append(commit)
                    elif category == 'refactor':
                        refactoring.append(commit)
                    elif category == 'docs':
                        documentation.append(commit)
                    categorized = True
                    break
            
            if not categorized:
                other_commits.append(commit)
        
        # Analyze file changes in recent commits
        recent_file_changes = self._analyze_recent_file_changes(recent_commits)
        
        return {
            "total_recent_commits": len(recent_commits),
            "feature_commits": feature_commits,
            "bug_fixes": bug_fixes,
            "refactoring": refactoring,
            "documentation": documentation,
            "other_commits": other_commits,
            "recent_file_changes": recent_file_changes,
            "most_active_recent_authors": self._get_most_active_authors(recent_commits)
        }
    
    def _identify_development_phases(self, commits: List[Dict]) -> List[Dict]:
        """Identify different development phases based on commit patterns"""
        
        if len(commits) < 10:
            return []
        
        # Sort commits by date
        sorted_commits = sorted(commits, key=lambda x: x['date'])
        
        # Analyze commit velocity in chunks
        chunk_size = max(10, len(commits) // 10)
        phases = []
        
        for i in range(0, len(sorted_commits), chunk_size):
            chunk = sorted_commits[i:i + chunk_size]
            if len(chunk) < 5:
                continue
            
            start_date = chunk[0]['date']
            end_date = chunk[-1]['date']
            duration = (end_date - start_date).days
            
            # Analyze commit types in this phase
            commit_types = defaultdict(int)
            authors = set()
            
            for commit in chunk:
                authors.add(commit['author'])
                message_lower = commit['message'].lower()
                
                if re.search(r'(initial|init|start)', message_lower):
                    commit_types['initialization'] += 1
                elif re.search(r'(feat|feature|add|new)', message_lower):
                    commit_types['feature_development'] += 1
                elif re.search(r'(fix|bug|patch)', message_lower):
                    commit_types['bug_fixing'] += 1
                elif re.search(r'(refactor|clean|improve)', message_lower):
                    commit_types['refactoring'] += 1
                elif re.search(r'(test|spec)', message_lower):
                    commit_types['testing'] += 1
                else:
                    commit_types['maintenance'] += 1
            
            # Determine phase type
            dominant_type = max(commit_types.items(), key=lambda x: x[1])[0]
            
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
    
    def _analyze_file_evolution(self) -> Dict[str, Any]:
        """Analyze how files have evolved over time"""
        
        file_stats = {}
        code_files = self.get_file_list(['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rb', '.php'])
        
        for file_path in code_files[:50]:  # Limit to avoid performance issues
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Get file history
            file_commits = self.get_git_history(file_path=relative_path, max_commits=100)
            
            if file_commits:
                file_stats[relative_path] = {
                    'total_commits': len(file_commits),
                    'first_commit': file_commits[-1]['date'] if file_commits else None,
                    'last_commit': file_commits[0]['date'] if file_commits else None,
                    'contributors': len(set(c['author'] for c in file_commits)),
                    'recent_activity': len([c for c in file_commits 
                                          if (datetime.now() - c['date'].replace(tzinfo=None)).days <= 30])
                }
        
        return file_stats
    
    def _analyze_release_patterns(self) -> Dict[str, Any]:
        """Analyze release patterns from tags"""
        
        if not self.repo:
            return {}
        
        try:
            tags = list(self.repo.tags)
            releases = []
            
            for tag in tags:
                try:
                    releases.append({
                        'name': tag.name,
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
        st.header("📅 Project Timeline Analysis")
        st.markdown("Understanding project evolution and recent changes")
        
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
        
        file_evolution = analysis["file_evolution"]
        if file_evolution:
            # Most active files
            active_files = sorted(
                [(path, stats) for path, stats in file_evolution.items()],
                key=lambda x: x[1]['total_commits'],
                reverse=True
            )[:20]
            
            if active_files:
                files_df = pd.DataFrame([
                    {
                        "File": path,
                        "Total Commits": stats['total_commits'],
                        "Contributors": stats['contributors'],
                        "Recent Activity": stats['recent_activity'],
                        "Age (days)": (datetime.now() - stats['first_commit'].replace(tzinfo=None)).days if stats['first_commit'] else 0
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
        
        # AI-powered insights
        st.subheader("🤖 AI Timeline Insights")
        
        # Check if parallel AI insights are available
        if not self.display_parallel_ai_insights("timeline_analysis"):
            # Fallback to individual AI insight generation
            if st.button("Generate Timeline Insights"):
                with self.display_loading_message("Generating AI insights..."):
                    # Prepare timeline summary for AI
                    timeline_summary = {
                        "project_age_years": analysis["project_age"]["age_years"] if analysis["project_age"] else 0,
                        "total_commits": analysis["total_commits"],
                        "recent_activity": recent_data["total_recent_commits"],
                        "development_phases": len(phases),
                        "release_count": release_data.get("total_releases", 0) if release_data else 0,
                        "most_active_period": max(timeline_data["monthly_commits"].items(), key=lambda x: x[1])[0] if timeline_data["monthly_commits"] else "Unknown"
                    }
                    
                    prompt = f"""
                    Analyze this project timeline data and provide insights:
                    
                    {timeline_summary}
                    
                    Recent changes breakdown:
                    - Features: {len(recent_data["feature_commits"])}
                    - Bug fixes: {len(recent_data["bug_fixes"])}
                    - Refactoring: {len(recent_data["refactoring"])}
                    - Documentation: {len(recent_data["documentation"])}
                    
                    Please provide:
                    1. Project maturity assessment
                    2. Development velocity trends
                    3. Team activity patterns
                    4. Release cadence analysis
                    5. Recommendations for project timeline management
                    """
                    
                    insights = self.ai_client.query(prompt)
                    
                    if insights:
                        st.markdown("**AI-Generated Timeline Insights:**")
                        st.markdown(insights)
                    else:
                        st.error("Failed to generate AI insights")
        else:
            st.info("💡 Tip: Use 'Run AI Analysis for All Tabs' in the sidebar for faster parallel processing!")
        
        # Add save options
        self.add_save_options("timeline_analysis", analysis)
