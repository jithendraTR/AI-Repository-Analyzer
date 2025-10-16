"""
Risk Analysis Analyzer
Identifies test coverage gaps and potential risk areas in the codebase
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
from .expertise_mapping import ExpertiseMapper

class RiskAnalysisAnalyzer(BaseAnalyzer):
    """Analyzes codebase for risk factors and test coverage gaps"""
    
    # Pre-compiled regex patterns for maximum performance
    _PATTERNS = {
        'python_test': re.compile(r'(import pytest|@pytest|def test_|import unittest|class.*TestCase)', re.IGNORECASE),
        'js_test': re.compile(r'(describe\(|it\(|test\(|expect\()', re.IGNORECASE),
        'java_test': re.compile(r'(@Test|@Before|@After|import org.junit)', re.IGNORECASE),
        'complexity': re.compile(r'\b(if|else|elif|for|while|try|catch|except|switch|case)\b|&&|\|\||\?.*:', re.IGNORECASE),
        'functions': re.compile(r'(def \w+\(|function \w+\(|public \w+ \w+\()', re.IGNORECASE),
        'error_handling_py': re.compile(r'(try:\s*\n|except\s+\w*Error|raise\s+\w*Error|finally:)', re.IGNORECASE),
        'error_handling_js': re.compile(r'(try\s*{|catch\s*\(|throw\s+new\s+Error|finally\s*{)', re.IGNORECASE),
        'security_sql': re.compile(r'(execute\([\'"].*%s.*[\'"]|query\([\'"].*\+.*[\'"]|SELECT.*\+.*FROM)', re.IGNORECASE),
        'security_xss': re.compile(r'(innerHTML\s*=.*\+|document\.write\(|eval\()', re.IGNORECASE),
        'security_secrets': re.compile(r'(password\s*=\s*[\'"][^\'\"]+[\'"]|api_key\s*=\s*[\'"][^\'\"]+[\'"]|secret\s*=\s*[\'"][^\'\"]+[\'"])', re.IGNORECASE),
        'deprecated_py': re.compile(r'(import imp\b|\.has_key\(|execfile\()', re.IGNORECASE),
        'deprecated_js': re.compile(r'(var\s+\w+|\.substr\(|escape\()', re.IGNORECASE),
    }
    
    def analyze(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Ultra-fast risk analysis with aggressive optimizations"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("risk_analysis")
        if cached_result:
            return cached_result
        
        try:
            total_steps = 4  # Updated to 4 steps including knowledge risk assessment
            current_step = 0
            
            # Step 1: Ultra-fast test coverage analysis
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing test coverage (ultra-fast)...")
            
            if token:
                token.check_cancellation()
            
            test_coverage = self._ultra_fast_test_coverage(token)
            current_step += 1
            
            # Step 2: Quick complexity analysis
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing code complexity (ultra-fast)...")
            
            if token:
                token.check_cancellation()
            
            complexity_analysis = self._ultra_fast_complexity()
            current_step += 1
            
            # Step 3: Fast security scan (most critical)
            if progress_callback:
                progress_callback(current_step, total_steps, "Scanning for security risks (ultra-fast)...")
            
            if token:
                token.check_cancellation()
            
            security_risks = self._ultra_fast_security_scan(token)
            current_step += 1
            
            # Step 4: Knowledge Risk Assessment
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing knowledge risks and single points of failure...")
            
            if token:
                token.check_cancellation()
            
            knowledge_risks = self._analyze_knowledge_risks(token)
            
            # Add test coverage gaps analysis
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing test coverage gaps...")
            
            if token:
                token.check_cancellation()
            
            test_coverage_gaps = self._analyze_test_coverage_gaps(token)
            
            # Add enhanced code duplication analysis
            if progress_callback:
                progress_callback(current_step, total_steps, "Enhanced code duplication analysis...")
                
            if token:
                token.check_cancellation()
                
            enhanced_duplication = self._analyze_code_duplication_enhanced(token)
            
            # Skip expensive operations for speed - generate quick summary
            result = {
                "test_coverage": test_coverage,
                "untested_code": [],  # Skip for ultra-fast mode
                "complexity_analysis": complexity_analysis,
                "error_handling": {"files_with_error_handling": [], "files_without_error_handling": []},  # Skip for speed
                "security_risks": security_risks,
                "deprecated_code": [],  # Skip for ultra-fast mode
                "dependency_risks": {"outdated_dependencies": []},  # Skip for speed
                "knowledge_risks": knowledge_risks,  # NEW: Knowledge risk assessment
                "test_coverage_gaps": test_coverage_gaps,  # NEW: Test coverage gaps analysis
                "enhanced_code_duplication": enhanced_duplication,  # NEW: Enhanced code duplication analysis
                "risk_summary": self._generate_fast_risk_summary(
                    test_coverage, complexity_analysis, security_risks, knowledge_risks
                )
            }
            
            # Cache the result
            self.cache_analysis("risk_analysis", result)
            
            return result
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _ultra_fast_test_coverage(self, token=None) -> Dict[str, Any]:
        """Ultra-fast test coverage analysis with aggressive limits"""
        
        coverage = {
            "test_files": [],
            "source_files": [],
            "coverage_ratio": 0.0,
            "test_patterns": defaultdict(int),
            "framework_usage": defaultdict(int)
        }
        
        # Quick file counting - only check top-level files for speed
        all_files = list(self.repo_path.rglob("*.py"))[:50]  # Limit to 50 Python files only
        all_files.extend(list(self.repo_path.rglob("*.js"))[:20])  # Add 20 JS files
        
        test_files = []
        source_files = []
        
        for file_path in all_files:
            file_name = str(file_path).lower()
            if any(pattern in file_name for pattern in ['test', 'spec']):
                test_files.append(file_path)
            else:
                source_files.append(file_path)
        
        coverage["test_files"] = [str(f.relative_to(self.repo_path)) for f in test_files]
        coverage["source_files"] = [str(f.relative_to(self.repo_path)) for f in source_files]
        
        # Calculate basic coverage ratio
        if source_files:
            coverage["coverage_ratio"] = len(test_files) / len(source_files)
        
        # Quick framework detection - only check first 5 test files
        for test_file in test_files[:5]:
            content = self.read_file_content(test_file)
            if not content:
                continue
            
            # Use pre-compiled patterns for speed
            if self._PATTERNS['python_test'].search(content):
                coverage["framework_usage"]["pytest/unittest"] += 1
            if self._PATTERNS['js_test'].search(content):
                coverage["framework_usage"]["jest/mocha"] += 1
            if self._PATTERNS['java_test'].search(content):
                coverage["framework_usage"]["junit"] += 1
        
        return coverage
    
    def _ultra_fast_complexity(self) -> Dict[str, Any]:
        """Ultra-fast complexity analysis with aggressive limits"""
        
        complexity = {
            "high_complexity_files": [],
            "complexity_distribution": {"low": 0, "medium": 0, "high": 0},
            "average_complexity": 0.0,
            "complexity_hotspots": []
        }
        
        # Only process 15 files maximum for ultra-fast analysis
        source_files = self.get_file_list(['.py', '.js', '.ts'])[:15]
        total_complexity = 0
        file_count = 0
        
        for file_path in source_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Ultra-fast complexity calculation using pre-compiled patterns
            complexity_matches = len(self._PATTERNS['complexity'].findall(content))
            line_count = len(content.split('\n'))
            
            # Simple complexity score: matches + line_count/100
            file_complexity = complexity_matches + (line_count // 100)
            
            total_complexity += file_complexity
            file_count += 1
            
            # Categorize complexity
            if file_complexity < 8:
                complexity["complexity_distribution"]["low"] += 1
            elif file_complexity < 20:
                complexity["complexity_distribution"]["medium"] += 1
            else:
                complexity["complexity_distribution"]["high"] += 1
                complexity["high_complexity_files"].append({
                    "file": relative_path,
                    "complexity": file_complexity,
                    "lines": line_count
                })
        
        if file_count > 0:
            complexity["average_complexity"] = total_complexity / file_count
        
        # Sort high complexity files - keep only top 5
        complexity["high_complexity_files"].sort(key=lambda x: x["complexity"], reverse=True)
        complexity["high_complexity_files"] = complexity["high_complexity_files"][:5]
        
        return complexity

    def _analyze_test_coverage(self) -> Dict[str, Any]:
        """Analyze test coverage patterns"""
        
        coverage = {
            "test_files": [],
            "source_files": [],
            "coverage_ratio": 0.0,
            "test_patterns": defaultdict(int),
            "framework_usage": defaultdict(int)
        }
        
        # Find test files
        test_patterns = [
            "**/test_*.py", "**/tests.py", "**/test*.py",
            "**/*_test.py", "**/tests/**/*.py",
            "**/*.test.js", "**/*.spec.js", "**/*.test.ts", "**/*.spec.ts",
            "**/test/**/*.java", "**/*Test.java", "**/*Tests.java"
        ]
        
        test_files = []
        for pattern in test_patterns:
            test_files.extend(self.find_files_by_pattern(pattern))
        
        # Remove duplicates
        test_files = list(set(test_files))
        
        # Find source files (excluding tests)
        all_files = self.get_file_list(['.py', '.js', '.ts', '.java', '.cpp', '.cs'])
        source_files = [f for f in all_files if f not in test_files]
        
        coverage["test_files"] = [str(f.relative_to(self.repo_path)) for f in test_files]
        coverage["source_files"] = [str(f.relative_to(self.repo_path)) for f in source_files]
        
        # Calculate basic coverage ratio
        if source_files:
            coverage["coverage_ratio"] = len(test_files) / len(source_files)
        
        # Analyze test patterns and frameworks
        for test_file in test_files[:20]:  # Limit for performance
            content = self.read_file_content(test_file)
            if not content:
                continue
            
            # Detect test frameworks
            frameworks = {
                "pytest": r"(import pytest|@pytest|def test_)",
                "unittest": r"(import unittest|class.*TestCase|def test)",
                "jest": r"(describe\(|it\(|test\(|expect\()",
                "mocha": r"(describe\(|it\(|before\(|after\()",
                "junit": r"(@Test|@Before|@After|import org.junit)",
                "testng": r"(@Test|import org.testng)",
                "jasmine": r"(describe\(|it\(|beforeEach\(|afterEach\()"
            }
            
            for framework, pattern in frameworks.items():
                if re.search(pattern, content, re.IGNORECASE):
                    coverage["framework_usage"][framework] += 1
            
            # Count test patterns
            test_method_patterns = [
                r"def test_\w+",
                r"function test\w+",
                r"it\(['\"].*['\"]",
                r"test\(['\"].*['\"]",
                r"@Test.*\n.*def \w+"
            ]
            
            for pattern in test_method_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                coverage["test_patterns"]["test_methods"] += len(matches)
        
        return coverage
    
    def _find_untested_code(self) -> List[Dict]:
        """Find code that appears to lack test coverage"""
        
        untested = []
        
        # Get source files
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        test_files = set()
        
        # Identify test files
        for file_path in source_files:
            if any(pattern in str(file_path).lower() for pattern in ['test', 'spec']):
                test_files.add(file_path)
        
        # Find source files without corresponding tests
        for file_path in source_files:
            if file_path in test_files:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Look for corresponding test file
            possible_test_names = [
                f"test_{file_path.stem}.py",
                f"{file_path.stem}_test.py",
                f"{file_path.stem}.test.js",
                f"{file_path.stem}.spec.js"
            ]
            
            has_test = False
            for test_name in possible_test_names:
                test_path = file_path.parent / test_name
                if test_path.exists():
                    has_test = True
                    break
            
            if not has_test:
                # Analyze the file for complexity indicators
                content = self.read_file_content(file_path)
                if content:
                    complexity_score = self._calculate_file_complexity(content)
                    
                    untested.append({
                        "file": relative_path,
                        "complexity_score": complexity_score,
                        "lines_of_code": len(content.split('\n')),
                        "risk_level": self._calculate_risk_level(complexity_score, len(content.split('\n')))
                    })
        
        # Sort by risk level
        untested.sort(key=lambda x: x["complexity_score"], reverse=True)
        
        return untested
    
    def _analyze_complexity(self) -> Dict[str, Any]:
        """Analyze code complexity metrics"""
        
        complexity = {
            "high_complexity_files": [],
            "complexity_distribution": {"low": 0, "medium": 0, "high": 0},
            "average_complexity": 0.0,
            "complexity_hotspots": []
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        total_complexity = 0
        file_count = 0
        
        for file_path in source_files[:50]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            file_complexity = self._calculate_file_complexity(content)
            
            total_complexity += file_complexity
            file_count += 1
            
            # Categorize complexity
            if file_complexity < 10:
                complexity["complexity_distribution"]["low"] += 1
            elif file_complexity < 25:
                complexity["complexity_distribution"]["medium"] += 1
            else:
                complexity["complexity_distribution"]["high"] += 1
                complexity["high_complexity_files"].append({
                    "file": relative_path,
                    "complexity": file_complexity,
                    "lines": len(content.split('\n'))
                })
        
        if file_count > 0:
            complexity["average_complexity"] = total_complexity / file_count
        
        # Sort high complexity files
        complexity["high_complexity_files"].sort(key=lambda x: x["complexity"], reverse=True)
        
        return complexity
    
    def _analyze_error_handling(self) -> Dict[str, Any]:
        """Analyze error handling patterns and gaps"""
        
        error_handling = {
            "files_with_error_handling": [],
            "files_without_error_handling": [],
            "error_patterns": defaultdict(int),
            "exception_types": defaultdict(int)
        }
        
        # Error handling patterns for different languages
        error_patterns = {
            "python": [
                r"try:\s*\n",
                r"except\s+\w*Error",
                r"raise\s+\w*Error",
                r"finally:"
            ],
            "javascript": [
                r"try\s*{",
                r"catch\s*\(",
                r"throw\s+new\s+Error",
                r"finally\s*{"
            ],
            "java": [
                r"try\s*{",
                r"catch\s*\(",
                r"throw\s+new\s+\w*Exception",
                r"finally\s*{"
            ]
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        
        for file_path in source_files[:50]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            file_ext = file_path.suffix
            
            # Determine language
            if file_ext == '.py':
                patterns = error_patterns["python"]
            elif file_ext in ['.js', '.ts']:
                patterns = error_patterns["javascript"]
            elif file_ext == '.java':
                patterns = error_patterns["java"]
            else:
                continue
            
            # Check for error handling
            has_error_handling = False
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    has_error_handling = True
                    error_handling["error_patterns"][pattern] += len(matches)
            
            if has_error_handling:
                error_handling["files_with_error_handling"].append(relative_path)
            else:
                # Check if file has functions that might need error handling
                function_patterns = [
                    r"def \w+\(",
                    r"function \w+\(",
                    r"public \w+ \w+\("
                ]
                
                has_functions = any(re.search(pattern, content) for pattern in function_patterns)
                if has_functions:
                    error_handling["files_without_error_handling"].append({
                        "file": relative_path,
                        "lines": len(content.split('\n')),
                        "functions": sum(len(re.findall(pattern, content)) for pattern in function_patterns)
                    })
        
        return error_handling
    
    def _ultra_fast_security_scan(self, token=None) -> List[Dict]:
        """Ultra-fast security risk scan with pre-compiled patterns"""
        
        security_risks = []
        
        # Only scan 12 files maximum for ultra-fast analysis
        source_files = self.get_file_list(['.py', '.js', '.ts'])[:12]
        
        for file_path in source_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Use pre-compiled patterns for maximum speed
            risk_checks = [
                ('sql_injection', self._PATTERNS['security_sql']),
                ('xss_vulnerability', self._PATTERNS['security_xss']),
                ('hardcoded_secrets', self._PATTERNS['security_secrets'])
            ]
            
            for risk_type, pattern in risk_checks:
                matches = list(pattern.finditer(content))[:3]  # Limit to first 3 matches per type per file
                
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    
                    security_risks.append({
                        "type": risk_type,
                        "file": relative_path,
                        "line": line_num,
                        "pattern": match.group(0)[:50],  # Truncate long patterns
                        "context": "Context skipped for speed",
                        "severity": self._get_quick_severity(risk_type)
                    })
        
        # Sort by severity and return top 20 for performance
        security_risks.sort(key=lambda x: x["severity"], reverse=True)
        return security_risks[:20]
    
    def _analyze_knowledge_risks(self, token=None) -> Dict[str, Any]:
        """Analyze knowledge risks and single points of failure in team expertise"""
        
        knowledge_risks = {
            "single_point_failures": [],
            "knowledge_silos": [],
            "bus_factor_risks": [],
            "critical_files_with_few_contributors": [],
            "summary": {
                "total_risks": 0,
                "high_risk_files": 0,
                "contributors_at_risk": 0
            }
        }
        
        try:
            # Use ExpertiseMapper to get team contribution data
            expertise_mapper = ExpertiseMapper(self.repo_path, self.repo, self.ai_client)
            expertise_data = expertise_mapper.analyze(token=token)
            
            if "error" in expertise_data:
                return knowledge_risks
            
            file_expertise = expertise_data.get("file_expertise", {})
            tech_expertise = expertise_data.get("tech_expertise", {})
            
            # Analyze file-level single points of failure
            self._identify_file_spofs(file_expertise, knowledge_risks, token)
            
            # Analyze technology-level knowledge silos
            self._identify_technology_silos(tech_expertise, knowledge_risks)
            
            # Calculate bus factor risks
            self._calculate_bus_factor_risks(file_expertise, knowledge_risks)
            
            # Identify critical files with limited knowledge
            self._identify_critical_files_limited_knowledge(file_expertise, knowledge_risks)
            
            # Generate summary
            knowledge_risks["summary"]["total_risks"] = (
                len(knowledge_risks["single_point_failures"]) + 
                len(knowledge_risks["knowledge_silos"]) + 
                len(knowledge_risks["bus_factor_risks"])
            )
            knowledge_risks["summary"]["high_risk_files"] = len(knowledge_risks["critical_files_with_few_contributors"])
            knowledge_risks["summary"]["contributors_at_risk"] = len(set(
                risk.get("primary_contributor", "") for risk in 
                knowledge_risks["single_point_failures"] + knowledge_risks["bus_factor_risks"]
            ))
            
        except Exception as e:
            # Return empty structure on error but don't fail the entire analysis
            pass
        
        return knowledge_risks
    
    def _identify_file_spofs(self, file_expertise: Dict, knowledge_risks: Dict, token=None) -> None:
        """Identify files with single points of failure (only one contributor)"""
        
        for file_path, contributors in file_expertise.items():
            if token:
                token.check_cancellation()
            
            total_commits = sum(contributors.values())
            contributor_count = len(contributors)
            
            # Check for single point of failure (only one contributor)
            if contributor_count == 1:
                primary_contributor = list(contributors.keys())[0]
                
                # Calculate file complexity/importance
                file_complexity = self._calculate_file_importance(file_path, total_commits)
                
                risk_explanation = f"Critical knowledge risk: Only {primary_contributor} has worked on this file ({total_commits} commits). If this person leaves, knowledge transfer will be difficult."
                
                knowledge_risks["single_point_failures"].append({
                    "file": file_path,
                    "primary_contributor": primary_contributor,
                    "commits": total_commits,
                    "risk_level": self._calculate_spof_risk_level(file_complexity, total_commits),
                    "explanation": risk_explanation,
                    "mitigation_suggestion": "Assign secondary developers to review and contribute to this file"
                })
            
            # Check for dominant contributor (>80% of commits)
            elif contributor_count > 1:
                sorted_contributors = sorted(contributors.items(), key=lambda x: x[1], reverse=True)
                primary_contributor, primary_commits = sorted_contributors[0]
                
                if primary_commits / total_commits > 0.8:
                    file_complexity = self._calculate_file_importance(file_path, total_commits)
                    
                    risk_explanation = f"Knowledge concentration risk: {primary_contributor} owns {primary_commits}/{total_commits} commits ({(primary_commits/total_commits)*100:.1f}%). Limited knowledge sharing detected."
                    
                    knowledge_risks["bus_factor_risks"].append({
                        "file": file_path,
                        "primary_contributor": primary_contributor,
                        "primary_commits": primary_commits,
                        "total_commits": total_commits,
                        "dominance_percentage": (primary_commits / total_commits) * 100,
                        "risk_level": self._calculate_spof_risk_level(file_complexity, total_commits),
                        "explanation": risk_explanation,
                        "mitigation_suggestion": "Encourage knowledge sharing through code reviews and pair programming"
                    })
    
    def _identify_technology_silos(self, tech_expertise: Dict, knowledge_risks: Dict) -> None:
        """Identify technology areas with knowledge silos"""
        
        for technology, contributors in tech_expertise.items():
            total_commits = sum(contributors.values())
            contributor_count = len(contributors)
            
            # Technology handled by only one person
            if contributor_count == 1:
                primary_contributor = list(contributors.keys())[0]
                
                risk_explanation = f"Technology silo risk: Only {primary_contributor} has expertise in {technology} ({total_commits} commits). This creates a critical dependency on one person."
                
                knowledge_risks["knowledge_silos"].append({
                    "technology": technology,
                    "primary_contributor": primary_contributor,
                    "commits": total_commits,
                    "risk_level": "high" if total_commits > 20 else "medium",
                    "explanation": risk_explanation,
                    "mitigation_suggestion": f"Cross-train other team members in {technology} through workshops or mentoring"
                })
            
            # Technology dominated by one contributor (>75% of commits)
            elif contributor_count > 1:
                sorted_contributors = sorted(contributors.items(), key=lambda x: x[1], reverse=True)
                primary_contributor, primary_commits = sorted_contributors[0]
                
                if primary_commits / total_commits > 0.75:
                    risk_explanation = f"Technology concentration risk: {primary_contributor} dominates {technology} with {primary_commits}/{total_commits} commits ({(primary_commits/total_commits)*100:.1f}%)."
                    
                    knowledge_risks["knowledge_silos"].append({
                        "technology": technology,
                        "primary_contributor": primary_contributor,
                        "primary_commits": primary_commits,
                        "total_commits": total_commits,
                        "dominance_percentage": (primary_commits / total_commits) * 100,
                        "risk_level": "medium",
                        "explanation": risk_explanation,
                        "mitigation_suggestion": f"Distribute {technology} work among team members to reduce concentration"
                    })
    
    def _calculate_bus_factor_risks(self, file_expertise: Dict, knowledge_risks: Dict) -> None:
        """Calculate overall bus factor risks for the project"""
        
        # Count files where each person is the primary contributor
        primary_contributor_counts = defaultdict(int)
        
        for file_path, contributors in file_expertise.items():
            if contributors:
                primary_contributor = max(contributors.items(), key=lambda x: x[1])[0]
                primary_contributor_counts[primary_contributor] += 1
        
        # Identify people who are critical (primary for many files)
        for contributor, file_count in primary_contributor_counts.items():
            if file_count >= 5:  # Primary contributor for 5 or more files
                risk_explanation = f"Bus factor risk: {contributor} is the primary contributor for {file_count} files. Loss of this person would significantly impact project knowledge."
                
                knowledge_risks["bus_factor_risks"].append({
                    "contributor": contributor,
                    "primary_files_count": file_count,
                    "risk_level": "high" if file_count >= 10 else "medium",
                    "explanation": risk_explanation,
                    "mitigation_suggestion": "Implement knowledge transfer sessions and documentation for this contributor's areas"
                })
    
    def _identify_critical_files_limited_knowledge(self, file_expertise: Dict, knowledge_risks: Dict) -> None:
        """Identify important files with limited contributor diversity"""
        
        critical_files = []
        
        for file_path, contributors in file_expertise.items():
            total_commits = sum(contributors.values())
            contributor_count = len(contributors)
            
            # Consider files with significant activity but few contributors
            if total_commits >= 10 and contributor_count <= 2:
                file_complexity = self._calculate_file_importance(file_path, total_commits)
                
                primary_contributors = sorted(contributors.items(), key=lambda x: x[1], reverse=True)
                contributor_names = [name for name, _ in primary_contributors]
                
                risk_explanation = f"Limited knowledge diversity: Important file with {total_commits} commits but only {contributor_count} contributor(s): {', '.join(contributor_names)}."
                
                critical_files.append({
                    "file": file_path,
                    "total_commits": total_commits,
                    "contributor_count": contributor_count,
                    "contributors": contributor_names,
                    "importance_score": file_complexity,
                    "risk_level": self._calculate_spof_risk_level(file_complexity, total_commits),
                    "explanation": risk_explanation,
                    "mitigation_suggestion": "Encourage more team members to review and contribute to this file"
                })
        
        # Sort by importance score and keep top risks
        critical_files.sort(key=lambda x: x["importance_score"], reverse=True)
        knowledge_risks["critical_files_with_few_contributors"] = critical_files[:15]
    
    def _calculate_file_importance(self, file_path: str, commit_count: int) -> float:
        """Calculate importance score for a file based on various factors"""
        
        importance = 0.0
        
        # Base score from commit activity
        importance += min(commit_count * 0.5, 50)  # Cap at 50 points
        
        # Bonus for file type/location importance
        if any(pattern in file_path.lower() for pattern in ['main', 'index', 'app', 'core', 'base']):
            importance += 20
        
        if any(pattern in file_path.lower() for pattern in ['config', 'settings', 'env']):
            importance += 15
        
        if any(pattern in file_path.lower() for pattern in ['api', 'server', 'client']):
            importance += 10
        
        # File extension importance
        if file_path.endswith(('.py', '.js', '.ts', '.java', '.cpp')):
            importance += 5
        
        # Path depth (deeper files might be more specialized)
        path_depth = file_path.count('/')
        importance += max(0, 10 - path_depth)  # Prefer files closer to root
        
        return importance
    
    def _calculate_spof_risk_level(self, importance: float, commits: int) -> str:
        """Calculate risk level for single point of failure"""
        
        if importance > 50 or commits > 50:
            return "high"
        elif importance > 25 or commits > 20:
            return "medium"
        else:
            return "low"
    
    def _analyze_test_coverage_gaps(self, token=None) -> Dict[str, Any]:
        """Analyze test coverage gaps and identify risk areas"""
        
        coverage_analysis = {
            "uncovered_files": [],
            "high_risk_files": [],
            "coverage_summary": {},
            "risk_categories": {}
        }
        
        # Get all source files
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java', '.cpp'])[:25]  # Limit for performance
        test_files = self.get_file_list(['test_*.py', '*_test.py', '*.test.js', '*.spec.js', '*Test.java'])
        
        # Extract test file patterns for matching
        test_patterns = set()
        for test_file in test_files:
            stem = test_file.stem.lower()
            # Extract the core name from test file
            if stem.startswith('test_'):
                test_patterns.add(stem[5:])
            elif stem.endswith('_test'):
                test_patterns.add(stem[:-5])
            elif stem.endswith('.test'):
                test_patterns.add(stem[:-5])
            elif stem.endswith('.spec'):
                test_patterns.add(stem[:-5])
            elif stem.endswith('test'):
                test_patterns.add(stem[:-4])
        
        total_files = 0
        uncovered_count = 0
        high_risk_count = 0
        
        for file_path in source_files:
            if token:
                token.check_cancellation()
            
            # Skip test files themselves
            if any(test_keyword in str(file_path).lower() for test_keyword in ['test', 'spec']):
                continue
            
            total_files += 1
            relative_path = str(file_path.relative_to(self.repo_path))
            file_stem = file_path.stem.lower()
            
            # Check if file has corresponding tests
            has_test = any(pattern in file_stem or file_stem in pattern for pattern in test_patterns)
            
            if not has_test:
                uncovered_count += 1
                
                # Calculate risk level based on file characteristics
                risk_score = self._calculate_file_risk_score(file_path, relative_path)
                
                file_info = {
                    "file": relative_path,
                    "risk_score": risk_score,
                    "risk_level": self._get_risk_level(risk_score),
                    "file_type": self._get_file_type(relative_path),
                    "reasons": self._get_risk_reasons(file_path, relative_path)
                }
                
                coverage_analysis["uncovered_files"].append(file_info)
                
                if risk_score >= 70:  # High risk threshold
                    coverage_analysis["high_risk_files"].append(file_info)
                    high_risk_count += 1
        
        # Calculate coverage statistics
        coverage_percentage = ((total_files - uncovered_count) / max(total_files, 1)) * 100
        
        coverage_analysis["coverage_summary"] = {
            "total_source_files": total_files,
            "files_with_tests": total_files - uncovered_count,
            "files_without_tests": uncovered_count,
            "coverage_percentage": round(coverage_percentage, 1),
            "high_risk_uncovered": high_risk_count
        }
        
        # Categorize by risk
        risk_categories = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for file_info in coverage_analysis["uncovered_files"]:
            risk_level = file_info["risk_level"]
            risk_categories[risk_level] = risk_categories.get(risk_level, 0) + 1
        
        coverage_analysis["risk_categories"] = risk_categories
        
        return coverage_analysis
    
    def _calculate_file_risk_score(self, file_path: Path, relative_path: str) -> int:
        """Calculate risk score for a file based on various factors"""
        
        risk_score = 30  # Base risk
        
        # File type importance
        if any(keyword in relative_path.lower() for keyword in ['main', 'index', 'app']):
            risk_score += 40  # Entry points are critical
        elif any(keyword in relative_path.lower() for keyword in ['api', 'endpoint', 'controller']):
            risk_score += 35  # API files are high risk
        elif any(keyword in relative_path.lower() for keyword in ['core', 'service', 'business']):
            risk_score += 30  # Core business logic
        elif any(keyword in relative_path.lower() for keyword in ['model', 'data', 'db']):
            risk_score += 25  # Data layer
        elif any(keyword in relative_path.lower() for keyword in ['util', 'helper', 'common']):
            risk_score += 15  # Utilities
        elif any(keyword in relative_path.lower() for keyword in ['config', 'settings']):
            risk_score += 20  # Configuration files
        
        # File size complexity indicator
        content = self.read_file_content(file_path)
        if content:
            lines = len(content.split('\n'))
            if lines > 200:
                risk_score += 20
            elif lines > 100:
                risk_score += 10
            
            # Function/class count as complexity indicator
            if file_path.suffix == '.py':
                class_count = len(re.findall(r'class\s+\w+', content))
                func_count = len(re.findall(r'def\s+\w+', content))
                risk_score += min((class_count * 5) + (func_count * 2), 30)
            elif file_path.suffix in ['.js', '.ts']:
                func_count = len(re.findall(r'function\s+\w+|const\s+\w+\s*=.*=>', content))
                risk_score += min(func_count * 3, 25)
        
        return min(risk_score, 100)
    
    def _get_risk_level(self, risk_score: int) -> str:
        """Get risk level based on score"""
        if risk_score >= 80:
            return "critical"
        elif risk_score >= 60:
            return "high"
        elif risk_score >= 40:
            return "medium"
        else:
            return "low"
    
    def _get_file_type(self, relative_path: str) -> str:
        """Determine file type category"""
        path_lower = relative_path.lower()
        
        if any(keyword in path_lower for keyword in ['main', 'index', 'app']):
            return "Entry Point"
        elif any(keyword in path_lower for keyword in ['api', 'endpoint', 'controller']):
            return "API/Controller"
        elif any(keyword in path_lower for keyword in ['core', 'service', 'business']):
            return "Business Logic"
        elif any(keyword in path_lower for keyword in ['model', 'data', 'db']):
            return "Data Layer"
        elif any(keyword in path_lower for keyword in ['util', 'helper', 'common']):
            return "Utility"
        elif any(keyword in path_lower for keyword in ['config', 'settings']):
            return "Configuration"
        else:
            return "General"
    
    def _get_risk_reasons(self, file_path: Path, relative_path: str) -> List[str]:
        """Get reasons why file is considered risky"""
        reasons = []
        
        path_lower = relative_path.lower()
        
        if any(keyword in path_lower for keyword in ['main', 'index', 'app']):
            reasons.append("Entry point file")
        if any(keyword in path_lower for keyword in ['api', 'endpoint']):
            reasons.append("API endpoint")
        if any(keyword in path_lower for keyword in ['core', 'business']):
            reasons.append("Core business logic")
        
        content = self.read_file_content(file_path)
        if content:
            lines = len(content.split('\n'))
            if lines > 200:
                reasons.append(f"Large file ({lines} lines)")
            
            if file_path.suffix == '.py':
                class_count = len(re.findall(r'class\s+\w+', content))
                if class_count > 3:
                    reasons.append(f"Multiple classes ({class_count})")
        
        if not reasons:
            reasons.append("Untested source file")
        
        return reasons
    
    def _analyze_code_duplication_enhanced(self, token=None) -> Dict[str, Any]:
        """Enhanced code duplication analysis with categorization"""
        
        duplication = {
            "exact_duplicates": [],
            "similar_functions": [],
            "structural_duplicates": [],
            "duplication_summary": {},
            "consolidation_opportunities": []
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts'])[:20]  # Limit for performance
        
        # Track code blocks for comparison
        code_blocks = []
        function_signatures = defaultdict(list)
        
        for file_path in source_files:
            if token:
                token.check_cancellation()
            
            content = self.read_file_content(file_path)
            if not content or len(content) > 50000:  # Skip very large files
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            lines = content.split('\n')
            
            # Extract functions for comparison
            if file_path.suffix == '.py':
                self._extract_python_functions(content, relative_path, function_signatures, code_blocks)
            elif file_path.suffix in ['.js', '.ts']:
                self._extract_js_functions(content, relative_path, function_signatures, code_blocks)
            
            # Check for exact line duplicates
            self._find_exact_duplicates(lines, relative_path, duplication)
        
        # Find similar functions
        self._find_similar_functions(function_signatures, duplication)
        
        # Find structural duplicates
        self._find_structural_duplicates(code_blocks, duplication)
        
        # Generate consolidation opportunities
        self._generate_consolidation_opportunities(duplication)
        
        # Summary
        duplication["duplication_summary"] = {
            "exact_duplicates": len(duplication["exact_duplicates"]),
            "similar_functions": len(duplication["similar_functions"]),
            "structural_duplicates": len(duplication["structural_duplicates"]),
            "total_opportunities": len(duplication["consolidation_opportunities"])
        }
        
        return duplication
    
    def _extract_python_functions(self, content: str, file_path: str, function_signatures: Dict, code_blocks: List):
        """Extract Python function information"""
        
        func_pattern = re.compile(r'def\s+(\w+)\s*\([^)]*\):', re.MULTILINE)
        matches = list(func_pattern.finditer(content))
        
        for match in matches:
            func_name = match.group(1)
            start_pos = match.start()
            line_num = content[:start_pos].count('\n') + 1
            
            # Extract function body (simplified)
            lines = content[start_pos:].split('\n')[:20]  # Limit to first 20 lines
            func_body = '\n'.join(lines)
            
            function_signatures[func_name].append({
                "file": file_path,
                "line": line_num,
                "body": func_body,
                "signature": match.group(0)
            })
    
    def _extract_js_functions(self, content: str, file_path: str, function_signatures: Dict, code_blocks: List):
        """Extract JavaScript/TypeScript function information"""
        
        # Simple function patterns
        patterns = [
            re.compile(r'function\s+(\w+)\s*\([^)]*\)', re.MULTILINE),
            re.compile(r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>', re.MULTILINE),
            re.compile(r'(\w+)\s*:\s*function\s*\([^)]*\)', re.MULTILINE)
        ]
        
        for pattern in patterns:
            matches = list(pattern.finditer(content))
            for match in matches:
                func_name = match.group(1)
                start_pos = match.start()
                line_num = content[:start_pos].count('\n') + 1
                
                function_signatures[func_name].append({
                    "file": file_path,
                    "line": line_num,
                    "signature": match.group(0)
                })
    
    def _find_exact_duplicates(self, lines: List[str], file_path: str, duplication: Dict):
        """Find exact duplicate lines"""
        
        line_counts = Counter()
        significant_lines = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if len(stripped) > 15 and not stripped.startswith('#') and not stripped.startswith('//'):
                line_counts[stripped] += 1
                significant_lines.append((i + 1, stripped))
        
        # Find lines that appear multiple times
        for line_content, count in line_counts.items():
            if count > 2:  # Appears more than twice
                line_numbers = [line_num for line_num, content in significant_lines if content == line_content]
                
                duplication["exact_duplicates"].append({
                    "file": file_path,
                    "content": line_content[:80] + "..." if len(line_content) > 80 else line_content,
                    "occurrences": count,
                    "lines": line_numbers[:5],  # First 5 occurrences
                    "category": "exact_duplicate",
                    "consolidation_potential": "high" if count > 3 else "medium"
                })
    
    def _find_similar_functions(self, function_signatures: Dict, duplication: Dict):
        """Find functions with similar names that might be duplicates"""
        
        for func_name, occurrences in function_signatures.items():
            if len(occurrences) > 1:  # Same function name in multiple files
                duplication["similar_functions"].append({
                    "function_name": func_name,
                    "occurrences": len(occurrences),
                    "files": [occ["file"] for occ in occurrences[:5]],
                    "category": "similar_function",
                    "consolidation_potential": "medium"
                })
    
    def _find_structural_duplicates(self, code_blocks: List, duplication: Dict):
        """Find structurally similar code blocks"""
        # Simple implementation - can be enhanced with AST analysis
        pass
    
    def _generate_consolidation_opportunities(self, duplication: Dict):
        """Generate actionable consolidation opportunities"""
        
        opportunities = []
        
        # From exact duplicates
        for dup in duplication["exact_duplicates"]:
            if dup["consolidation_potential"] == "high":
                opportunities.append({
                    "type": "Extract Constant/Method",
                    "description": f"Duplicate code found in {dup['file']} ({dup['occurrences']} times)",
                    "priority": "high",
                    "effort": "low"
                })
        
        # From similar functions
        for func in duplication["similar_functions"]:
            if len(func["files"]) > 2:
                opportunities.append({
                    "type": "Create Common Utility",
                    "description": f"Function '{func['function_name']}' appears in {len(func['files'])} files",
                    "priority": "medium", 
                    "effort": "medium"
                })
        
        duplication["consolidation_opportunities"] = opportunities
    
    def _get_quick_severity(self, risk_type: str) -> int:
        """Quick security severity mapping"""
        severity_map = {
            "sql_injection": 10,
            "xss_vulnerability": 8,
            "hardcoded_secrets": 6
        }
        return severity_map.get(risk_type, 5)
    
    def _generate_fast_risk_summary(self, test_coverage: Dict, complexity: Dict, security_risks: List, knowledge_risks: Dict) -> Dict[str, Any]:
        """Generate fast risk summary with minimal calculations including knowledge risks"""
        
        summary = {
            "overall_risk_score": 0,
            "critical_issues": 0,
            "high_risk_files": 0,
            "test_coverage_score": test_coverage.get("coverage_ratio", 0) * 100,
            "complexity_score": complexity.get("average_complexity", 0),
            "security_issues": len(security_risks),
            "knowledge_risk_score": knowledge_risks.get("summary", {}).get("total_risks", 0),
            "untested_high_complexity": 0
        }
        
        # Quick risk score calculation including knowledge risks
        coverage_risk = max(0, 50 - summary["test_coverage_score"]) * 0.3
        complexity_risk = min(50, summary["complexity_score"] * 1.5) * 0.25
        security_risk = min(50, len(security_risks) * 5) * 0.25
        knowledge_risk = min(50, summary["knowledge_risk_score"] * 3) * 0.2  # NEW: Knowledge risk factor
        
        summary["overall_risk_score"] = coverage_risk + complexity_risk + security_risk + knowledge_risk
        summary["critical_issues"] = len([r for r in security_risks if r["severity"] >= 8])
        summary["high_risk_files"] = len(complexity.get("high_complexity_files", []))
        
        return summary
    
    def render(self):
        """Render the risk analysis"""
        # Add rerun button
        self.add_rerun_button("risk_analysis")
        
        with self.display_loading_message("Analyzing risks and test coverage..."):
            analysis = self.analyze()
        
        if "error" in analysis:
            self.display_error(analysis["error"])
            return
        
        # Risk Summary Dashboard
        st.subheader("📊 Risk Summary Dashboard")
        
        risk_summary = analysis["risk_summary"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            risk_score = risk_summary["overall_risk_score"]
            risk_color = "red" if risk_score > 70 else "orange" if risk_score > 40 else "green"
            st.metric("Overall Risk Score", f"{risk_score:.1f}/100", delta_color="inverse")
        
        with col2:
            st.metric("Critical Issues", risk_summary["critical_issues"])
        
        with col3:
            coverage_score = risk_summary["test_coverage_score"]
            st.metric("Test Coverage", f"{coverage_score:.1f}%")
        
        with col4:
            st.metric("High-Risk Files", risk_summary["high_risk_files"])
        
        # Test Coverage Analysis
        st.subheader("🧪 Test Coverage Analysis")
        
        test_coverage = analysis["test_coverage"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Coverage ratio visualization
            fig_coverage = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = test_coverage["coverage_ratio"] * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Test Coverage Ratio"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            st.plotly_chart(fig_coverage, use_container_width=True)
        
        with col2:
            # Test framework usage
            if test_coverage["framework_usage"]:
                framework_data = dict(test_coverage["framework_usage"])
                fig_frameworks = px.pie(
                    values=list(framework_data.values()),
                    names=list(framework_data.keys()),
                    title="Test Frameworks Used"
                )
                st.plotly_chart(fig_frameworks, use_container_width=True)
        
        # Test Coverage Risk Assessment
        st.subheader("🧪 Test Coverage Risk Assessment")
        st.markdown("Detailed analysis of files without test coverage and their risk levels")
        
        test_coverage_gaps = analysis.get("test_coverage_gaps", {})
        
        if test_coverage_gaps and test_coverage_gaps.get("coverage_summary"):
            summary = test_coverage_gaps["coverage_summary"]
            
            # Coverage summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Files Without Tests", summary["files_without_tests"])
            with col2:
                st.metric("Coverage Percentage", f"{summary['coverage_percentage']}%")
            with col3:
                st.metric("High Risk Uncovered", summary["high_risk_uncovered"])
            with col4:
                st.metric("Total Source Files", summary["total_source_files"])
            
            # Risk category distribution
            if test_coverage_gaps.get("risk_categories"):
                risk_categories = test_coverage_gaps["risk_categories"]
                
                if any(count > 0 for count in risk_categories.values()):
                    fig_risk_dist = px.bar(
                        x=list(risk_categories.keys()),
                        y=list(risk_categories.values()),
                        title="Risk Level Distribution of Uncovered Files",
                        color=list(risk_categories.keys()),
                        color_discrete_map={
                            "critical": "#d63031", 
                            "high": "#ff6b6b", 
                            "medium": "#ffd93d", 
                            "low": "#6bcf7f"
                        }
                    )
                    fig_risk_dist.update_layout(
                        xaxis_title="Risk Level",
                        yaxis_title="Number of Files"
                    )
                    st.plotly_chart(fig_risk_dist, use_container_width=True)
            
            # High-risk uncovered files
            if test_coverage_gaps.get("high_risk_files"):
                st.write("**🚨 High-Risk Files Without Test Coverage**")
                
                high_risk_data = []
                for file_info in test_coverage_gaps["high_risk_files"]:
                    high_risk_data.append({
                        "File Path": file_info["file"],
                        "Risk Score": f"{file_info['risk_score']}/100",
                        "Risk Level": file_info["risk_level"].upper(),
                        "File Type": file_info["file_type"],
                        "Risk Reasons": ", ".join(file_info["reasons"][:3])  # Show first 3 reasons
                    })
                
                high_risk_df = pd.DataFrame(high_risk_data)
                
                # Style the dataframe with risk level highlighting
                def highlight_risk_level(val):
                    if val == "CRITICAL":
                        return 'background-color: #ff9999; font-weight: bold; color: darkred'
                    elif val == "HIGH":
                        return 'background-color: #ffcccc; font-weight: bold'
                    elif val == "MEDIUM":
                        return 'background-color: #fff2cc; font-weight: bold'
                    else:
                        return 'background-color: #ccffcc'
                
                styled_high_risk = high_risk_df.style.applymap(highlight_risk_level, subset=['Risk Level'])
                st.dataframe(styled_high_risk, use_container_width=True)
            
            # All uncovered files with details
            if test_coverage_gaps.get("uncovered_files"):
                st.write("**📋 All Files Without Test Coverage**")
                
                uncovered_data = []
                for file_info in test_coverage_gaps["uncovered_files"]:
                    uncovered_data.append({
                        "File Path": file_info["file"],
                        "Risk Score": file_info["risk_score"],
                        "Risk Level": file_info["risk_level"].upper(),
                        "File Type": file_info["file_type"],
                        "Primary Risk Factors": ", ".join(file_info["reasons"][:2])  # Show top 2 reasons
                    })
                
                uncovered_df = pd.DataFrame(uncovered_data)
                
                # Sort by risk score
                uncovered_df = uncovered_df.sort_values("Risk Score", ascending=False)
                
                # Apply styling
                styled_uncovered = uncovered_df.style.applymap(highlight_risk_level, subset=['Risk Level'])
                st.dataframe(styled_uncovered, use_container_width=True)
                
                # File type distribution
                if uncovered_df["File Type"].nunique() > 1:
                    file_type_counts = uncovered_df["File Type"].value_counts()
                    
                    fig_file_types = px.pie(
                        values=file_type_counts.values,
                        names=file_type_counts.index,
                        title="Uncovered Files by Type"
                    )
                    st.plotly_chart(fig_file_types, use_container_width=True)
            
            # Recommendations
            st.write("**💡 Recommendations for Test Coverage Improvement**")
            
            recommendations = [
                "🎯 **Priority 1**: Focus on critical and high-risk files first",
                "🏗️ **Entry Points**: Ensure main, index, and app files have comprehensive tests", 
                "🔌 **API Coverage**: Add tests for all API endpoints and controllers",
                "💼 **Business Logic**: Test core service and business logic files thoroughly",
                "📊 **Data Layer**: Verify model and database interaction code",
                "🛠️ **Utilities**: Even utility functions need basic validation tests"
            ]
            
            for rec in recommendations:
                st.markdown(f"- {rec}")
        
        else:
            st.info("No test coverage gap analysis available")
        
        # Untested Code
        st.subheader("🚨 Untested Code")
        
        untested_code = analysis["untested_code"]
        if untested_code:
            untested_df = pd.DataFrame([
                {
                    "File": code["file"],
                    "Complexity Score": code["complexity_score"],
                    "Lines of Code": code["lines_of_code"],
                    "Risk Level": code["risk_level"]
                }
                for code in untested_code[:20]
            ])
            
            st.dataframe(untested_df, use_container_width=True)
            
            # Risk level distribution
            risk_counts = Counter(code["risk_level"] for code in untested_code)
            fig_risk_levels = px.bar(
                x=list(risk_counts.keys()),
                y=list(risk_counts.values()),
                title="Untested Code Risk Distribution",
                color=list(risk_counts.keys()),
                color_discrete_map={"high": "red", "medium": "orange", "low": "green"}
            )
            st.plotly_chart(fig_risk_levels, use_container_width=True)
        else:
            st.success("All code appears to have corresponding test files!")
        
        # Complexity Analysis
        st.subheader("🔄 Complexity Analysis")
        
        complexity_analysis = analysis["complexity_analysis"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Complexity distribution
            complexity_dist = complexity_analysis["complexity_distribution"]
            fig_complexity = px.pie(
                values=list(complexity_dist.values()),
                names=list(complexity_dist.keys()),
                title="Complexity Distribution",
                color_discrete_map={"low": "green", "medium": "yellow", "high": "red"}
            )
            st.plotly_chart(fig_complexity, use_container_width=True)
        
        with col2:
            # High complexity files
            if complexity_analysis["high_complexity_files"]:
                high_complex_df = pd.DataFrame(complexity_analysis["high_complexity_files"][:10])
                st.write("**Top High-Complexity Files:**")
                st.dataframe(high_complex_df, use_container_width=True)
        
        # Security Risks
        st.subheader("🔒 Security Risk Analysis")
        
        security_risks = analysis["security_risks"]
        if security_risks:
            # Security risk types
            risk_type_counts = Counter(risk["type"] for risk in security_risks)
            fig_security = px.bar(
                x=list(risk_type_counts.keys()),
                y=list(risk_type_counts.values()),
                title="Security Risk Types"
            )
            st.plotly_chart(fig_security, use_container_width=True)
            
            # Detailed security risks
            security_df = pd.DataFrame([
                {
                    "Type": risk["type"],
                    "File": risk["file"],
                    "Line": risk["line"],
                    "Severity": risk["severity"],
                    "Pattern": risk["pattern"][:50] + "..." if len(risk["pattern"]) > 50 else risk["pattern"]
                }
                for risk in security_risks[:20]
            ])
            
            st.dataframe(security_df, use_container_width=True)
        else:
            st.success("No obvious security risks detected!")
        
        # Error Handling Analysis
        st.subheader("🛡️ Error Handling Analysis")
        
        error_handling = analysis["error_handling"]
        
        files_with_handling = len(error_handling["files_with_error_handling"])
        files_without_handling = len(error_handling["files_without_error_handling"])
        
        if files_with_handling + files_without_handling > 0:
            fig_error_handling = px.pie(
                values=[files_with_handling, files_without_handling],
                names=["With Error Handling", "Without Error Handling"],
                title="Error Handling Coverage",
                color_discrete_map={"With Error Handling": "green", "Without Error Handling": "red"}
            )
            st.plotly_chart(fig_error_handling, use_container_width=True)
            
            # Files without error handling details
            if error_handling["files_without_error_handling"]:
                st.write("**Files Without Error Handling:**")
                no_error_df = pd.DataFrame(error_handling["files_without_error_handling"][:10])
                st.dataframe(no_error_df, use_container_width=True)
        
        # Deprecated Code
        st.subheader("⚠️ Deprecated Code")
        
        deprecated_code = analysis["deprecated_code"]
        if deprecated_code:
            deprecated_df = pd.DataFrame([
                {
                    "File": dep["file"],
                    "Line": dep["line"],
                    "Pattern": dep["pattern"],
                    "Language": dep["language"]
                }
                for dep in deprecated_code[:15]
            ])
            
            st.dataframe(deprecated_df, use_container_width=True)
            
            # Deprecated patterns by language
            lang_counts = Counter(dep["language"] for dep in deprecated_code)
            if lang_counts:
                fig_deprecated = px.bar(
                    x=list(lang_counts.keys()),
                    y=list(lang_counts.values()),
                    title="Deprecated Code by Language"
                )
                st.plotly_chart(fig_deprecated, use_container_width=True)
        else:
            st.success("No deprecated code patterns detected!")
        
        # Knowledge Risk Assessment - NEW FEATURE
        st.subheader("🧠 Knowledge Risk Assessment")
        st.markdown("Identifying single points of failure in team expertise and knowledge distribution")
        
        knowledge_risks = analysis.get("knowledge_risks", {})
        
        # Knowledge risks summary
        if knowledge_risks:
            summary = knowledge_risks.get("summary", {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Knowledge Risks", summary.get("total_risks", 0))
            with col2:
                st.metric("High-Risk Files", summary.get("high_risk_files", 0))
            with col3:
                st.metric("Contributors at Risk", summary.get("contributors_at_risk", 0))
            
            # Single Point of Failures
            if knowledge_risks.get("single_point_failures"):
                st.write("**🚨 Single Points of Failure**")
                st.markdown("Files where only one person has worked - critical knowledge risks")
                
                spof_data = []
                for risk in knowledge_risks["single_point_failures"]:
                    spof_data.append({
                        "File Path": risk["file"],
                        "Primary Contributor": risk["primary_contributor"],
                        "Commits": risk["commits"],
                        "Risk Level": risk["risk_level"].upper(),
                        "Risk Explanation": risk["explanation"],
                        "Mitigation Suggestion": risk["mitigation_suggestion"]
                    })
                
                spof_df = pd.DataFrame(spof_data)
                
                # Style the dataframe with risk level highlighting
                def highlight_risk_level(val):
                    if val == "HIGH":
                        return 'background-color: #ffcccc; font-weight: bold'
                    elif val == "MEDIUM":
                        return 'background-color: #fff2cc; font-weight: bold'
                    elif val == "CRITICAL":
                        return 'background-color: #ff9999; font-weight: bold; color: darkred'
                    else:
                        return 'background-color: #ccffcc'
                
                styled_spof = spof_df.style.applymap(highlight_risk_level, subset=['Risk Level'])
                st.dataframe(styled_spof, use_container_width=True)
            
            # Knowledge Silos (Technology-based)
            if knowledge_risks.get("knowledge_silos"):
                st.write("**🏢 Technology Knowledge Silos**")
                st.markdown("Technology areas dominated by single contributors")
                
                silo_data = []
                for risk in knowledge_risks["knowledge_silos"]:
                    silo_data.append({
                        "Technology": risk["technology"],
                        "Primary Expert": risk["primary_contributor"],
                        "Commits": risk.get("commits", risk.get("primary_commits", 0)),
                        "Dominance %": f"{risk.get('dominance_percentage', 100):.1f}%",
                        "Risk Level": risk["risk_level"].upper(),
                        "Risk Explanation": risk["explanation"],
                        "Mitigation Suggestion": risk["mitigation_suggestion"]
                    })
                
                silo_df = pd.DataFrame(silo_data)
                styled_silo = silo_df.style.applymap(highlight_risk_level, subset=['Risk Level'])
                st.dataframe(styled_silo, use_container_width=True)
            
            # Bus Factor Risks
            if knowledge_risks.get("bus_factor_risks"):
                st.write("**🚌 Bus Factor Risks**")
                st.markdown("Contributors critical to project success - high dependency risks")
                
                bus_factor_data = []
                for risk in knowledge_risks["bus_factor_risks"]:
                    bus_factor_data.append({
                        "Contributor": risk.get("contributor", risk.get("primary_contributor", "")),
                        "Primary Files": risk.get("primary_files_count", "N/A"),
                        "Dominance %": f"{risk.get('dominance_percentage', 0):.1f}%",
                        "Risk Level": risk["risk_level"].upper(),
                        "Risk Explanation": risk["explanation"],
                        "Mitigation Suggestion": risk["mitigation_suggestion"]
                    })
                
                bus_df = pd.DataFrame(bus_factor_data)
                styled_bus = bus_df.style.applymap(highlight_risk_level, subset=['Risk Level'])
                st.dataframe(styled_bus, use_container_width=True)
            
            # Critical Files with Limited Knowledge
            if knowledge_risks.get("critical_files_with_few_contributors"):
                st.write("**📁 Critical Files with Limited Knowledge Diversity**")
                st.markdown("Important files with few contributors - knowledge concentration risks")
                
                critical_data = []
                for risk in knowledge_risks["critical_files_with_few_contributors"]:
                    critical_data.append({
                        "File Path": risk["file"],
                        "Total Commits": risk["total_commits"],
                        "Contributor Count": risk["contributor_count"],
                        "Contributors": ", ".join(risk["contributors"]),
                        "Risk Level": risk["risk_level"].upper(),
                        "Risk Explanation": risk["explanation"],
                        "Mitigation Suggestion": risk["mitigation_suggestion"]
                    })
                
                critical_df = pd.DataFrame(critical_data)
                styled_critical = critical_df.style.applymap(highlight_risk_level, subset=['Risk Level'])
                st.dataframe(styled_critical, use_container_width=True)
            
            # Knowledge Risk Visualization
            if (knowledge_risks.get("single_point_failures") or 
                knowledge_risks.get("knowledge_silos") or 
                knowledge_risks.get("bus_factor_risks")):
                
                st.write("**📊 Knowledge Risk Distribution**")
                
                # Create risk level distribution chart
                all_risks = (knowledge_risks.get("single_point_failures", []) + 
                           knowledge_risks.get("knowledge_silos", []) + 
                           knowledge_risks.get("bus_factor_risks", []))
                
                if all_risks:
                    risk_levels = [risk["risk_level"] for risk in all_risks]
                    risk_level_counts = Counter(risk_levels)
                    
                    fig_knowledge_risks = px.bar(
                        x=list(risk_level_counts.keys()),
                        y=list(risk_level_counts.values()),
                        title="Knowledge Risk Levels Distribution",
                        color=list(risk_level_counts.keys()),
                        color_discrete_map={
                            "high": "#ff6b6b", 
                            "medium": "#ffd93d", 
                            "low": "#6bcf7f",
                            "critical": "#d63031"
                        }
                    )
                    st.plotly_chart(fig_knowledge_risks, use_container_width=True)
        else:
            st.info("No knowledge risks detected or analysis failed")
        
        # Enhanced Code Duplication Analysis
        st.subheader("🔍 Code Duplication Analysis")
        st.markdown("Enhanced analysis of code duplication patterns with consolidation opportunities")
        
        enhanced_duplication = analysis.get("enhanced_code_duplication", {})
        duplication_summary = enhanced_duplication.get("duplication_summary", {})
        
        if duplication_summary:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Exact Duplicates", duplication_summary.get("exact_duplicates", 0))
            
            with col2:
                st.metric("Similar Functions", duplication_summary.get("similar_functions", 0))
            
            with col3:
                st.metric("Structural Duplicates", duplication_summary.get("structural_duplicates", 0))
            
            with col4:
                st.metric("Consolidation Opportunities", duplication_summary.get("total_opportunities", 0))
            
            # Consolidation Opportunities
            opportunities = enhanced_duplication.get("consolidation_opportunities", [])
            if opportunities:
                st.write("**💡 Consolidation Opportunities**")
                
                for opportunity in opportunities[:8]:
                    priority_icon = "🔴" if opportunity["priority"] == "high" else "🟡"
                    effort_icon = "🟢" if opportunity["effort"] == "low" else "🟡" if opportunity["effort"] == "medium" else "🔴"
                    
                    st.write(f"{priority_icon} **{opportunity['type']}** {effort_icon}")
                    st.write(f"   {opportunity['description']}")
                    st.write(f"   Priority: {opportunity['priority'].title()} | Effort: {opportunity['effort'].title()}")
                    st.write("")
            
            # Detailed Duplication Tables
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**🎯 Exact Duplicates**")
                exact_duplicates = enhanced_duplication.get("exact_duplicates", [])[:5]
                if exact_duplicates:
                    for dup in exact_duplicates:
                        consolidation_icon = "🔴" if dup["consolidation_potential"] == "high" else "🟡"
                        st.write(f"{consolidation_icon} **{dup['file']}**")
                        st.write(f"   `{dup['content']}`")
                        st.write(f"   Appears {dup['occurrences']} times | Lines: {', '.join(map(str, dup['lines'][:3]))}")
                        st.write("")
                else:
                    st.success("✅ No exact duplicates found")
            
            with col2:
                st.write("**🔄 Similar Functions**") 
                similar_functions = enhanced_duplication.get("similar_functions", [])[:5]
                if similar_functions:
                    for func in similar_functions:
                        st.write(f"📋 **{func['function_name']}()**")
                        st.write(f"   Found in {func['occurrences']} files")
                        st.write(f"   Files: {', '.join(func['files'][:3])}")
                        if len(func['files']) > 3:
                            st.write(f"   ...and {len(func['files']) - 3} more files")
                        st.write("")
                else:
                    st.success("✅ No similar functions across files")
            
            # Duplication Categories Explanation
            with st.expander("ℹ️ Duplication Categories Explained", expanded=False):
                st.write("""
                **🎯 Exact Duplicates**: Identical lines of code appearing multiple times
                - **High consolidation potential**: Extract to constants or methods
                - **Medium consolidation potential**: Consider refactoring if appropriate
                
                **🔄 Similar Functions**: Functions with same name across different files  
                - May indicate opportunity for shared utilities
                - Consider creating common library or base class
                
                **🏗️ Structural Duplicates**: Code with similar structure but different content
                - Look for patterns that can be abstracted
                - Consider template methods or strategy patterns
                """)
        else:
            st.info("No duplication analysis data available")
        
        # Dependency Risks
        st.subheader("📦 Dependency Risks")
        
        dependency_risks = analysis["dependency_risks"]
        if dependency_risks["outdated_dependencies"]:
            dep_df = pd.DataFrame([
                {
                    "File": dep["file"],
                    "Issue": dep["issue"],
                    "Dependency": dep["dependency"],
                    "Severity": dep["severity"]
                }
                for dep in dependency_risks["outdated_dependencies"][:15]
            ])
            
            st.dataframe(dep_df, use_container_width=True)
        else:
            st.info("No dependency files found or no issues detected")
        
        
        # Add save options
        self.add_save_options("risk_analysis", analysis)
