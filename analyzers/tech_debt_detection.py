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
            
            result = {
                "code_smells": code_smells,
                "complexity_metrics": complexity_metrics,
                "todo_analysis": todo_analysis,
                "deprecated_code": deprecated_code,
                "duplication_analysis": {"duplicate_blocks": [], "duplication_score": 0},  # Skip for speed
                "architectural_debt": {"circular_dependencies": [], "god_classes": []},  # Skip for speed
                "performance_issues": {"performance_antipatterns": []},  # Skip for speed
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
        """Ultra-fast code smells analysis with aggressive limits"""
        
        smells = {
            "long_methods": [],
            "large_classes": [],
            "magic_numbers": [],
            "smell_counts": {}
        }
        
        # Drastically limit file processing for speed
        source_files = self.get_file_list(['.py', '.js', '.ts'])[:15]  # Only 15 files
        
        for file_path in source_files:
            if token:
                token.check_cancellation()
            
            content = self.read_file_content(file_path)
            if not content or len(content) > 50000:  # Skip very large files
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Quick method length check using pre-compiled regex
            function_matches = self._COMPLEXITY_PATTERNS['functions'].findall(content)
            if len(function_matches) > 0:
                # Rough estimate: if file has many functions and is long, likely has long methods
                lines_count = len(content.split('\n'))
                if lines_count > 200 and len(function_matches) < 5:
                    smells["long_methods"].append({
                        "file": relative_path,
                        "method": "multiple_methods",
                        "lines": lines_count // len(function_matches),
                        "start_line": 1
                    })
                    smells["smell_counts"]["long_methods"] = smells["smell_counts"].get("long_methods", 0) + 1
            
            # Quick magic numbers check
            magic_matches = self._COMPLEXITY_PATTERNS['magic_numbers'].findall(content)
            if len(magic_matches) > 5:
                smells["magic_numbers"].extend([{
                    "file": relative_path,
                    "line": 1,
                    "number": match,
                    "context": "multiple_occurrences"
                } for match in magic_matches[:3]])  # Only first 3
                smells["smell_counts"]["magic_numbers"] = smells["smell_counts"].get("magic_numbers", 0) + len(magic_matches[:3])
        
        return smells
    
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
    
    def _generate_debt_summary_ultra_fast(self, code_smells: Dict, complexity_metrics: Dict, 
                                         todo_analysis: Dict, deprecated_code: Dict) -> Dict[str, Any]:
        """Ultra-fast debt summary generation"""
        
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
        
        # Display AI insights from parallel analysis if available
        self.display_parallel_ai_insights("tech_debt_detection")
        
        # Add save options
        self.add_save_options("tech_debt_detection", analysis)
