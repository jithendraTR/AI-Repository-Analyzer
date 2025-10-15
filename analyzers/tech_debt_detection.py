"""
Tech Debt Detection Analyzer
Identifies technical debt patterns and code quality issues
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

class TechDebtDetectionAnalyzer(BaseAnalyzer):
    """Analyzes technical debt patterns and code quality issues - Ultra-optimized for performance"""
    
    # Pre-compile all regex patterns at class level for maximum performance
    _COMPLEXITY_PATTERNS = {
        'decisions': re.compile(r'\b(if|else|elif|for|while|try|except|catch|switch|case|and|or|\?|&&|\|\|)\b', re.IGNORECASE),
        'functions': re.compile(r'\b(def|function|public|private|protected)\s+\w+\s*\(', re.IGNORECASE),
        'classes': re.compile(r'\bclass\s+(\w+)', re.IGNORECASE),
        'magic_numbers': re.compile(r'\b(?<![\w.])[2-9]\d*(?:\.\d+)?\b(?![\w.])', re.IGNORECASE)
    }
    
    _COMMENT_PATTERNS = {
        'todo': re.compile(r'#\s*(TODO|FIXME|HACK|NOTE|BUG|OPTIMIZE)[:|\s]*(.*)', re.IGNORECASE),
        'js_comment': re.compile(r'//\s*(TODO|FIXME|HACK|NOTE|BUG|OPTIMIZE)[:|\s]*(.*)', re.IGNORECASE)
    }
    
    _DEPRECATED_PATTERNS = {
        'python': re.compile(r'(import imp\b|\.has_key\(|execfile\()', re.IGNORECASE),
        'javascript': re.compile(r'(var\s+\w+|\.substr\(|escape\()', re.IGNORECASE)
    }
    
    def analyze(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Ultra-optimized analyze method for sub-5-minute performance"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("tech_debt_detection")
        if cached_result:
            return cached_result
        
        try:
            total_steps = 4  # Reduced from 7 steps
            current_step = 0
            
            # Step 1: Quick code smells analysis (limited files)
            if progress_callback:
                progress_callback(current_step, total_steps, "Quick code smells analysis...")
            
            if token:
                token.check_cancellation()
            
            code_smells = self._analyze_code_smells_ultra_fast(token)
            current_step += 1
            
            # Step 2: Fast complexity metrics
            if progress_callback:
                progress_callback(current_step, total_steps, "Fast complexity analysis...")
            
            if token:
                token.check_cancellation()
            
            complexity_metrics = self._analyze_complexity_metrics_ultra_fast(token)
            current_step += 1
            
            # Step 3: Quick TODO/FIXME scan
            if progress_callback:
                progress_callback(current_step, total_steps, "Quick TODO/FIXME scan...")
            
            if token:
                token.check_cancellation()
            
            todo_analysis = self._analyze_todo_comments_ultra_fast(token)
            current_step += 1
            
            # Step 4: Generate summary (skip expensive analyses)
            if progress_callback:
                progress_callback(current_step, total_steps, "Finalizing debt analysis...")
            
            if token:
                token.check_cancellation()
            
            # Skip expensive operations for speed
            deprecated_code = self._analyze_deprecated_code_ultra_fast(token)
            
            # Add new enhanced features
            if progress_callback:
                progress_callback(current_step, total_steps, "Analyzing test coverage gaps...")
            
            test_coverage_gaps = self._analyze_test_coverage_gaps(token)
            
            if progress_callback:
                progress_callback(current_step, total_steps, "Detecting framework inconsistencies...")
            
            framework_inconsistencies = self._analyze_framework_inconsistencies(token)
            
            if progress_callback:
                progress_callback(current_step, total_steps, "Enhanced code duplication analysis...")
                
            enhanced_duplication = self._analyze_code_duplication_enhanced(token)
            
            result = {
                "code_smells": code_smells,
                "complexity_metrics": complexity_metrics,
                "todo_analysis": todo_analysis,
                "deprecated_code": deprecated_code,
                "duplication_analysis": {"duplicate_blocks": [], "duplication_score": 0},  # Skip for speed
                "architectural_debt": {"circular_dependencies": [], "god_classes": []},  # Skip for speed
                "performance_issues": {"performance_antipatterns": []},  # Skip for speed
                "test_coverage_gaps": test_coverage_gaps,  # New feature
                "framework_inconsistencies": framework_inconsistencies,  # New feature
                "enhanced_code_duplication": enhanced_duplication,  # New feature
                "debt_summary": self._generate_debt_summary_ultra_fast(
                    code_smells, complexity_metrics, todo_analysis, deprecated_code
                )
            }
            
            # Cache the result
            self.cache_analysis("tech_debt_detection", result)
            
            return result
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _analyze_code_smells_ultra_fast(self, token=None) -> Dict[str, Any]:
        """Enhanced code smells analysis with proper detection"""
        
        smells = {
            "long_methods": [],
            "large_classes": [],
            "magic_numbers": [],
            "nested_complexity": [],
            "smell_counts": {}
        }
        
        # Limit file processing for speed but provide meaningful results
        source_files = self.get_file_list(['.py', '.js', '.ts'])[:20]  # Slightly more files for better coverage
        
        for file_path in source_files:
            if token:
                token.check_cancellation()
            
            content = self.read_file_content(file_path)
            if not content or len(content) > 100000:  # Skip extremely large files
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            lines = content.split('\n')
            
            # Detect long methods with proper analysis
            self._detect_long_methods(content, relative_path, lines, smells)
            
            # Detect large classes
            self._detect_large_classes(content, relative_path, lines, smells)
            
            # Enhanced magic numbers detection
            self._detect_magic_numbers(content, relative_path, lines, smells)
            
            # Detect nested complexity (deeply nested code)
            self._detect_nested_complexity(content, relative_path, lines, smells)
        
        return smells
    
    def _detect_long_methods(self, content: str, file_path: str, lines: List[str], smells: Dict):
        """Detect long methods with proper line counting"""
        
        if file_path.endswith('.py'):
            # Python function detection
            func_pattern = re.compile(r'^(\s*)def\s+(\w+)\s*\([^)]*\):', re.MULTILINE)
            matches = list(func_pattern.finditer(content))
            
            for i, match in enumerate(matches):
                func_name = match.group(2)
                start_line = content[:match.start()].count('\n') + 1
                indent_level = len(match.group(1))
                
                # Find end of function by looking for next function at same or lower indent level
                end_line = len(lines)
                for j in range(i + 1, len(matches)):
                    next_indent = len(matches[j].group(1))
                    if next_indent <= indent_level:
                        end_line = content[:matches[j].start()].count('\n') + 1
                        break
                
                method_lines = end_line - start_line
                if method_lines > 50:  # Long method threshold
                    smells["long_methods"].append({
                        "file": file_path,
                        "method": func_name,
                        "lines": method_lines,
                        "start_line": start_line,
                        "severity": "high" if method_lines > 100 else "medium",
                        "risk_score": min(method_lines * 2, 100)
                    })
                    smells["smell_counts"]["long_methods"] = smells["smell_counts"].get("long_methods", 0) + 1
        
        elif file_path.endswith(('.js', '.ts')):
            # JavaScript/TypeScript function detection
            func_patterns = [
                re.compile(r'function\s+(\w+)\s*\([^)]*\)\s*\{', re.MULTILINE),
                re.compile(r'(\w+)\s*:\s*function\s*\([^)]*\)\s*\{', re.MULTILINE),
                re.compile(r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{', re.MULTILINE)
            ]
            
            for pattern in func_patterns:
                matches = list(pattern.finditer(content))
                for match in matches:
                    func_name = match.group(1)
                    start_pos = match.start()
                    start_line = content[:start_pos].count('\n') + 1
                    
                    # Simple brace counting to find function end
                    brace_count = 0
                    pos = match.end() - 1  # Start from the opening brace
                    end_pos = len(content)
                    
                    for i in range(pos, len(content)):
                        if content[i] == '{':
                            brace_count += 1
                        elif content[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                end_pos = i
                                break
                    
                    end_line = content[:end_pos].count('\n') + 1
                    method_lines = end_line - start_line
                    
                    if method_lines > 40:  # Long method threshold for JS
                        smells["long_methods"].append({
                            "file": file_path,
                            "method": func_name,
                            "lines": method_lines,
                            "start_line": start_line,
                            "severity": "high" if method_lines > 80 else "medium",
                            "risk_score": min(method_lines * 2.5, 100)
                        })
                        smells["smell_counts"]["long_methods"] = smells["smell_counts"].get("long_methods", 0) + 1
    
    def _detect_large_classes(self, content: str, file_path: str, lines: List[str], smells: Dict):
        """Detect large classes with method counting"""
        
        if file_path.endswith('.py'):
            # Python class detection
            class_pattern = re.compile(r'^(\s*)class\s+(\w+)', re.MULTILINE)
            method_pattern = re.compile(r'^\s+def\s+(\w+)', re.MULTILINE)
            
            class_matches = list(class_pattern.finditer(content))
            
            for i, match in enumerate(class_matches):
                class_name = match.group(2)
                start_line = content[:match.start()].count('\n') + 1
                indent_level = len(match.group(1))
                
                # Find end of class
                end_pos = len(content)
                for j in range(i + 1, len(class_matches)):
                    next_indent = len(class_matches[j].group(1))
                    if next_indent <= indent_level:
                        end_pos = class_matches[j].start()
                        break
                
                class_content = content[match.start():end_pos]
                methods = method_pattern.findall(class_content)
                method_count = len(methods)
                class_lines = class_content.count('\n')
                
                if method_count > 15 or class_lines > 300:  # Large class thresholds
                    smells["large_classes"].append({
                        "file": file_path,
                        "class": class_name,
                        "methods": method_count,
                        "lines": class_lines,
                        "start_line": start_line,
                        "severity": "high" if method_count > 25 or class_lines > 500 else "medium",
                        "complexity_score": min((method_count * 3) + (class_lines // 10), 100)
                    })
                    smells["smell_counts"]["large_classes"] = smells["smell_counts"].get("large_classes", 0) + 1
        
        elif file_path.endswith(('.js', '.ts')):
            # JavaScript/TypeScript class detection
            class_pattern = re.compile(r'class\s+(\w+)', re.MULTILINE)
            method_pattern = re.compile(r'^\s*(\w+)\s*\([^)]*\)\s*\{', re.MULTILINE)
            
            class_matches = list(class_pattern.finditer(content))
            
            for match in class_matches:
                class_name = match.group(1)
                start_line = content[:match.start()].count('\n') + 1
                
                # Simple approximation for class content (until next class or end)
                next_class_pos = len(content)
                for next_match in class_matches:
                    if next_match.start() > match.start():
                        next_class_pos = next_match.start()
                        break
                
                class_content = content[match.start():next_class_pos]
                methods = method_pattern.findall(class_content)
                method_count = len(methods)
                class_lines = class_content.count('\n')
                
                if method_count > 12 or class_lines > 250:
                    smells["large_classes"].append({
                        "file": file_path,
                        "class": class_name,
                        "methods": method_count,
                        "lines": class_lines,
                        "start_line": start_line,
                        "severity": "high" if method_count > 20 or class_lines > 400 else "medium",
                        "complexity_score": min((method_count * 4) + (class_lines // 8), 100)
                    })
                    smells["smell_counts"]["large_classes"] = smells["smell_counts"].get("large_classes", 0) + 1
    
    def _detect_magic_numbers(self, content: str, file_path: str, lines: List[str], smells: Dict):
        """Enhanced magic numbers detection with context"""
        
        # Enhanced regex to avoid false positives
        magic_pattern = re.compile(r'\b(?<![\w\.])[2-9]\d+(?:\.\d+)?(?![\w\.])', re.MULTILINE)
        
        for line_num, line in enumerate(lines, 1):
            # Skip comments, strings, and common patterns
            stripped = line.strip()
            if (stripped.startswith('#') or stripped.startswith('//') or 
                '"' in line or "'" in line or 
                any(keyword in stripped.lower() for keyword in ['version', 'port', 'timeout', 'sleep'])):
                continue
            
            matches = magic_pattern.finditer(line)
            for match in matches:
                number = match.group(0)
                # Skip common non-magic numbers
                if number in ['10', '100', '1000', '60', '24', '365', '2', '3', '4', '5']:
                    continue
                
                context = line.strip()[:80]  # Context around the magic number
                
                smells["magic_numbers"].append({
                    "file": file_path,
                    "line": line_num,
                    "number": number,
                    "context": context,
                    "severity": "medium",
                    "suggestion": f"Consider extracting '{number}' as a named constant"
                })
                
                if len(smells["magic_numbers"]) >= 15:  # Limit results
                    break
            
            if len(smells["magic_numbers"]) >= 15:
                break
        
        if smells["magic_numbers"]:
            smells["smell_counts"]["magic_numbers"] = len(smells["magic_numbers"])
    
    def _detect_nested_complexity(self, content: str, file_path: str, lines: List[str], smells: Dict):
        """Detect deeply nested code structures"""
        
        for line_num, line in enumerate(lines, 1):
            # Count indentation/nesting level
            if file_path.endswith('.py'):
                # Python uses indentation
                indent_level = (len(line) - len(line.lstrip())) // 4  # Assuming 4-space indentation
                if indent_level > 4:  # More than 4 levels of nesting
                    smells["nested_complexity"].append({
                        "file": file_path,
                        "line": line_num,
                        "nesting_depth": indent_level,
                        "content": line.strip()[:60],
                        "severity": "high" if indent_level > 6 else "medium",
                        "suggestion": "Consider extracting nested logic into separate methods"
                    })
                    
            elif file_path.endswith(('.js', '.ts')):
                # JavaScript/TypeScript uses braces
                brace_level = line.count('{') - line.count('}')
                if '{' in line and brace_level > 0:
                    # Rough estimation of nesting depth
                    leading_spaces = len(line) - len(line.lstrip())
                    estimated_depth = leading_spaces // 2  # Rough estimate
                    
                    if estimated_depth > 4:
                        smells["nested_complexity"].append({
                            "file": file_path,
                            "line": line_num,
                            "nesting_depth": estimated_depth,
                            "content": line.strip()[:60],
                            "severity": "high" if estimated_depth > 6 else "medium",
                            "suggestion": "Consider extracting nested logic into separate functions"
                        })
        
        # Limit results and update counts
        smells["nested_complexity"] = smells["nested_complexity"][:10]
        if smells["nested_complexity"]:
            smells["smell_counts"]["nested_complexity"] = len(smells["nested_complexity"])
    
    def _analyze_complexity_metrics_ultra_fast(self, token=None) -> Dict[str, Any]:
        """Ultra-fast complexity analysis using pre-compiled patterns"""
        
        metrics = {
            "cyclomatic_complexity": [],
            "file_complexity": {},
            "complexity_distribution": {"low": 0, "medium": 0, "high": 0}
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts'])[:10]  # Only 10 files
        
        for file_path in source_files:
            if token:
                token.check_cancellation()
            
            content = self.read_file_content(file_path)
            if not content or len(content) > 30000:  # Skip large files
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Ultra-fast complexity calculation using pre-compiled regex
            decision_count = len(self._COMPLEXITY_PATTERNS['decisions'].findall(content))
            complexity = min(decision_count, 50)  # Cap at 50 for performance
            
            if complexity > 15:  # Only track high complexity
                metrics["cyclomatic_complexity"].append({
                    "file": relative_path,
                    "complexity": complexity
                })
            
            metrics["file_complexity"][relative_path] = complexity
            
            # Quick categorization
            if complexity <= 10:
                metrics["complexity_distribution"]["low"] += 1
            elif complexity <= 20:
                metrics["complexity_distribution"]["medium"] += 1
            else:
                metrics["complexity_distribution"]["high"] += 1
        
        return metrics
    
    def _analyze_todo_comments_ultra_fast(self, token=None) -> Dict[str, Any]:
        """Ultra-fast TODO/FIXME analysis"""
        
        analysis = {
            "todo_items": [],
            "fixme_items": [],
            "comment_types": {},
            "priority_distribution": {}
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts'])[:20]  # Limited files
        
        for file_path in source_files:
            if token:
                token.check_cancellation()
            
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Use pre-compiled patterns for speed
            for pattern_name, pattern in self._COMMENT_PATTERNS.items():
                matches = pattern.finditer(content)
                
                for match in matches:
                    comment_type = match.group(1).upper()
                    comment_text = match.group(2).strip() if len(match.groups()) > 1 else ""
                    
                    # Quick line calculation
                    line_num = content[:match.start()].count('\n') + 1
                    
                    item = {
                        "file": relative_path,
                        "line": line_num,
                        "type": comment_type,
                        "text": comment_text[:100],  # Truncate for speed
                        "priority": "high" if comment_type == "FIXME" else "medium"
                    }
                    
                    if comment_type == "TODO":
                        analysis["todo_items"].append(item)
                    elif comment_type == "FIXME":
                        analysis["fixme_items"].append(item)
                    
                    analysis["comment_types"][comment_type] = analysis["comment_types"].get(comment_type, 0) + 1
                    analysis["priority_distribution"][item["priority"]] = analysis["priority_distribution"].get(item["priority"], 0) + 1
        
        return analysis
    
    def _analyze_deprecated_code_ultra_fast(self, token=None) -> Dict[str, Any]:
        """Ultra-fast deprecated code analysis"""
        
        deprecated = {
            "deprecated_patterns": []
        }
        
        source_files = self.get_file_list(['.py', '.js'])[:10]  # Very limited
        
        for file_path in source_files:
            if token:
                token.check_cancellation()
            
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            file_ext = file_path.suffix
            
            # Use pre-compiled patterns
            if file_ext == '.py' and 'python' in self._DEPRECATED_PATTERNS:
                pattern = self._DEPRECATED_PATTERNS['python']
                matches = pattern.finditer(content)
            elif file_ext == '.js' and 'javascript' in self._DEPRECATED_PATTERNS:
                pattern = self._DEPRECATED_PATTERNS['javascript']
                matches = pattern.finditer(content)
            else:
                continue
            
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                deprecated["deprecated_patterns"].append({
                    "file": relative_path,
                    "line": line_num,
                    "pattern": match.group(0),
                    "context": match.group(0)
                })
        
        return deprecated
    
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
    
    def _analyze_framework_inconsistencies(self, token=None) -> Dict[str, Any]:
        """Analyze framework and approach inconsistencies across the codebase"""
        
        inconsistencies = {
            "http_clients": [],
            "date_handling": [],
            "logging": [],
            "configuration": [],
            "testing_frameworks": [],
            "inconsistency_summary": {}
        }
        
        # Patterns to detect different approaches for same functionality
        framework_patterns = {
            "http_clients": {
                "requests": re.compile(r'import requests|from requests', re.IGNORECASE),
                "urllib": re.compile(r'import urllib|from urllib', re.IGNORECASE),
                "httpx": re.compile(r'import httpx|from httpx', re.IGNORECASE),
                "aiohttp": re.compile(r'import aiohttp|from aiohttp', re.IGNORECASE),
                "fetch": re.compile(r'fetch\s*\(', re.IGNORECASE),
                "axios": re.compile(r'import axios|from axios', re.IGNORECASE)
            },
            "date_handling": {
                "datetime": re.compile(r'from datetime import|import datetime', re.IGNORECASE),
                "arrow": re.compile(r'import arrow', re.IGNORECASE),
                "pendulum": re.compile(r'import pendulum', re.IGNORECASE),
                "moment": re.compile(r'import moment|require.*moment', re.IGNORECASE),
                "dayjs": re.compile(r'import dayjs|require.*dayjs', re.IGNORECASE)
            },
            "logging": {
                "logging": re.compile(r'import logging', re.IGNORECASE),
                "loguru": re.compile(r'import loguru|from loguru', re.IGNORECASE),
                "console.log": re.compile(r'console\.log', re.IGNORECASE),
                "winston": re.compile(r'import winston|require.*winston', re.IGNORECASE)
            }
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts'])[:30]  # Limit for performance
        
        # Track usage patterns across files
        usage_tracker = defaultdict(lambda: defaultdict(list))
        
        for file_path in source_files:
            if token:
                token.check_cancellation()
            
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Check for different framework usage patterns
            for category, patterns in framework_patterns.items():
                for framework, pattern in patterns.items():
                    if pattern.search(content):
                        usage_tracker[category][framework].append(relative_path)
        
        # Identify inconsistencies (multiple frameworks used for same purpose)
        for category, framework_usage in usage_tracker.items():
            if len(framework_usage) > 1:  # Multiple frameworks used
                frameworks_used = list(framework_usage.keys())
                total_files = sum(len(files) for files in framework_usage.values())
                
                inconsistency_info = {
                    "category": category.replace('_', ' ').title(),
                    "frameworks_used": frameworks_used,
                    "total_affected_files": total_files,
                    "details": []
                }
                
                for framework, files in framework_usage.items():
                    inconsistency_info["details"].append({
                        "framework": framework,
                        "files": files[:5],  # Limit to first 5 files
                        "file_count": len(files)
                    })
                
                inconsistencies[category] = inconsistency_info
        
        # Generate summary
        total_inconsistencies = len([cat for cat, data in inconsistencies.items() 
                                   if isinstance(data, dict) and data.get("frameworks_used")])
        
        inconsistencies["inconsistency_summary"] = {
            "total_categories_with_inconsistencies": total_inconsistencies,
            "most_problematic_category": max(
                [(cat, data.get("total_affected_files", 0)) for cat, data in inconsistencies.items() 
                 if isinstance(data, dict) and "total_affected_files" in data],
                key=lambda x: x[1], default=("none", 0)
            )[0] if total_inconsistencies > 0 else "none"
        }
        
        return inconsistencies
    
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

    def _generate_debt_summary_ultra_fast(self, code_smells: Dict, complexity_metrics: Dict, 
                                         todo_analysis: Dict, deprecated_code: Dict) -> Dict[str, Any]:
        
        # Quick counting without deep analysis
        smell_count = sum(len(items) for items in code_smells.values() if isinstance(items, list))
        complexity_count = len(complexity_metrics.get("cyclomatic_complexity", []))
        todo_count = sum(len(items) for items in todo_analysis.values() if isinstance(items, list))
        deprecated_count = len(deprecated_code.get("deprecated_patterns", []))
        
        total_items = smell_count + complexity_count + todo_count + deprecated_count
        
        # Simple debt score calculation
        debt_score = min(total_items * 2, 100)
        
        return {
            "total_debt_items": total_items,
            "debt_score": debt_score,
            "critical_issues": deprecated_count + len(todo_analysis.get("fixme_items", [])),
            "debt_categories": {
                "code_smells": smell_count,
                "complexity": complexity_count,
                "todos": todo_count,
                "deprecated": deprecated_count
            }
        }
    
    def render(self):
        """Render the technical debt analysis"""
        # Add rerun button
        self.add_rerun_button("tech_debt_detection")
        
        with self.display_loading_message("Analyzing technical debt..."):
            analysis = self.analyze()
        
        if "error" in analysis:
            self.display_error(analysis["error"])
            return
        
        # Debt Summary
        st.subheader("📊 Technical Debt Summary")
        
        debt_summary = analysis["debt_summary"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Debt Score", f"{debt_summary['debt_score']}/100")
        
        with col2:
            st.metric("Total Issues", debt_summary["total_debt_items"])
        
        with col3:
            st.metric("Critical Issues", debt_summary["critical_issues"])
        
        with col4:
            debt_categories = dict(debt_summary["debt_categories"])
            main_category = max(debt_categories.items(), key=lambda x: x[1])[0] if debt_categories else "None"
            st.metric("Main Category", main_category.title())
        
        # Code Smells Analysis
        st.subheader("👃 Code Smells")
        
        code_smells = analysis["code_smells"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Smell Distribution**")
            smell_counts = dict(code_smells["smell_counts"])
            if smell_counts:
                fig = px.pie(
                    values=list(smell_counts.values()),
                    names=list(smell_counts.keys()),
                    title="Code Smell Types"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Top Issues**")
            
            # Show top long methods
            long_methods = code_smells["long_methods"][:5]
            if long_methods:
                st.write("**Long Methods:**")
                for method in long_methods:
                    severity_icon = "🔴" if method.get("severity") == "high" else "🟡"
                    st.write(f"{severity_icon} {method['method']} ({method['lines']} lines) - {method['file']}")
            
            # Show top large classes
            large_classes = code_smells["large_classes"][:3]
            if large_classes:
                st.write("**Large Classes:**")
                for cls in large_classes:
                    severity_icon = "🔴" if cls.get("severity") == "high" else "🟡"
                    st.write(f"{severity_icon} {cls['class']} ({cls['methods']} methods) - {cls['file']}")

        # Enhanced Detailed Code Smells Section
        with st.expander("🔍 Detailed Code Smells", expanded=False):
            
            # Long Methods Section
            st.write("### 📏 Long Methods")
            if long_methods:
                long_methods_data = []
                for method in code_smells["long_methods"][:10]:
                    long_methods_data.append({
                        "File": method["file"],
                        "Method": method["method"],
                        "Lines": method["lines"],
                        "Severity": method.get("severity", "medium"),
                        "Risk Score": method.get("risk_score", 0)
                    })
                
                df_methods = pd.DataFrame(long_methods_data)
                st.dataframe(df_methods, use_container_width=True)
            else:
                st.success("✅ No long methods detected")
            
            st.write("---")
            
            # Large Classes Section
            st.write("### 🏢 Large Classes")
            if large_classes:
                large_classes_data = []
                for cls in code_smells["large_classes"][:10]:
                    large_classes_data.append({
                        "File": cls["file"],
                        "Class": cls["class"],
                        "Methods": cls["methods"],
                        "Lines": cls["lines"],
                        "Severity": cls.get("severity", "medium"),
                        "Complexity Score": cls.get("complexity_score", 0)
                    })
                
                df_classes = pd.DataFrame(large_classes_data)
                st.dataframe(df_classes, use_container_width=True)
            else:
                st.success("✅ No large classes detected")
            
            st.write("---")
            
            # Magic Numbers Section
            st.write("### 🔢 Magic Numbers")
            magic_numbers = code_smells.get("magic_numbers", [])
            if magic_numbers:
                magic_data = []
                for magic in magic_numbers[:15]:
                    magic_data.append({
                        "File": magic["file"],
                        "Line": magic["line"],
                        "Magic Number": magic["number"],
                        "Context": magic["context"][:50] + "..." if len(magic["context"]) > 50 else magic["context"]
                    })
                
                df_magic = pd.DataFrame(magic_data)
                st.dataframe(df_magic, use_container_width=True)
            else:
                st.success("✅ No magic numbers detected")
            
            st.write("---")
            
            # Nested Complexity Section
            st.write("### 🌀 Nested Complexity")
            nested_complexity = code_smells.get("nested_complexity", [])
            if nested_complexity:
                nested_data = []
                for nested in nested_complexity:
                    nested_data.append({
                        "File": nested["file"],
                        "Line": nested["line"],
                        "Nesting Depth": nested["nesting_depth"],
                        "Severity": nested.get("severity", "medium"),
                        "Code": nested["content"]
                    })
                
                df_nested = pd.DataFrame(nested_data)
                st.dataframe(df_nested, use_container_width=True)
            else:
                st.success("✅ No deeply nested code detected")
        
        # Complexity Analysis
        st.subheader("🔄 Complexity Metrics")
        
        complexity_metrics = analysis["complexity_metrics"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Complexity Distribution**")
            complexity_dist = dict(complexity_metrics["complexity_distribution"])
            if complexity_dist:
                fig = px.bar(
                    x=list(complexity_dist.keys()),
                    y=list(complexity_dist.values()),
                    title="Complexity Levels"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**High Complexity Files**")
            high_complexity = complexity_metrics["cyclomatic_complexity"][:10]
            if high_complexity:
                for item in high_complexity:
                    st.write(f"• {item['file']}: {item['complexity']}")
            else:
                st.success("No high complexity files detected")
        
        # TODO/FIXME Analysis
        st.subheader("📝 TODO & FIXME Analysis")
        
        todo_analysis = analysis["todo_analysis"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Comment Types**")
            comment_types = dict(todo_analysis["comment_types"])
            if comment_types:
                fig = px.bar(
                    x=list(comment_types.keys()),
                    y=list(comment_types.values()),
                    title="Comment Type Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Priority Distribution**")
            priority_dist = dict(todo_analysis["priority_distribution"])
            if priority_dist:
                fig = px.pie(
                    values=list(priority_dist.values()),
                    names=list(priority_dist.keys()),
                    title="Priority Levels"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # High Priority Items
        st.write("**High Priority Items**")
        high_priority_items = []
        
        for item_list in [todo_analysis["fixme_items"], todo_analysis["todo_items"]]:
            high_priority_items.extend([item for item in item_list if item.get("priority") == "high"])
        
        if high_priority_items:
            for item in high_priority_items[:10]:
                st.write(f"• **{item['type']}**: {item['text']} ({item['file']}:{item['line']})")
        else:
            st.success("No high priority items found")

        # NEW FEATURE 1: Test Coverage Gaps
        st.subheader("🧪 Test Coverage Risk Assessment")
        
        test_coverage = analysis.get("test_coverage_gaps", {})
        coverage_summary = test_coverage.get("coverage_summary", {})
        
        if coverage_summary:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Coverage %", f"{coverage_summary.get('coverage_percentage', 0)}%")
            
            with col2:
                st.metric("Files Without Tests", coverage_summary.get('files_without_tests', 0))
            
            with col3:
                st.metric("High Risk Files", coverage_summary.get('high_risk_uncovered', 0))
            
            with col4:
                st.metric("Total Source Files", coverage_summary.get('total_source_files', 0))
            
            # Risk Categories Chart
            col1, col2 = st.columns(2)
            
            with col1:
                risk_categories = test_coverage.get("risk_categories", {})
                if any(risk_categories.values()):
                    fig = px.pie(
                        values=list(risk_categories.values()),
                        names=[f"{k.title()} Risk" for k in risk_categories.keys()],
                        title="Risk Distribution of Untested Files",
                        color_discrete_map={
                            'Critical Risk': '#ff4444',
                            'High Risk': '#ff8800', 
                            'Medium Risk': '#ffaa00',
                            'Low Risk': '#44aa44'
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("**🔴 High Risk Untested Files**")
                high_risk_files = test_coverage.get("high_risk_files", [])[:8]
                if high_risk_files:
                    for file_info in high_risk_files:
                        risk_icon = "🔴" if file_info["risk_level"] == "critical" else "🟠"
                        st.write(f"{risk_icon} **{file_info['file']}** ({file_info['file_type']})")
                        st.write(f"   Risk Score: {file_info['risk_score']}/100")
                        st.write(f"   Reasons: {', '.join(file_info['reasons'][:2])}")
                        st.write("")
                else:
                    st.success("✅ No high-risk untested files detected")
            
            # Detailed Test Coverage Table
            with st.expander("📋 Detailed Coverage Analysis", expanded=False):
                uncovered_files = test_coverage.get("uncovered_files", [])
                if uncovered_files:
                    df = pd.DataFrame(uncovered_files)
                    # Add risk level colors
                    def color_risk_level(val):
                        colors = {'critical': '#ff4444', 'high': '#ff8800', 'medium': '#ffaa00', 'low': '#44aa44'}
                        return f'background-color: {colors.get(val, "#ffffff")}'
                    
                    styled_df = df.style.applymap(color_risk_level, subset=['risk_level'])
                    st.dataframe(styled_df, use_container_width=True)
                else:
                    st.success("🎉 All source files have corresponding tests!")

        # NEW FEATURE 2: Framework Inconsistencies
        st.subheader("⚖️ Framework Inconsistencies")
        
        inconsistencies = analysis.get("framework_inconsistencies", {})
        inconsistency_summary = inconsistencies.get("inconsistency_summary", {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            total_inconsistencies = inconsistency_summary.get("total_categories_with_inconsistencies", 0)
            st.metric("Inconsistent Categories", total_inconsistencies)
            
            if total_inconsistencies > 0:
                most_problematic = inconsistency_summary.get("most_problematic_category", "none")
                st.info(f"💡 **Most Problematic**: {most_problematic.replace('_', ' ').title()}")
        
        with col2:
            # Show framework inconsistency chart if any exist
            inconsistency_data = []
            for category, data in inconsistencies.items():
                if isinstance(data, dict) and "frameworks_used" in data:
                    inconsistency_data.append({
                        "Category": data["category"],
                        "Frameworks": len(data["frameworks_used"]),
                        "Affected Files": data["total_affected_files"]
                    })
            
            if inconsistency_data:
                df = pd.DataFrame(inconsistency_data)
                fig = px.bar(df, x="Category", y="Affected Files", title="Framework Inconsistencies by Category")
                st.plotly_chart(fig, use_container_width=True)
        
        # Detailed Framework Inconsistencies
        if total_inconsistencies > 0:
            with st.expander("🔍 Framework Inconsistency Details", expanded=False):
                for category, data in inconsistencies.items():
                    if isinstance(data, dict) and "frameworks_used" in data:
                        st.write(f"**{data['category']} Inconsistencies**")
                        st.write(f"Multiple frameworks detected: {', '.join(data['frameworks_used'])}")
                        
                        # Create table showing framework usage
                        detail_data = []
                        for detail in data["details"]:
                            detail_data.append({
                                "Framework": detail["framework"],
                                "Files Using": detail["file_count"],
                                "Example Files": ", ".join(detail["files"][:3])
                            })
                        
                        if detail_data:
                            detail_df = pd.DataFrame(detail_data)
                            st.dataframe(detail_df, use_container_width=True)
                            
                            st.warning(f"💡 **Recommendation**: Standardize on one {data['category'].lower()} approach across the codebase")
                        st.write("---")
        else:
            st.success("✅ No framework inconsistencies detected - codebase uses consistent approaches")

        # NEW FEATURE 3: Enhanced Code Duplication
        st.subheader("🔍 Code Duplication Analysis")
        
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
        
        # Display AI insights from parallel analysis if available
        self.display_parallel_ai_insights("tech_debt_detection")
        
        # Add save options
        self.add_save_options("tech_debt_detection", analysis)
