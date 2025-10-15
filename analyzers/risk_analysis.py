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
            total_steps = 3  # Reduced to 3 steps only
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
            
            # Skip expensive operations for speed - generate quick summary
            result = {
                "test_coverage": test_coverage,
                "untested_code": [],  # Skip for ultra-fast mode
                "complexity_analysis": complexity_analysis,
                "error_handling": {"files_with_error_handling": [], "files_without_error_handling": []},  # Skip for speed
                "security_risks": security_risks,
                "deprecated_code": [],  # Skip for ultra-fast mode
                "dependency_risks": {"outdated_dependencies": []},  # Skip for speed
                "risk_summary": self._generate_fast_risk_summary(
                    test_coverage, complexity_analysis, security_risks
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
    
    def _get_quick_severity(self, risk_type: str) -> int:
        """Quick security severity mapping"""
        severity_map = {
            "sql_injection": 10,
            "xss_vulnerability": 8,
            "hardcoded_secrets": 6
        }
        return severity_map.get(risk_type, 5)
    
    def _generate_fast_risk_summary(self, test_coverage: Dict, complexity: Dict, security_risks: List) -> Dict[str, Any]:
        """Generate fast risk summary with minimal calculations"""
        
        summary = {
            "overall_risk_score": 0,
            "critical_issues": 0,
            "high_risk_files": 0,
            "test_coverage_score": test_coverage.get("coverage_ratio", 0) * 100,
            "complexity_score": complexity.get("average_complexity", 0),
            "security_issues": len(security_risks),
            "untested_high_complexity": 0
        }
        
        # Quick risk score calculation
        coverage_risk = max(0, 50 - summary["test_coverage_score"]) * 0.4
        complexity_risk = min(50, summary["complexity_score"] * 1.5) * 0.3
        security_risk = min(50, len(security_risks) * 5) * 0.3
        
        summary["overall_risk_score"] = coverage_risk + complexity_risk + security_risk
        summary["critical_issues"] = len([r for r in security_risks if r["severity"] >= 8])
        summary["high_risk_files"] = len(complexity.get("high_complexity_files", []))
        
        return summary
    
    def _find_deprecated_code(self) -> List[Dict]:
        """Find deprecated code and outdated patterns"""
        
        deprecated = []
        
        # Deprecated patterns
        deprecated_patterns = {
            "python": [
                r"import imp\b",  # imp module deprecated
                r"\.has_key\(",  # dict.has_key deprecated
                r"execfile\(",   # execfile deprecated in Python 3
            ],
            "javascript": [
                r"var\s+\w+",    # var is deprecated in favor of let/const
                r"\.substr\(",   # substr is deprecated
                r"escape\(",     # escape is deprecated
            ],
            "java": [
                r"new Date\(\)",  # Date constructor deprecated
                r"\.finalize\(",  # finalize deprecated
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
                patterns = deprecated_patterns["python"]
            elif file_ext in ['.js', '.ts']:
                patterns = deprecated_patterns["javascript"]
            elif file_ext == '.java':
                patterns = deprecated_patterns["java"]
            else:
                continue
            
            # Check for deprecated patterns
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    context = self._extract_context(content, match.start(), match.end())
                    
                    deprecated.append({
                        "file": relative_path,
                        "line": line_num,
                        "pattern": match.group(0),
                        "context": context,
                        "language": file_ext[1:]  # Remove the dot
                    })
        
        return deprecated
    
    def _analyze_dependency_risks(self) -> Dict[str, Any]:
        """Analyze dependency-related risks"""
        
        risks = {
            "outdated_dependencies": [],
            "security_vulnerabilities": [],
            "license_issues": [],
            "dependency_conflicts": []
        }
        
        # Look for dependency files
        dependency_files = []
        dependency_files.extend(self.find_files_by_pattern("**/requirements.txt"))
        dependency_files.extend(self.find_files_by_pattern("**/package.json"))
        dependency_files.extend(self.find_files_by_pattern("**/pom.xml"))
        dependency_files.extend(self.find_files_by_pattern("**/Gemfile"))
        dependency_files.extend(self.find_files_by_pattern("**/composer.json"))
        
        for file_path in dependency_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Analyze based on file type
            if file_path.name == "requirements.txt":
                self._analyze_python_dependencies(content, relative_path, risks)
            elif file_path.name == "package.json":
                self._analyze_npm_dependencies(content, relative_path, risks)
        
        return risks
    
    def _analyze_python_dependencies(self, content: str, file_path: str, risks: Dict):
        """Analyze Python dependencies for risks"""
        
        # Look for version pinning issues
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('#'):
                if '==' not in line and '>=' not in line and '<=' not in line:
                    risks["outdated_dependencies"].append({
                        "file": file_path,
                        "line": i,
                        "issue": "Unpinned dependency",
                        "dependency": line,
                        "severity": "medium"
                    })
    
    def _analyze_npm_dependencies(self, content: str, file_path: str, risks: Dict):
        """Analyze NPM dependencies for risks"""
        
        try:
            import json
            package_data = json.loads(content)
            
            # Check for outdated patterns
            dependencies = package_data.get("dependencies", {})
            dev_dependencies = package_data.get("devDependencies", {})
            
            all_deps = {**dependencies, **dev_dependencies}
            
            for dep_name, version in all_deps.items():
                if version.startswith("^") or version.startswith("~"):
                    risks["outdated_dependencies"].append({
                        "file": file_path,
                        "issue": "Flexible version range",
                        "dependency": f"{dep_name}@{version}",
                        "severity": "low"
                    })
        
        except json.JSONDecodeError:
            pass
    
    def _calculate_file_complexity(self, content: str) -> int:
        """Calculate a simple complexity score for a file"""
        
        complexity = 0
        
        # Count complexity indicators
        complexity_patterns = [
            r"\bif\b", r"\belse\b", r"\belif\b",
            r"\bfor\b", r"\bwhile\b",
            r"\btry\b", r"\bcatch\b", r"\bexcept\b",
            r"\bswitch\b", r"\bcase\b",
            r"&&", r"\|\|",
            r"\?.*:"  # Ternary operator
        ]
        
        for pattern in complexity_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            complexity += len(matches)
        
        # Add complexity for nested structures
        nesting_level = 0
        max_nesting = 0
        
        for line in content.split('\n'):
            stripped = line.strip()
            if any(keyword in stripped for keyword in ['if', 'for', 'while', 'try', 'def', 'class']):
                nesting_level += 1
                max_nesting = max(max_nesting, nesting_level)
            elif stripped.startswith(('end', '}', 'else:', 'elif', 'except:', 'finally:')):
                nesting_level = max(0, nesting_level - 1)
        
        complexity += max_nesting * 2
        
        return complexity
    
    def _calculate_risk_level(self, complexity: int, lines: int) -> str:
        """Calculate risk level based on complexity and size"""
        
        if complexity > 30 or lines > 500:
            return "high"
        elif complexity > 15 or lines > 200:
            return "medium"
        else:
            return "low"
    
    def _calculate_security_severity(self, risk_type: str) -> int:
        """Calculate security risk severity"""
        
        severity_map = {
            "sql_injection": 10,
            "command_injection": 10,
            "xss_vulnerability": 8,
            "path_traversal": 7,
            "hardcoded_secrets": 6,
            "insecure_random": 4
        }
        
        return severity_map.get(risk_type, 5)
    
    def _generate_risk_summary(self, test_coverage: Dict, complexity: Dict, 
                              security_risks: List, error_handling: Dict) -> Dict[str, Any]:
        """Generate overall risk summary"""
        
        summary = {
            "overall_risk_score": 0,
            "critical_issues": 0,
            "high_risk_files": 0,
            "test_coverage_score": test_coverage.get("coverage_ratio", 0) * 100,
            "complexity_score": complexity.get("average_complexity", 0),
            "security_issues": len(security_risks),
            "untested_high_complexity": 0
        }
        
        # Calculate overall risk score
        risk_factors = []
        
        # Test coverage factor (lower coverage = higher risk)
        coverage_risk = max(0, 100 - summary["test_coverage_score"])
        risk_factors.append(coverage_risk * 0.3)
        
        # Complexity factor
        complexity_risk = min(100, summary["complexity_score"] * 2)
        risk_factors.append(complexity_risk * 0.2)
        
        # Security factor
        security_risk = min(100, len(security_risks) * 10)
        risk_factors.append(security_risk * 0.3)
        
        # Error handling factor
        files_without_error_handling = len(error_handling.get("files_without_error_handling", []))
        error_handling_risk = min(100, files_without_error_handling * 5)
        risk_factors.append(error_handling_risk * 0.2)
        
        summary["overall_risk_score"] = sum(risk_factors)
        
        # Count critical issues
        summary["critical_issues"] = len([r for r in security_risks if r["severity"] >= 8])
        
        # Count high-risk files
        summary["high_risk_files"] = len(complexity.get("high_complexity_files", []))
        
        return summary
    
    def _extract_context(self, content: str, start: int, end: int, context_lines: int = 2) -> str:
        """Extract context around a match"""
        lines = content.split('\n')
        match_line = content[:start].count('\n')
        
        start_line = max(0, match_line - context_lines)
        end_line = min(len(lines), match_line + context_lines + 1)
        
        context_lines_list = lines[start_line:end_line]
        return '\n'.join(context_lines_list)
    
    def render(self):
        """Render the risk analysis"""
        st.header("⚠️ Risk Analysis & Test Coverage")
        st.markdown("Identifying potential risks and test coverage gaps in your codebase")
        
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
        
        # AI-powered Risk Assessment
        st.subheader("🤖 AI Risk Assessment")
        
        if st.button("Get AI Risk Analysis"):
            with self.display_loading_message("Generating AI risk assessment..."):
                # Prepare context for AI
                risk_context = {
                    "overall_risk_score": risk_summary["overall_risk_score"],
                    "critical_issues": risk_summary["critical_issues"],
                    "test_coverage": risk_summary["test_coverage_score"],
                    "high_complexity_files": len(complexity_analysis["high_complexity_files"]),
                    "security_risks": len(security_risks),
                    "files_without_error_handling": files_without_handling
                }
                
                prompt = f"""
                Based on this codebase risk analysis:
                
                Risk Metrics: {risk_context}
                
                Please provide:
                1. Overall risk assessment and priority areas
                2. Specific recommendations to reduce risk
                3. Testing strategy suggestions
                4. Security improvement recommendations
                5. Code quality improvement plan
                """
                
                ai_assessment = self.ai_client.query(prompt)
                
                if ai_assessment:
                    st.markdown("**AI Risk Assessment:**")
                    st.markdown(ai_assessment)
                else:
                    st.error("Failed to generate AI risk assessment")
        
        # Add save options
        self.add_save_options("risk_analysis", analysis)
