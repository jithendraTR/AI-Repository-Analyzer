"""
API Contracts Analyzer
Discovers and analyzes API contracts and integration points in the codebase
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
from typing import Dict, List, Any, Set
import re
import json
from pathlib import Path

from .base_analyzer import BaseAnalyzer

class APIContractAnalyzer(BaseAnalyzer):
    """Analyzes API contracts and integration points - Ultra-optimized for performance"""
    
    # Pre-compiled regex patterns for maximum performance
    _PATTERNS = {
        'flask_route': re.compile(r'@app\.route\([\'"]([^\'"]+)[\'"]', re.IGNORECASE),
        'django_path': re.compile(r'path\([\'"]([^\'"]+)[\'"]', re.IGNORECASE),
        'express_route': re.compile(r'app\.(get|post|put|delete)\([\'"]([^\'"]+)[\'"]', re.IGNORECASE),
        'fastapi_route': re.compile(r'@app\.(get|post|put|delete)\([\'"]([^\'"]+)[\'"]', re.IGNORECASE),
        'graphql_type': re.compile(r'type\s+(\w+)\s*\{', re.IGNORECASE),
        'sql_table': re.compile(r'CREATE\s+TABLE\s+(\w+)', re.IGNORECASE),
        'orm_model': re.compile(r'class\s+(\w+)\s*\([^)]*Model', re.IGNORECASE),
        'aws_service': re.compile(r'amazonaws\.com', re.IGNORECASE),
        'api_url': re.compile(r'https?://[^\s\'\"]+api[^\s\'\"]*', re.IGNORECASE),
        'json_config': re.compile(r'\{[\s\S]*\}'),
        'env_var': re.compile(r'([A-Z_][A-Z0-9_]*)\s*=', re.IGNORECASE),
        'queue_pattern': re.compile(r'(queue|publish|subscribe|kafka|redis)', re.IGNORECASE),
        'openapi_spec': re.compile(r'openapi|swagger', re.IGNORECASE)
    }
    
    def analyze(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Ultra-fast API contract analysis with aggressive optimizations"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("api_contracts")
        if cached_result:
            return cached_result
        
        total_steps = 7
        current_step = 0
        
        if token:
            token.check_cancellation()
        
        # Step 1: Ultra-fast REST API discovery
        if progress_callback:
            progress_callback(current_step, total_steps, "Discovering REST APIs (ultra-fast)...")
        rest_apis = self._ultra_fast_rest_discovery()
        current_step += 1
        
        if token:
            token.check_cancellation()
        
        # Step 2: Quick external integrations
        if progress_callback:
            progress_callback(current_step, total_steps, "Finding external integrations...")
        external_integrations = self._ultra_fast_external_discovery()
        current_step += 1
        
        if token:
            token.check_cancellation()
        
        # Step 3: Fast database schemas
        if progress_callback:
            progress_callback(current_step, total_steps, "Analyzing database schemas...")
        database_schemas = self._ultra_fast_database_discovery()
        current_step += 1
        
        if token:
            token.check_cancellation()
        
        # Step 4: API Stability Analysis
        if progress_callback:
            progress_callback(current_step, total_steps, "Analyzing API stability...")
        api_stability = self._analyze_api_stability(rest_apis)
        current_step += 1
        
        if token:
            token.check_cancellation()
        
        # Step 5: Coupling Analysis
        if progress_callback:
            progress_callback(current_step, total_steps, "Analyzing coupling patterns...")
        coupling_analysis = self._analyze_coupling_patterns(rest_apis, external_integrations)
        current_step += 1
        
        if token:
            token.check_cancellation()
        
        # Step 6: Data Flow Mapping
        if progress_callback:
            progress_callback(current_step, total_steps, "Mapping data flows...")
        data_flow_mapping = self._analyze_data_flow_mapping(rest_apis, database_schemas)
        current_step += 1
        
        if token:
            token.check_cancellation()
        
        # Step 7: Event System Understanding
        if progress_callback:
            progress_callback(current_step, total_steps, "Analyzing event systems...")
        event_system = self._analyze_event_system()
        
        # Skip expensive operations for speed
        result = {
            "rest_apis": rest_apis,
            "graphql_apis": [],  # Skip for speed
            "database_schemas": database_schemas,
            "external_integrations": external_integrations,
            "config_contracts": [],  # Skip for speed
            "messaging_contracts": [],  # Skip for speed  
            "openapi_specs": [],  # Skip for speed
            "summary": self._generate_fast_summary(rest_apis, external_integrations, database_schemas),
            # New Integration Complexity Scoring features
            "integration_complexity_scoring": {
                "api_stability": api_stability,
                "coupling_analysis": coupling_analysis,
                "data_flow_mapping": data_flow_mapping,
                "event_system_understanding": event_system
            }
        }
        
        # Cache the result
        self.cache_analysis("api_contracts", result)
        
        return result
    
    def _ultra_fast_rest_discovery(self) -> Dict[str, List[Dict]]:
        """Ultra-fast REST API endpoint discovery with aggressive file limits"""
        rest_apis = defaultdict(list)
        
        # Limit to 12 files maximum for ultra-fast analysis
        code_files = self.get_file_list(['.py', '.js', '.ts'])[:12]
        
        for file_path in code_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Use pre-compiled patterns for ultra-fast detection
            # Flask routes
            for match in self._PATTERNS['flask_route'].finditer(content):
                rest_apis["flask"].append({
                    'endpoint': match.group(1),
                    'methods': 'GET',
                    'file': relative_path,
                    'line': content[:match.start()].count('\n') + 1
                })
                if len(rest_apis["flask"]) >= 5:  # Limit per framework
                    break
            
            # Django paths
            for match in self._PATTERNS['django_path'].finditer(content):
                rest_apis["django"].append({
                    'endpoint': match.group(1),
                    'methods': 'GET',
                    'file': relative_path,
                    'line': content[:match.start()].count('\n') + 1
                })
                if len(rest_apis["django"]) >= 5:
                    break
            
            # Express routes
            for match in self._PATTERNS['express_route'].finditer(content):
                rest_apis["express"].append({
                    'endpoint': match.group(2),
                    'methods': match.group(1).upper(),
                    'file': relative_path,
                    'line': content[:match.start()].count('\n') + 1
                })
                if len(rest_apis["express"]) >= 5:
                    break
            
            # FastAPI routes
            for match in self._PATTERNS['fastapi_route'].finditer(content):
                rest_apis["fastapi"].append({
                    'endpoint': match.group(2),
                    'methods': match.group(1).upper(),
                    'file': relative_path,
                    'line': content[:match.start()].count('\n') + 1
                })
                if len(rest_apis["fastapi"]) >= 5:
                    break
        
        return dict(rest_apis)
    
    def _ultra_fast_external_discovery(self) -> List[Dict]:
        """Ultra-fast external integration discovery"""
        integrations = []
        
        # Limit to 10 files for ultra-fast analysis
        all_files = self.get_file_list(['.py', '.js', '.ts', '.json', '.yaml'])[:10]
        
        for file_path in all_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Quick AWS detection
            if self._PATTERNS['aws_service'].search(content):
                integrations.append({
                    'service': 'aws',
                    'url_pattern': 'amazonaws.com',
                    'file': relative_path,
                    'line': 1
                })
            
            # Quick API URL detection - limit to first 3 matches
            api_matches = list(self._PATTERNS['api_url'].finditer(content))[:3]
            for match in api_matches:
                integrations.append({
                    'service': 'external_api',
                    'url_pattern': match.group(0)[:50],  # Truncate for speed
                    'file': relative_path,
                    'line': content[:match.start()].count('\n') + 1
                })
            
            # Stop if we have enough integrations
            if len(integrations) >= 15:
                break
        
        return integrations
    
    def _ultra_fast_database_discovery(self) -> Dict[str, List[Dict]]:
        """Ultra-fast database schema discovery"""
        schemas = defaultdict(list)
        
        # Limit to 8 files for ultra-fast analysis
        model_files = self.get_file_list(['.py', '.sql'])[:8]
        
        for file_path in model_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Quick SQL table detection - limit to first 3 matches
            table_matches = list(self._PATTERNS['sql_table'].finditer(content))[:3]
            for match in table_matches:
                schemas['sql_tables'].append({
                    'name': match.group(1),
                    'columns': [],  # Skip for speed
                    'file': relative_path,
                    'line': content[:match.start()].count('\n') + 1
                })
            
            # Quick ORM model detection - limit to first 3 matches  
            model_matches = list(self._PATTERNS['orm_model'].finditer(content))[:3]
            for match in model_matches:
                schemas['orm_models'].append({
                    'name': match.group(1),
                    'fields': [],  # Skip for speed
                    'file': relative_path,
                    'line': content[:match.start()].count('\n') + 1
                })
        
        return dict(schemas)
    
    def _analyze_api_stability(self, rest_apis: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Analyze API stability patterns and identify safe interfaces"""
        stability_analysis = {
            "stable_interfaces": [],
            "unstable_interfaces": [],
            "stability_factors": {},
            "modification_indicators": {},
            "files_analysis": []
        }
        
        # Collect all API endpoints with their files
        all_endpoints = []
        for framework, endpoints in rest_apis.items():
            for endpoint in endpoints:
                all_endpoints.append({
                    **endpoint,
                    'framework': framework
                })
        
        # Analyze each API file for stability indicators
        api_files = set(ep['file'] for ep in all_endpoints)
        
        for file_path in list(api_files)[:10]:  # Limit for performance
            try:
                full_path = self.repo_path / file_path
                content = self.read_file_content(full_path)
                if not content:
                    continue
                
                # Stability indicators
                stability_score = 0
                factors = []
                
                # Check for version indicators
                if re.search(r'v\d+|version|api_version', content, re.IGNORECASE):
                    stability_score += 20
                    factors.append("Version management present")
                
                # Check for documentation
                if re.search(r'"""[\s\S]*?"""', content) or re.search(r"'''[\s\S]*?'''", content):
                    stability_score += 15
                    factors.append("API documentation found")
                
                # Check for error handling
                if re.search(r'try:|except:|catch|error|Error', content):
                    stability_score += 15
                    factors.append("Error handling implemented")
                
                # Check for validation
                if re.search(r'validate|schema|pydantic|joi', content, re.IGNORECASE):
                    stability_score += 10
                    factors.append("Input validation present")
                
                # Check for deprecation warnings
                if re.search(r'deprecat|obsolete|legacy', content, re.IGNORECASE):
                    stability_score -= 20
                    factors.append("Deprecation indicators found")
                
                # Check for TODO/FIXME comments
                todo_count = len(re.findall(r'TODO|FIXME|BUG|HACK', content, re.IGNORECASE))
                if todo_count > 0:
                    stability_score -= todo_count * 5
                    factors.append(f"{todo_count} TODO/FIXME comments")
                
                # Count number of endpoints in file
                file_endpoints = [ep for ep in all_endpoints if ep['file'] == file_path]
                endpoint_complexity = len(file_endpoints)
                
                file_analysis = {
                    'file': file_path,
                    'stability_score': max(0, min(100, stability_score)),
                    'endpoint_count': endpoint_complexity,
                    'factors': factors,
                    'endpoints': [ep['endpoint'] for ep in file_endpoints]
                }
                
                stability_analysis['files_analysis'].append(file_analysis)
                
                # Categorize endpoints
                for ep in file_endpoints:
                    endpoint_data = {
                        'endpoint': ep['endpoint'],
                        'file': file_path,
                        'stability_score': file_analysis['stability_score'],
                        'factors': factors
                    }
                    
                    if file_analysis['stability_score'] >= 60:
                        stability_analysis['stable_interfaces'].append(endpoint_data)
                    else:
                        stability_analysis['unstable_interfaces'].append(endpoint_data)
                
            except Exception:
                continue
        
        # Generate summary factors
        all_scores = [fa['stability_score'] for fa in stability_analysis['files_analysis']]
        if all_scores:
            stability_analysis['stability_factors'] = {
                'average_stability': sum(all_scores) / len(all_scores),
                'stable_files_count': sum(1 for score in all_scores if score >= 60),
                'unstable_files_count': sum(1 for score in all_scores if score < 60),
                'total_files_analyzed': len(all_scores)
            }
        
        return stability_analysis
    
    def _analyze_coupling_patterns(self, rest_apis: Dict[str, List[Dict]], 
                                  external_integrations: List[Dict]) -> Dict[str, Any]:
        """Analyze coupling between different systems and APIs"""
        coupling_analysis = {
            "tight_coupling_indicators": [],
            "loose_coupling_patterns": [],
            "module_dependencies": {},
            "impact_analysis": {},
            "use_cases": []
        }
        
        # Collect all API files and external integration files
        api_files = set()
        for endpoints in rest_apis.values():
            for endpoint in endpoints:
                api_files.add(endpoint['file'])
        
        external_files = set(integration['file'] for integration in external_integrations)
        
        # Analyze coupling patterns in API files
        for file_path in list(api_files)[:8]:  # Limit for performance
            try:
                full_path = self.repo_path / file_path
                content = self.read_file_content(full_path)
                if not content:
                    continue
                
                coupling_indicators = []
                
                # Check for direct database access in API layer
                if re.search(r'\.query\(|\.execute\(|SELECT|INSERT|UPDATE|DELETE', content, re.IGNORECASE):
                    coupling_indicators.append("Direct database access in API layer")
                
                # Check for hardcoded URLs or configurations
                hardcoded_urls = re.findall(r'https?://[^\s\'"]+', content)
                if hardcoded_urls:
                    coupling_indicators.append(f"Hardcoded URLs found: {len(hardcoded_urls)}")
                
                # Check for direct service imports
                service_imports = re.findall(r'from\s+[\w.]+service|import\s+[\w.]*service', content, re.IGNORECASE)
                if service_imports:
                    coupling_indicators.append(f"Direct service imports: {len(service_imports)}")
                
                # Check for shared state or global variables
                if re.search(r'global\s+\w+|Global|GLOBAL|shared_state', content):
                    coupling_indicators.append("Shared state indicators")
                
                # Check for exception handling across services
                cross_service_exceptions = re.findall(r'except\s+\w*Service\w*Error|ServiceException', content)
                if cross_service_exceptions:
                    coupling_indicators.append("Cross-service exception handling")
                
                if coupling_indicators:
                    coupling_analysis['tight_coupling_indicators'].append({
                        'file': file_path,
                        'indicators': coupling_indicators,
                        'severity': 'High' if len(coupling_indicators) >= 3 else 'Medium'
                    })
                
                # Look for loose coupling patterns
                loose_patterns = []
                
                # Check for dependency injection
                if re.search(r'inject|Inject|DI|dependency', content, re.IGNORECASE):
                    loose_patterns.append("Dependency injection pattern")
                
                # Check for event-driven patterns
                if re.search(r'event|Event|publish|subscribe|emit', content):
                    loose_patterns.append("Event-driven communication")
                
                # Check for interface/abstract usage
                if re.search(r'interface|Interface|abstract|Abstract|Protocol', content):
                    loose_patterns.append("Interface-based design")
                
                if loose_patterns:
                    coupling_analysis['loose_coupling_patterns'].append({
                        'file': file_path,
                        'patterns': loose_patterns
                    })
                
            except Exception:
                continue
        
        # Generate impact analysis with distinct use cases
        use_cases = [
            {
                'scenario': 'Database Schema Change',
                'impact': 'High' if any('Direct database access' in tc['indicators'] for tc in coupling_analysis['tight_coupling_indicators']) else 'Low',
                'affected_modules': [tc['file'] for tc in coupling_analysis['tight_coupling_indicators'] if any('database' in ind.lower() for ind in tc['indicators'])],
                'description': 'Changing database schema may require updates to multiple API endpoints'
            },
            {
                'scenario': 'External Service URL Change',
                'impact': 'High' if any('Hardcoded URLs' in tc['indicators'] for tc in coupling_analysis['tight_coupling_indicators']) else 'Low',
                'affected_modules': [tc['file'] for tc in coupling_analysis['tight_coupling_indicators'] if any('URL' in ind for ind in tc['indicators'])],
                'description': 'External service endpoint changes require code modifications'
            },
            {
                'scenario': 'Authentication Method Change',
                'impact': 'Medium',
                'affected_modules': list(api_files)[:3],
                'description': 'Authentication changes may propagate across API endpoints'
            }
        ]
        
        coupling_analysis['use_cases'] = use_cases
        
        # Module dependency summary
        coupling_analysis['module_dependencies'] = {
            'highly_coupled_modules': len(coupling_analysis['tight_coupling_indicators']),
            'loosely_coupled_modules': len(coupling_analysis['loose_coupling_patterns']),
            'total_api_modules': len(api_files),
            'coupling_ratio': len(coupling_analysis['tight_coupling_indicators']) / len(api_files) if api_files else 0
        }
        
        return coupling_analysis
    
    def _analyze_data_flow_mapping(self, rest_apis: Dict[str, List[Dict]], 
                                  database_schemas: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Map data flow through the system including sources, transforms, and sinks"""
        data_flow = {
            "data_sources": [],
            "data_transforms": [],
            "data_sinks": [],
            "entry_points": [],
            "flow_patterns": {},
            "files_analysis": []
        }
        
        # Collect all relevant files
        api_files = set()
        for endpoints in rest_apis.values():
            for endpoint in endpoints:
                api_files.add(endpoint['file'])
        
        # Data source patterns
        source_patterns = {
            'database': re.compile(r'SELECT|\.query\(|\.get\(|\.find\(|\.filter\(', re.IGNORECASE),
            'external_api': re.compile(r'requests\.|fetch\(|axios\.|http\.|urllib', re.IGNORECASE),
            'file_input': re.compile(r'open\(|read\(|csv\.|json\.load|yaml\.load', re.IGNORECASE),
            'user_input': re.compile(r'request\.|input\(|form\.|POST|PUT', re.IGNORECASE),
            'cache': re.compile(r'cache\.|redis\.|memcached', re.IGNORECASE),
            'queue': re.compile(r'queue\.|consume\(|receive\(', re.IGNORECASE)
        }
        
        # Data transform patterns
        transform_patterns = {
            'validation': re.compile(r'validate|schema|pydantic|joi|check', re.IGNORECASE),
            'serialization': re.compile(r'serialize|json\.|yaml\.|pickle|marshal', re.IGNORECASE),
            'filtering': re.compile(r'filter|where|grep|exclude', re.IGNORECASE),
            'mapping': re.compile(r'map\(|transform|convert|format', re.IGNORECASE),
            'aggregation': re.compile(r'sum\(|count\(|group|aggregate|reduce', re.IGNORECASE),
            'sorting': re.compile(r'sort|order|rank', re.IGNORECASE)
        }
        
        # Data sink patterns
        sink_patterns = {
            'database_write': re.compile(r'INSERT|UPDATE|DELETE|\.save\(|\.create\(|\.update\(', re.IGNORECASE),
            'file_output': re.compile(r'write\(|dump\(|export|\.csv|\.json|\.txt', re.IGNORECASE),
            'external_api_send': re.compile(r'post\(|put\(|requests\.post|axios\.post', re.IGNORECASE),
            'response': re.compile(r'return|response|render|jsonify|json\.dumps', re.IGNORECASE),
            'cache_write': re.compile(r'cache\.set|redis\.set|store', re.IGNORECASE),
            'queue_publish': re.compile(r'publish\(|send\(|produce\(', re.IGNORECASE),
            'logging': re.compile(r'log\.|logger\.|print\(|console\.log', re.IGNORECASE)
        }
        
        # Analyze each API file for data flow patterns
        for file_path in list(api_files)[:10]:  # Limit for performance
            try:
                full_path = self.repo_path / file_path
                content = self.read_file_content(full_path)
                if not content:
                    continue
                
                file_sources = []
                file_transforms = []
                file_sinks = []
                file_endpoints = []
                
                # Find data sources
                for source_type, pattern in source_patterns.items():
                    matches = pattern.findall(content)
                    if matches:
                        file_sources.append({
                            'type': source_type,
                            'count': len(matches),
                            'examples': matches[:3]  # First 3 examples
                        })
                
                # Find data transforms
                for transform_type, pattern in transform_patterns.items():
                    matches = pattern.findall(content)
                    if matches:
                        file_transforms.append({
                            'type': transform_type,
                            'count': len(matches),
                            'examples': matches[:3]
                        })
                
                # Find data sinks
                for sink_type, pattern in sink_patterns.items():
                    matches = pattern.findall(content)
                    if matches:
                        file_sinks.append({
                            'type': sink_type,
                            'count': len(matches),
                            'examples': matches[:3]
                        })
                
                # Find API endpoints (entry points)
                for framework, endpoints in rest_apis.items():
                    for endpoint in endpoints:
                        if endpoint['file'] == file_path:
                            file_endpoints.append({
                                'endpoint': endpoint['endpoint'],
                                'method': endpoint.get('methods', 'GET'),
                                'line': endpoint.get('line', 1)
                            })
                
                file_analysis = {
                    'file': file_path,
                    'entry_points': file_endpoints,
                    'data_sources': file_sources,
                    'data_transforms': file_transforms,
                    'data_sinks': file_sinks,
                    'flow_complexity': len(file_sources) + len(file_transforms) + len(file_sinks)
                }
                
                data_flow['files_analysis'].append(file_analysis)
                
                # Add to global collections
                data_flow['data_sources'].extend(file_sources)
                data_flow['data_transforms'].extend(file_transforms)
                data_flow['data_sinks'].extend(file_sinks)
                data_flow['entry_points'].extend(file_endpoints)
                
            except Exception:
                continue
        
        # Aggregate flow patterns
        source_summary = {}
        transform_summary = {}
        sink_summary = {}
        
        for source in data_flow['data_sources']:
            source_type = source['type']
            source_summary[source_type] = source_summary.get(source_type, 0) + source['count']
        
        for transform in data_flow['data_transforms']:
            transform_type = transform['type']
            transform_summary[transform_type] = transform_summary.get(transform_type, 0) + transform['count']
        
        for sink in data_flow['data_sinks']:
            sink_type = sink['type']
            sink_summary[sink_type] = sink_summary.get(sink_type, 0) + sink['count']
        
        data_flow['flow_patterns'] = {
            'sources_summary': source_summary,
            'transforms_summary': transform_summary,
            'sinks_summary': sink_summary,
            'total_entry_points': len(data_flow['entry_points']),
            'files_with_data_flow': len([f for f in data_flow['files_analysis'] if f['flow_complexity'] > 0])
        }
        
        return data_flow
    
    def _analyze_event_system(self) -> Dict[str, Any]:
        """Analyze pub/sub patterns and event dependency chains"""
        event_system = {
            "event_files": [],
            "events_dispatched": [],
            "events_received": [],
            "event_patterns": {},
            "dependency_chains": []
        }
        
        # Event patterns to look for
        event_patterns = {
            'publish': re.compile(r'publish\(|emit\(|dispatch\(|trigger\(|fire\(', re.IGNORECASE),
            'subscribe': re.compile(r'subscribe\(|on\(|listen\(|addEventListener|bind\(', re.IGNORECASE),
            'event_handler': re.compile(r'@event|@listener|event_handler|on_\w+|handle_\w+', re.IGNORECASE),
            'event_bus': re.compile(r'event_bus|EventBus|events\.|Events\.', re.IGNORECASE),
            'message_queue': re.compile(r'queue|Queue|publish|subscribe|kafka|rabbitmq', re.IGNORECASE)
        }
        
        # Search through code files
        code_files = self.get_file_list(['.py', '.js', '.ts', '.java'])[:15]  # Limit for performance
        
        for file_path in code_files:
            try:
                content = self.read_file_content(file_path)
                if not content:
                    continue
                
                relative_path = str(file_path.relative_to(self.repo_path))
                
                file_events_dispatched = []
                file_events_received = []
                file_has_events = False
                
                # Look for event dispatch patterns
                publish_matches = event_patterns['publish'].finditer(content)
                for match in publish_matches:
                    # Try to extract event name from context
                    line_start = content.rfind('\n', 0, match.start()) + 1
                    line_end = content.find('\n', match.end())
                    if line_end == -1:
                        line_end = len(content)
                    line_content = content[line_start:line_end]
                    
                    # Extract event name (basic parsing)
                    event_name = "unknown_event"
                    if '"' in line_content:
                        try:
                            # Basic event name extraction
                            quotes = line_content.split('"')
                            if len(quotes) > 1:
                                event_name = quotes[1]
                        except Exception:
                            event_name = "parse_error"
                    
                    file_events_dispatched.append({
                        'event_name': event_name,
                        'pattern': match.group(0),
                        'line': content[:match.start()].count('\n') + 1
                    })
                    file_has_events = True
                
                # Look for event subscription patterns
                subscribe_matches = event_patterns['subscribe'].finditer(content)
                for match in subscribe_matches:
                    line_start = content.rfind('\n', 0, match.start()) + 1
                    line_end = content.find('\n', match.end())
                    if line_end == -1:
                        line_end = len(content)
                    line_content = content[line_start:line_end]
                    
                    event_name = "unknown_event"
                    if '"' in line_content:
                        try:
                            quotes = line_content.split('"')
                            if len(quotes) > 1:
                                event_name = quotes[1]
                        except Exception:
                            event_name = "parse_error"
                    
                    file_events_received.append({
                        'event_name': event_name,
                        'pattern': match.group(0),
                        'line': content[:match.start()].count('\n') + 1
                    })
                    file_has_events = True
                
                # Add file to analysis if it has events
                if file_has_events:
                    event_system['event_files'].append({
                        'file': relative_path,
                        'events_dispatched': file_events_dispatched,
                        'events_received': file_events_received,
                        'dispatch_count': len(file_events_dispatched),
                        'receive_count': len(file_events_received)
                    })
                    
                    # Add to global collections
                    event_system['events_dispatched'].extend(file_events_dispatched)
                    event_system['events_received'].extend(file_events_received)
                
            except Exception:
                continue
        
        # Create event summary table
        event_files_summary = []
        for file_data in event_system['event_files']:
            for event in file_data['events_dispatched']:
                event_files_summary.append({
                    'file': file_data['file'],
                    'event_name': event['event_name'],
                    'action': 'dispatched',
                    'pattern': event['pattern'],
                    'line': event['line']
                })
            
            for event in file_data['events_received']:
                event_files_summary.append({
                    'file': file_data['file'],
                    'event_name': event['event_name'],
                    'action': 'received',
                    'pattern': event['pattern'],
                    'line': event['line']
                })
        
        # Analyze event patterns
        dispatch_counts = {}
        receive_counts = {}
        
        for event in event_system['events_dispatched']:
            event_name = event['event_name']
            dispatch_counts[event_name] = dispatch_counts.get(event_name, 0) + 1
        
        for event in event_system['events_received']:
            event_name = event['event_name']
            receive_counts[event_name] = receive_counts.get(event_name, 0) + 1
        
        event_system['event_patterns'] = {
            'total_files_with_events': len(event_system['event_files']),
            'total_events_dispatched': len(event_system['events_dispatched']),
            'total_events_received': len(event_system['events_received']),
            'unique_dispatched_events': len(dispatch_counts),
            'unique_received_events': len(receive_counts),
            'dispatch_summary': dispatch_counts,
            'receive_summary': receive_counts
        }
        
        # Create dependency chains (basic analysis)
        dependency_chains = []
        for event_name in dispatch_counts:
            if event_name in receive_counts:
                dependency_chains.append({
                    'event_name': event_name,
                    'publishers': dispatch_counts[event_name],
                    'subscribers': receive_counts[event_name],
                    'coupling_strength': 'High' if dispatch_counts[event_name] > 2 or receive_counts[event_name] > 2 else 'Low'
                })
        
        event_system['dependency_chains'] = dependency_chains
        
        return event_system
    
    def _generate_fast_summary(self, rest_apis: Dict[str, List[Dict]], external_integrations: List[Dict], 
                              database_schemas: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Generate fast summary with minimal calculations"""
        
        total_rest_endpoints = sum(len(endpoints) for endpoints in rest_apis.values())
        total_external_services = min(len(external_integrations), 20)  # Cap for speed
        total_db_tables = len(database_schemas.get('sql_tables', []))
        total_db_models = len(database_schemas.get('orm_models', []))
        
        # Quick service extraction
        external_services = []
        for integration in external_integrations[:10]:  # Limit for speed
            service = integration.get('service', 'unknown')
            if service not in external_services:
                external_services.append(service)
        
        return {
            'total_rest_endpoints': total_rest_endpoints,
            'total_graphql_types': 0,  # Skip for speed
            'total_db_tables': total_db_tables,
            'total_db_models': total_db_models,
            'total_external_services': len(external_services),
            'total_messaging_patterns': 0,  # Skip for speed
            'frameworks_detected': list(rest_apis.keys()),
            'external_services': external_services
        }

    def analyze_original(self, token=None, progress_callback=None) -> Dict[str, Any]:
        """Analyze API contracts and integration points"""
        
        # Check cache first
        cached_result = self.get_cached_analysis("api_contracts")
        if cached_result:
            return cached_result
        
        # Discover REST APIs
        rest_apis = self._discover_rest_apis()
        
        # Discover GraphQL APIs
        graphql_apis = self._discover_graphql_apis()
        
        # Find database schemas
        database_schemas = self._discover_database_schemas()
        
        # Discover external integrations
        external_integrations = self._discover_external_integrations()
        
        # Find configuration files
        config_contracts = self._discover_config_contracts()
        
        # Analyze message queues and events
        messaging_contracts = self._discover_messaging_contracts()
        
        # Find OpenAPI/Swagger specifications
        openapi_specs = self._discover_openapi_specs()
        
        result = {
            "rest_apis": rest_apis,
            "graphql_apis": graphql_apis,
            "database_schemas": database_schemas,
            "external_integrations": external_integrations,
            "config_contracts": config_contracts,
            "messaging_contracts": messaging_contracts,
            "openapi_specs": openapi_specs,
            "summary": self._generate_summary(rest_apis, graphql_apis, database_schemas, 
                                            external_integrations, messaging_contracts)
        }
        
        # Cache the result
        self.cache_analysis("api_contracts", result)
        
        return result
    
    def _discover_rest_apis(self) -> Dict[str, List[Dict]]:
        """Discover REST API endpoints"""
        rest_apis = defaultdict(list)
        
        # Common web framework patterns
        patterns = {
            'flask': [
                r'@app\.route\([\'"]([^\'"]+)[\'"](?:,\s*methods\s*=\s*\[([^\]]+)\])?',
                r'@bp\.route\([\'"]([^\'"]+)[\'"](?:,\s*methods\s*=\s*\[([^\]]+)\])?'
            ],
            'django': [
                r'path\([\'"]([^\'"]+)[\'"],\s*([^,]+)',
                r'url\(r[\'"]([^\'"]+)[\'"],\s*([^,]+)'
            ],
            'express': [
                r'app\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]',
                r'router\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]'
            ],
            'spring': [
                r'@(Get|Post|Put|Delete|Patch)Mapping\([\'"]([^\'"]+)[\'"]',
                r'@RequestMapping\([\'"]([^\'"]+)[\'"]'
            ],
            'fastapi': [
                r'@app\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]',
                r'@router\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]'
            ]
        }
        
        # Search through code files
        code_files = self.get_file_list(['.py', '.js', '.ts', '.java', '.rb', '.php', '.go'])
        
        for file_path in code_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            for framework, framework_patterns in patterns.items():
                for pattern in framework_patterns:
                    matches = re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE)
                    
                    for match in matches:
                        if framework in ['flask', 'django', 'fastapi']:
                            endpoint = match.group(1)
                            methods = match.group(2) if len(match.groups()) > 1 and match.group(2) else 'GET'
                        elif framework in ['express', 'spring']:
                            method = match.group(1).upper() if match.group(1) else 'GET'
                            endpoint = match.group(2) if len(match.groups()) > 1 else match.group(1)
                            methods = method
                        else:
                            endpoint = match.group(1) if match.groups() else match.group(0)
                            methods = 'GET'
                        
                        # Extract line number
                        line_num = content[:match.start()].count('\n') + 1
                        
                        rest_apis[framework].append({
                            'endpoint': endpoint,
                            'methods': methods,
                            'file': relative_path,
                            'line': line_num,
                            'context': self._extract_context(content, match.start(), match.end())
                        })
        
        return dict(rest_apis)
    
    def _discover_graphql_apis(self) -> List[Dict]:
        """Discover GraphQL schemas and resolvers"""
        graphql_apis = []
        
        # Look for GraphQL schema files
        schema_files = []
        schema_files.extend(self.find_files_by_pattern("**/*.graphql"))
        schema_files.extend(self.find_files_by_pattern("**/*.gql"))
        schema_files.extend(self.find_files_by_pattern("**/schema.py"))
        
        for file_path in schema_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Extract GraphQL types and operations
            type_matches = re.finditer(r'type\s+(\w+)\s*{([^}]+)}', content, re.MULTILINE | re.DOTALL)
            query_matches = re.finditer(r'type\s+Query\s*{([^}]+)}', content, re.MULTILINE | re.DOTALL)
            mutation_matches = re.finditer(r'type\s+Mutation\s*{([^}]+)}', content, re.MULTILINE | re.DOTALL)
            
            for match in type_matches:
                type_name = match.group(1)
                fields = self._parse_graphql_fields(match.group(2))
                
                graphql_apis.append({
                    'type': 'GraphQL Type',
                    'name': type_name,
                    'fields': fields,
                    'file': relative_path,
                    'line': content[:match.start()].count('\n') + 1
                })
            
            for match in query_matches:
                queries = self._parse_graphql_fields(match.group(1))
                
                graphql_apis.append({
                    'type': 'GraphQL Query',
                    'name': 'Query',
                    'operations': queries,
                    'file': relative_path,
                    'line': content[:match.start()].count('\n') + 1
                })
            
            for match in mutation_matches:
                mutations = self._parse_graphql_fields(match.group(1))
                
                graphql_apis.append({
                    'type': 'GraphQL Mutation',
                    'name': 'Mutation',
                    'operations': mutations,
                    'file': relative_path,
                    'line': content[:match.start()].count('\n') + 1
                })
        
        return graphql_apis
    
    def _discover_database_schemas(self) -> Dict[str, List[Dict]]:
        """Discover database schemas and models"""
        schemas = defaultdict(list)
        
        # Look for database migration files
        migration_files = []
        migration_files.extend(self.find_files_by_pattern("**/migrations/**/*.py"))
        migration_files.extend(self.find_files_by_pattern("**/migrations/**/*.sql"))
        migration_files.extend(self.find_files_by_pattern("**/migrate/**/*.sql"))
        
        # Look for model files
        model_files = []
        model_files.extend(self.find_files_by_pattern("**/models.py"))
        model_files.extend(self.find_files_by_pattern("**/models/**/*.py"))
        model_files.extend(self.find_files_by_pattern("**/entity/**/*.java"))
        
        # Analyze migration files
        for file_path in migration_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # SQL table creation patterns
            table_matches = re.finditer(
                r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)\s*\(([^;]+)\)',
                content, re.MULTILINE | re.IGNORECASE | re.DOTALL
            )
            
            for match in table_matches:
                table_name = match.group(1)
                columns_text = match.group(2)
                columns = self._parse_sql_columns(columns_text)
                
                schemas['sql_tables'].append({
                    'name': table_name,
                    'columns': columns,
                    'file': relative_path,
                    'line': content[:match.start()].count('\n') + 1
                })
        
        # Analyze model files
        for file_path in model_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Django/SQLAlchemy model patterns
            model_matches = re.finditer(
                r'class\s+(\w+)\s*\([^)]*Model[^)]*\):\s*\n((?:\s+[^\n]+\n)*)',
                content, re.MULTILINE
            )
            
            for match in model_matches:
                model_name = match.group(1)
                model_body = match.group(2)
                fields = self._parse_model_fields(model_body)
                
                schemas['orm_models'].append({
                    'name': model_name,
                    'fields': fields,
                    'file': relative_path,
                    'line': content[:match.start()].count('\n') + 1
                })
        
        return dict(schemas)
    
    def _discover_external_integrations(self) -> List[Dict]:
        """Discover external API integrations"""
        integrations = []
        
        # Common external service patterns
        service_patterns = {
            'aws': r'(s3|ec2|lambda|dynamodb|rds|sns|sqs)\.amazonaws\.com',
            'google': r'(googleapis\.com|google\.com/api)',
            'stripe': r'api\.stripe\.com',
            'github': r'api\.github\.com',
            'slack': r'(slack\.com/api|hooks\.slack\.com)',
            'twilio': r'api\.twilio\.com',
            'sendgrid': r'api\.sendgrid\.com',
            'mailgun': r'api\.mailgun\.net',
            'redis': r'redis://',
            'mongodb': r'mongodb://',
            'postgresql': r'postgresql://',
            'mysql': r'mysql://'
        }
        
        # Search through all files
        all_files = self.get_file_list()
        
        for file_path in all_files[:100]:  # Limit to avoid performance issues
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            for service, pattern in service_patterns.items():
                matches = re.finditer(pattern, content, re.IGNORECASE)
                
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    context = self._extract_context(content, match.start(), match.end())
                    
                    integrations.append({
                        'service': service,
                        'url_pattern': match.group(0),
                        'file': relative_path,
                        'line': line_num,
                        'context': context
                    })
        
        return integrations
    
    def _discover_config_contracts(self) -> List[Dict]:
        """Discover configuration contracts"""
        configs = []
        
        # Look for configuration files
        config_files = []
        config_files.extend(self.find_files_by_pattern("**/*.json"))
        config_files.extend(self.find_files_by_pattern("**/*.yaml"))
        config_files.extend(self.find_files_by_pattern("**/*.yml"))
        config_files.extend(self.find_files_by_pattern("**/*.toml"))
        config_files.extend(self.find_files_by_pattern("**/*.ini"))
        config_files.extend(self.find_files_by_pattern("**/config.py"))
        config_files.extend(self.find_files_by_pattern("**/settings.py"))
        
        for file_path in config_files:
            if any(skip in str(file_path) for skip in ['node_modules', '.git', '__pycache__']):
                continue
            
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            # Try to parse as JSON
            if file_path.suffix == '.json':
                try:
                    config_data = json.loads(content)
                    configs.append({
                        'type': 'JSON Config',
                        'file': relative_path,
                        'keys': list(config_data.keys()) if isinstance(config_data, dict) else [],
                        'structure': self._analyze_config_structure(config_data)
                    })
                except json.JSONDecodeError:
                    pass
            
            # Look for environment variables
            env_vars = re.findall(r'([A-Z_][A-Z0-9_]*)\s*=', content)
            if env_vars:
                configs.append({
                    'type': 'Environment Variables',
                    'file': relative_path,
                    'variables': list(set(env_vars))
                })
        
        return configs
    
    def _discover_messaging_contracts(self) -> List[Dict]:
        """Discover message queue and event contracts"""
        messaging = []
        
        # Look for messaging patterns
        code_files = self.get_file_list(['.py', '.js', '.ts', '.java', '.go'])
        
        messaging_patterns = {
            'rabbitmq': r'(queue_declare|basic_publish|basic_consume)',
            'kafka': r'(KafkaProducer|KafkaConsumer|produce|consume)',
            'redis_pub_sub': r'(publish|subscribe|psubscribe)',
            'aws_sqs': r'(send_message|receive_message|delete_message)',
            'celery': r'(@task|apply_async|delay)',
            'event_bus': r'(emit|on|addEventListener|publish|subscribe)'
        }
        
        for file_path in code_files[:50]:  # Limit to avoid performance issues
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            for msg_type, pattern in messaging_patterns.items():
                matches = re.finditer(pattern, content, re.IGNORECASE)
                
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    context = self._extract_context(content, match.start(), match.end())
                    
                    messaging.append({
                        'type': msg_type,
                        'pattern': match.group(0),
                        'file': relative_path,
                        'line': line_num,
                        'context': context
                    })
        
        return messaging
    
    def _discover_openapi_specs(self) -> List[Dict]:
        """Discover OpenAPI/Swagger specifications"""
        specs = []
        
        # Look for OpenAPI/Swagger files
        spec_files = []
        spec_files.extend(self.find_files_by_pattern("**/swagger.json"))
        spec_files.extend(self.find_files_by_pattern("**/openapi.json"))
        spec_files.extend(self.find_files_by_pattern("**/swagger.yaml"))
        spec_files.extend(self.find_files_by_pattern("**/openapi.yaml"))
        spec_files.extend(self.find_files_by_pattern("**/api-docs.json"))
        
        for file_path in spec_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
            
            relative_path = str(file_path.relative_to(self.repo_path))
            
            try:
                if file_path.suffix == '.json':
                    spec_data = json.loads(content)
                else:
                    # For YAML files, we'll do basic parsing
                    spec_data = {'info': {'title': 'API Spec'}}
                
                specs.append({
                    'file': relative_path,
                    'title': spec_data.get('info', {}).get('title', 'Unknown API'),
                    'version': spec_data.get('info', {}).get('version', 'Unknown'),
                    'paths': list(spec_data.get('paths', {}).keys()) if 'paths' in spec_data else [],
                    'components': list(spec_data.get('components', {}).keys()) if 'components' in spec_data else []
                })
            except (json.JSONDecodeError, Exception):
                specs.append({
                    'file': relative_path,
                    'title': 'API Specification',
                    'version': 'Unknown',
                    'paths': [],
                    'components': []
                })
        
        return specs
    
    def _generate_summary(self, rest_apis, graphql_apis, database_schemas, 
                         external_integrations, messaging_contracts) -> Dict[str, Any]:
        """Generate summary statistics"""
        
        total_rest_endpoints = sum(len(endpoints) for endpoints in rest_apis.values())
        total_graphql_types = len([api for api in graphql_apis if api['type'] == 'GraphQL Type'])
        total_db_tables = len(database_schemas.get('sql_tables', []))
        total_db_models = len(database_schemas.get('orm_models', []))
        total_external_services = len(set(integration['service'] for integration in external_integrations))
        total_messaging_patterns = len(messaging_contracts)
        
        return {
            'total_rest_endpoints': total_rest_endpoints,
            'total_graphql_types': total_graphql_types,
            'total_db_tables': total_db_tables,
            'total_db_models': total_db_models,
            'total_external_services': total_external_services,
            'total_messaging_patterns': total_messaging_patterns,
            'frameworks_detected': list(rest_apis.keys()),
            'external_services': list(set(integration['service'] for integration in external_integrations))
        }
    
    def _parse_graphql_fields(self, fields_text: str) -> List[str]:
        """Parse GraphQL fields from schema text"""
        fields = []
        for line in fields_text.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract field name (before colon)
                if ':' in line:
                    field_name = line.split(':')[0].strip()
                    fields.append(field_name)
        return fields
    
    def _parse_sql_columns(self, columns_text: str) -> List[Dict]:
        """Parse SQL column definitions"""
        columns = []
        for line in columns_text.split(','):
            line = line.strip()
            if line and not line.startswith('--'):
                parts = line.split()
                if len(parts) >= 2:
                    columns.append({
                        'name': parts[0],
                        'type': parts[1],
                        'constraints': ' '.join(parts[2:]) if len(parts) > 2 else ''
                    })
        return columns
    
    def _parse_model_fields(self, model_body: str) -> List[Dict]:
        """Parse ORM model fields"""
        fields = []
        for line in model_body.split('\n'):
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                field_name = line.split('=')[0].strip()
                field_def = line.split('=')[1].strip()
                fields.append({
                    'name': field_name,
                    'definition': field_def
                })
        return fields
    
    def _analyze_config_structure(self, config_data: Any, max_depth: int = 3) -> Dict:
        """Analyze configuration structure"""
        if max_depth <= 0:
            return {'type': type(config_data).__name__}
        
        if isinstance(config_data, dict):
            return {
                'type': 'object',
                'keys': len(config_data),
                'structure': {k: self._analyze_config_structure(v, max_depth - 1) 
                            for k, v in list(config_data.items())[:10]}  # Limit to first 10 keys
            }
        elif isinstance(config_data, list):
            return {
                'type': 'array',
                'length': len(config_data),
                'item_type': self._analyze_config_structure(config_data[0], max_depth - 1) if config_data else None
            }
        else:
            return {'type': type(config_data).__name__}
    
    def _extract_context(self, content: str, start: int, end: int, context_lines: int = 2) -> str:
        """Extract context around a match"""
        lines = content.split('\n')
        match_line = content[:start].count('\n')
        
        start_line = max(0, match_line - context_lines)
        end_line = min(len(lines), match_line + context_lines + 1)
        
        context_lines_list = lines[start_line:end_line]
        return '\n'.join(context_lines_list)
    
    def render(self):
        """Render the API contracts analysis"""
        # Add rerun button
        self.add_rerun_button("api_contracts")
        
        with self.display_loading_message("Analyzing API contracts..."):
            analysis = self.analyze()
        
        if "error" in analysis:
            self.display_error(analysis["error"])
            return
        
        # Summary metrics
        summary = analysis["summary"]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("REST Endpoints", summary["total_rest_endpoints"])
        with col2:
            st.metric("GraphQL Types", summary["total_graphql_types"])
        with col3:
            st.metric("Database Tables", summary["total_db_tables"] + summary["total_db_models"])
        with col4:
            st.metric("External Services", summary["total_external_services"])
        
        # REST APIs
        st.subheader("🌐 REST API Endpoints")
        
        rest_apis = analysis["rest_apis"]
        if rest_apis:
            # Framework distribution
            framework_counts = {fw: len(endpoints) for fw, endpoints in rest_apis.items()}
            
            if framework_counts:
                fig_frameworks = px.pie(
                    values=list(framework_counts.values()),
                    names=list(framework_counts.keys()),
                    title="API Frameworks Distribution"
                )
                st.plotly_chart(fig_frameworks, use_container_width=True)
            
            # Detailed endpoints
            for framework, endpoints in rest_apis.items():
                if endpoints:
                    st.write(f"**{framework.title()} Endpoints:**")
                    
                    endpoints_df = pd.DataFrame([
                        {
                            "Endpoint": ep["endpoint"],
                            "Methods": ep["methods"],
                            "File": ep["file"],
                            "Line": ep["line"]
                        }
                        for ep in endpoints
                    ])
                    
                    st.dataframe(endpoints_df, use_container_width=True)
        else:
            st.info("No REST API endpoints found")
        
        # GraphQL APIs
        st.subheader("📊 GraphQL APIs")
        
        graphql_apis = analysis["graphql_apis"]
        if graphql_apis:
            graphql_df = pd.DataFrame([
                {
                    "Type": api["type"],
                    "Name": api["name"],
                    "Fields/Operations": len(api.get("fields", api.get("operations", []))),
                    "File": api["file"],
                    "Line": api["line"]
                }
                for api in graphql_apis
            ])
            
            st.dataframe(graphql_df, use_container_width=True)
            
            # GraphQL type distribution
            type_counts = {}
            for api in graphql_apis:
                api_type = api["type"]
                type_counts[api_type] = type_counts.get(api_type, 0) + 1
            
            if type_counts:
                fig_gql_types = px.bar(
                    x=list(type_counts.keys()),
                    y=list(type_counts.values()),
                    title="GraphQL API Types"
                )
                st.plotly_chart(fig_gql_types, use_container_width=True)
        else:
            st.info("No GraphQL APIs found")
        
        # Database Schemas
        st.subheader("🗄️ Database Schemas")
        
        database_schemas = analysis["database_schemas"]
        if database_schemas:
            # SQL Tables
            if "sql_tables" in database_schemas:
                st.write("**SQL Tables:**")
                tables_df = pd.DataFrame([
                    {
                        "Table": table["name"],
                        "Columns": len(table["columns"]),
                        "File": table["file"],
                        "Line": table["line"]
                    }
                    for table in database_schemas["sql_tables"]
                ])
                st.dataframe(tables_df, use_container_width=True)
            
            # ORM Models
            if "orm_models" in database_schemas:
                st.write("**ORM Models:**")
                models_df = pd.DataFrame([
                    {
                        "Model": model["name"],
                        "Fields": len(model["fields"]),
                        "File": model["file"],
                        "Line": model["line"]
                    }
                    for model in database_schemas["orm_models"]
                ])
                st.dataframe(models_df, use_container_width=True)
        else:
            st.info("No database schemas found")
        
        # External Integrations
        st.subheader("🔗 External Integrations")
        
        external_integrations = analysis["external_integrations"]
        if external_integrations:
            # Service distribution
            service_counts = {}
            for integration in external_integrations:
                service = integration["service"]
                service_counts[service] = service_counts.get(service, 0) + 1
            
            fig_services = px.bar(
                x=list(service_counts.keys()),
                y=list(service_counts.values()),
                title="External Services Usage"
            )
            st.plotly_chart(fig_services, use_container_width=True)
            
            # Detailed integrations
            integrations_df = pd.DataFrame([
                {
                    "Service": integration["service"],
                    "URL Pattern": integration["url_pattern"],
                    "File": integration["file"],
                    "Line": integration["line"]
                }
                for integration in external_integrations[:50]  # Limit display
            ])
            
            st.dataframe(integrations_df, use_container_width=True)
        else:
            st.info("No external integrations found")
        
        # Configuration Contracts
        st.subheader("⚙️ Configuration Contracts")
        
        config_contracts = analysis["config_contracts"]
        if config_contracts:
            config_df = pd.DataFrame([
                {
                    "Type": config["type"],
                    "File": config["file"],
                    "Keys/Variables": len(config.get("keys", config.get("variables", [])))
                }
                for config in config_contracts
            ])
            
            st.dataframe(config_df, use_container_width=True)
        else:
            st.info("No configuration contracts found")
        
        # Messaging Contracts
        st.subheader("📨 Messaging & Events")
        
        messaging_contracts = analysis["messaging_contracts"]
        if messaging_contracts:
            # Messaging type distribution
            msg_type_counts = {}
            for msg in messaging_contracts:
                msg_type = msg["type"]
                msg_type_counts[msg_type] = msg_type_counts.get(msg_type, 0) + 1
            
            fig_messaging = px.bar(
                x=list(msg_type_counts.keys()),
                y=list(msg_type_counts.values()),
                title="Messaging Patterns"
            )
            st.plotly_chart(fig_messaging, use_container_width=True)
            
            # Detailed messaging
            messaging_df = pd.DataFrame([
                {
                    "Type": msg["type"],
                    "Pattern": msg["pattern"],
                    "File": msg["file"],
                    "Line": msg["line"]
                }
                for msg in messaging_contracts[:30]  # Limit display
            ])
            
            st.dataframe(messaging_df, use_container_width=True)
        else:
            st.info("No messaging patterns found")
        
        # OpenAPI Specifications
        st.subheader("📋 OpenAPI Specifications")
        
        openapi_specs = analysis["openapi_specs"]
        if openapi_specs:
            specs_df = pd.DataFrame([
                {
                    "Title": spec["title"],
                    "Version": spec["version"],
                    "Paths": len(spec["paths"]),
                    "Components": len(spec["components"]),
                    "File": spec["file"]
                }
                for spec in openapi_specs
            ])
            
            st.dataframe(specs_df, use_container_width=True)
        else:
            st.info("No OpenAPI specifications found")
        
        # AI-powered insights
        st.subheader("🤖 AI Contract Insights")
        
        if st.button("Generate API Contract Insights"):
            with self.display_loading_message("Generating AI insights..."):
                # Prepare contract summary for AI
                contract_summary = {
                    "rest_endpoints": summary["total_rest_endpoints"],
                    "graphql_types": summary["total_graphql_types"],
                    "database_entities": summary["total_db_tables"] + summary["total_db_models"],
                    "external_services": summary["external_services"],
                    "frameworks": summary["frameworks_detected"],
                    "messaging_patterns": summary["total_messaging_patterns"]
                }
                
                prompt = f"""
                Analyze this API contract and integration data:
                
                {contract_summary}
                
                Please provide:
                1. API architecture assessment
                2. Integration complexity analysis
                3. Potential contract versioning issues
                4. Security considerations for external integrations
                5. Recommendations for API governance and documentation
                6. Suggestions for improving integration patterns
                """
                
                insights = self.ai_client.query(prompt)
                
                if insights:
                    st.markdown("**AI-Generated Contract Insights:**")
                    st.markdown(insights)
                else:
                    st.error("Failed to generate AI insights")
        
        # Integration Complexity Scoring Features
        st.subheader("🎯 Integration Complexity Scoring")
        
        if "integration_complexity_scoring" in analysis:
            complexity_data = analysis["integration_complexity_scoring"]
            
            # API Stability Analysis
            if "api_stability" in complexity_data:
                st.write("**🔒 API Stability Analysis**")
                stability = complexity_data["api_stability"]
                
                if stability["files_analysis"]:
                    stability_df = pd.DataFrame([
                        {
                            "File": file_data["file"],
                            "Stability Score": f"{file_data['stability_score']}/100",
                            "Endpoint Count": file_data["endpoint_count"],
                            "Key Factors": ", ".join(file_data["factors"][:2])  # Show first 2 factors
                        }
                        for file_data in stability["files_analysis"]
                    ])
                    
                    st.dataframe(stability_df, use_container_width=True)
                    
                    # Stability distribution chart
                    if stability["stability_factors"]:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Average Stability", f"{stability['stability_factors']['average_stability']:.1f}/100")
                            st.metric("Stable Files", stability["stability_factors"]["stable_files_count"])
                        with col2:
                            st.metric("Unstable Files", stability["stability_factors"]["unstable_files_count"])
                            st.metric("Total Analyzed", stability["stability_factors"]["total_files_analyzed"])
                else:
                    st.info("No API stability data found")
            
            # Coupling Analysis
            if "coupling_analysis" in complexity_data:
                st.write("**🔗 Coupling Analysis**")
                coupling = complexity_data["coupling_analysis"]
                
                if coupling["tight_coupling_indicators"]:
                    st.write("*Tight Coupling Indicators:*")
                    coupling_df = pd.DataFrame([
                        {
                            "File": indicator["file"],
                            "Severity": indicator["severity"],
                            "Issues": len(indicator["indicators"]),
                            "Main Issues": ", ".join(indicator["indicators"][:2])
                        }
                        for indicator in coupling["tight_coupling_indicators"]
                    ])
                    st.dataframe(coupling_df, use_container_width=True)
                
                # Use Cases Impact Analysis
                if coupling["use_cases"]:
                    st.write("*Impact Analysis - Distinct Use Cases:*")
                    use_cases_df = pd.DataFrame([
                        {
                            "Scenario": case["scenario"],
                            "Impact": case["impact"],
                            "Affected Modules": len(case["affected_modules"]),
                            "Description": case["description"]
                        }
                        for case in coupling["use_cases"]
                    ])
                    st.dataframe(use_cases_df, use_container_width=True)
                
                # Coupling summary metrics
                if coupling["module_dependencies"]:
                    deps = coupling["module_dependencies"]
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Highly Coupled", deps["highly_coupled_modules"])
                    with col2:
                        st.metric("Loosely Coupled", deps["loosely_coupled_modules"])
                    with col3:
                        st.metric("Coupling Ratio", f"{deps['coupling_ratio']:.2f}")
            
            # Data Flow Mapping
            if "data_flow_mapping" in complexity_data:
                st.write("**📊 Data Flow Mapping**")
                data_flow = complexity_data["data_flow_mapping"]
                
                if data_flow["flow_patterns"]:
                    patterns = data_flow["flow_patterns"]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Entry Points", patterns["total_entry_points"])
                        st.metric("Files with Data Flow", patterns["files_with_data_flow"])
                    
                    # Data sources chart
                    if patterns["sources_summary"]:
                        fig_sources = px.bar(
                            x=list(patterns["sources_summary"].keys()),
                            y=list(patterns["sources_summary"].values()),
                            title="Data Sources Distribution",
                            labels={"x": "Source Type", "y": "Count"}
                        )
                        st.plotly_chart(fig_sources, use_container_width=True)
                    
                    # Data sinks chart
                    if patterns["sinks_summary"]:
                        fig_sinks = px.bar(
                            x=list(patterns["sinks_summary"].keys()),
                            y=list(patterns["sinks_summary"].values()),
                            title="Data Sinks Distribution",
                            labels={"x": "Sink Type", "y": "Count"}
                        )
                        st.plotly_chart(fig_sinks, use_container_width=True)
                
                # File-level data flow analysis
                if data_flow["files_analysis"]:
                    st.write("*Files with Data Flow (showing entry points and flow complexity):*")
                    flow_df = pd.DataFrame([
                        {
                            "File": file_data["file"],
                            "Entry Points": len(file_data["entry_points"]),
                            "API Endpoints": ", ".join([ep["endpoint"] for ep in file_data["entry_points"][:2]]),
                            "Flow Complexity": file_data["flow_complexity"],
                            "Sources": len(file_data["data_sources"]),
                            "Transforms": len(file_data["data_transforms"]),
                            "Sinks": len(file_data["data_sinks"])
                        }
                        for file_data in data_flow["files_analysis"][:10]  # Show first 10
                    ])
                    st.dataframe(flow_df, use_container_width=True)
            
            # Event System Understanding
            if "event_system_understanding" in complexity_data:
                st.write("**⚡ Event System Understanding**")
                events = complexity_data["event_system_understanding"]
                
                if events["event_patterns"]:
                    patterns = events["event_patterns"]
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Files with Events", patterns["total_files_with_events"])
                    with col2:
                        st.metric("Events Dispatched", patterns["total_events_dispatched"])
                    with col3:
                        st.metric("Events Received", patterns["total_events_received"])
                
                # Event dependency chains
                if events["dependency_chains"]:
                    st.write("*Event Dependency Chains:*")
                    chains_df = pd.DataFrame([
                        {
                            "Event Name": chain["event_name"],
                            "Publishers": chain["publishers"],
                            "Subscribers": chain["subscribers"],
                            "Coupling Strength": chain["coupling_strength"]
                        }
                        for chain in events["dependency_chains"]
                    ])
                    st.dataframe(chains_df, use_container_width=True)
                
                # Events table listing files, events dispatched, and events received
                if events["event_files"]:
                    st.write("*Files with Event Activity:*")
                    event_table_data = []
                    
                    for file_data in events["event_files"]:
                        # Add dispatched events
                        for event in file_data["events_dispatched"]:
                            event_table_data.append({
                                "File": file_data["file"],
                                "Event Name": event["event_name"],
                                "Action": "Dispatched",
                                "Pattern": event["pattern"],
                                "Line": event["line"]
                            })
                        
                        # Add received events
                        for event in file_data["events_received"]:
                            event_table_data.append({
                                "File": file_data["file"],
                                "Event Name": event["event_name"],
                                "Action": "Received",
                                "Pattern": event["pattern"],
                                "Line": event["line"]
                            })
                    
                    if event_table_data:
                        events_table_df = pd.DataFrame(event_table_data[:20])  # Show first 20
                        st.dataframe(events_table_df, use_container_width=True)
                else:
                    st.info("No event system patterns found")
        
        # Add save options
        self.add_save_options("api_contracts", analysis)
