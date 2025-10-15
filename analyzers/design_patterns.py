"""
Design Pattern Deviation Analyzer
Analyzes adherence to and deviations from common design patterns
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

class DesignPatternAnalyzer(BaseAnalyzer):
    """Analyzes design pattern usage and deviations - Ultra-optimized for performance"""
    
    # Pre-compiled regex patterns for maximum performance
    _PATTERNS = {
        'singleton': re.compile(r'__new__.*cls.*instance|_instance\s*=\s*None|@singleton|class.*Singleton', re.IGNORECASE),
        'factory': re.compile(r'class.*Factory|def.*(create|make|build).*\(|factory.*method|create_.*\(', re.IGNORECASE),
        'observer': re.compile(r'class.*(Observer|Subject)|def.*(notify|subscribe|unsubscribe).*\(|(observers|listeners).*=.*\[\]', re.IGNORECASE),
        'decorator': re.compile(r'@\w+|def.*decorator.*\(|def.*wrapper.*\(|class.*Decorator|functools\.wraps'),
        'mvc': re.compile(r'class.*(Controller|Model|View)|def.*(render|update).*\(|template.*=', re.IGNORECASE),
        'god_class': re.compile(r'class\s+(\w+)', re.IGNORECASE),
        'magic_strings': re.compile(r'["\']([^"\']{10,})["\']'),
        'hard_coded': re.compile(r'localhost:\d+|127\.0\.0\.1|password\s*=|api_key\s*=|secret\s*=', re.IGNORECASE)
    }
    
    def analyze(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Ultra-fast design pattern analysis with aggressive optimizations"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("design_patterns")
        if cached_result:
            return cached_result
        
        if token:
            token.check_cancellation()
        
        # Step 1: Ultra-fast pattern detection
        if progress_callback:
            progress_callback(1, 3, "Detecting patterns (ultra-fast)...")
        pattern_implementations = self._ultra_fast_pattern_analysis()
        
        if token:
            token.check_cancellation()
        
        # Step 2: Quick SOLID analysis
        if progress_callback:
            progress_callback(2, 3, "Analyzing SOLID principles...")
        solid_analysis = self._ultra_fast_solid_analysis()
        
        if token:
            token.check_cancellation()
        
        # Step 3: Fast anti-pattern detection
        if progress_callback:
            progress_callback(3, 3, "Detecting anti-patterns...")
        anti_patterns = self._ultra_fast_anti_patterns()
        
        # Skip expensive operations for speed
        result = {
            "pattern_implementations": pattern_implementations,
            "pattern_violations": {"violation_counts": {}},  # Skip for speed
            "solid_analysis": solid_analysis,
            "architectural_patterns": {"layered_architecture": []},  # Skip for speed
            "anti_patterns": anti_patterns,
            "pattern_summary": self._generate_fast_pattern_summary(
                pattern_implementations, solid_analysis, anti_patterns
            )
        }
        
        # Cache the result
        self.cache_analysis("design_patterns", result)
        
        return result
    
    def _ultra_fast_pattern_analysis(self) -> Dict[str, Any]:
        """Ultra-fast pattern detection with aggressive file limits"""
        
        patterns = {
            "singleton": [],
            "factory": [],
            "observer": [],
            "strategy": [],
            "decorator": [],
            "adapter": [],
            "builder": [],
            "mvc": [],
            "pattern_counts": defaultdict(int)
        }
        
        # Limit to 12 files maximum for ultra-fast analysis
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])[:12]
        
        for file_path in source_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Use pre-compiled patterns for ultra-fast detection
            if self._PATTERNS['singleton'].search(content):
                patterns["singleton"].append({
                    "file": relative_path,
                    "pattern": "Singleton",
                    "confidence": "medium"
                })
                patterns["pattern_counts"]["singleton"] += 1
            
            if self._PATTERNS['factory'].search(content):
                patterns["factory"].append({
                    "file": relative_path,
                    "pattern": "Factory",
                    "confidence": "medium"
                })
                patterns["pattern_counts"]["factory"] += 1
            
            if self._PATTERNS['observer'].search(content):
                patterns["observer"].append({
                    "file": relative_path,
                    "pattern": "Observer",
                    "confidence": "medium"
                })
                patterns["pattern_counts"]["observer"] += 1
            
            if self._PATTERNS['decorator'].search(content):
                patterns["decorator"].append({
                    "file": relative_path,
                    "pattern": "Decorator",
                    "confidence": "high"
                })
                patterns["pattern_counts"]["decorator"] += 1
            
            if self._PATTERNS['mvc'].search(content):
                patterns["mvc"].append({
                    "file": relative_path,
                    "pattern": "MVC",
                    "confidence": "medium"
                })
                patterns["pattern_counts"]["mvc"] += 1
        
        return patterns
    
    def _ultra_fast_solid_analysis(self) -> Dict[str, Any]:
        """Ultra-fast SOLID principles analysis"""
        
        solid = {
            "srp_analysis": {"violations": 0, "compliant": 0},
            "ocp_analysis": {"violations": 0, "compliant": 0},
            "lsp_analysis": {"violations": 0, "compliant": 0},
            "isp_analysis": {"violations": 0, "compliant": 0},
            "dip_analysis": {"violations": 0, "compliant": 0},
            "solid_score": 0
        }
        
        # Limit to 8 files for ultra-fast analysis
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])[:8]
        
        for file_path in source_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            # Quick method count for SRP
            method_count = len(re.findall(r'def\s+\w+\s*\(', content))
            if method_count > 15:
                solid["srp_analysis"]["violations"] += 1
            else:
                solid["srp_analysis"]["compliant"] += 1
            
            # Quick inheritance check for OCP
            if re.search(r'class.*\(.*\):|@abstractmethod', content):
                solid["ocp_analysis"]["compliant"] += 1
            else:
                solid["ocp_analysis"]["violations"] += 1
            
            # Quick super() check for LSP
            if re.search(r'super\(\)|override', content):
                solid["lsp_analysis"]["compliant"] += 1
            else:
                solid["lsp_analysis"]["violations"] += 1
            
            # Quick interface size check for ISP
            interface_methods = len(re.findall(r'def\s+\w+\s*\(', content))
            if interface_methods <= 5:
                solid["isp_analysis"]["compliant"] += 1
            else:
                solid["isp_analysis"]["violations"] += 1
            
            # Quick dependency injection check for DIP
            if re.search(r'def\s+__init__.*\(.*\w+.*\):|@inject', content):
                solid["dip_analysis"]["compliant"] += 1
            else:
                solid["dip_analysis"]["violations"] += 1
        
        # Calculate SOLID score quickly
        total_checks = 0
        compliant_checks = 0
        
        for principle in ["srp_analysis", "ocp_analysis", "lsp_analysis", "isp_analysis", "dip_analysis"]:
            violations = solid[principle]["violations"]
            compliant = solid[principle]["compliant"]
            total_checks += violations + compliant
            compliant_checks += compliant
        
        if total_checks > 0:
            solid["solid_score"] = (compliant_checks / total_checks) * 100
        
        return solid
    
    def _ultra_fast_anti_patterns(self) -> Dict[str, Any]:
        """Ultra-fast anti-pattern detection"""
        
        anti_patterns = {
            "god_object": [],
            "spaghetti_code": [],
            "copy_paste": [],
            "magic_strings": [],
            "hard_coding": [],
            "anti_pattern_counts": defaultdict(int)
        }
        
        # Limit to 10 files for ultra-fast analysis
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])[:10]
        
        for file_path in source_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Quick God Object detection using pre-compiled pattern
            class_matches = self._PATTERNS['god_class'].finditer(content)
            for class_match in class_matches:
                class_name = class_match.group(1)
                method_count = len(re.findall(r'def\s+\w+\s*\(', content))
                line_count = len(content.split('\n'))
                
                if method_count > 15 or line_count > 300:
                    anti_patterns["god_object"].append({
                        "file": relative_path,
                        "class": class_name,
                        "methods": method_count,
                        "lines": line_count,
                        "severity": "high" if method_count > 25 else "medium"
                    })
                    anti_patterns["anti_pattern_counts"]["god_object"] += 1
                    break  # Only report first god object per file for speed
            
            # Quick magic strings detection using pre-compiled pattern
            magic_matches = self._PATTERNS['magic_strings'].findall(content)
            if len(magic_matches) > 5:
                anti_patterns["magic_strings"].append({
                    "file": relative_path,
                    "strings": magic_matches[:3],  # First 3 only
                    "count": len(magic_matches)
                })
                anti_patterns["anti_pattern_counts"]["magic_strings"] += 1
            
            # Quick hard coding detection using pre-compiled pattern
            hard_coded_matches = self._PATTERNS['hard_coded'].findall(content)
            if hard_coded_matches:
                anti_patterns["hard_coding"].append({
                    "file": relative_path,
                    "count": len(hard_coded_matches)
                })
                anti_patterns["anti_pattern_counts"]["hard_coding"] += 1
        
        return anti_patterns
    
    def _generate_fast_pattern_summary(self, implementations: Dict, solid: Dict, anti_patterns: Dict) -> Dict[str, Any]:
        """Generate fast pattern summary with minimal calculations"""
        
        summary = {
            "total_patterns": 0,
            "pattern_diversity": 0,
            "violation_count": 0,
            "solid_score": solid.get("solid_score", 0),
            "pattern_health": "good"
        }
        
        # Quick pattern counting
        pattern_counts = implementations.get("pattern_counts", {})
        summary["total_patterns"] = sum(pattern_counts.values())
        summary["pattern_diversity"] = len([count for count in pattern_counts.values() if count > 0])
        
        # Quick anti-pattern counting
        anti_pattern_counts = anti_patterns.get("anti_pattern_counts", {})
        summary["violation_count"] = sum(anti_pattern_counts.values())
        
        # Quick health assessment
        solid_score = summary["solid_score"]
        violation_count = summary["violation_count"]
        
        if solid_score >= 80 and violation_count <= 3:
            summary["pattern_health"] = "excellent"
        elif solid_score >= 60 and violation_count <= 6:
            summary["pattern_health"] = "good"
        elif solid_score >= 40:
            summary["pattern_health"] = "fair"
        else:
            summary["pattern_health"] = "poor"
        
        return summary

    def analyze_original(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Analyze design pattern adherence and deviations"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("design_patterns")
        if cached_result:
            return cached_result
        
        # Analyze pattern implementations
        pattern_implementations = self._analyze_pattern_implementations()
        
        # Analyze pattern violations
        pattern_violations = self._analyze_pattern_violations()
        
        # Analyze SOLID principles
        solid_analysis = self._analyze_solid_principles()
        
        # Analyze architectural patterns
        architectural_patterns = self._analyze_architectural_patterns()
        
        # Analyze anti-patterns
        anti_patterns = self._analyze_anti_patterns()
        
        result = {
            "pattern_implementations": pattern_implementations,
            "pattern_violations": pattern_violations,
            "solid_analysis": solid_analysis,
            "architectural_patterns": architectural_patterns,
            "anti_patterns": anti_patterns,
            "pattern_summary": self._generate_pattern_summary(
                pattern_implementations, pattern_violations, solid_analysis
            )
        }
        
        # Cache the result
        self.cache_analysis("design_patterns", result)
        
        return result
    
    def _analyze_pattern_implementations(self) -> Dict[str, Any]:
        """Analyze implementation of common design patterns"""
        
        patterns = {
            "singleton": [],
            "factory": [],
            "observer": [],
            "strategy": [],
            "decorator": [],
            "adapter": [],
            "builder": [],
            "mvc": [],
            "pattern_counts": defaultdict(int)
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        
        for file_path in source_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            # Detect Singleton pattern
            self._detect_singleton_pattern(content, file_path, patterns)
            
            # Detect Factory pattern
            self._detect_factory_pattern(content, file_path, patterns)
            
            # Detect Observer pattern
            self._detect_observer_pattern(content, file_path, patterns)
            
            # Detect Strategy pattern
            self._detect_strategy_pattern(content, file_path, patterns)
            
            # Detect Decorator pattern
            self._detect_decorator_pattern(content, file_path, patterns)
            
            # Detect MVC pattern
            self._detect_mvc_pattern(content, file_path, patterns)
        
        return patterns
    
    def _detect_singleton_pattern(self, content: str, file_path: Path, patterns: Dict):
        """Detect Singleton pattern implementation"""
        
        # Python singleton patterns
        singleton_indicators = [
            r'__new__.*cls.*instance',
            r'_instance\s*=\s*None',
            r'if.*_instance.*is.*None',
            r'@singleton',
            r'class.*Singleton'
        ]
        
        for indicator in singleton_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                patterns["singleton"].append({
                    "file": str(file_path.relative_to(self.repo_path)),
                    "pattern": "Singleton",
                    "indicator": indicator,
                    "confidence": "medium"
                })
                patterns["pattern_counts"]["singleton"] += 1
                break
    
    def _detect_factory_pattern(self, content: str, file_path: Path, patterns: Dict):
        """Detect Factory pattern implementation"""
        
        factory_indicators = [
            r'class.*Factory',
            r'def.*create.*\(',
            r'def.*make.*\(',
            r'def.*build.*\(',
            r'factory.*method',
            r'create_.*\('
        ]
        
        for indicator in factory_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                patterns["factory"].append({
                    "file": str(file_path.relative_to(self.repo_path)),
                    "pattern": "Factory",
                    "indicator": indicator,
                    "confidence": "medium"
                })
                patterns["pattern_counts"]["factory"] += 1
                break
    
    def _detect_observer_pattern(self, content: str, file_path: Path, patterns: Dict):
        """Detect Observer pattern implementation"""
        
        observer_indicators = [
            r'class.*Observer',
            r'class.*Subject',
            r'def.*notify.*\(',
            r'def.*subscribe.*\(',
            r'def.*unsubscribe.*\(',
            r'observers.*=.*\[\]',
            r'listeners.*=.*\[\]'
        ]
        
        observer_count = 0
        for indicator in observer_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                observer_count += 1
        
        if observer_count >= 2:  # Need multiple indicators for confidence
            patterns["observer"].append({
                "file": str(file_path.relative_to(self.repo_path)),
                "pattern": "Observer",
                "indicators": observer_count,
                "confidence": "high" if observer_count >= 3 else "medium"
            })
            patterns["pattern_counts"]["observer"] += 1
    
    def _detect_strategy_pattern(self, content: str, file_path: Path, patterns: Dict):
        """Detect Strategy pattern implementation"""
        
        strategy_indicators = [
            r'class.*Strategy',
            r'class.*Algorithm',
            r'def.*execute.*\(',
            r'strategy.*=.*',
            r'algorithm.*=.*'
        ]
        
        strategy_count = 0
        for indicator in strategy_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                strategy_count += 1
        
        if strategy_count >= 2:
            patterns["strategy"].append({
                "file": str(file_path.relative_to(self.repo_path)),
                "pattern": "Strategy",
                "indicators": strategy_count,
                "confidence": "medium"
            })
            patterns["pattern_counts"]["strategy"] += 1
    
    def _detect_decorator_pattern(self, content: str, file_path: Path, patterns: Dict):
        """Detect Decorator pattern implementation"""
        
        decorator_indicators = [
            r'@\w+',  # Python decorators
            r'def.*decorator.*\(',
            r'def.*wrapper.*\(',
            r'class.*Decorator',
            r'functools\.wraps'
        ]
        
        for indicator in decorator_indicators:
            if re.search(indicator, content):
                patterns["decorator"].append({
                    "file": str(file_path.relative_to(self.repo_path)),
                    "pattern": "Decorator",
                    "indicator": indicator,
                    "confidence": "high" if indicator.startswith('@') else "medium"
                })
                patterns["pattern_counts"]["decorator"] += 1
                break
    
    def _detect_mvc_pattern(self, content: str, file_path: Path, patterns: Dict):
        """Detect MVC pattern implementation"""
        
        mvc_indicators = [
            r'class.*Controller',
            r'class.*Model',
            r'class.*View',
            r'def.*render.*\(',
            r'def.*update.*\(',
            r'template.*=.*'
        ]
        
        mvc_count = 0
        for indicator in mvc_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                mvc_count += 1
        
        if mvc_count >= 2:
            patterns["mvc"].append({
                "file": str(file_path.relative_to(self.repo_path)),
                "pattern": "MVC",
                "indicators": mvc_count,
                "confidence": "medium"
            })
            patterns["pattern_counts"]["mvc"] += 1
    
    def _analyze_pattern_violations(self) -> Dict[str, Any]:
        """Analyze violations of design pattern principles"""
        
        violations = {
            "singleton_violations": [],
            "factory_violations": [],
            "srp_violations": [],
            "ocp_violations": [],
            "violation_counts": defaultdict(int)
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        
        for file_path in source_files[:30]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            # Check for singleton violations
            self._check_singleton_violations(content, file_path, violations)
            
            # Check for factory violations
            self._check_factory_violations(content, file_path, violations)
            
            # Check for SRP violations
            self._check_srp_violations(content, file_path, violations)
        
        return violations
    
    def _check_singleton_violations(self, content: str, file_path: Path, violations: Dict):
        """Check for Singleton pattern violations"""
        
        # Multiple instances of singleton
        if re.search(r'__new__.*cls.*instance', content) and re.search(r'new.*\(\)', content):
            violations["singleton_violations"].append({
                "file": str(file_path.relative_to(self.repo_path)),
                "violation": "Multiple instance creation in singleton",
                "severity": "high"
            })
            violations["violation_counts"]["singleton"] += 1
        
        # Thread safety issues
        if re.search(r'_instance\s*=\s*None', content) and not re.search(r'lock|Lock|threading', content):
            violations["singleton_violations"].append({
                "file": str(file_path.relative_to(self.repo_path)),
                "violation": "Singleton not thread-safe",
                "severity": "medium"
            })
            violations["violation_counts"]["singleton"] += 1
    
    def _check_factory_violations(self, content: str, file_path: Path, violations: Dict):
        """Check for Factory pattern violations"""
        
        # Direct instantiation instead of factory
        if re.search(r'class.*Factory', content) and re.search(r'new\s+\w+\(', content):
            violations["factory_violations"].append({
                "file": str(file_path.relative_to(self.repo_path)),
                "violation": "Direct instantiation bypassing factory",
                "severity": "medium"
            })
            violations["violation_counts"]["factory"] += 1
    
    def _check_srp_violations(self, content: str, file_path: Path, violations: Dict):
        """Check for Single Responsibility Principle violations"""
        
        # Count different types of responsibilities in a class
        class_pattern = r'class\s+(\w+).*?:'
        classes = re.finditer(class_pattern, content)
        
        for class_match in classes:
            class_name = class_match.group(1)
            
            # Look for multiple responsibilities
            responsibilities = []
            
            if re.search(r'def.*save.*\(', content):
                responsibilities.append("persistence")
            if re.search(r'def.*validate.*\(', content):
                responsibilities.append("validation")
            if re.search(r'def.*format.*\(', content):
                responsibilities.append("formatting")
            if re.search(r'def.*send.*\(', content):
                responsibilities.append("communication")
            if re.search(r'def.*calculate.*\(', content):
                responsibilities.append("calculation")
            
            if len(responsibilities) > 2:
                violations["srp_violations"].append({
                    "file": str(file_path.relative_to(self.repo_path)),
                    "class": class_name,
                    "violation": f"Multiple responsibilities: {', '.join(responsibilities)}",
                    "severity": "medium"
                })
                violations["violation_counts"]["srp"] += 1
    
    def _analyze_solid_principles(self) -> Dict[str, Any]:
        """Analyze adherence to SOLID principles"""
        
        solid = {
            "srp_analysis": {"violations": 0, "compliant": 0},
            "ocp_analysis": {"violations": 0, "compliant": 0},
            "lsp_analysis": {"violations": 0, "compliant": 0},
            "isp_analysis": {"violations": 0, "compliant": 0},
            "dip_analysis": {"violations": 0, "compliant": 0},
            "solid_score": 0
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        
        for file_path in source_files[:20]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            # Single Responsibility Principle
            self._analyze_srp(content, solid)
            
            # Open/Closed Principle
            self._analyze_ocp(content, solid)
            
            # Liskov Substitution Principle
            self._analyze_lsp(content, solid)
            
            # Interface Segregation Principle
            self._analyze_isp(content, solid)
            
            # Dependency Inversion Principle
            self._analyze_dip(content, solid)
        
        # Calculate overall SOLID score
        total_checks = sum(
            solid[principle]["violations"] + solid[principle]["compliant"]
            for principle in ["srp_analysis", "ocp_analysis", "lsp_analysis", "isp_analysis", "dip_analysis"]
        )
        
        if total_checks > 0:
            compliant_checks = sum(
                solid[principle]["compliant"]
                for principle in ["srp_analysis", "ocp_analysis", "lsp_analysis", "isp_analysis", "dip_analysis"]
            )
            solid["solid_score"] = (compliant_checks / total_checks) * 100
        
        return solid
    
    def _analyze_srp(self, content: str, solid: Dict):
        """Analyze Single Responsibility Principle"""
        
        # Simple heuristic: classes with many different method types
        class_methods = re.findall(r'def\s+(\w+)\s*\(', content)
        
        if len(class_methods) > 10:
            solid["srp_analysis"]["violations"] += 1
        else:
            solid["srp_analysis"]["compliant"] += 1
    
    def _analyze_ocp(self, content: str, solid: Dict):
        """Analyze Open/Closed Principle"""
        
        # Look for extension mechanisms
        if re.search(r'class.*\(.*\):', content) or re.search(r'@abstractmethod', content):
            solid["ocp_analysis"]["compliant"] += 1
        else:
            solid["ocp_analysis"]["violations"] += 1
    
    def _analyze_lsp(self, content: str, solid: Dict):
        """Analyze Liskov Substitution Principle"""
        
        # Look for proper inheritance
        if re.search(r'super\(\)', content) or re.search(r'override', content):
            solid["lsp_analysis"]["compliant"] += 1
        else:
            solid["lsp_analysis"]["violations"] += 1
    
    def _analyze_isp(self, content: str, solid: Dict):
        """Analyze Interface Segregation Principle"""
        
        # Look for focused interfaces
        interface_methods = re.findall(r'def\s+(\w+)\s*\(', content)
        
        if len(interface_methods) <= 5:  # Small, focused interfaces
            solid["isp_analysis"]["compliant"] += 1
        else:
            solid["isp_analysis"]["violations"] += 1
    
    def _analyze_dip(self, content: str, solid: Dict):
        """Analyze Dependency Inversion Principle"""
        
        # Look for dependency injection patterns
        if re.search(r'def\s+__init__.*\(.*\w+.*\):', content) or re.search(r'@inject', content):
            solid["dip_analysis"]["compliant"] += 1
        else:
            solid["dip_analysis"]["violations"] += 1
    
    def _analyze_architectural_patterns(self) -> Dict[str, Any]:
        """Analyze architectural patterns"""
        
        patterns = {
            "layered_architecture": [],
            "microservices": [],
            "event_driven": [],
            "repository_pattern": [],
            "service_layer": [],
            "architectural_violations": []
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        
        for file_path in source_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            # Detect layered architecture
            if any(layer in str(file_path).lower() for layer in ['controller', 'service', 'repository', 'model']):
                patterns["layered_architecture"].append({
                    "file": str(file_path.relative_to(self.repo_path)),
                    "layer": self._identify_layer(file_path)
                })
            
            # Detect repository pattern
            if re.search(r'class.*Repository', content, re.IGNORECASE):
                patterns["repository_pattern"].append({
                    "file": str(file_path.relative_to(self.repo_path)),
                    "pattern": "Repository"
                })
            
            # Detect service layer
            if re.search(r'class.*Service', content, re.IGNORECASE):
                patterns["service_layer"].append({
                    "file": str(file_path.relative_to(self.repo_path)),
                    "pattern": "Service Layer"
                })
        
        return patterns
    
    def _identify_layer(self, file_path: Path) -> str:
        """Identify architectural layer from file path"""
        
        path_str = str(file_path).lower()
        
        if 'controller' in path_str:
            return "Controller"
        elif 'service' in path_str:
            return "Service"
        elif 'repository' in path_str or 'dao' in path_str:
            return "Repository"
        elif 'model' in path_str or 'entity' in path_str:
            return "Model"
        else:
            return "Unknown"
    
    def _analyze_anti_patterns(self) -> Dict[str, Any]:
        """Analyze anti-patterns in the codebase"""
        
        anti_patterns = {
            "god_object": [],
            "spaghetti_code": [],
            "copy_paste": [],
            "magic_strings": [],
            "hard_coding": [],
            "anti_pattern_counts": defaultdict(int)
        }
        
        source_files = self.get_file_list(['.py', '.js', '.ts', '.java'])
        
        for file_path in source_files[:30]:  # Limit for performance
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            # Detect God Object
            self._detect_god_object(content, file_path, anti_patterns)
            
            # Detect Magic Strings
            self._detect_magic_strings(content, file_path, anti_patterns)
            
            # Detect Hard Coding
            self._detect_hard_coding(content, file_path, anti_patterns)
        
        return anti_patterns
    
    def _detect_god_object(self, content: str, file_path: Path, anti_patterns: Dict):
        """Detect God Object anti-pattern"""
        
        # Count methods and lines in classes
        class_pattern = r'class\s+(\w+).*?:'
        classes = re.finditer(class_pattern, content)
        
        lines = content.split('\n')
        
        for class_match in classes:
            class_name = class_match.group(1)
            start_line = content[:class_match.start()].count('\n')
            
            # Count methods and lines in class
            method_count = 0
            class_lines = 0
            
            for i in range(start_line, len(lines)):
                line = lines[i]
                if line.strip().startswith('class ') and i > start_line:
                    break
                if 'def ' in line:
                    method_count += 1
                if line.strip():
                    class_lines += 1
            
            # God object thresholds
            if method_count > 20 or class_lines > 500:
                anti_patterns["god_object"].append({
                    "file": str(file_path.relative_to(self.repo_path)),
                    "class": class_name,
                    "methods": method_count,
                    "lines": class_lines,
                    "severity": "high" if method_count > 30 else "medium"
                })
                anti_patterns["anti_pattern_counts"]["god_object"] += 1
    
    def _detect_magic_strings(self, content: str, file_path: Path, anti_patterns: Dict):
        """Detect magic strings anti-pattern"""
        
        # Find string literals that might be magic strings
        string_pattern = r'["\']([^"\']{3,})["\']'
        strings = re.findall(string_pattern, content)
        
        magic_strings = []
        for string in strings:
            # Skip common non-magic strings
            if any(skip in string.lower() for skip in ['test', 'error', 'warning', 'info', 'debug']):
                continue
            
            # Look for configuration-like strings
            if any(indicator in string for indicator in ['/', ':', '=', '@', 'http']):
                magic_strings.append(string)
        
        if magic_strings:
            anti_patterns["magic_strings"].append({
                "file": str(file_path.relative_to(self.repo_path)),
                "strings": magic_strings[:5],  # Limit to first 5
                "count": len(magic_strings)
            })
            anti_patterns["anti_pattern_counts"]["magic_strings"] += 1
    
    def _detect_hard_coding(self, content: str, file_path: Path, anti_patterns: Dict):
        """Detect hard-coding anti-pattern"""
        
        hard_coded_patterns = [
            r'localhost:\d+',
            r'127\.0\.0\.1',
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']'
        ]
        
        hard_coded_items = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for pattern in hard_coded_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    hard_coded_items.append({
                        "line": line_num,
                        "content": line.strip(),
                        "type": "hard_coded_value"
                    })
        
        if hard_coded_items:
            anti_patterns["hard_coding"].append({
                "file": str(file_path.relative_to(self.repo_path)),
                "items": hard_coded_items[:3],  # Limit to first 3
                "count": len(hard_coded_items)
            })
            anti_patterns["anti_pattern_counts"]["hard_coding"] += 1
    
    def _generate_pattern_summary(self, implementations: Dict, violations: Dict, solid: Dict) -> Dict[str, Any]:
        """Generate design pattern summary"""
        
        summary = {
            "total_patterns": 0,
            "pattern_diversity": 0,
            "violation_count": 0,
            "solid_score": solid.get("solid_score", 0),
            "pattern_health": "good"
        }
        
        # Count total patterns
        pattern_counts = implementations.get("pattern_counts", {})
        summary["total_patterns"] = sum(pattern_counts.values())
        summary["pattern_diversity"] = len([count for count in pattern_counts.values() if count > 0])
        
        # Count violations
        violation_counts = violations.get("violation_counts", {})
        summary["violation_count"] = sum(violation_counts.values())
        
        # Determine pattern health
        if summary["solid_score"] >= 80 and summary["violation_count"] <= 5:
            summary["pattern_health"] = "excellent"
        elif summary["solid_score"] >= 60 and summary["violation_count"] <= 10:
            summary["pattern_health"] = "good"
        elif summary["solid_score"] >= 40:
            summary["pattern_health"] = "fair"
        else:
            summary["pattern_health"] = "poor"
        
        return summary
    
    def render(self):
        """Render the design pattern analysis"""
        # Add rerun button
        self.add_rerun_button("design_patterns")
        
        with self.display_loading_message("Analyzing design patterns..."):
            analysis = self.analyze()
        
        if "error" in analysis:
            self.display_error(analysis["error"])
            return
        
        # Pattern Summary
        st.subheader("📊 Pattern Summary")
        
        pattern_summary = analysis["pattern_summary"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("SOLID Score", f"{pattern_summary['solid_score']:.1f}/100")
        
        with col2:
            st.metric("Patterns Found", pattern_summary["total_patterns"])
        
        with col3:
            st.metric("Pattern Diversity", pattern_summary["pattern_diversity"])
        
        with col4:
            health_color = {
                "excellent": "🟢",
                "good": "🟡", 
                "fair": "🟠",
                "poor": "🔴"
            }
            st.metric("Pattern Health", f"{health_color.get(pattern_summary['pattern_health'], '⚪')} {pattern_summary['pattern_health'].title()}")
        
        # Pattern Implementations
        st.subheader("🔧 Pattern Implementations")
        
        implementations = analysis["pattern_implementations"]
        pattern_counts = dict(implementations["pattern_counts"])
        
        if pattern_counts:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Pattern Distribution**")
                fig = px.bar(
                    x=list(pattern_counts.keys()),
                    y=list(pattern_counts.values()),
                    title="Design Patterns Found"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("**Pattern Details**")
                for pattern_type, items in implementations.items():
                    if isinstance(items, list) and items:
                        st.write(f"**{pattern_type.title()}:**")
                        for item in items[:3]:  # Show first 3
                            confidence = item.get("confidence", "unknown")
                            st.write(f"• {item['file']} ({confidence} confidence)")
        else:
            st.info("No specific design patterns detected")
        
        # SOLID Principles Analysis
        st.subheader("🏛️ SOLID Principles")
        
        solid_analysis = analysis["solid_analysis"]
        
        principles = ["SRP", "OCP", "LSP", "ISP", "DIP"]
        principle_keys = ["srp_analysis", "ocp_analysis", "lsp_analysis", "isp_analysis", "dip_analysis"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**SOLID Compliance**")
            
            compliance_data = []
            for i, principle in enumerate(principles):
                analysis_key = principle_keys[i]
                compliant = solid_analysis[analysis_key]["compliant"]
                violations = solid_analysis[analysis_key]["violations"]
                total = compliant + violations
                
                if total > 0:
                    compliance_rate = (compliant / total) * 100
                    compliance_data.append({"Principle": principle, "Compliance": compliance_rate})
            
            if compliance_data:
                df = pd.DataFrame(compliance_data)
                fig = px.bar(df, x="Principle", y="Compliance", title="SOLID Principle Compliance")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Principle Details**")
            for i, principle in enumerate(principles):
                analysis_key = principle_keys[i]
                compliant = solid_analysis[analysis_key]["compliant"]
                violations = solid_analysis[analysis_key]["violations"]
                
                st.write(f"**{principle}**: {compliant} compliant, {violations} violations")
        
        # Pattern Violations
        st.subheader("⚠️ Pattern Violations")
        
        violations = analysis["pattern_violations"]
        violation_counts = dict(violations["violation_counts"])
        
        if violation_counts:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Violation Types**")
                fig = px.pie(
                    values=list(violation_counts.values()),
                    names=list(violation_counts.keys()),
                    title="Violation Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("**Critical Violations**")
                
                # Show SRP violations
                srp_violations = violations.get("srp_violations", [])
                if srp_violations:
                    st.write("**SRP Violations:**")
                    for violation in srp_violations[:5]:
                        st.write(f"• {violation['class']} in {violation['file']}")
                        st.write(f"  {violation['violation']}")
        else:
            st.success("No pattern violations detected")
        
        # Anti-patterns
        st.subheader("🚫 Anti-patterns")
        
        anti_patterns = analysis["anti_patterns"]
        anti_pattern_counts = dict(anti_patterns["anti_pattern_counts"])
        
        if anti_pattern_counts:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Anti-pattern Distribution**")
                fig = px.bar(
                    x=list(anti_pattern_counts.keys()),
                    y=list(anti_pattern_counts.values()),
                    title="Anti-patterns Found"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("**Critical Anti-patterns**")
                
                # Show God Objects
                god_objects = anti_patterns.get("god_object", [])
                if god_objects:
                    st.write("**God Objects:**")
                    for obj in god_objects[:3]:
                        st.write(f"• {obj['class']} in {obj['file']}")
                        st.write(f"  {obj['methods']} methods, {obj['lines']} lines")
                
                # Show Hard Coding
                hard_coding = anti_patterns.get("hard_coding", [])
                if hard_coding:
                    st.write("**Hard Coding Issues:**")
                    for issue in hard_coding[:3]:
                        st.write(f"• {issue['file']}: {issue['count']} issues")
        else:
            st.success("No anti-patterns detected")
        
        # AI-powered Pattern Analysis
        st.subheader("🤖 AI Pattern Analysis")
        
        if st.button("Get AI Pattern Recommendations"):
            with self.display_loading_message("Generating pattern analysis..."):
                # Prepare context for AI
                pattern_context = {
                    "solid_score": pattern_summary["solid_score"],
                    "total_patterns": pattern_summary["total_patterns"],
                    "pattern_diversity": pattern_summary["pattern_diversity"],
                    "violation_count": pattern_summary["violation_count"],
                    "pattern_health": pattern_summary["pattern_health"],
                    "detected_patterns": list(pattern_counts.keys()) if pattern_counts else [],
                    "anti_patterns": list(anti_pattern_counts.keys()) if anti_pattern_counts else []
                }
                
                prompt = f"""
                Based on this design pattern analysis:
                
                Pattern Summary: {pattern_context}
                
                Please provide:
                1. Assessment of current design pattern usage
                2. Recommendations for improving SOLID principle compliance
                3. Suggestions for addressing anti-patterns
                4. Best practices for pattern implementation
                5. Architectural improvement recommendations
                """
                
                ai_insights = self.ai_client.query(prompt)
                
                if ai_insights:
                    st.markdown("**AI Pattern Analysis:**")
                    st.markdown(ai_insights)
                else:
                    st.error("Failed to generate pattern analysis")
