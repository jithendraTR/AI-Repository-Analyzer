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
    """Analyzes technical debt patterns and code quality issues"""
    
    def analyze(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Analyze technical debt patterns"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("tech_debt_detection")
        if cached_result:
            return cached_result
        
        # Analyze code smells
        code_smells = self._analyze_code_smells()
        
        # Analyze complexity metrics
        complexity_metrics = self._analyze_complexity_metrics()
        
        # Analyze TODO/FIXME comments
        todo_analysis = self._analyze_todo_comments()
        
        # Analyze deprecated code
        deprecated_code = self._analyze_deprecated_code()
        
        # Analyze code duplication
        duplication_analysis = self._analyze_code_duplication()
        
        # Analyze architectural debt
        architectural_debt = self._analyze_architectural_debt()
        
        # Analyze performance issues
        performance_issues = self._analyze_performance_issues()
        
        result = {
            "code_smells": code_smells,
            "complexity_metrics": complexity_metrics,
            "todo_analysis": todo_analysis,
            "deprecated_code": deprecated_code,
            "duplication_analysis": duplication_analysis,
            "architectural_debt": architectural_debt,
            "performance_issues": performance_issues,
            "debt_summary": self._generate_debt_summary(
                code_smells, complexity_metrics, todo_analysis, deprecated_code
            )
        }
        
        # Cache the result
        self.cache_analysis("tech_debt_detection", result)
        
        return result
    
    def _analyze_code_smells(self) -> Dict[str, Any]:
        """Analyze code smells and anti-patterns"""
        
        smells = {
            "long_methods": [],
            "large_classes": [],
            "god_objects": [],
            "dead_code": [],
            "magic_numbers": [],
            "long_parameter_lists": [],
            "nested_conditionals": [],
            "smell_counts": defaultdict(int)
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        
        for file_path in source_files[:50]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            lines = content.split('\n')
            
            # Analyze long methods
            self._detect_long_methods(content, file_path, smells)
            
            # Analyze large classes
            self._detect_large_classes(content, file_path, smells)
            
            # Analyze magic numbers
            self._detect_magic_numbers(content, file_path, smells)
            
            # Analyze long parameter lists
            self._detect_long_parameter_lists(content, file_path, smells)
            
            # Analyze nested conditionals
            self._detect_nested_conditionals(content, file_path, smells)
            
            # Analyze dead code
            self._detect_dead_code(content, file_path, smells)
        
        return smells
    
    def _detect_long_methods(self, content: str, file_path: Path, smells: Dict):
        """Detect methods that are too long"""
        
        # Python function detection
        function_pattern = r'def\s+(\w+)\s*\([^)]*\):'
        functions = re.finditer(function_pattern, content)
        
        lines = content.split('\n')
        
        for func_match in functions:
            func_name = func_match.group(1)
            start_line = content[:func_match.start()].count('\n')
            
            # Find function end (simplified)
            indent_level = len(lines[start_line]) - len(lines[start_line].lstrip())
            end_line = start_line + 1
            
            for i in range(start_line + 1, len(lines)):
                line = lines[i]
                if line.strip() and len(line) - len(line.lstrip()) <= indent_level and not line.strip().startswith('#'):
                    end_line = i
                    break
            
            method_length = end_line - start_line
            
            if method_length > 50:  # Threshold for long methods
                smells["long_methods"].append({
                    "file": str(file_path.relative_to(self.repo_path)),
                    "method": func_name,
                    "lines": method_length,
                    "start_line": start_line + 1
                })
                smells["smell_counts"]["long_methods"] += 1
    
    def _detect_large_classes(self, content: str, file_path: Path, smells: Dict):
        """Detect classes that are too large"""
        
        # Python class detection
        class_pattern = r'class\s+(\w+).*?:'
        classes = re.finditer(class_pattern, content)
        
        lines = content.split('\n')
        
        for class_match in classes:
            class_name = class_match.group(1)
            start_line = content[:class_match.start()].count('\n')
            
            # Count methods in class
            method_count = 0
            class_lines = 0
            
            # Find class end (simplified)
            indent_level = len(lines[start_line]) - len(lines[start_line].lstrip())
            
            for i in range(start_line + 1, len(lines)):
                line = lines[i]
                if line.strip():
                    if len(line) - len(line.lstrip()) <= indent_level and not line.strip().startswith('#'):
                        break
                    if 'def ' in line:
                        method_count += 1
                    class_lines += 1
            
            if method_count > 20 or class_lines > 200:  # Thresholds for large classes
                smells["large_classes"].append({
                    "file": str(file_path.relative_to(self.repo_path)),
                    "class": class_name,
                    "methods": method_count,
                    "lines": class_lines,
                    "start_line": start_line + 1
                })
                smells["smell_counts"]["large_classes"] += 1
    
    def _detect_magic_numbers(self, content: str, file_path: Path, smells: Dict):
        """Detect magic numbers in code"""
        
        # Pattern for numeric literals (excluding common ones like 0, 1, -1)
        magic_number_pattern = r'\b(?<![\w.])[2-9]\d*(?:\.\d+)?\b(?![\w.])'
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Skip comments and strings
            if line.strip().startswith('#') or line.strip().startswith('//'):
                continue
            
            matches = re.finditer(magic_number_pattern, line)
            for match in matches:
                number = match.group()
                
                # Skip common acceptable numbers
                if number in ['2', '3', '4', '5', '10', '100', '1000']:
                    continue
                
                smells["magic_numbers"].append({
                    "file": str(file_path.relative_to(self.repo_path)),
                    "line": line_num,
                    "number": number,
                    "context": line.strip()
                })
                smells["smell_counts"]["magic_numbers"] += 1
    
    def _detect_long_parameter_lists(self, content: str, file_path: Path, smells: Dict):
        """Detect functions with too many parameters"""
        
        # Function definition patterns
        patterns = [
            r'def\s+(\w+)\s*\(([^)]+)\):',  # Python
            r'function\s+(\w+)\s*\(([^)]+)\)',  # JavaScript
            r'(\w+)\s*\(([^)]+)\)\s*{',  # Java/C-style
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            
            for match in matches:
                func_name = match.group(1)
                params = match.group(2)
                
                # Count parameters (simplified)
                param_count = len([p.strip() for p in params.split(',') if p.strip()])
                
                if param_count > 5:  # Threshold for too many parameters
                    line_num = content[:match.start()].count('\n') + 1
                    
                    smells["long_parameter_lists"].append({
                        "file": str(file_path.relative_to(self.repo_path)),
                        "function": func_name,
                        "parameters": param_count,
                        "line": line_num
                    })
                    smells["smell_counts"]["long_parameter_lists"] += 1
    
    def _detect_nested_conditionals(self, content: str, file_path: Path, smells: Dict):
        """Detect deeply nested conditional statements"""
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Count nesting level based on indentation and if/for/while keywords
            if any(keyword in line for keyword in ['if ', 'for ', 'while ', 'try:']):
                indent_level = (len(line) - len(line.lstrip())) // 4  # Assuming 4-space indentation
                
                if indent_level > 3:  # Threshold for deep nesting
                    smells["nested_conditionals"].append({
                        "file": str(file_path.relative_to(self.repo_path)),
                        "line": line_num,
                        "nesting_level": indent_level,
                        "context": line.strip()
                    })
                    smells["smell_counts"]["nested_conditionals"] += 1
    
    def _detect_dead_code(self, content: str, file_path: Path, smells: Dict):
        """Detect potentially dead code"""
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            stripped_line = line.strip()
            
            # Look for commented out code
            if (stripped_line.startswith('#') and 
                any(keyword in stripped_line for keyword in ['def ', 'class ', 'import ', 'if ', 'for '])):
                
                smells["dead_code"].append({
                    "file": str(file_path.relative_to(self.repo_path)),
                    "line": line_num,
                    "type": "commented_code",
                    "context": stripped_line
                })
                smells["smell_counts"]["dead_code"] += 1
            
            # Look for unreachable code after return statements
            if 'return ' in stripped_line and line_num < len(lines):
                next_line = lines[line_num].strip() if line_num < len(lines) else ""
                if next_line and not next_line.startswith(('def ', 'class ', '#', 'except', 'finally')):
                    smells["dead_code"].append({
                        "file": str(file_path.relative_to(self.repo_path)),
                        "line": line_num + 1,
                        "type": "unreachable_code",
                        "context": next_line
                    })
                    smells["smell_counts"]["dead_code"] += 1
    
    def _analyze_complexity_metrics(self) -> Dict[str, Any]:
        """Analyze code complexity metrics"""
        
        metrics = {
            "cyclomatic_complexity": [],
            "cognitive_complexity": [],
            "file_complexity": defaultdict(int),
            "complexity_distribution": defaultdict(int)
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        
        for file_path in source_files[:30]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            # Calculate cyclomatic complexity (simplified)
            complexity = self._calculate_cyclomatic_complexity(content)
            
            if complexity > 10:  # Threshold for high complexity
                metrics["cyclomatic_complexity"].append({
                    "file": str(file_path.relative_to(self.repo_path)),
                    "complexity": complexity
                })
            
            metrics["file_complexity"][str(file_path.relative_to(self.repo_path))] = complexity
            
            # Categorize complexity
            if complexity <= 5:
                metrics["complexity_distribution"]["low"] += 1
            elif complexity <= 10:
                metrics["complexity_distribution"]["medium"] += 1
            elif complexity <= 20:
                metrics["complexity_distribution"]["high"] += 1
            else:
                metrics["complexity_distribution"]["very_high"] += 1
        
        return metrics
    
    def _calculate_cyclomatic_complexity(self, content: str) -> int:
        """Calculate simplified cyclomatic complexity"""
        
        # Count decision points
        decision_keywords = [
            r'\bif\b', r'\belif\b', r'\belse\b',
            r'\bfor\b', r'\bwhile\b',
            r'\btry\b', r'\bexcept\b',
            r'\band\b', r'\bor\b',
            r'\?', r'&&', r'\|\|'
        ]
        
        complexity = 1  # Base complexity
        
        for keyword in decision_keywords:
            matches = re.findall(keyword, content, re.IGNORECASE)
            complexity += len(matches)
        
        return complexity
    
    def _analyze_todo_comments(self) -> Dict[str, Any]:
        """Analyze TODO, FIXME, and similar comments"""
        
        analysis = {
            "todo_items": [],
            "fixme_items": [],
            "hack_items": [],
            "note_items": [],
            "comment_types": defaultdict(int),
            "priority_distribution": defaultdict(int)
        }
        
        # Comment patterns
        comment_patterns = [
            (r'#\s*(TODO|FIXME|HACK|NOTE|BUG|OPTIMIZE)[:|\s]*(.*)', "python"),
            (r'//\s*(TODO|FIXME|HACK|NOTE|BUG|OPTIMIZE)[:|\s]*(.*)', "javascript"),
            (r'/\*\s*(TODO|FIXME|HACK|NOTE|BUG|OPTIMIZE)[:|\s]*(.*?)\*/', "block_comment")
        ]
        
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java', '.cpp', '.c'])
        
        for file_path in source_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern, comment_type in comment_patterns:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    
                    for match in matches:
                        comment_type_found = match.group(1).upper()
                        comment_text = match.group(2).strip()
                        
                        item = {
                            "file": str(file_path.relative_to(self.repo_path)),
                            "line": line_num,
                            "type": comment_type_found,
                            "text": comment_text,
                            "priority": self._assess_comment_priority(comment_type_found, comment_text)
                        }
                        
                        # Categorize by type
                        if comment_type_found == "TODO":
                            analysis["todo_items"].append(item)
                        elif comment_type_found == "FIXME":
                            analysis["fixme_items"].append(item)
                        elif comment_type_found == "HACK":
                            analysis["hack_items"].append(item)
                        elif comment_type_found == "NOTE":
                            analysis["note_items"].append(item)
                        
                        analysis["comment_types"][comment_type_found] += 1
                        analysis["priority_distribution"][item["priority"]] += 1
        
        return analysis
    
    def _assess_comment_priority(self, comment_type: str, text: str) -> str:
        """Assess priority of TODO/FIXME comments"""
        
        high_priority_keywords = ["urgent", "critical", "asap", "important", "security", "bug"]
        medium_priority_keywords = ["soon", "refactor", "optimize", "improve"]
        
        text_lower = text.lower()
        
        if comment_type in ["FIXME", "BUG"] or any(keyword in text_lower for keyword in high_priority_keywords):
            return "high"
        elif any(keyword in text_lower for keyword in medium_priority_keywords):
            return "medium"
        else:
            return "low"
    
    def _analyze_deprecated_code(self) -> Dict[str, Any]:
        """Analyze deprecated code patterns"""
        
        deprecated = {
            "deprecated_functions": [],
            "deprecated_imports": [],
            "deprecated_patterns": [],
            "deprecation_warnings": []
        }
        
        # Deprecated patterns by language
        deprecated_patterns = {
            "python": [
                (r"@deprecated", "Deprecated decorator"),
                (r"warnings\.warn.*deprecated", "Deprecation warning"),
                (r"import imp\b", "Deprecated imp module"),
                (r"from imp import", "Deprecated imp module")
            ],
            "javascript": [
                (r"@deprecated", "Deprecated JSDoc tag"),
                (r"console\.warn.*deprecated", "Deprecation warning"),
                (r"var\s+\w+", "Deprecated var declaration")
            ]
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        
        for file_path in source_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            file_ext = file_path.suffix
            
            # Determine language patterns
            if file_ext == '.py':
                patterns = deprecated_patterns.get("python", [])
            elif file_ext in ['.js', '.ts']:
                patterns = deprecated_patterns.get("javascript", [])
            else:
                continue
            
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern, description in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        deprecated["deprecated_patterns"].append({
                            "file": str(file_path.relative_to(self.repo_path)),
                            "line": line_num,
                            "pattern": description,
                            "context": line.strip()
                        })
        
        return deprecated
    
    def _analyze_code_duplication(self) -> Dict[str, Any]:
        """Analyze code duplication patterns"""
        
        duplication = {
            "duplicate_blocks": [],
            "similar_functions": [],
            "copy_paste_indicators": [],
            "duplication_score": 0
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        
        # Simple duplication detection based on similar lines
        line_hashes = defaultdict(list)
        
        for file_path in source_files[:20]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # Skip empty lines and comments
                stripped_line = line.strip()
                if len(stripped_line) > 10 and not stripped_line.startswith(('#', '//')):
                    # Simple hash of the line content
                    line_hash = hash(stripped_line)
                    line_hashes[line_hash].append({
                        "file": str(file_path.relative_to(self.repo_path)),
                        "line": line_num,
                        "content": stripped_line
                    })
        
        # Find duplicated lines
        for line_hash, occurrences in line_hashes.items():
            if len(occurrences) > 1:
                duplication["duplicate_blocks"].append({
                    "content": occurrences[0]["content"],
                    "occurrences": occurrences,
                    "count": len(occurrences)
                })
        
        # Calculate duplication score
        total_duplicates = sum(len(block["occurrences"]) for block in duplication["duplicate_blocks"])
        total_lines = sum(len(self.read_file_content(f).split('\n')) for f in source_files[:20] if self.read_file_content(f))
        
        if total_lines > 0:
            duplication["duplication_score"] = (total_duplicates / total_lines) * 100
        
        return duplication
    
    def _analyze_architectural_debt(self) -> Dict[str, Any]:
        """Analyze architectural debt patterns"""
        
        architectural = {
            "circular_dependencies": [],
            "god_classes": [],
            "tight_coupling": [],
            "violation_patterns": []
        }
        
        # Analyze import patterns for circular dependencies
        import_graph = defaultdict(set)
        
        source_files = self.get_file_list(['.py', '.js', '.ts'])
        
        for file_path in source_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            file_name = file_path.stem
            
            # Extract imports
            import_patterns = [
                r'from\s+(\w+)\s+import',  # Python from import
                r'import\s+(\w+)',  # Python import
                r'import\s+.*from\s+["\']([^"\']+)["\']',  # ES6 import
                r'require\(["\']([^"\']+)["\']\)'  # CommonJS require
            ]
            
            for pattern in import_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if isinstance(match, tuple):
                        imported_module = match[0] if match[0] else match[1]
                    else:
                        imported_module = match
                    
                    if imported_module and imported_module != file_name:
                        import_graph[file_name].add(imported_module)
        
        # Simple circular dependency detection
        for module, imports in import_graph.items():
            for imported in imports:
                if imported in import_graph and module in import_graph[imported]:
                    architectural["circular_dependencies"].append({
                        "module1": module,
                        "module2": imported,
                        "type": "circular_import"
                    })
        
        return architectural
    
    def _analyze_performance_issues(self) -> Dict[str, Any]:
        """Analyze potential performance issues"""
        
        performance = {
            "inefficient_loops": [],
            "memory_leaks": [],
            "blocking_operations": [],
            "performance_antipatterns": []
        }
        
        # Performance anti-patterns
        antipatterns = [
            (r'for.*in.*range\(len\(', "Inefficient loop pattern"),
            (r'\.append\(.*\)\s*$', "List append in loop"),
            (r'time\.sleep\(', "Blocking sleep operation"),
            (r'while\s+True:', "Infinite loop pattern"),
            (r'\.find\(.*\)\s*!=\s*-1', "Inefficient string search")
        ]
        
        source_files = self.get_file_list(['.py', '.js', '.ts'])
        
        for file_path in source_files[:30]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern, description in antipatterns:
                    if re.search(pattern, line):
                        performance["performance_antipatterns"].append({
                            "file": str(file_path.relative_to(self.repo_path)),
                            "line": line_num,
                            "pattern": description,
                            "context": line.strip()
                        })
        
        return performance
    
    def _generate_debt_summary(self, code_smells: Dict, complexity_metrics: Dict, 
                              todo_analysis: Dict, deprecated_code: Dict) -> Dict[str, Any]:
        """Generate technical debt summary"""
        
        summary = {
            "total_debt_items": 0,
            "debt_score": 0,
            "critical_issues": 0,
            "debt_categories": defaultdict(int),
            "priority_breakdown": defaultdict(int)
        }
        
        # Count total debt items
        debt_items = []
        
        # Code smells
        for smell_type, items in code_smells.items():
            if isinstance(items, list):
                debt_items.extend(items)
                summary["debt_categories"]["code_smells"] += len(items)
        
        # Complexity issues
        debt_items.extend(complexity_metrics.get("cyclomatic_complexity", []))
        summary["debt_categories"]["complexity"] += len(complexity_metrics.get("cyclomatic_complexity", []))
        
        # TODO items
        for todo_type, items in todo_analysis.items():
            if isinstance(items, list):
                debt_items.extend(items)
                summary["debt_categories"]["todos"] += len(items)
        
        # Deprecated code
        for dep_type, items in deprecated_code.items():
            if isinstance(items, list):
                debt_items.extend(items)
                summary["debt_categories"]["deprecated"] += len(items)
        
        summary["total_debt_items"] = len(debt_items)
        
        # Calculate debt score (0-100)
        score_factors = []
        
        # Code smell penalty
        smell_count = sum(len(items) for items in code_smells.values() if isinstance(items, list))
        score_factors.append(min(smell_count * 2, 30))
        
        # Complexity penalty
        high_complexity_files = len(complexity_metrics.get("cyclomatic_complexity", []))
        score_factors.append(min(high_complexity_files * 5, 25))
        
        # TODO penalty
        todo_count = sum(len(items) for items in todo_analysis.values() if isinstance(items, list))
        score_factors.append(min(todo_count * 1, 20))
        
        # Deprecated code penalty
        deprecated_count = sum(len(items) for items in deprecated_code.values() if isinstance(items, list))
        score_factors.append(min(deprecated_count * 3, 25))
        
        summary["debt_score"] = min(sum(score_factors), 100)
        
        # Count critical issues
        summary["critical_issues"] = (
            len(code_smells.get("god_objects", [])) +
            len([item for item in todo_analysis.get("fixme_items", []) if item.get("priority") == "high"]) +
            len(deprecated_code.get("deprecated_functions", []))
        )
        
        return summary
    
    def render(self):
        """Render the technical debt analysis"""
        st.header("🔧 Technical Debt Detection")
        st.markdown("Identifying code quality issues and technical debt patterns")
        
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
                    st.write(f"• {method['method']} ({method['lines']} lines) - {method['file']}")
            
            # Show top large classes
            large_classes = code_smells["large_classes"][:3]
            if large_classes:
                st.write("**Large Classes:**")
                for cls in large_classes:
                    st.write(f"• {cls['class']} ({cls['methods']} methods) - {cls['file']}")
        
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
        
        # Code Duplication
        st.subheader("🔄 Code Duplication")
        
        duplication_analysis = analysis["duplication_analysis"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Duplication Score", f"{duplication_analysis['duplication_score']:.1f}%")
            st.metric("Duplicate Blocks", len(duplication_analysis["duplicate_blocks"]))
        
        with col2:
            st.write("**Most Duplicated Code**")
            duplicate_blocks = duplication_analysis["duplicate_blocks"][:5]
            if duplicate_blocks:
                for block in duplicate_blocks:
                    st.write(f"• {block['count']} occurrences: `{block['content'][:50]}...`")
            else:
                st.success("No significant code duplication detected")
        
        # Performance Issues
        st.subheader("⚡ Performance Issues")
        
        performance_issues = analysis["performance_issues"]
        performance_antipatterns = performance_issues["performance_antipatterns"]
        
        if performance_antipatterns:
            st.write("**Performance Anti-patterns Found:**")
            for issue in performance_antipatterns[:10]:
                st.write(f"• **{issue['pattern']}**: {issue['file']}:{issue['line']}")
                st.code(issue['context'])
        else:
            st.success("No performance anti-patterns detected")
        
        # AI-powered Debt Analysis
        st.subheader("🤖 AI Debt Analysis")
        
        if st.button("Get AI Debt Recommendations"):
            with self.display_loading_message("Generating debt analysis..."):
                # Prepare context for AI
                debt_context = {
                    "debt_score": debt_summary["debt_score"],
                    "total_issues": debt_summary["total_debt_items"],
                    "critical_issues": debt_summary["critical_issues"],
                    "main_categories": dict(debt_summary["debt_categories"]),
                    "code_smells": len(code_smells.get("long_methods", [])),
                    "complexity_issues": len(complexity_metrics.get("cyclomatic_complexity", [])),
                    "todo_count": len(todo_analysis.get("todo_items", [])),
                    "duplication_score": duplication_analysis["duplication_score"]
                }
                
                prompt = f"""
                Based on this technical debt analysis:
                
                Debt Summary: {debt_context}
                
                Please provide:
                1. Assessment of current technical debt levels
                2. Priority recommendations for debt reduction
                3. Refactoring strategies for high-impact improvements
                4. Code quality improvement suggestions
                5. Long-term maintenance recommendations
                """
                
                ai_insights = self.ai_client.query(prompt)
                
                if ai_insights:
                    st.markdown("**AI Debt Analysis:**")
                    st.markdown(ai_insights)
                else:
                    st.error("Failed to generate debt analysis")
        
        # Display AI insights from parallel analysis if available
        self.display_parallel_ai_insights("tech_debt_detection")
        
        # Add save options
        self.add_save_options("tech_debt_detection", analysis)
