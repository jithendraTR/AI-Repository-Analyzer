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
        
        total_steps = 3
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
        
        # Skip expensive operations for speed
        result = {
            "rest_apis": rest_apis,
            "graphql_apis": [],  # Skip for speed
            "database_schemas": database_schemas,
            "external_integrations": external_integrations,
            "config_contracts": [],  # Skip for speed
            "messaging_contracts": [],  # Skip for speed  
            "openapi_specs": [],  # Skip for speed
            "summary": self._generate_fast_summary(rest_apis, external_integrations, database_schemas)
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
    
    def _generate_fast_summary(self, rest_apis: Dict, external_integrations: List, 
                              database_schemas: Dict) -> Dict[str, Any]:
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
        st.header("🔌 API Contracts & Integration Points")
        st.markdown("Discovering API contracts and integration patterns in your codebase")
        
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
        
        # Add save options
        self.add_save_options("api_contracts", analysis)
