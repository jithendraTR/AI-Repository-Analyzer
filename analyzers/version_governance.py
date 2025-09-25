"""
Version Governance Analyzer
Analyzes dependency management and version control patterns
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict, Counter
from typing import Dict, List, Any, Tuple
import re
from pathlib import Path
import json

from .base_analyzer import BaseAnalyzer

class VersionGovernanceAnalyzer(BaseAnalyzer):
    """Analyzes version governance and dependency management"""
    
    def analyze(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Analyze version governance patterns"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("version_governance")
        if cached_result:
            return cached_result
        
        # Analyze dependency files
        dependency_analysis = self._analyze_dependency_files()
        
        # Analyze version patterns
        version_patterns = self._analyze_version_patterns()
        
        # Analyze lock files
        lock_file_analysis = self._analyze_lock_files()
        
        # Analyze version conflicts
        version_conflicts = self._detect_version_conflicts()
        
        # Analyze update frequency
        update_patterns = self._analyze_update_patterns()
        
        # Analyze security vulnerabilities
        security_analysis = self._analyze_security_vulnerabilities()
        
        result = {
            "dependency_analysis": dependency_analysis,
            "version_patterns": version_patterns,
            "lock_file_analysis": lock_file_analysis,
            "version_conflicts": version_conflicts,
            "update_patterns": update_patterns,
            "security_analysis": security_analysis,
            "governance_summary": self._generate_governance_summary(
                dependency_analysis, version_patterns, lock_file_analysis
            )
        }
        
        # Cache the result
        self.cache_analysis("version_governance", result)
        
        return result
    
    def _analyze_dependency_files(self) -> Dict[str, Any]:
        """Analyze dependency management files"""
        
        analysis = {
            "python_dependencies": [],
            "node_dependencies": [],
            "java_dependencies": [],
            "dependency_counts": defaultdict(int),
            "package_managers": defaultdict(int)
        }
        
        # Python dependencies
        python_files = [
            "**/requirements.txt", "**/requirements-*.txt",
            "**/setup.py", "**/pyproject.toml", "**/Pipfile"
        ]
        
        for pattern in python_files:
            files = self.find_files_by_pattern(pattern)
            for file_path in files:
                content = self.read_file_content(file_path)
                if content:
                    deps = self._parse_python_dependencies(content, file_path)
                    analysis["python_dependencies"].extend(deps)
                    analysis["package_managers"]["pip/conda"] += 1
        
        # Node.js dependencies
        package_files = self.find_files_by_pattern("**/package.json")
        for file_path in package_files:
            content = self.read_file_content(file_path)
            if content:
                deps = self._parse_node_dependencies(content, file_path)
                analysis["node_dependencies"].extend(deps)
                analysis["package_managers"]["npm/yarn"] += 1
        
        # Java dependencies
        java_files = ["**/pom.xml", "**/build.gradle", "**/build.gradle.kts"]
        for pattern in java_files:
            files = self.find_files_by_pattern(pattern)
            for file_path in files:
                content = self.read_file_content(file_path)
                if content:
                    deps = self._parse_java_dependencies(content, file_path)
                    analysis["java_dependencies"].extend(deps)
                    if "pom.xml" in str(file_path):
                        analysis["package_managers"]["maven"] += 1
                    else:
                        analysis["package_managers"]["gradle"] += 1
        
        # Count dependencies by type
        all_deps = (analysis["python_dependencies"] + 
                   analysis["node_dependencies"] + 
                   analysis["java_dependencies"])
        
        for dep in all_deps:
            analysis["dependency_counts"][dep.get("type", "unknown")] += 1
        
        return analysis
    
    def _parse_python_dependencies(self, content: str, file_path: Path) -> List[Dict]:
        """Parse Python dependency files"""
        
        dependencies = []
        
        if file_path.name == "requirements.txt" or "requirements" in file_path.name:
            for line_num, line in enumerate(content.split('\n'), 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    dep_info = self._parse_python_requirement_line(line)
                    if dep_info:
                        dep_info.update({
                            "file": str(file_path.relative_to(self.repo_path)),
                            "line": line_num,
                            "type": "production" if "dev" not in file_path.name else "development"
                        })
                        dependencies.append(dep_info)
        
        elif file_path.name == "setup.py":
            # Extract dependencies from setup.py
            install_requires_match = re.search(r'install_requires\s*=\s*\[(.*?)\]', content, re.DOTALL)
            if install_requires_match:
                deps_text = install_requires_match.group(1)
                for dep in re.findall(r'["\']([^"\']+)["\']', deps_text):
                    dep_info = self._parse_python_requirement_line(dep)
                    if dep_info:
                        dep_info.update({
                            "file": str(file_path.relative_to(self.repo_path)),
                            "type": "production"
                        })
                        dependencies.append(dep_info)
        
        elif file_path.name == "pyproject.toml":
            # Basic TOML parsing for dependencies
            deps_section = re.search(r'\[tool\.poetry\.dependencies\](.*?)(?=\[|\Z)', content, re.DOTALL)
            if deps_section:
                for line in deps_section.group(1).split('\n'):
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        parts = line.split('=', 1)
                        if len(parts) == 2:
                            name = parts[0].strip()
                            version = parts[1].strip().strip('"\'')
                            dependencies.append({
                                "name": name,
                                "version": version,
                                "file": str(file_path.relative_to(self.repo_path)),
                                "type": "production"
                            })
        
        return dependencies
    
    def _parse_python_requirement_line(self, line: str) -> Dict:
        """Parse a single Python requirement line"""
        
        # Handle different version specifiers
        version_patterns = [
            r'([a-zA-Z0-9_-]+)==([0-9\.]+)',  # exact version
            r'([a-zA-Z0-9_-]+)>=([0-9\.]+)',  # minimum version
            r'([a-zA-Z0-9_-]+)<=([0-9\.]+)',  # maximum version
            r'([a-zA-Z0-9_-]+)~=([0-9\.]+)',  # compatible version
            r'([a-zA-Z0-9_-]+)\[.*\]==([0-9\.]+)',  # with extras
            r'([a-zA-Z0-9_-]+)$'  # no version specified
        ]
        
        for pattern in version_patterns:
            match = re.match(pattern, line)
            if match:
                if len(match.groups()) == 2:
                    return {
                        "name": match.group(1),
                        "version": match.group(2),
                        "version_type": "pinned" if "==" in line else "flexible"
                    }
                else:
                    return {
                        "name": match.group(1),
                        "version": "latest",
                        "version_type": "unpinned"
                    }
        
        return None
    
    def _parse_node_dependencies(self, content: str, file_path: Path) -> List[Dict]:
        """Parse Node.js package.json dependencies"""
        
        dependencies = []
        
        try:
            package_data = json.loads(content)
            
            # Production dependencies
            deps = package_data.get("dependencies", {})
            for name, version in deps.items():
                dependencies.append({
                    "name": name,
                    "version": version,
                    "version_type": self._classify_node_version(version),
                    "file": str(file_path.relative_to(self.repo_path)),
                    "type": "production"
                })
            
            # Development dependencies
            dev_deps = package_data.get("devDependencies", {})
            for name, version in dev_deps.items():
                dependencies.append({
                    "name": name,
                    "version": version,
                    "version_type": self._classify_node_version(version),
                    "file": str(file_path.relative_to(self.repo_path)),
                    "type": "development"
                })
        
        except json.JSONDecodeError:
            pass
        
        return dependencies
    
    def _classify_node_version(self, version: str) -> str:
        """Classify Node.js version specification"""
        
        if version.startswith("^"):
            return "caret"
        elif version.startswith("~"):
            return "tilde"
        elif version.startswith(">="):
            return "minimum"
        elif version.startswith("<="):
            return "maximum"
        elif re.match(r'^\d+\.\d+\.\d+$', version):
            return "exact"
        else:
            return "other"
    
    def _parse_java_dependencies(self, content: str, file_path: Path) -> List[Dict]:
        """Parse Java dependency files"""
        
        dependencies = []
        
        if file_path.name == "pom.xml":
            # Parse Maven dependencies
            dep_pattern = r'<dependency>.*?<groupId>(.*?)</groupId>.*?<artifactId>(.*?)</artifactId>.*?<version>(.*?)</version>.*?</dependency>'
            matches = re.findall(dep_pattern, content, re.DOTALL)
            
            for group_id, artifact_id, version in matches:
                dependencies.append({
                    "name": f"{group_id}:{artifact_id}",
                    "version": version.strip(),
                    "version_type": "exact" if not any(c in version for c in ['$', '[', '(']) else "variable",
                    "file": str(file_path.relative_to(self.repo_path)),
                    "type": "production"
                })
        
        elif "build.gradle" in file_path.name:
            # Parse Gradle dependencies
            dep_patterns = [
                r"implementation\s+['\"]([^:]+):([^:]+):([^'\"]+)['\"]",
                r"compile\s+['\"]([^:]+):([^:]+):([^'\"]+)['\"]",
                r"testImplementation\s+['\"]([^:]+):([^:]+):([^'\"]+)['\"]"
            ]
            
            for pattern in dep_patterns:
                matches = re.findall(pattern, content)
                dep_type = "development" if "test" in pattern else "production"
                
                for group_id, artifact_id, version in matches:
                    dependencies.append({
                        "name": f"{group_id}:{artifact_id}",
                        "version": version,
                        "version_type": "exact" if not any(c in version for c in ['+', '$']) else "variable",
                        "file": str(file_path.relative_to(self.repo_path)),
                        "type": dep_type
                    })
        
        return dependencies
    
    def _analyze_version_patterns(self) -> Dict[str, Any]:
        """Analyze version specification patterns"""
        
        patterns = {
            "version_strategies": defaultdict(int),
            "pinning_analysis": defaultdict(int),
            "version_ranges": defaultdict(int),
            "semantic_versioning": defaultdict(int)
        }
        
        # Get all dependencies
        dep_analysis = self._analyze_dependency_files()
        all_deps = (dep_analysis["python_dependencies"] + 
                   dep_analysis["node_dependencies"] + 
                   dep_analysis["java_dependencies"])
        
        for dep in all_deps:
            version_type = dep.get("version_type", "unknown")
            patterns["version_strategies"][version_type] += 1
            
            version = dep.get("version", "")
            
            # Analyze pinning
            if version_type in ["pinned", "exact"]:
                patterns["pinning_analysis"]["pinned"] += 1
            elif version_type in ["flexible", "caret", "tilde", "minimum", "maximum"]:
                patterns["pinning_analysis"]["flexible"] += 1
            else:
                patterns["pinning_analysis"]["unpinned"] += 1
            
            # Analyze semantic versioning
            if re.match(r'^\d+\.\d+\.\d+', version):
                patterns["semantic_versioning"]["semver_compliant"] += 1
            else:
                patterns["semantic_versioning"]["non_semver"] += 1
        
        return patterns
    
    def _analyze_lock_files(self) -> Dict[str, Any]:
        """Analyze lock files for dependency resolution"""
        
        analysis = {
            "lock_files_found": [],
            "lock_file_types": defaultdict(int),
            "locked_dependencies": 0,
            "lock_file_freshness": {}
        }
        
        # Look for lock files
        lock_patterns = [
            "**/package-lock.json", "**/yarn.lock",
            "**/Pipfile.lock", "**/poetry.lock",
            "**/composer.lock", "**/Gemfile.lock"
        ]
        
        for pattern in lock_patterns:
            lock_files = self.find_files_by_pattern(pattern)
            for lock_file in lock_files:
                relative_path = str(lock_file.relative_to(self.repo_path))
                analysis["lock_files_found"].append(relative_path)
                
                # Determine lock file type
                if "package-lock.json" in lock_file.name:
                    analysis["lock_file_types"]["npm"] += 1
                elif "yarn.lock" in lock_file.name:
                    analysis["lock_file_types"]["yarn"] += 1
                elif "Pipfile.lock" in lock_file.name:
                    analysis["lock_file_types"]["pipenv"] += 1
                elif "poetry.lock" in lock_file.name:
                    analysis["lock_file_types"]["poetry"] += 1
                
                # Analyze lock file content
                content = self.read_file_content(lock_file)
                if content:
                    locked_deps = self._count_locked_dependencies(content, lock_file.name)
                    analysis["locked_dependencies"] += locked_deps
        
        return analysis
    
    def _count_locked_dependencies(self, content: str, filename: str) -> int:
        """Count dependencies in lock files"""
        
        try:
            if "package-lock.json" in filename:
                data = json.loads(content)
                return len(data.get("dependencies", {}))
            elif "yarn.lock" in filename:
                # Count yarn lock entries
                return len(re.findall(r'^[^#\s].*?:', content, re.MULTILINE))
            elif ".lock" in filename:
                # Generic lock file - count lines that look like dependencies
                return len([line for line in content.split('\n') if line.strip() and not line.strip().startswith('#')])
        except (json.JSONDecodeError, Exception):
            return 0
        
        return 0
    
    def _detect_version_conflicts(self) -> Dict[str, Any]:
        """Detect potential version conflicts"""
        
        conflicts = {
            "duplicate_dependencies": [],
            "version_mismatches": [],
            "conflicting_ranges": []
        }
        
        # Get all dependencies
        dep_analysis = self._analyze_dependency_files()
        all_deps = (dep_analysis["python_dependencies"] + 
                   dep_analysis["node_dependencies"] + 
                   dep_analysis["java_dependencies"])
        
        # Group by package name
        packages = defaultdict(list)
        for dep in all_deps:
            packages[dep["name"]].append(dep)
        
        # Check for conflicts
        for package_name, deps in packages.items():
            if len(deps) > 1:
                versions = [dep["version"] for dep in deps]
                unique_versions = set(versions)
                
                if len(unique_versions) > 1:
                    conflicts["version_mismatches"].append({
                        "package": package_name,
                        "versions": list(unique_versions),
                        "files": [dep["file"] for dep in deps]
                    })
                
                conflicts["duplicate_dependencies"].append({
                    "package": package_name,
                    "count": len(deps),
                    "files": [dep["file"] for dep in deps]
                })
        
        return conflicts
    
    def _analyze_update_patterns(self) -> Dict[str, Any]:
        """Analyze dependency update patterns"""
        
        patterns = {
            "outdated_dependencies": [],
            "update_frequency": defaultdict(int),
            "major_version_updates": [],
            "security_updates": []
        }
        
        # This would typically integrate with package registries
        # For now, we'll analyze based on version patterns
        
        dep_analysis = self._analyze_dependency_files()
        all_deps = (dep_analysis["python_dependencies"] + 
                   dep_analysis["node_dependencies"] + 
                   dep_analysis["java_dependencies"])
        
        for dep in all_deps:
            version = dep.get("version", "")
            
            # Check for potentially outdated versions
            if re.match(r'^[0-2]\.\d+\.\d+$', version):
                patterns["outdated_dependencies"].append({
                    "package": dep["name"],
                    "current_version": version,
                    "file": dep["file"]
                })
        
        return patterns
    
    def _analyze_security_vulnerabilities(self) -> Dict[str, Any]:
        """Analyze potential security vulnerabilities"""
        
        security = {
            "vulnerable_packages": [],
            "security_advisories": [],
            "risk_assessment": defaultdict(int)
        }
        
        # Known vulnerable package patterns (simplified)
        vulnerable_patterns = [
            (r"lodash", r"^[0-3]\.", "High"),
            (r"moment", r"^2\.[0-9]\.", "Medium"),
            (r"jquery", r"^[1-2]\.", "High"),
            (r"express", r"^[0-3]\.", "High")
        ]
        
        dep_analysis = self._analyze_dependency_files()
        all_deps = (dep_analysis["python_dependencies"] + 
                   dep_analysis["node_dependencies"] + 
                   dep_analysis["java_dependencies"])
        
        for dep in all_deps:
            package_name = dep.get("name", "").lower()
            version = dep.get("version", "")
            
            for pattern, vuln_version, risk_level in vulnerable_patterns:
                if re.search(pattern, package_name) and re.match(vuln_version, version):
                    security["vulnerable_packages"].append({
                        "package": dep["name"],
                        "version": version,
                        "risk_level": risk_level,
                        "file": dep["file"]
                    })
                    security["risk_assessment"][risk_level] += 1
        
        return security
    
    def _generate_governance_summary(self, dependency_analysis: Dict, 
                                   version_patterns: Dict, 
                                   lock_file_analysis: Dict) -> Dict[str, Any]:
        """Generate governance summary"""
        
        summary = {
            "total_dependencies": 0,
            "governance_score": 0,
            "package_managers": [],
            "version_strategy": "Mixed",
            "lock_file_coverage": 0
        }
        
        # Count total dependencies
        all_deps = (dependency_analysis["python_dependencies"] + 
                   dependency_analysis["node_dependencies"] + 
                   dependency_analysis["java_dependencies"])
        summary["total_dependencies"] = len(all_deps)
        
        # Identify package managers
        summary["package_managers"] = list(dependency_analysis["package_managers"].keys())
        
        # Determine version strategy
        pinning_analysis = version_patterns["pinning_analysis"]
        if pinning_analysis["pinned"] > pinning_analysis["flexible"]:
            summary["version_strategy"] = "Conservative (Pinned)"
        elif pinning_analysis["flexible"] > pinning_analysis["pinned"]:
            summary["version_strategy"] = "Flexible (Ranges)"
        
        # Calculate governance score
        score_factors = []
        
        # Lock file presence
        if lock_file_analysis["lock_files_found"]:
            score_factors.append(25)
        
        # Version pinning strategy
        if pinning_analysis["pinned"] > 0:
            score_factors.append(20)
        
        # Package manager consistency
        if len(summary["package_managers"]) <= 2:
            score_factors.append(15)
        
        # Semantic versioning compliance
        semver_compliance = version_patterns["semantic_versioning"]
        if semver_compliance["semver_compliant"] > semver_compliance["non_semver"]:
            score_factors.append(20)
        
        # Dependency count (not too many, not too few)
        if 10 <= summary["total_dependencies"] <= 100:
            score_factors.append(20)
        
        summary["governance_score"] = sum(score_factors)
        
        return summary
    
    def render(self):
        """Render the version governance analysis"""
        st.header("📦 Version Governance & Dependency Management")
        st.markdown("Analyzing dependency management practices and version control")
        
        # Add rerun button
        self.add_rerun_button("version_governance")
        
        with self.display_loading_message("Analyzing version governance..."):
            analysis = self.analyze()
        
        if "error" in analysis:
            self.display_error(analysis["error"])
            return
        
        # Governance Summary
        st.subheader("📊 Governance Summary")
        
        governance_summary = analysis["governance_summary"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Governance Score", f"{governance_summary['governance_score']}/100")
        
        with col2:
            st.metric("Total Dependencies", governance_summary["total_dependencies"])
        
        with col3:
            st.metric("Package Managers", len(governance_summary["package_managers"]))
        
        with col4:
            st.metric("Version Strategy", governance_summary["version_strategy"])
        
        # Dependency Analysis
        st.subheader("📋 Dependency Analysis")
        
        dependency_analysis = analysis["dependency_analysis"]
        
        # Package managers distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Package Managers**")
            package_managers = dict(dependency_analysis["package_managers"])
            if package_managers:
                fig = px.pie(
                    values=list(package_managers.values()),
                    names=list(package_managers.keys()),
                    title="Package Manager Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Dependency Types**")
            dep_counts = dict(dependency_analysis["dependency_counts"])
            if dep_counts:
                fig = px.pie(
                    values=list(dep_counts.values()),
                    names=list(dep_counts.keys()),
                    title="Dependency Types"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Version Patterns Analysis
        st.subheader("🔢 Version Patterns")
        
        version_patterns = analysis["version_patterns"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Version Strategies**")
            version_strategies = dict(version_patterns["version_strategies"])
            if version_strategies:
                fig = px.bar(
                    x=list(version_strategies.values()),
                    y=list(version_strategies.keys()),
                    orientation='h',
                    title="Version Strategy Usage"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Pinning Analysis**")
            pinning_analysis = dict(version_patterns["pinning_analysis"])
            if pinning_analysis:
                fig = px.pie(
                    values=list(pinning_analysis.values()),
                    names=list(pinning_analysis.keys()),
                    title="Version Pinning Strategy"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Lock File Analysis
        st.subheader("🔒 Lock File Analysis")
        
        lock_file_analysis = analysis["lock_file_analysis"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Lock Files Found**")
            lock_files = lock_file_analysis["lock_files_found"]
            if lock_files:
                for lock_file in lock_files:
                    st.write(f"• {lock_file}")
            else:
                st.info("No lock files found")
        
        with col2:
            st.write("**Lock File Types**")
            lock_types = dict(lock_file_analysis["lock_file_types"])
            if lock_types:
                fig = px.bar(
                    x=list(lock_types.values()),
                    y=list(lock_types.keys()),
                    orientation='h',
                    title="Lock File Types"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Version Conflicts
        st.subheader("⚠️ Version Conflicts")
        
        version_conflicts = analysis["version_conflicts"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Duplicate Dependencies**")
            duplicates = version_conflicts["duplicate_dependencies"]
            if duplicates:
                for dup in duplicates[:10]:  # Show top 10
                    st.write(f"• {dup['package']}: {dup['count']} occurrences")
            else:
                st.success("No duplicate dependencies found")
        
        with col2:
            st.write("**Version Mismatches**")
            mismatches = version_conflicts["version_mismatches"]
            if mismatches:
                for mismatch in mismatches[:10]:  # Show top 10
                    st.write(f"• {mismatch['package']}: {', '.join(mismatch['versions'])}")
            else:
                st.success("No version mismatches found")
        
        # Security Analysis
        st.subheader("🛡️ Security Analysis")
        
        security_analysis = analysis["security_analysis"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Risk Assessment**")
            risk_assessment = dict(security_analysis["risk_assessment"])
            if risk_assessment:
                fig = px.pie(
                    values=list(risk_assessment.values()),
                    names=list(risk_assessment.keys()),
                    title="Security Risk Levels"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("No security risks identified")
        
        with col2:
            st.write("**Vulnerable Packages**")
            vulnerable_packages = security_analysis["vulnerable_packages"]
            if vulnerable_packages:
                for vuln in vulnerable_packages[:10]:  # Show top 10
                    st.write(f"• {vuln['package']} v{vuln['version']} ({vuln['risk_level']})")
            else:
                st.success("No vulnerable packages detected")
        
        # AI-powered Governance Analysis
        st.subheader("🤖 AI Governance Insights")
        
        if st.button("Get AI Governance Recommendations"):
            with self.display_loading_message("Generating governance recommendations..."):
                # Prepare context for AI
                governance_context = {
                    "total_dependencies": governance_summary["total_dependencies"],
                    "governance_score": governance_summary["governance_score"],
                    "package_managers": governance_summary["package_managers"],
                    "version_strategy": governance_summary["version_strategy"],
                    "conflicts": len(version_conflicts["version_mismatches"]),
                    "security_risks": len(security_analysis["vulnerable_packages"])
                }
                
                prompt = f"""
                Based on this dependency governance analysis:
                
                Governance Summary: {governance_context}
                
                Please provide:
                1. Assessment of current dependency management practices
                2. Recommendations for improving version governance
                3. Security vulnerability mitigation strategies
                4. Best practices for dependency updates
                5. Package manager optimization suggestions
                """
                
                ai_insights = self.ai_client.query(prompt)
                
                if ai_insights:
                    st.markdown("**AI Governance Recommendations:**")
                    st.markdown(ai_insights)
                else:
                    st.error("Failed to generate governance recommendations")
        
        # Display AI insights from parallel analysis if available
        self.display_parallel_ai_insights("version_governance")
        
        # Add save options
        self.add_save_options("version_governance", analysis)
