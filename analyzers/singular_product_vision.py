"""
Singular Product Vision Analyzer
Analyzes the repository for product vision consistency, feature alignment, and strategic coherence
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict, Counter
from typing import Dict, List, Any
from pathlib import Path
import re
import json

from .base_analyzer import BaseAnalyzer, OperationCancelledException

class SingularProductVisionAnalyzer(BaseAnalyzer):
    """Analyzes product vision consistency and strategic alignment across the codebase"""
    
    def analyze(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Analyze product vision coherence across the codebase with cancellation support"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("singular_product_vision")
        if cached_result:
            return cached_result
        
        try:
            total_steps = 6
            current_step = 0
            
            # Step 1: Analyze documentation for product vision
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing product documentation...")
            
            if token:
                token.check_cancellation()
            
            vision_docs = self._analyze_product_documentation(token)
            current_step += 1
            
            # Step 2: Analyze feature architecture
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing feature architecture...")
            
            if token:
                token.check_cancellation()
            
            feature_analysis = self._analyze_feature_architecture(token)
            current_step += 1
            
            # Step 3: Analyze API consistency
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing API consistency...")
            
            if token:
                token.check_cancellation()
            
            api_consistency = self._analyze_api_consistency(token)
            current_step += 1
            
            # Step 4: Analyze commit patterns for product focus
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing development focus...")
            
            if token:
                token.check_cancellation()
            
            development_focus = self._analyze_development_focus(token)
            current_step += 1
            
            # Step 5: Analyze configuration consistency
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing configuration consistency...")
            
            if token:
                token.check_cancellation()
            
            config_analysis = self._analyze_configuration_consistency(token)
            current_step += 1
            
            # Step 6: Calculate product vision score
            if progress_callback:
                progress_callback(current_step, total_steps, "Calculating product vision coherence...")
            
            if token:
                token.check_cancellation()
            
            vision_score = self._calculate_vision_coherence_score(
                vision_docs, feature_analysis, api_consistency, development_focus, config_analysis
            )
            current_step += 1
            
            if progress_callback:
                progress_callback(current_step, total_steps, "Finalizing product vision analysis...")
            
            result = {
                "vision_documentation": vision_docs,
                "feature_architecture": feature_analysis,
                "api_consistency": api_consistency,
                "development_focus": development_focus,
                "configuration_consistency": config_analysis,
                "vision_coherence_score": vision_score,
                "total_features_identified": len(feature_analysis.get("features", [])),
                "documentation_coverage": len(vision_docs.get("vision_statements", []))
            }
            
            # Cache the result
            self.cache_analysis("singular_product_vision", result)
            
            return result
            
        except OperationCancelledException:
            return {"error": "Analysis was cancelled by user"}
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_product_documentation(self, token=None) -> Dict[str, Any]:
        """Analyze documentation files for product vision statements"""
        vision_docs = {
            "vision_statements": [],
            "readme_analysis": {},
            "docs_structure": {},
            "mission_keywords": []
        }
        
        # Documentation file patterns
        doc_patterns = [
            "**/README.md", "**/README.rst", "**/README.txt",
            "**/VISION.md", "**/MISSION.md", "**/PRODUCT.md",
            "**/docs/**/*.md", "**/documentation/**/*.md",
            "**/wiki/**/*.md", "**/CHANGELOG.md", "**/ROADMAP.md"
        ]
        
        # Vision-related keywords
        vision_keywords = [
            "vision", "mission", "purpose", "goal", "objective",
            "strategy", "roadmap", "direction", "focus", "aim",
            "ambition", "aspiration", "commitment", "dedication"
        ]
        
        doc_files = []
        for pattern in doc_patterns:
            if token:
                token.check_cancellation()
            doc_files.extend(self.find_files_by_pattern(pattern))
        
        for i, doc_file in enumerate(doc_files):
            if token and i % 5 == 0:
                token.check_cancellation()
            
            content = self.read_file_content(doc_file)
            if not content:
                continue
            
            relative_path = str(doc_file.relative_to(self.repo_path))
            
            # Analyze README files specifically
            if "readme" in doc_file.name.lower():
                vision_docs["readme_analysis"][relative_path] = self._extract_vision_from_readme(content)
            
            # Look for vision statements
            vision_statements = self._extract_vision_statements(content, vision_keywords)
            if vision_statements:
                vision_docs["vision_statements"].extend([{
                    "file": relative_path,
                    "statements": vision_statements
                }])
            
            # Count mission keywords
            content_lower = content.lower()
            for keyword in vision_keywords:
                if keyword in content_lower:
                    vision_docs["mission_keywords"].append({
                        "keyword": keyword,
                        "file": relative_path,
                        "count": content_lower.count(keyword)
                    })
        
        return vision_docs
    
    def _analyze_feature_architecture(self, token=None) -> Dict[str, Any]:
        """Analyze the codebase architecture to identify product features"""
        feature_analysis = {
            "features": [],
            "modules": [],
            "services": [],
            "components": [],
            "feature_consistency": {}
        }
        
        # Get all source code files
        source_files = self.get_file_list_cancellable(
            ['.py', '.js', '.ts', '.java', '.cpp', '.cs', '.go', '.rb', '.php'], token
        )
        
        # Feature detection patterns
        feature_patterns = {
            "authentication": ["auth", "login", "signin", "signup", "oauth", "jwt"],
            "user_management": ["user", "profile", "account", "member"],
            "data_processing": ["process", "transform", "parse", "analyze"],
            "api_integration": ["api", "client", "service", "integration"],
            "notification": ["notify", "alert", "message", "email", "sms"],
            "payment": ["payment", "billing", "subscription", "checkout"],
            "search": ["search", "query", "index", "elasticsearch", "solr"],
            "reporting": ["report", "analytics", "dashboard", "metrics"],
            "file_management": ["file", "upload", "download", "storage"],
            "security": ["security", "encryption", "hash", "validate"]
        }
        
        feature_files = defaultdict(list)
        
        for i, file_path in enumerate(source_files):
            if token and i % 20 == 0:
                token.check_cancellation()
            
            relative_path = str(file_path.relative_to(self.repo_path))
            file_content = self.read_file_content(file_path)
            
            if not file_content:
                continue
            
            # Detect features based on file names and content
            for feature_name, keywords in feature_patterns.items():
                for keyword in keywords:
                    if (keyword in relative_path.lower() or 
                        keyword in file_content.lower()):
                        feature_files[feature_name].append(relative_path)
                        break
        
        # Analyze feature consistency
        for feature, files in feature_files.items():
            if files:
                feature_analysis["features"].append({
                    "name": feature,
                    "file_count": len(files),
                    "files": files[:10],  # Limit for performance
                    "coverage_score": min(len(files) / 5.0, 1.0)  # Normalize to 0-1
                })
        
        return feature_analysis
    
    def _analyze_api_consistency(self, token=None) -> Dict[str, Any]:
        """Analyze API consistency across the codebase"""
        api_analysis = {
            "endpoints": [],
            "naming_patterns": {},
            "response_formats": [],
            "consistency_score": 0.0
        }
        
        # API file patterns
        api_files = []
        api_patterns = [
            "**/*api*", "**/*controller*", "**/*route*", "**/*endpoint*",
            "**/*handler*", "**/*service*"
        ]
        
        for pattern in api_patterns:
            if token:
                token.check_cancellation()
            api_files.extend(self.find_files_by_pattern(pattern))
        
        endpoint_patterns = []
        naming_conventions = defaultdict(int)
        
        for i, api_file in enumerate(api_files):
            if token and i % 10 == 0:
                token.check_cancellation()
            
            content = self.read_file_content(api_file)
            if not content:
                continue
            
            # Extract API endpoints
            endpoints = self._extract_api_endpoints(content)
            api_analysis["endpoints"].extend(endpoints)
            
            # Analyze naming patterns
            for endpoint in endpoints:
                if "/" in endpoint:
                    parts = endpoint.split("/")
                    for part in parts:
                        if part and not part.startswith("{"):
                            naming_conventions[part] += 1
        
        api_analysis["naming_patterns"] = dict(naming_conventions)
        
        # Calculate consistency score
        if api_analysis["endpoints"]:
            consistency_score = self._calculate_api_consistency_score(api_analysis["endpoints"])
            api_analysis["consistency_score"] = consistency_score
        
        return api_analysis
    
    def _analyze_development_focus(self, token=None) -> Dict[str, Any]:
        """Analyze commit messages and development patterns for product focus"""
        focus_analysis = {
            "feature_development": {},
            "maintenance_ratio": 0.0,
            "product_keywords": [],
            "development_trends": {}
        }
        
        if not self.repo:
            return focus_analysis
        
        # Get recent commits
        commits = self.get_git_history_cancellable(max_commits=500, token=token)
        
        # Product-focused keywords in commits
        product_keywords = [
            "feature", "product", "user", "customer", "experience",
            "improvement", "enhancement", "new", "add", "implement"
        ]
        
        maintenance_keywords = [
            "fix", "bug", "patch", "hotfix", "maintenance", "update",
            "refactor", "cleanup", "dependency", "security"
        ]
        
        feature_commits = 0
        maintenance_commits = 0
        keyword_counts = defaultdict(int)
        
        for i, commit in enumerate(commits):
            if token and i % 50 == 0:
                token.check_cancellation()
            
            message_lower = commit['message'].lower()
            
            # Classify commit type
            is_feature = any(keyword in message_lower for keyword in product_keywords)
            is_maintenance = any(keyword in message_lower for keyword in maintenance_keywords)
            
            if is_feature:
                feature_commits += 1
            if is_maintenance:
                maintenance_commits += 1
            
            # Count product keywords
            for keyword in product_keywords:
                if keyword in message_lower:
                    keyword_counts[keyword] += 1
        
        total_commits = len(commits)
        if total_commits > 0:
            focus_analysis["maintenance_ratio"] = maintenance_commits / total_commits
            focus_analysis["feature_ratio"] = feature_commits / total_commits
        
        focus_analysis["product_keywords"] = dict(keyword_counts)
        focus_analysis["total_commits_analyzed"] = total_commits
        
        return focus_analysis
    
    def _analyze_configuration_consistency(self, token=None) -> Dict[str, Any]:
        """Analyze configuration files for consistency"""
        config_analysis = {
            "config_files": [],
            "environment_consistency": {},
            "naming_consistency": 0.0,
            "structure_consistency": 0.0
        }
        
        # Configuration file patterns
        config_patterns = [
            "**/package.json", "**/requirements.txt", "**/Gemfile",
            "**/pom.xml", "**/build.gradle", "**/Cargo.toml",
            "**/*.env", "**/.env*", "**/config.*",
            "**/settings.*", "**/configuration.*"
        ]
        
        config_files = []
        for pattern in config_patterns:
            if token:
                token.check_cancellation()
            config_files.extend(self.find_files_by_pattern(pattern))
        
        config_data = []
        for i, config_file in enumerate(config_files):
            if token and i % 5 == 0:
                token.check_cancellation()
            
            content = self.read_file_content(config_file)
            if content:
                config_data.append({
                    "file": str(config_file.relative_to(self.repo_path)),
                    "size": len(content),
                    "type": config_file.suffix
                })
        
        config_analysis["config_files"] = config_data
        
        return config_analysis
    
    def _calculate_vision_coherence_score(self, vision_docs, feature_analysis, 
                                        api_consistency, development_focus, config_analysis) -> Dict[str, float]:
        """Calculate an overall product vision coherence score"""
        scores = {
            "documentation_score": 0.0,
            "architecture_score": 0.0,
            "api_consistency_score": 0.0,
            "development_focus_score": 0.0,
            "overall_score": 0.0
        }
        
        # Documentation score (0-1)
        if vision_docs["vision_statements"]:
            scores["documentation_score"] = min(len(vision_docs["vision_statements"]) / 3.0, 1.0)
        
        # Architecture score (0-1)
        if feature_analysis["features"]:
            avg_coverage = sum(f["coverage_score"] for f in feature_analysis["features"]) / len(feature_analysis["features"])
            scores["architecture_score"] = avg_coverage
        
        # API consistency score (0-1)
        scores["api_consistency_score"] = api_consistency.get("consistency_score", 0.0)
        
        # Development focus score (0-1)
        if development_focus.get("feature_ratio", 0) > 0:
            scores["development_focus_score"] = min(development_focus["feature_ratio"] * 2, 1.0)
        
        # Overall score
        scores["overall_score"] = (
            scores["documentation_score"] * 0.3 +
            scores["architecture_score"] * 0.3 +
            scores["api_consistency_score"] * 0.2 +
            scores["development_focus_score"] * 0.2
        )
        
        return scores
    
    def _extract_vision_from_readme(self, content: str) -> Dict[str, Any]:
        """Extract product vision information from README content"""
        readme_analysis = {
            "has_description": False,
            "has_features": False,
            "has_roadmap": False,
            "description_length": 0
        }
        
        content_lower = content.lower()
        
        # Check for common README sections
        readme_analysis["has_description"] = any(
            section in content_lower for section in 
            ["description", "about", "overview", "what is"]
        )
        
        readme_analysis["has_features"] = any(
            section in content_lower for section in 
            ["features", "functionality", "capabilities"]
        )
        
        readme_analysis["has_roadmap"] = any(
            section in content_lower for section in 
            ["roadmap", "future", "planned", "upcoming"]
        )
        
        # Estimate description length (first paragraph after title)
        lines = content.split('\n')
        description_lines = []
        found_title = False
        
        for line in lines:
            if line.strip().startswith('#') and not found_title:
                found_title = True
                continue
            elif found_title and line.strip():
                if not line.startswith('#'):
                    description_lines.append(line.strip())
                else:
                    break
            elif found_title and not line.strip():
                break
        
        readme_analysis["description_length"] = len(' '.join(description_lines))
        
        return readme_analysis
    
    def _extract_vision_statements(self, content: str, keywords: List[str]) -> List[str]:
        """Extract vision-related statements from content"""
        statements = []
        
        # Split content into sentences
        sentences = re.split(r'[.!?]+', content)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Avoid short fragments
                for keyword in keywords:
                    if keyword in sentence.lower():
                        statements.append(sentence)
                        break
        
        return statements[:5]  # Limit to top 5 statements
    
    def _extract_api_endpoints(self, content: str) -> List[str]:
        """Extract API endpoints from code content"""
        endpoints = []
        
        # Common API endpoint patterns
        patterns = [
            r'["\']/([\w\-/{}]+)["\']',  # Generic path patterns
            r'@\w+Mapping\(["\']/([\w\-/{}]+)["\']',  # Spring Boot
            r'app\.(get|post|put|delete)\(["\']/([\w\-/{}]+)["\']',  # Express.js
            r'Route::(get|post|put|delete)\(["\']/([\w\-/{}]+)["\']',  # Laravel
            r'router\.(get|post|put|delete)\(["\']/([\w\-/{}]+)["\']'  # Various frameworks
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    endpoint = match[1] if len(match) > 1 else match[0]
                else:
                    endpoint = match
                
                if endpoint and len(endpoint) > 1:
                    endpoints.append("/" + endpoint)
        
        return list(set(endpoints))  # Remove duplicates
    
    def _calculate_api_consistency_score(self, endpoints: List[str]) -> float:
        """Calculate API consistency score based on naming patterns"""
        if not endpoints:
            return 0.0
        
        # Analyze naming consistency
        naming_patterns = defaultdict(int)
        for endpoint in endpoints:
            parts = endpoint.split("/")
            for part in parts:
                if part and not part.startswith("{"):
                    # Check for consistent naming patterns
                    if "_" in part:
                        naming_patterns["snake_case"] += 1
                    elif "-" in part:
                        naming_patterns["kebab-case"] += 1
                    elif part.islower():
                        naming_patterns["lowercase"] += 1
                    elif any(c.isupper() for c in part):
                        naming_patterns["camelCase"] += 1
        
        if not naming_patterns:
            return 0.0
        
        # Calculate consistency as the ratio of the most common pattern
        max_pattern_count = max(naming_patterns.values())
        total_parts = sum(naming_patterns.values())
        
        return max_pattern_count / total_parts if total_parts > 0 else 0.0
    
    def render(self):
        """Render the singular product vision analysis"""
        st.header("🎯 Singular Product Vision Analysis")
        st.markdown("Analyzing product vision consistency, feature alignment, and strategic coherence")
        
        # Add rerun button
        self.add_rerun_button("singular_product_vision")
        
        with self.display_loading_message("Analyzing product vision and strategic coherence..."):
            analysis = self.analyze()
        
        if "error" in analysis:
            self.display_error(analysis["error"])
            return
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Vision Coherence Score", f"{analysis['vision_coherence_score']['overall_score']:.2f}")
        with col2:
            st.metric("Features Identified", analysis["total_features_identified"])
        with col3:
            st.metric("Documentation Coverage", analysis["documentation_coverage"])
        with col4:
            api_score = analysis['vision_coherence_score']['api_consistency_score']
            st.metric("API Consistency", f"{api_score:.2f}")
        
        # Vision coherence breakdown
        st.subheader("📊 Vision Coherence Breakdown")
        
        coherence_scores = analysis["vision_coherence_score"]
        score_data = [
            {"Category": "Documentation", "Score": coherence_scores["documentation_score"]},
            {"Category": "Architecture", "Score": coherence_scores["architecture_score"]},
            {"Category": "API Consistency", "Score": coherence_scores["api_consistency_score"]},
            {"Category": "Development Focus", "Score": coherence_scores["development_focus_score"]}
        ]
        
        df_scores = pd.DataFrame(score_data)
        fig_scores = px.bar(
            df_scores,
            x="Category",
            y="Score",
            title="Product Vision Coherence by Category",
            color="Score",
            color_continuous_scale="RdYlGn",
            range_color=[0, 1]
        )
        fig_scores.update_layout(height=400)
        st.plotly_chart(fig_scores, use_container_width=True)
        
        # Product documentation analysis
        st.subheader("📚 Product Documentation Analysis")
        
        vision_docs = analysis["vision_documentation"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Vision Statements Found:**")
            if vision_docs["vision_statements"]:
                for item in vision_docs["vision_statements"]:
                    with st.expander(f"📄 {item['file']}"):
                        for statement in item["statements"]:
                            st.write(f"• {statement}")
            else:
                st.info("No explicit vision statements found in documentation")
        
        with col2:
            st.write("**Mission Keywords Distribution:**")
            if vision_docs["mission_keywords"]:
                keyword_counts = defaultdict(int)
                for item in vision_docs["mission_keywords"]:
                    keyword_counts[item["keyword"]] += item["count"]
                
                keyword_df = pd.DataFrame([
                    {"Keyword": k, "Count": v}
                    for k, v in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
                ])
                
                fig_keywords = px.bar(
                    keyword_df.head(10),
                    x="Keyword",
                    y="Count",
                    title="Top Vision-Related Keywords"
                )
                st.plotly_chart(fig_keywords, use_container_width=True)
            else:
                st.info("No vision-related keywords found")
        
        # README analysis
        if vision_docs["readme_analysis"]:
            st.write("**README Analysis:**")
            readme_data = []
            for file_path, readme_info in vision_docs["readme_analysis"].items():
                readme_data.append({
                    "File": file_path,
                    "Has Description": "✅" if readme_info["has_description"] else "❌",
                    "Has Features": "✅" if readme_info["has_features"] else "❌",
                    "Has Roadmap": "✅" if readme_info["has_roadmap"] else "❌",
                    "Description Length": readme_info["description_length"]
                })
            
            if readme_data:
                st.dataframe(pd.DataFrame(readme_data), use_container_width=True)
        
        # Feature architecture analysis
        st.subheader("🏗️ Feature Architecture Analysis")
        
        feature_analysis = analysis["feature_architecture"]
        
        if feature_analysis["features"]:
            # Feature coverage visualization
            feature_data = []
            for feature in feature_analysis["features"]:
                feature_data.append({
                    "Feature": feature["name"].replace("_", " ").title(),
                    "File Count": feature["file_count"],
                    "Coverage Score": feature["coverage_score"]
                })
            
            df_features = pd.DataFrame(feature_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_feature_files = px.bar(
                    df_features.sort_values("File Count", ascending=False).head(10),
                    x="Feature",
                    y="File Count",
                    title="Features by File Count"
                )
                fig_feature_files.update_xaxes(tickangle=45)
                st.plotly_chart(fig_feature_files, use_container_width=True)
            
            with col2:
                fig_coverage = px.bar(
                    df_features.sort_values("Coverage Score", ascending=False).head(10),
                    x="Feature",
                    y="Coverage Score",
                    title="Feature Coverage Scores",
                    color="Coverage Score",
                    color_continuous_scale="RdYlGn"
                )
                fig_coverage.update_xaxes(tickangle=45)
                st.plotly_chart(fig_coverage, use_container_width=True)
            
            # Feature details
            st.write("**Feature Details:**")
            for feature in sorted(feature_analysis["features"], key=lambda x: x["file_count"], reverse=True)[:10]:
                with st.expander(f"🔧 {feature['name'].replace('_', ' ').title()} ({feature['file_count']} files)"):
                    st.write("**Files involved:**")
                    for file_path in feature["files"]:
                        st.write(f"• {file_path}")
                    if len(feature.get("files", [])) == 10 and feature["file_count"] > 10:
                        st.write(f"... and {feature['file_count'] - 10} more files")
        else:
            st.info("No clear feature patterns detected in the codebase")
        
        # Development focus analysis
        st.subheader("💡 Development Focus Analysis")
        
        dev_focus = analysis["development_focus"]
        
        if dev_focus.get("total_commits_analyzed", 0) > 0:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                feature_ratio = dev_focus.get("feature_ratio", 0)
                st.metric("Feature Development Ratio", f"{feature_ratio:.2%}")
            
            with col2:
                maintenance_ratio = dev_focus.get("maintenance_ratio", 0)
                st.metric("Maintenance Ratio", f"{maintenance_ratio:.2%}")
            
            with col3:
                st.metric("Commits Analyzed", dev_focus["total_commits_analyzed"])
            
            # Product keywords in commits
            if dev_focus["product_keywords"]:
                st.write("**Product-Focused Keywords in Commits:**")
                keyword_df = pd.DataFrame([
                    {"Keyword": k, "Occurrences": v}
                    for k, v in sorted(dev_focus["product_keywords"].items(), key=lambda x: x[1], reverse=True)
                ])
                
                fig_commit_keywords = px.bar(
                    keyword_df.head(10),
                    x="Keyword",
                    y="Occurrences",
                    title="Product Keywords in Commit Messages"
                )
                st.plotly_chart(fig_commit_keywords, use_container_width=True)
        else:
            st.info("No commit history available for development focus analysis")
        
        # API consistency analysis
        st.subheader("🔗 API Consistency Analysis")
        
        api_analysis = analysis["api_consistency"]
        
        if api_analysis["endpoints"]:
            st.write(f"**Found {len(api_analysis['endpoints'])} API endpoints**")
            
            if api_analysis["naming_patterns"]:
                # API naming patterns
                pattern_df = pd.DataFrame([
                    {"Pattern": k, "Count": v}
                    for k, v in sorted(api_analysis["naming_patterns"].items(), key=lambda x: x[1], reverse=True)
                ])
                
                fig_patterns = px.pie(
                    pattern_df.head(10),
                    values="Count",
                    names="Pattern",
                    title="API Naming Patterns Distribution"
                )
                st.plotly_chart(fig_patterns, use_container_width=True)
            
            # Show sample endpoints
            with st.expander("📋 Sample API Endpoints"):
                sample_endpoints = api_analysis["endpoints"][:20]
                for endpoint in sample_endpoints:
                    st.code(endpoint)
                if len(api_analysis["endpoints"]) > 20:
                    st.write(f"... and {len(api_analysis['endpoints']) - 20} more endpoints")
        else:
            st.info("No API endpoints detected in the codebase")
        
        # Configuration consistency
        st.subheader("⚙️ Configuration Analysis")
        
        config_analysis = analysis["configuration_consistency"]
        
        if config_analysis["config_files"]:
            config_df = pd.DataFrame(config_analysis["config_files"])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Configuration Files Found:**")
                st.dataframe(config_df, use_container_width=True)
            
            with col2:
                # Configuration file types
                type_counts = config_df["type"].value_counts()
                fig_config_types = px.pie(
                    values=type_counts.values,
                    names=type_counts.index,
                    title="Configuration File Types"
                )
                st.plotly_chart(fig_config_types, use_container_width=True)
        else:
            st.info("No configuration files detected")
        
        # AI-powered insights
        st.subheader("🤖 AI Insights")
        
        if st.button("Generate Product Vision Insights"):
            with self.display_loading_message("Generating AI insights..."):
                # Prepare data for AI analysis
                vision_summary = {
                    "overall_score": analysis["vision_coherence_score"]["overall_score"],
                    "features_identified": analysis["total_features_identified"],
                    "documentation_coverage": analysis["documentation_coverage"],
                    "api_consistency": analysis["vision_coherence_score"]["api_consistency_score"],
                    "development_focus_ratio": dev_focus.get("feature_ratio", 0),
                    "top_features": [f["name"] for f in sorted(
                        feature_analysis.get("features", []), 
                        key=lambda x: x["file_count"], reverse=True
                    )[:5]]
                }
                
                prompt = f"""
                Analyze this product vision coherence data and provide strategic insights:
                
                {vision_summary}
                
                Please provide:
                1. Assessment of product vision clarity and consistency
                2. Strengths in current product direction
                3. Areas where vision could be improved
                4. Recommendations for better feature alignment
                5. Strategic suggestions for maintaining product focus
                6. Potential risks to product coherence
                """
                
                insights = self.ai_client.query(prompt)
                
                if insights:
                    st.markdown("**AI-Generated Strategic Insights:**")
                    st.markdown(insights)
                else:
                    st.error("Failed to generate AI insights")
        
        # Add save options
        self.add_save_options("singular_product_vision", analysis)
