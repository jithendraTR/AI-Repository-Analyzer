"""
AI Integration Analysis Analyzer
Provides AI-powered context for where to add new features and functionality
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict, Counter
from typing import Dict, List, Any, Tuple
import re
from pathlib import Path

from .base_analyzer import BaseAnalyzer

class AIContextAnalyzer(BaseAnalyzer):
    """Analyzes codebase to provide AI context for new feature development"""
    
    def analyze(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Analyze codebase for AI context insights"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("ai_context")
        if cached_result:
            return cached_result
        
        # Analyze code structure and patterns
        code_structure = self._analyze_code_structure()
        
        # Find extension points
        extension_points = self._find_extension_points()
        
        # Analyze architectural patterns
        architectural_patterns = self._analyze_architectural_patterns()
        
        # Find similar implementations
        similar_implementations = self._find_similar_implementations()
        
        # Analyze module dependencies
        module_dependencies = self._analyze_module_dependencies()
        
        # Find configuration patterns
        config_patterns = self._analyze_config_patterns()
        
        result = {
            "code_structure": code_structure,
            "extension_points": extension_points,
            "architectural_patterns": architectural_patterns,
            "similar_implementations": similar_implementations,
            "module_dependencies": module_dependencies,
            "config_patterns": config_patterns,
            "recommendations": self._generate_recommendations(
                code_structure, extension_points, architectural_patterns
            )
        }
        
        # Cache the result
        self.cache_analysis("ai_context", result)
        
        return result
    
    def _analyze_code_structure(self) -> Dict[str, Any]:
        """Analyze overall code structure and organization"""
        
        structure = {
            "directories": {},
            "file_types": defaultdict(int),
            "naming_patterns": defaultdict(int),
            "size_distribution": {},
            "complexity_indicators": {}
        }
        
        all_files = self.get_file_list()
        
        # Analyze directory structure
        directories = set()
        for file_path in all_files:
            parts = file_path.parts
            for i in range(1, len(parts)):
                dir_path = "/".join(parts[:i])
                directories.add(dir_path)
        
        # Count files per directory
        dir_file_counts = defaultdict(int)
        for file_path in all_files:
            parent_dir = str(file_path.parent.relative_to(self.repo_path))
            if parent_dir == ".":
                parent_dir = "root"
            dir_file_counts[parent_dir] += 1
        
        structure["directories"] = dict(dir_file_counts)
        
        # Analyze file types
        for file_path in all_files:
            suffix = file_path.suffix.lower()
            structure["file_types"][suffix] += 1
        
        # Analyze naming patterns
        for file_path in all_files:
            name = file_path.stem
            
            # Check naming conventions
            if "_" in name:
                structure["naming_patterns"]["snake_case"] += 1
            if "-" in name:
                structure["naming_patterns"]["kebab_case"] += 1
            if any(c.isupper() for c in name) and any(c.islower() for c in name):
                structure["naming_patterns"]["camelCase"] += 1
            if name.isupper():
                structure["naming_patterns"]["UPPER_CASE"] += 1
        
        # Analyze file sizes (simplified)
        size_ranges = {"small": 0, "medium": 0, "large": 0}
        for file_path in all_files[:100]:  # Limit for performance
            try:
                size = file_path.stat().st_size
                if size < 1000:
                    size_ranges["small"] += 1
                elif size < 10000:
                    size_ranges["medium"] += 1
                else:
                    size_ranges["large"] += 1
            except:
                continue
        
        structure["size_distribution"] = size_ranges
        
        return structure
    
    def _find_extension_points(self) -> List[Dict]:
        """Find potential extension points in the codebase"""
        
        extension_points = []
        
        # Common extension patterns
        patterns = {
            "abstract_classes": r"class\s+(\w+)\s*\([^)]*ABC[^)]*\):",
            "interfaces": r"class\s+(\w+)\s*\([^)]*Interface[^)]*\):",
            "base_classes": r"class\s+(\w+Base\w*):",
            "factory_methods": r"def\s+(create_\w+|make_\w+|build_\w+)",
            "plugin_systems": r"(plugin|extension|addon|module).*register",
            "hooks": r"(hook|callback|handler).*register",
            "decorators": r"@(\w+)\s*\n\s*def",
            "strategy_pattern": r"class\s+(\w+Strategy):",
            "observer_pattern": r"(subscribe|observe|listen|notify)",
            "template_methods": r"def\s+(\w*template\w*|process_\w+)"
        }
        
        code_files = self.get_file_list(['.py', '.js', '.ts', '.java', '.cpp', '.cs'])
        
        for file_path in code_files[:50]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            for pattern_name, pattern in patterns.items():
                matches = re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE)
                
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    context = self._extract_context(content, match.start(), match.end())
                    
                    extension_points.append({
                        "type": pattern_name,
                        "name": match.group(1) if match.groups() else match.group(0),
                        "file": relative_path,
                        "line": line_num,
                        "context": context,
                        "extensibility_score": self._calculate_extensibility_score(pattern_name, context)
                    })
        
        # Sort by extensibility score
        extension_points.sort(key=lambda x: x["extensibility_score"], reverse=True)
        
        return extension_points
    
    def _analyze_architectural_patterns(self) -> Dict[str, Any]:
        """Analyze architectural patterns in the codebase"""
        
        patterns = {
            "mvc": {"score": 0, "indicators": []},
            "mvp": {"score": 0, "indicators": []},
            "mvvm": {"score": 0, "indicators": []},
            "layered": {"score": 0, "indicators": []},
            "microservices": {"score": 0, "indicators": []},
            "event_driven": {"score": 0, "indicators": []},
            "repository": {"score": 0, "indicators": []},
            "service_layer": {"score": 0, "indicators": []},
            "dependency_injection": {"score": 0, "indicators": []}
        }
        
        # Pattern indicators
        pattern_indicators = {
            "mvc": [
                r"(model|view|controller)",
                r"class\s+\w*(Model|View|Controller)",
                r"(models|views|controllers)/"
            ],
            "mvp": [
                r"(presenter|view)",
                r"class\s+\w*(Presenter|View)",
                r"(presenters|views)/"
            ],
            "mvvm": [
                r"(viewmodel|view|model)",
                r"class\s+\w*(ViewModel|View|Model)",
                r"(viewmodels|views|models)/"
            ],
            "layered": [
                r"(service|repository|controller|domain)",
                r"(services|repositories|controllers|domain)/"
            ],
            "microservices": [
                r"(service|microservice|api)",
                r"docker",
                r"kubernetes",
                r"(services|microservices)/"
            ],
            "event_driven": [
                r"(event|message|queue|pub|sub)",
                r"(events|messages|queues)/"
            ],
            "repository": [
                r"class\s+\w*Repository",
                r"(repositories|repos)/"
            ],
            "service_layer": [
                r"class\s+\w*Service",
                r"(services|service)/"
            ],
            "dependency_injection": [
                r"(inject|dependency|container)",
                r"@inject",
                r"(di|ioc)/"
            ]
        }
        
        # Search for pattern indicators
        all_files = self.get_file_list()
        all_content = ""
        
        for file_path in all_files[:100]:  # Limit for performance
            content = self.read_file_content(file_path)
            if content:
                all_content += f"\n{file_path}\n{content}"
        
        for pattern_name, indicators in pattern_indicators.items():
            for indicator in indicators:
                matches = re.findall(indicator, all_content, re.IGNORECASE)
                patterns[pattern_name]["score"] += len(matches)
                if matches:
                    patterns[pattern_name]["indicators"].extend(matches[:5])  # Limit examples
        
        return patterns
    
    def _find_similar_implementations(self) -> List[Dict]:
        """Find similar implementations that could serve as templates"""
        
        similar_implementations = []
        
        # Common implementation patterns to look for
        implementation_patterns = {
            "crud_operations": r"(create|read|update|delete|get|post|put|patch)",
            "authentication": r"(auth|login|logout|token|session)",
            "validation": r"(validate|check|verify|sanitize)",
            "serialization": r"(serialize|deserialize|json|xml)",
            "caching": r"(cache|redis|memcache)",
            "logging": r"(log|logger|debug|info|warn|error)",
            "configuration": r"(config|settings|env|environment)",
            "database": r"(db|database|query|sql|orm)",
            "api_endpoints": r"(api|endpoint|route|handler)",
            "error_handling": r"(error|exception|try|catch|handle)"
        }
        
        code_files = self.get_file_list(['.py', '.js', '.ts', '.java', '.cpp', '.cs'])
        
        for file_path in code_files[:30]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Count pattern occurrences in this file
            file_patterns = {}
            for pattern_name, pattern in implementation_patterns.items():
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    file_patterns[pattern_name] = len(matches)
            
            if file_patterns:
                # Calculate implementation complexity
                complexity_score = sum(file_patterns.values())
                
                similar_implementations.append({
                    "file": relative_path,
                    "patterns": file_patterns,
                    "complexity_score": complexity_score,
                    "dominant_pattern": max(file_patterns.items(), key=lambda x: x[1])[0],
                    "lines_of_code": len(content.split('\n'))
                })
        
        # Sort by complexity score
        similar_implementations.sort(key=lambda x: x["complexity_score"], reverse=True)
        
        return similar_implementations[:20]  # Return top 20
    
    def _analyze_module_dependencies(self) -> Dict[str, Any]:
        """Analyze module dependencies and coupling"""
        
        dependencies = {
            "imports": defaultdict(list),
            "internal_deps": defaultdict(set),
            "external_deps": defaultdict(set),
            "coupling_metrics": {}
        }
        
        # Import patterns for different languages
        import_patterns = {
            "python": [
                r"from\s+([\w\.]+)\s+import",
                r"import\s+([\w\.]+)"
            ],
            "javascript": [
                r"import\s+.*\s+from\s+['\"]([^'\"]+)['\"]",
                r"require\(['\"]([^'\"]+)['\"]\)"
            ],
            "java": [
                r"import\s+([\w\.]+);"
            ]
        }
        
        code_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        
        for file_path in code_files[:50]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            file_ext = file_path.suffix
            
            # Determine language and patterns
            if file_ext == '.py':
                patterns = import_patterns["python"]
            elif file_ext in ['.js', '.ts']:
                patterns = import_patterns["javascript"]
            elif file_ext == '.java':
                patterns = import_patterns["java"]
            else:
                continue
            
            # Find imports
            for pattern in patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    dependencies["imports"][relative_path].append(match)
                    
                    # Classify as internal or external
                    if match.startswith('.') or any(part in match for part in ['src', 'lib', 'app']):
                        dependencies["internal_deps"][relative_path].add(match)
                    else:
                        dependencies["external_deps"][relative_path].add(match)
        
        # Calculate coupling metrics
        for file_path, imports in dependencies["imports"].items():
            internal_count = len(dependencies["internal_deps"][file_path])
            external_count = len(dependencies["external_deps"][file_path])
            total_count = len(imports)
            
            dependencies["coupling_metrics"][file_path] = {
                "total_dependencies": total_count,
                "internal_dependencies": internal_count,
                "external_dependencies": external_count,
                "coupling_ratio": internal_count / max(1, total_count)
            }
        
        return dependencies
    
    def _analyze_config_patterns(self) -> Dict[str, Any]:
        """Analyze configuration patterns for extensibility"""
        
        config_patterns = {
            "environment_vars": [],
            "config_files": [],
            "feature_flags": [],
            "plugin_configs": [],
            "extensibility_configs": []
        }
        
        # Look for configuration files
        config_files = []
        config_files.extend(self.find_files_by_pattern("**/*.json"))
        config_files.extend(self.find_files_by_pattern("**/*.yaml"))
        config_files.extend(self.find_files_by_pattern("**/*.yml"))
        config_files.extend(self.find_files_by_pattern("**/config.py"))
        config_files.extend(self.find_files_by_pattern("**/settings.py"))
        config_files.extend(self.find_files_by_pattern("**/.env*"))
        
        for file_path in config_files:
            if any(skip in str(file_path) for skip in ['node_modules', '.git', '__pycache__']):
                continue
            
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Look for feature flags
            feature_flag_patterns = [
                r"(feature_flag|flag|toggle|switch).*=.*true|false",
                r"if.*flag.*enabled",
                r"@feature_flag"
            ]
            
            for pattern in feature_flag_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    config_patterns["feature_flags"].extend([{
                        "file": relative_path,
                        "flags": matches
                    }])
            
            # Look for plugin configurations
            plugin_patterns = [
                r"plugin.*config",
                r"extension.*config",
                r"addon.*config"
            ]
            
            for pattern in plugin_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    config_patterns["plugin_configs"].extend([{
                        "file": relative_path,
                        "configs": matches
                    }])
        
        return config_patterns
    
    def _calculate_extensibility_score(self, pattern_type: str, context: str) -> int:
        """Calculate extensibility score for a pattern"""
        
        base_scores = {
            "abstract_classes": 10,
            "interfaces": 9,
            "factory_methods": 8,
            "plugin_systems": 10,
            "hooks": 8,
            "strategy_pattern": 9,
            "observer_pattern": 7,
            "template_methods": 6,
            "decorators": 5,
            "base_classes": 7
        }
        
        score = base_scores.get(pattern_type, 5)
        
        # Boost score based on context indicators
        extensibility_indicators = [
            "abstract", "interface", "plugin", "extension", "hook",
            "callback", "strategy", "factory", "builder", "template"
        ]
        
        for indicator in extensibility_indicators:
            if indicator.lower() in context.lower():
                score += 1
        
        return min(score, 15)  # Cap at 15
    
    def _generate_recommendations(self, code_structure: Dict, extension_points: List[Dict], 
                                architectural_patterns: Dict) -> List[Dict]:
        """Generate AI-powered recommendations for feature placement"""
        
        recommendations = []
        
        # Analyze dominant architectural pattern
        dominant_pattern = max(architectural_patterns.items(), key=lambda x: x[1]["score"])
        
        # Generate recommendations based on extension points
        for ext_point in extension_points[:5]:  # Top 5 extension points
            recommendations.append({
                "type": "Extension Point",
                "title": f"Extend {ext_point['name']} ({ext_point['type']})",
                "description": f"This {ext_point['type']} in {ext_point['file']} provides a good extension point for new functionality",
                "file": ext_point["file"],
                "line": ext_point["line"],
                "confidence": ext_point["extensibility_score"] / 15.0,
                "category": "Architecture"
            })
        
        # Generate recommendations based on architectural patterns
        if dominant_pattern[1]["score"] > 0:
            pattern_name = dominant_pattern[0]
            recommendations.append({
                "type": "Architectural Pattern",
                "title": f"Follow {pattern_name.upper()} Pattern",
                "description": f"Your codebase follows the {pattern_name} pattern. New features should align with this architecture.",
                "confidence": min(dominant_pattern[1]["score"] / 10.0, 1.0),
                "category": "Architecture"
            })
        
        # Generate recommendations based on directory structure
        main_dirs = sorted(code_structure["directories"].items(), key=lambda x: x[1], reverse=True)[:3]
        for dir_name, file_count in main_dirs:
            if file_count > 5:  # Only recommend directories with substantial content
                recommendations.append({
                    "type": "Directory Structure",
                    "title": f"Add to {dir_name} directory",
                    "description": f"The {dir_name} directory contains {file_count} files and appears to be a main module",
                    "confidence": min(file_count / 20.0, 1.0),
                    "category": "Organization"
                })
        
        return recommendations
    
    def _extract_context(self, content: str, start: int, end: int, context_lines: int = 3) -> str:
        """Extract context around a match"""
        lines = content.split('\n')
        match_line = content[:start].count('\n')
        
        start_line = max(0, match_line - context_lines)
        end_line = min(len(lines), match_line + context_lines + 1)
        
        context_lines_list = lines[start_line:end_line]
        return '\n'.join(context_lines_list)
    
    def render(self):
        """Render the AI integration analysis"""
        st.header("🤖 AI Integration Analysis for New Features")
        st.markdown("AI-powered insights on where and how to add new functionality")
        
        # Add rerun button
        self.add_rerun_button("ai_context")
        
        with self.display_loading_message("Analyzing codebase context..."):
            analysis = self.analyze()
        
        if "error" in analysis:
            self.display_error(analysis["error"])
            return
        
        # Code Structure Overview
        st.subheader("📁 Code Structure Analysis")
        
        code_structure = analysis["code_structure"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Directory distribution
            if code_structure["directories"]:
                dir_df = pd.DataFrame([
                    {"Directory": k, "Files": v}
                    for k, v in sorted(code_structure["directories"].items(), 
                                     key=lambda x: x[1], reverse=True)[:10]
                ])
                
                fig_dirs = px.bar(
                    dir_df, x="Files", y="Directory",
                    title="Files per Directory",
                    orientation='h'
                )
                st.plotly_chart(fig_dirs, use_container_width=True)
        
        with col2:
            # File type distribution
            if code_structure["file_types"]:
                file_types = dict(code_structure["file_types"])
                fig_types = px.pie(
                    values=list(file_types.values()),
                    names=list(file_types.keys()),
                    title="File Types Distribution"
                )
                st.plotly_chart(fig_types, use_container_width=True)
        
        # Extension Points
        st.subheader("🔌 Extension Points")
        
        extension_points = analysis["extension_points"]
        if extension_points:
            ext_df = pd.DataFrame([
                {
                    "Type": ep["type"],
                    "Name": ep["name"],
                    "File": ep["file"],
                    "Line": ep["line"],
                    "Extensibility Score": ep["extensibility_score"]
                }
                for ep in extension_points[:15]
            ])
            
            st.dataframe(ext_df, use_container_width=True)
            
            # Extension points by type
            type_counts = Counter(ep["type"] for ep in extension_points)
            if type_counts:
                fig_ext_types = px.bar(
                    x=list(type_counts.keys()),
                    y=list(type_counts.values()),
                    title="Extension Points by Type"
                )
                st.plotly_chart(fig_ext_types, use_container_width=True)
        else:
            st.info("No extension points found")
        
        # Architectural Patterns
        st.subheader("🏗️ Architectural Patterns")
        
        arch_patterns = analysis["architectural_patterns"]
        pattern_scores = {k: v["score"] for k, v in arch_patterns.items() if v["score"] > 0}
        
        if pattern_scores:
            fig_patterns = px.bar(
                x=list(pattern_scores.keys()),
                y=list(pattern_scores.values()),
                title="Architectural Pattern Indicators"
            )
            st.plotly_chart(fig_patterns, use_container_width=True)
            
            # Show dominant pattern details
            dominant = max(pattern_scores.items(), key=lambda x: x[1])
            st.info(f"**Dominant Pattern:** {dominant[0].upper()} (Score: {dominant[1]})")
        else:
            st.info("No clear architectural patterns detected")
        
        # Similar Implementations
        st.subheader("📋 Similar Implementation Templates")
        
        similar_impls = analysis["similar_implementations"]
        if similar_impls:
            impl_df = pd.DataFrame([
                {
                    "File": impl["file"],
                    "Dominant Pattern": impl["dominant_pattern"],
                    "Complexity Score": impl["complexity_score"],
                    "Lines of Code": impl["lines_of_code"]
                }
                for impl in similar_impls[:10]
            ])
            
            st.dataframe(impl_df, use_container_width=True)
        else:
            st.info("No similar implementations found")
        
        # Module Dependencies
        st.subheader("🔗 Module Dependencies")
        
        dependencies = analysis["module_dependencies"]
        if dependencies["coupling_metrics"]:
            # Show high coupling files
            high_coupling = sorted(
                dependencies["coupling_metrics"].items(),
                key=lambda x: x[1]["total_dependencies"],
                reverse=True
            )[:10]
            
            coupling_df = pd.DataFrame([
                {
                    "File": file_path,
                    "Total Dependencies": metrics["total_dependencies"],
                    "Internal": metrics["internal_dependencies"],
                    "External": metrics["external_dependencies"],
                    "Coupling Ratio": f"{metrics['coupling_ratio']:.2f}"
                }
                for file_path, metrics in high_coupling
            ])
            
            st.dataframe(coupling_df, use_container_width=True)
        else:
            st.info("No dependency information found")
        
        # AI Recommendations
        st.subheader("💡 AI Recommendations")
        
        recommendations = analysis["recommendations"]
        if recommendations:
            for rec in recommendations:
                confidence_color = "green" if rec["confidence"] > 0.7 else "orange" if rec["confidence"] > 0.4 else "red"
                
                st.markdown(f"""
                **{rec['title']}** 
                <span style="color: {confidence_color}">●</span> Confidence: {rec['confidence']:.1%}
                
                {rec['description']}
                
                *Category: {rec['category']}*
                """, unsafe_allow_html=True)
                
                if 'file' in rec:
                    st.code(f"File: {rec['file']}" + (f", Line: {rec['line']}" if 'line' in rec else ""))
                
                st.markdown("---")
        else:
            st.info("No specific recommendations generated")
        
        # AI-powered feature placement suggestions
        st.subheader("🎯 AI Feature Placement Assistant")
        
        feature_description = st.text_area(
            "Describe the new feature you want to add:",
            placeholder="e.g., Add user authentication, Implement caching layer, Create API endpoint for orders"
        )
        
        if st.button("Get AI Placement Suggestions") and feature_description:
            with self.display_loading_message("Analyzing feature placement..."):
                # Prepare context for AI
                context_summary = {
                    "architectural_patterns": pattern_scores,
                    "extension_points": [ep["type"] for ep in extension_points[:5]],
                    "directory_structure": list(code_structure["directories"].keys())[:10],
                    "similar_implementations": [impl["dominant_pattern"] for impl in similar_impls[:5]]
                }
                
                prompt = f"""
                Based on this codebase analysis:
                
                Architecture: {context_summary}
                
                Feature to implement: {feature_description}
                
                Please provide specific recommendations for:
                1. Which directory/module to place the new feature
                2. Which existing patterns or extension points to leverage
                3. What files might need modification
                4. Potential integration challenges
                5. Best practices to follow based on the existing codebase
                """
                
                suggestions = self.ai_client.query(prompt)
                
                if suggestions:
                    st.markdown("**AI-Generated Placement Suggestions:**")
                    st.markdown(suggestions)
                else:
                    st.error("Failed to generate placement suggestions")
        
        # Add save options
        self.add_save_options("ai_context", analysis)
