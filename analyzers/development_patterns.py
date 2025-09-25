"""
Development Patterns Analyzer
Analyzes framework usage patterns and development practices in the codebase
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

class DevelopmentPatternsAnalyzer(BaseAnalyzer):
    """Analyzes development patterns and framework usage in the codebase"""
    
    def analyze(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Analyze development patterns and framework usage"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("development_patterns")
        if cached_result:
            return cached_result
        
        # Analyze framework usage
        framework_usage = self._analyze_framework_usage()
        
        # Analyze coding patterns
        coding_patterns = self._analyze_coding_patterns()
        
        # Analyze design patterns
        design_patterns = self._analyze_design_patterns()
        
        # Analyze project structure patterns
        structure_patterns = self._analyze_structure_patterns()
        
        # Analyze configuration patterns
        config_patterns = self._analyze_config_patterns()
        
        # Analyze testing patterns
        testing_patterns = self._analyze_testing_patterns()
        
        # Analyze documentation patterns
        documentation_patterns = self._analyze_documentation_patterns()
        
        result = {
            "framework_usage": framework_usage,
            "coding_patterns": coding_patterns,
            "design_patterns": design_patterns,
            "structure_patterns": structure_patterns,
            "config_patterns": config_patterns,
            "testing_patterns": testing_patterns,
            "documentation_patterns": documentation_patterns,
            "pattern_summary": self._generate_pattern_summary(
                framework_usage, coding_patterns, design_patterns
            )
        }
        
        # Cache the result
        self.cache_analysis("development_patterns", result)
        
        return result
    
    def _analyze_framework_usage(self) -> Dict[str, Any]:
        """Analyze framework and library usage patterns"""
        
        frameworks = {
            "web_frameworks": defaultdict(int),
            "testing_frameworks": defaultdict(int),
            "database_frameworks": defaultdict(int),
            "ui_frameworks": defaultdict(int),
            "build_tools": defaultdict(int),
            "language_specific": defaultdict(int)
        }
        
        # Framework patterns by language
        framework_patterns = {
            "python": {
                "web_frameworks": [
                    (r"from django", "Django"),
                    (r"from flask", "Flask"),
                    (r"from fastapi", "FastAPI"),
                    (r"import tornado", "Tornado"),
                    (r"from pyramid", "Pyramid")
                ],
                "testing_frameworks": [
                    (r"import pytest", "pytest"),
                    (r"import unittest", "unittest"),
                    (r"from nose", "nose"),
                    (r"import mock", "mock")
                ],
                "database_frameworks": [
                    (r"from sqlalchemy", "SQLAlchemy"),
                    (r"import sqlite3", "SQLite"),
                    (r"import psycopg2", "PostgreSQL"),
                    (r"from django.db", "Django ORM"),
                    (r"import pymongo", "MongoDB")
                ]
            },
            "javascript": {
                "web_frameworks": [
                    (r"from ['\"]react['\"]", "React"),
                    (r"from ['\"]vue['\"]", "Vue.js"),
                    (r"from ['\"]angular", "Angular"),
                    (r"from ['\"]express['\"]", "Express.js"),
                    (r"from ['\"]next", "Next.js")
                ],
                "ui_frameworks": [
                    (r"from ['\"]@mui", "Material-UI"),
                    (r"from ['\"]antd", "Ant Design"),
                    (r"from ['\"]bootstrap", "Bootstrap"),
                    (r"from ['\"]tailwindcss", "Tailwind CSS")
                ],
                "testing_frameworks": [
                    (r"from ['\"]jest", "Jest"),
                    (r"from ['\"]mocha", "Mocha"),
                    (r"from ['\"]cypress", "Cypress"),
                    (r"from ['\"]@testing-library", "Testing Library")
                ]
            },
            "java": {
                "web_frameworks": [
                    (r"import.*springframework", "Spring Framework"),
                    (r"import.*struts", "Apache Struts"),
                    (r"import.*jersey", "Jersey"),
                    (r"import.*hibernate", "Hibernate")
                ],
                "testing_frameworks": [
                    (r"import.*junit", "JUnit"),
                    (r"import.*testng", "TestNG"),
                    (r"import.*mockito", "Mockito")
                ]
            }
        }
        
        # Analyze source files
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java', '.jsx', '.tsx'])
        
        for file_path in source_files[:100]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            file_ext = file_path.suffix
            
            # Determine language
            if file_ext == '.py':
                lang_patterns = framework_patterns.get("python", {})
            elif file_ext in ['.js', '.ts', '.jsx', '.tsx']:
                lang_patterns = framework_patterns.get("javascript", {})
            elif file_ext == '.java':
                lang_patterns = framework_patterns.get("java", {})
            else:
                continue
            
            # Check for framework patterns
            for category, patterns in lang_patterns.items():
                for pattern, framework_name in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        frameworks[category][framework_name] += 1
        
        # Analyze package files for additional framework detection
        self._analyze_package_files(frameworks)
        
        return frameworks
    
    def _analyze_package_files(self, frameworks: Dict):
        """Analyze package files for framework dependencies"""
        
        # Python requirements
        req_files = self.find_files_by_pattern("**/requirements*.txt")
        for req_file in req_files:
            content = self.read_file_content(req_file)
            if content:
                self._parse_python_requirements(content, frameworks)
        
        # Node.js package.json
        package_files = self.find_files_by_pattern("**/package.json")
        for package_file in package_files:
            content = self.read_file_content(package_file)
            if content:
                self._parse_package_json(content, frameworks)
        
        # Java pom.xml
        pom_files = self.find_files_by_pattern("**/pom.xml")
        for pom_file in pom_files:
            content = self.read_file_content(pom_file)
            if content:
                self._parse_maven_pom(content, frameworks)
    
    def _parse_python_requirements(self, content: str, frameworks: Dict):
        """Parse Python requirements file"""
        
        framework_mapping = {
            "django": "Django",
            "flask": "Flask",
            "fastapi": "FastAPI",
            "tornado": "Tornado",
            "pytest": "pytest",
            "sqlalchemy": "SQLAlchemy",
            "requests": "Requests",
            "numpy": "NumPy",
            "pandas": "Pandas",
            "scikit-learn": "Scikit-learn"
        }
        
        for line in content.split('\n'):
            line = line.strip().lower()
            if line and not line.startswith('#'):
                package_name = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                if package_name in framework_mapping:
                    framework_name = framework_mapping[package_name]
                    if 'test' in package_name:
                        frameworks["testing_frameworks"][framework_name] += 1
                    elif package_name in ['django', 'flask', 'fastapi', 'tornado']:
                        frameworks["web_frameworks"][framework_name] += 1
                    elif package_name in ['sqlalchemy']:
                        frameworks["database_frameworks"][framework_name] += 1
                    else:
                        frameworks["language_specific"][framework_name] += 1
    
    def _parse_package_json(self, content: str, frameworks: Dict):
        """Parse Node.js package.json"""
        
        try:
            import json
            package_data = json.loads(content)
            
            dependencies = package_data.get("dependencies", {})
            dev_dependencies = package_data.get("devDependencies", {})
            
            framework_mapping = {
                "react": ("web_frameworks", "React"),
                "vue": ("web_frameworks", "Vue.js"),
                "angular": ("web_frameworks", "Angular"),
                "express": ("web_frameworks", "Express.js"),
                "next": ("web_frameworks", "Next.js"),
                "jest": ("testing_frameworks", "Jest"),
                "mocha": ("testing_frameworks", "Mocha"),
                "cypress": ("testing_frameworks", "Cypress"),
                "@mui/material": ("ui_frameworks", "Material-UI"),
                "antd": ("ui_frameworks", "Ant Design"),
                "bootstrap": ("ui_frameworks", "Bootstrap"),
                "webpack": ("build_tools", "Webpack"),
                "vite": ("build_tools", "Vite"),
                "rollup": ("build_tools", "Rollup")
            }
            
            all_deps = {**dependencies, **dev_dependencies}
            
            for dep_name in all_deps.keys():
                for pattern, (category, framework_name) in framework_mapping.items():
                    if pattern in dep_name.lower():
                        frameworks[category][framework_name] += 1
                        break
        
        except json.JSONDecodeError:
            pass
    
    def _parse_maven_pom(self, content: str, frameworks: Dict):
        """Parse Maven pom.xml"""
        
        framework_patterns = [
            (r"<groupId>org\.springframework</groupId>", "web_frameworks", "Spring Framework"),
            (r"<groupId>junit</groupId>", "testing_frameworks", "JUnit"),
            (r"<groupId>org\.hibernate</groupId>", "database_frameworks", "Hibernate"),
            (r"<groupId>org\.apache\.struts</groupId>", "web_frameworks", "Apache Struts")
        ]
        
        for pattern, category, framework_name in framework_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                frameworks[category][framework_name] += 1
    
    def _analyze_coding_patterns(self) -> Dict[str, Any]:
        """Analyze coding patterns and conventions"""
        
        patterns = {
            "naming_conventions": defaultdict(int),
            "code_organization": defaultdict(int),
            "error_handling_patterns": defaultdict(int),
            "async_patterns": defaultdict(int),
            "functional_patterns": defaultdict(int)
        }
        
        # Coding pattern definitions
        coding_pattern_rules = {
            "naming_conventions": [
                (r"\bclass [A-Z][a-zA-Z]*:", "PascalCase Classes"),
                (r"\bdef [a-z][a-z_]*\(", "snake_case Functions"),
                (r"\bconst [A-Z_]+\s*=", "UPPER_CASE Constants"),
                (r"\blet [a-z][a-zA-Z]*\s*=", "camelCase Variables")
            ],
            "code_organization": [
                (r"from \.\w+ import", "Relative Imports"),
                (r"import \w+\.\w+", "Absolute Imports"),
                (r"class \w+\([A-Z]\w*\):", "Inheritance Usage"),
                (r"@\w+", "Decorator Usage")
            ],
            "error_handling_patterns": [
                (r"try:\s*\n.*except.*:", "Try-Except Blocks"),
                (r"\.catch\(", "Promise Catch"),
                (r"throw new \w*Error", "Custom Exceptions"),
                (r"assert \w+", "Assertions")
            ],
            "async_patterns": [
                (r"async def", "Async Functions"),
                (r"await \w+", "Await Usage"),
                (r"\.then\(", "Promise Chains"),
                (r"Observable\.", "Observable Pattern")
            ],
            "functional_patterns": [
                (r"\.map\(", "Map Operations"),
                (r"\.filter\(", "Filter Operations"),
                (r"\.reduce\(", "Reduce Operations"),
                (r"lambda \w+:", "Lambda Functions")
            ]
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        
        for file_path in source_files[:50]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            # Check for coding patterns
            for category, pattern_rules in coding_pattern_rules.items():
                for pattern, pattern_name in pattern_rules:
                    matches = re.findall(pattern, content, re.MULTILINE)
                    if matches:
                        patterns[category][pattern_name] += len(matches)
        
        return patterns
    
    def _analyze_design_patterns(self) -> Dict[str, Any]:
        """Analyze design patterns usage"""
        
        design_patterns = {
            "creational": defaultdict(int),
            "structural": defaultdict(int),
            "behavioral": defaultdict(int)
        }
        
        # Design pattern indicators
        pattern_indicators = {
            "creational": [
                (r"class \w*Factory", "Factory Pattern"),
                (r"class \w*Builder", "Builder Pattern"),
                (r"class \w*Singleton", "Singleton Pattern"),
                (r"def create_\w+", "Factory Method"),
                (r"@staticmethod.*create", "Static Factory")
            ],
            "structural": [
                (r"class \w*Adapter", "Adapter Pattern"),
                (r"class \w*Decorator", "Decorator Pattern"),
                (r"class \w*Facade", "Facade Pattern"),
                (r"class \w*Proxy", "Proxy Pattern"),
                (r"def __getattr__", "Proxy/Adapter")
            ],
            "behavioral": [
                (r"class \w*Observer", "Observer Pattern"),
                (r"class \w*Strategy", "Strategy Pattern"),
                (r"class \w*Command", "Command Pattern"),
                (r"class \w*State", "State Pattern"),
                (r"def notify\w*", "Observer Method")
            ]
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        
        for file_path in source_files[:50]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            # Check for design patterns
            for category, patterns in pattern_indicators.items():
                for pattern, pattern_name in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        design_patterns[category][pattern_name] += len(matches)
        
        return design_patterns
    
    def _analyze_structure_patterns(self) -> Dict[str, Any]:
        """Analyze project structure patterns"""
        
        structure = {
            "directory_patterns": defaultdict(int),
            "file_organization": defaultdict(int),
            "architecture_patterns": defaultdict(int)
        }
        
        # Analyze directory structure
        all_dirs = set()
        for file_path in self.get_file_list():
            all_dirs.add(file_path.parent)
        
        # Common directory patterns
        dir_patterns = [
            ("src", "Source Directory"),
            ("lib", "Library Directory"),
            ("tests", "Test Directory"),
            ("docs", "Documentation Directory"),
            ("config", "Configuration Directory"),
            ("utils", "Utilities Directory"),
            ("models", "Models Directory"),
            ("views", "Views Directory"),
            ("controllers", "Controllers Directory"),
            ("services", "Services Directory"),
            ("components", "Components Directory"),
            ("assets", "Assets Directory")
        ]
        
        for dir_path in all_dirs:
            dir_name = dir_path.name.lower()
            for pattern, pattern_name in dir_patterns:
                if pattern in dir_name:
                    structure["directory_patterns"][pattern_name] += 1
        
        # Analyze file organization patterns
        file_extensions = defaultdict(int)
        for file_path in self.get_file_list():
            file_extensions[file_path.suffix] += 1
        
        structure["file_organization"] = dict(file_extensions)
        
        # Architecture patterns based on directory structure
        if any("mvc" in str(d).lower() for d in all_dirs):
            structure["architecture_patterns"]["MVC Pattern"] += 1
        if any("mvp" in str(d).lower() for d in all_dirs):
            structure["architecture_patterns"]["MVP Pattern"] += 1
        if any("component" in str(d).lower() for d in all_dirs):
            structure["architecture_patterns"]["Component-Based"] += 1
        
        return structure
    
    def _analyze_config_patterns(self) -> Dict[str, Any]:
        """Analyze configuration patterns"""
        
        config = {
            "config_files": [],
            "config_formats": defaultdict(int),
            "environment_patterns": defaultdict(int)
        }
        
        # Find configuration files
        config_patterns = [
            "**/*.json", "**/*.yaml", "**/*.yml", "**/*.toml",
            "**/*.ini", "**/*.cfg", "**/*.conf", "**/config.*",
            "**/.env*", "**/settings.*"
        ]
        
        config_files = []
        for pattern in config_patterns:
            config_files.extend(self.find_files_by_pattern(pattern))
        
        # Remove duplicates and analyze
        config_files = list(set(config_files))
        
        for config_file in config_files:
            relative_path = str(config_file.relative_to(self.repo_path))
            config["config_files"].append(relative_path)
            
            # Determine format
            if config_file.suffix in ['.json']:
                config["config_formats"]["JSON"] += 1
            elif config_file.suffix in ['.yaml', '.yml']:
                config["config_formats"]["YAML"] += 1
            elif config_file.suffix in ['.toml']:
                config["config_formats"]["TOML"] += 1
            elif config_file.suffix in ['.ini', '.cfg']:
                config["config_formats"]["INI"] += 1
            elif '.env' in config_file.name:
                config["environment_patterns"]["Environment Files"] += 1
            elif 'settings' in config_file.name.lower():
                config["environment_patterns"]["Settings Files"] += 1
        
        return config
    
    def _analyze_testing_patterns(self) -> Dict[str, Any]:
        """Analyze testing patterns and practices"""
        
        testing = {
            "test_file_patterns": defaultdict(int),
            "test_types": defaultdict(int),
            "assertion_patterns": defaultdict(int),
            "mock_patterns": defaultdict(int)
        }
        
        # Find test files
        test_patterns = [
            "**/test_*.py", "**/*_test.py", "**/tests.py",
            "**/*.test.js", "**/*.spec.js", "**/*.test.ts", "**/*.spec.ts",
            "**/Test*.java", "**/*Test.java", "**/*Tests.java"
        ]
        
        test_files = []
        for pattern in test_patterns:
            test_files.extend(self.find_files_by_pattern(pattern))
        
        test_files = list(set(test_files))
        
        for test_file in test_files:
            content = self.read_file_content(test_file)
            if not content:
                continue
            
            # Analyze test patterns
            file_name = test_file.name.lower()
            
            if 'unit' in file_name:
                testing["test_types"]["Unit Tests"] += 1
            elif 'integration' in file_name:
                testing["test_types"]["Integration Tests"] += 1
            elif 'e2e' in file_name or 'end2end' in file_name:
                testing["test_types"]["E2E Tests"] += 1
            else:
                testing["test_types"]["General Tests"] += 1
            
            # Test file naming patterns
            if file_name.startswith('test_'):
                testing["test_file_patterns"]["test_*.py"] += 1
            elif file_name.endswith('_test.py'):
                testing["test_file_patterns"]["*_test.py"] += 1
            elif '.test.' in file_name:
                testing["test_file_patterns"]["*.test.js"] += 1
            elif '.spec.' in file_name:
                testing["test_file_patterns"]["*.spec.js"] += 1
            
            # Assertion patterns
            assertion_patterns = [
                (r"assert \w+", "Assert Statements"),
                (r"expect\(.*\)\.to", "Expect Assertions"),
                (r"\.should\.", "Should Assertions"),
                (r"assertEquals\(", "JUnit Assertions")
            ]
            
            for pattern, pattern_name in assertion_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    testing["assertion_patterns"][pattern_name] += len(matches)
            
            # Mock patterns
            mock_patterns = [
                (r"mock\.", "Mock Usage"),
                (r"@patch", "Patch Decorator"),
                (r"jest\.mock", "Jest Mock"),
                (r"sinon\.", "Sinon Mock")
            ]
            
            for pattern, pattern_name in mock_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    testing["mock_patterns"][pattern_name] += len(matches)
        
        return testing
    
    def _analyze_documentation_patterns(self) -> Dict[str, Any]:
        """Analyze documentation patterns"""
        
        documentation = {
            "doc_files": [],
            "doc_formats": defaultdict(int),
            "inline_documentation": defaultdict(int),
            "api_documentation": defaultdict(int)
        }
        
        # Find documentation files
        doc_patterns = [
            "**/README*", "**/CHANGELOG*", "**/LICENSE*",
            "**/*.md", "**/*.rst", "**/*.txt",
            "**/docs/**/*", "**/documentation/**/*"
        ]
        
        doc_files = []
        for pattern in doc_patterns:
            doc_files.extend(self.find_files_by_pattern(pattern))
        
        doc_files = list(set(doc_files))
        
        for doc_file in doc_files:
            relative_path = str(doc_file.relative_to(self.repo_path))
            documentation["doc_files"].append(relative_path)
            
            # Determine format
            if doc_file.suffix == '.md':
                documentation["doc_formats"]["Markdown"] += 1
            elif doc_file.suffix == '.rst':
                documentation["doc_formats"]["reStructuredText"] += 1
            elif doc_file.suffix == '.txt':
                documentation["doc_formats"]["Plain Text"] += 1
            elif 'README' in doc_file.name.upper():
                documentation["doc_formats"]["README"] += 1
        
        # Analyze inline documentation
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        
        for source_file in source_files[:20]:  # Limit for performance
            content = self.read_file_content(source_file)
            if not content:
                continue
            
            # Docstring patterns
            docstring_patterns = [
                (r'""".*?"""', "Python Docstrings"),
                (r"'''.*?'''", "Python Docstrings"),
                (r"/\*\*.*?\*/", "JSDoc Comments"),
                (r"//.*", "Inline Comments")
            ]
            
            for pattern, pattern_name in docstring_patterns:
                matches = re.findall(pattern, content, re.DOTALL)
                if matches:
                    documentation["inline_documentation"][pattern_name] += len(matches)
        
        return documentation
    
    def _generate_pattern_summary(self, framework_usage: Dict, coding_patterns: Dict, 
                                 design_patterns: Dict) -> Dict[str, Any]:
        """Generate summary of development patterns"""
        
        summary = {
            "primary_frameworks": [],
            "dominant_patterns": [],
            "architecture_style": "Unknown",
            "maturity_score": 0
        }
        
        # Identify primary frameworks
        all_frameworks = {}
        for category, frameworks in framework_usage.items():
            for framework, count in frameworks.items():
                all_frameworks[framework] = count
        
        # Sort by usage count
        sorted_frameworks = sorted(all_frameworks.items(), key=lambda x: x[1], reverse=True)
        summary["primary_frameworks"] = [fw[0] for fw in sorted_frameworks[:5]]
        
        # Identify dominant patterns
        all_patterns = {}
        for category, patterns in coding_patterns.items():
            for pattern, count in patterns.items():
                all_patterns[pattern] = count
        
        sorted_patterns = sorted(all_patterns.items(), key=lambda x: x[1], reverse=True)
        summary["dominant_patterns"] = [pat[0] for pat in sorted_patterns[:5]]
        
        # Determine architecture style
        if any("React" in fw for fw in summary["primary_frameworks"]):
            summary["architecture_style"] = "Component-Based (React)"
        elif any("Django" in fw for fw in summary["primary_frameworks"]):
            summary["architecture_style"] = "MVC (Django)"
        elif any("Spring" in fw for fw in summary["primary_frameworks"]):
            summary["architecture_style"] = "Enterprise (Spring)"
        
        # Calculate maturity score
        maturity_factors = []
        
        # Framework diversity
        framework_count = len(summary["primary_frameworks"])
        maturity_factors.append(min(framework_count * 10, 30))
        
        # Design pattern usage
        design_pattern_count = sum(sum(patterns.values()) for patterns in design_patterns.values())
        maturity_factors.append(min(design_pattern_count * 5, 25))
        
        # Coding pattern consistency
        pattern_count = len(summary["dominant_patterns"])
        maturity_factors.append(min(pattern_count * 8, 25))
        
        # Testing framework presence
        testing_frameworks = framework_usage.get("testing_frameworks", {})
        if testing_frameworks:
            maturity_factors.append(20)
        
        summary["maturity_score"] = sum(maturity_factors)
        
        return summary
    
    def render(self):
        """Render the development patterns analysis"""
        st.header("🔧 Development Patterns & Framework Usage")
        st.markdown("Analyzing development practices and framework usage patterns")
        
        # Add rerun button
        self.add_rerun_button("development_patterns")
        
        with self.display_loading_message("Analyzing development patterns..."):
            analysis = self.analyze()
        
        if "error" in analysis:
            self.display_error(analysis["error"])
            return
        
        # Pattern Summary
        st.subheader("📊 Pattern Summary")
        
        pattern_summary = analysis["pattern_summary"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Maturity Score", f"{pattern_summary['maturity_score']}/100")
        
        with col2:
            st.metric("Primary Frameworks", len(pattern_summary["primary_frameworks"]))
        
        with col3:
            st.metric("Architecture Style", pattern_summary["architecture_style"])
        
        with col4:
            st.metric("Pattern Diversity", len(pattern_summary["dominant_patterns"]))
        
        # Framework Usage Analysis
        st.subheader("🚀 Framework Usage")
        
        framework_usage = analysis["framework_usage"]
        
        # Create tabs for different framework categories
        framework_tabs = st.tabs(["Web Frameworks", "Testing Frameworks", "Database", "UI Frameworks", "Build Tools"])
        
        categories = ["web_frameworks", "testing_frameworks", "database_frameworks", "ui_frameworks", "build_tools"]
        
        for i, (tab, category) in enumerate(zip(framework_tabs, categories)):
            with tab:
                frameworks = dict(framework_usage[category])
                if frameworks:
                    fig = px.bar(
                        x=list(frameworks.values()),
                        y=list(frameworks.keys()),
                        orientation='h',
                        title=f"{category.replace('_', ' ').title()} Usage"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(f"No {category.replace('_', ' ')} detected")
        
        # Coding Patterns Analysis
        st.subheader("💻 Coding Patterns")
        
        coding_patterns = analysis["coding_patterns"]
        
        pattern_tabs = st.tabs(["Naming Conventions", "Code Organization", "Error Handling", "Async Patterns", "Functional Patterns"])
        pattern_categories = ["naming_conventions", "code_organization", "error_handling_patterns", "async_patterns", "functional_patterns"]
        
        for tab, category in zip(pattern_tabs, pattern_categories):
            with tab:
                patterns = dict(coding_patterns[category])
                if patterns:
                    fig = px.pie(
                        values=list(patterns.values()),
                        names=list(patterns.keys()),
                        title=f"{category.replace('_', ' ').title()}"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(f"No {category.replace('_', ' ')} patterns detected")
        
        # Design Patterns Analysis
        st.subheader("🏗️ Design Patterns")
        
        design_patterns = analysis["design_patterns"]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Creational Patterns**")
            creational = dict(design_patterns["creational"])
            if creational:
                for pattern, count in creational.items():
                    st.write(f"• {pattern}: {count}")
            else:
                st.info("No creational patterns detected")
        
        with col2:
            st.write("**Structural Patterns**")
            structural = dict(design_patterns["structural"])
            if structural:
                for pattern, count in structural.items():
                    st.write(f"• {pattern}: {count}")
            else:
                st.info("No structural patterns detected")
        
        with col3:
            st.write("**Behavioral Patterns**")
            behavioral = dict(design_patterns["behavioral"])
            if behavioral:
                for pattern, count in behavioral.items():
                    st.write(f"• {pattern}: {count}")
            else:
                st.info("No behavioral patterns detected")
        
        # Project Structure Analysis
        st.subheader("📁 Project Structure")
        
        structure_patterns = analysis["structure_patterns"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Directory Patterns**")
            dir_patterns = dict(structure_patterns["directory_patterns"])
            if dir_patterns:
                fig = px.bar(
                    x=list(dir_patterns.values()),
                    y=list(dir_patterns.keys()),
                    orientation='h',
                    title="Directory Structure Patterns"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No common directory patterns detected")
        
        with col2:
            st.write("**File Organization**")
            file_org = dict(structure_patterns["file_organization"])
            if file_org:
                # Show top file extensions
                sorted_extensions = sorted(file_org.items(), key=lambda x: x[1], reverse=True)[:10]
                fig = px.pie(
                    values=[count for ext, count in sorted_extensions],
                    names=[ext if ext else "No Extension" for ext, count in sorted_extensions],
                    title="File Types Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Configuration Patterns
        st.subheader("⚙️ Configuration Patterns")
        
        config_patterns = analysis["config_patterns"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Configuration Formats**")
            config_formats = dict(config_patterns["config_formats"])
            if config_formats:
                fig = px.pie(
                    values=list(config_formats.values()),
                    names=list(config_formats.keys()),
                    title="Configuration File Formats"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No configuration files detected")
        
        with col2:
            st.write("**Environment Patterns**")
            env_patterns = dict(config_patterns["environment_patterns"])
            if env_patterns:
                for pattern, count in env_patterns.items():
                    st.write(f"• {pattern}: {count}")
            else:
                st.info("No environment patterns detected")
        
        # Testing Patterns
        st.subheader("🧪 Testing Patterns")
        
        testing_patterns = analysis["testing_patterns"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Test Types**")
            test_types = dict(testing_patterns["test_types"])
            if test_types:
                fig = px.pie(
                    values=list(test_types.values()),
                    names=list(test_types.keys()),
                    title="Test Types Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Assertion Patterns**")
            assertion_patterns = dict(testing_patterns["assertion_patterns"])
            if assertion_patterns:
                fig = px.bar(
                    x=list(assertion_patterns.values()),
                    y=list(assertion_patterns.keys()),
                    orientation='h',
                    title="Assertion Patterns Usage"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Documentation Patterns
        st.subheader("📚 Documentation Patterns")
        
        documentation_patterns = analysis["documentation_patterns"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Documentation Formats**")
            doc_formats = dict(documentation_patterns["doc_formats"])
            if doc_formats:
                fig = px.pie(
                    values=list(doc_formats.values()),
                    names=list(doc_formats.keys()),
                    title="Documentation Formats"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Inline Documentation**")
            inline_docs = dict(documentation_patterns["inline_documentation"])
            if inline_docs:
                fig = px.bar(
                    x=list(inline_docs.values()),
                    y=list(inline_docs.keys()),
                    orientation='h',
                    title="Inline Documentation Types"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # AI-powered Pattern Analysis
        st.subheader("🤖 AI Pattern Analysis")
        
        if st.button("Get AI Pattern Insights"):
            with self.display_loading_message("Generating AI pattern analysis..."):
                # Prepare context for AI
                pattern_context = {
                    "primary_frameworks": pattern_summary["primary_frameworks"],
                    "architecture_style": pattern_summary["architecture_style"],
                    "maturity_score": pattern_summary["maturity_score"],
                    "dominant_patterns": pattern_summary["dominant_patterns"]
                }
                
                prompt = f"""
                Based on this development pattern analysis:
                
                Pattern Summary: {pattern_context}
                
                Please provide:
                1. Assessment of the current development practices
                2. Recommendations for pattern improvements
                3. Framework optimization suggestions
                4. Architecture enhancement opportunities
                5. Best practices alignment analysis
                """
                
                ai_insights = self.ai_client.query(prompt)
                
                if ai_insights:
                    st.markdown("**AI Pattern Insights:**")
                    st.markdown(ai_insights)
                else:
                    st.error("Failed to generate AI pattern insights")
        
        # Display AI insights from parallel analysis if available
        self.display_parallel_ai_insights("development_patterns")
        
        # Add save options
        self.add_save_options("development_patterns", analysis)
