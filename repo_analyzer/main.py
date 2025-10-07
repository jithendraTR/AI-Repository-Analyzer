"""
AI-Powered Repository Analyzer
Main application entry point with tabbed interface for different analysis types
"""

import streamlit as st
import os
from dotenv import load_dotenv
import asyncio
import concurrent.futures
from typing import Dict, Any
import threading
import time

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import analysis modules
from analyzers.expertise_mapping import ExpertiseMapper
from analyzers.timeline_analysis import TimelineAnalyzer
from analyzers.api_contracts import APIContractAnalyzer
from analyzers.ai_context import AIContextAnalyzer
from analyzers.risk_analysis import RiskAnalysisAnalyzer
from analyzers.development_patterns import DevelopmentPatternsAnalyzer
from analyzers.version_governance import VersionGovernanceAnalyzer
from analyzers.tech_debt_detection import TechDebtDetectionAnalyzer
from analyzers.design_patterns import DesignPatternAnalyzer
from utils.ai_client import OpenArenaClient

class ParallelAIAnalyzer:
    """Handles parallel AI analysis for all tabs with cancellation support"""
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.ai_client = OpenArenaClient()
        self.analyzers = {
            'expertise': ExpertiseMapper(repo_path),
            'timeline': TimelineAnalyzer(repo_path),
            'api_contracts': APIContractAnalyzer(repo_path),
            'ai_context': AIContextAnalyzer(repo_path),
            'risk_analysis': RiskAnalysisAnalyzer(repo_path),
            'development_patterns': DevelopmentPatternsAnalyzer(repo_path),
            'version_governance': VersionGovernanceAnalyzer(repo_path),
            'tech_debt': TechDebtDetectionAnalyzer(repo_path),
            'design_patterns': DesignPatternAnalyzer(repo_path)
        }
        self.cancellation_token = None
    
    def set_cancellation_token(self, token):
        """Set the cancellation token for this analyzer"""
        self.cancellation_token = token
    
    def run_single_analysis(self, analyzer_name: str, analyzer) -> Dict[str, Any]:
        """Run analysis and generate AI insight for a specific analyzer with cancellation support"""
        try:
            # Check for cancellation before starting
            if self.cancellation_token and self.cancellation_token.is_cancelled():
                return {
                    "analyzer": analyzer_name,
                    "error": "Operation was cancelled",
                    "success": False,
                    "cancelled": True
                }
            
            # Progress callback for individual analyzer steps
            def analyzer_progress(step, total, status):
                print(f"DEBUG: {analyzer_name} - Step {step}/{total}: {status}")
            
            # Get analysis data - this is now running in parallel with progress tracking
            analysis_data = analyzer.analyze(token=self.cancellation_token, progress_callback=analyzer_progress)
            
            # Check for cancellation after analysis
            if self.cancellation_token and self.cancellation_token.is_cancelled():
                return {
                    "analyzer": analyzer_name,
                    "error": "Operation was cancelled",
                    "success": False,
                    "cancelled": True
                }
            
            if "error" in analysis_data:
                return {"analyzer": analyzer_name, "error": analysis_data["error"]}
            
            # Generate appropriate prompt based on analyzer type
            prompt = self._generate_prompt(analyzer_name, analysis_data)
            
            # Check for cancellation before AI query
            if self.cancellation_token and self.cancellation_token.is_cancelled():
                return {
                    "analyzer": analyzer_name,
                    "error": "Operation was cancelled",
                    "success": False,
                    "cancelled": True
                }
            
            # Get AI insight
            insight = self.ai_client.query(prompt)
            
            return {
                "analyzer": analyzer_name,
                "insight": insight,
                "success": True,
                "analysis_data": analysis_data  # Include raw analysis data
            }
        except Exception as e:
            # Check if it's a cancellation
            if "cancelled" in str(e).lower():
                return {
                    "analyzer": analyzer_name,
                    "error": "Operation was cancelled",
                    "success": False,
                    "cancelled": True
                }
            return {
                "analyzer": analyzer_name,
                "error": str(e),
                "success": False
            }
    
    def _generate_prompt(self, analyzer_name: str, analysis_data: Dict[str, Any]) -> str:
        """Generate appropriate prompt for each analyzer type"""
        
        prompts = {
            'expertise': f"""
            Analyze this expertise mapping data and provide insights:
            {str(analysis_data)[:2000]}
            
            Provide:
            1. Key expertise areas and knowledge gaps
            2. Team collaboration patterns
            3. Knowledge transfer recommendations
            4. Risk assessment for key person dependencies
            """,
            
            'timeline': f"""
            Analyze this project timeline data:
            Total commits: {analysis_data.get('total_commits', 0)}
            Recent activity: {analysis_data.get('recent_changes', {}).get('total_recent_commits', 0)}
            
            Provide:
            1. Project maturity assessment
            2. Development velocity trends
            3. Team activity patterns
            4. Timeline management recommendations
            """,
            
            'api_contracts': f"""
            Analyze these API contracts and integration points:
            {str(analysis_data)[:2000]}
            
            Provide:
            1. API design quality assessment
            2. Integration complexity analysis
            3. Potential breaking changes risks
            4. API evolution recommendations
            """,
            
            'ai_context': f"""
            Analyze this codebase context for AI feature integration:
            {str(analysis_data)[:2000]}
            
            Provide:
            1. Best locations for new AI features
            2. Integration complexity assessment
            3. Architectural recommendations
            4. Implementation strategy
            """,
            
            'risk_analysis': f"""
            Analyze these risk factors:
            {str(analysis_data)[:2000]}
            
            Provide:
            1. Critical risk assessment
            2. Test coverage recommendations
            3. Security vulnerability priorities
            4. Risk mitigation strategies
            """,
            
            'development_patterns': f"""
            Analyze these development patterns:
            {str(analysis_data)[:2000]}
            
            Provide:
            1. Code quality assessment
            2. Pattern consistency analysis
            3. Best practices recommendations
            4. Refactoring priorities
            """,
            
            'version_governance': f"""
            Analyze version and dependency management:
            {str(analysis_data)[:2000]}
            
            Provide:
            1. Dependency health assessment
            2. Version conflict risks
            3. Update strategy recommendations
            4. Security vulnerability priorities
            """,
            
            'tech_debt': f"""
            Analyze technical debt indicators:
            {str(analysis_data)[:2000]}
            
            Provide:
            1. Technical debt severity assessment
            2. Refactoring priorities
            3. Code quality improvement plan
            4. Long-term maintenance strategy
            """,
            
            'design_patterns': f"""
            Analyze design pattern usage and deviations:
            {str(analysis_data)[:2000]}
            
            Provide:
            1. Design pattern compliance assessment
            2. Architecture consistency analysis
            3. Pattern improvement recommendations
            4. Code structure optimization suggestions
            """
        }
        
        return prompts.get(analyzer_name, f"Analyze this data: {str(analysis_data)[:2000]}")
    
    def run_parallel_analysis(self, progress_callback=None) -> Dict[str, Any]:
        """Run AI analysis for all analyzers in parallel with cancellation support"""
        results = {}
        completed_count = 0
        total_count = len(self.analyzers)
        
        # Debug: Print what analyzers we're about to run
        print(f"DEBUG: Starting parallel analysis for {total_count} analyzers: {list(self.analyzers.keys())}")
        
        # Use a smaller thread pool to avoid overwhelming the system
        max_workers = min(total_count, 2)  # Reduced to 2 to prevent timeouts
        print(f"DEBUG: Using {max_workers} worker threads")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks at once - this should start them all simultaneously
            future_to_analyzer = {}
            
            # Submit all tasks and track them
            for name, analyzer in self.analyzers.items():
                print(f"DEBUG: Submitting {name} to thread pool")
                future = executor.submit(self.run_single_analysis, name, analyzer)
                future_to_analyzer[future] = name
            
            print(f"DEBUG: All {len(future_to_analyzer)} tasks submitted to thread pool")
            
            # Update progress to show all analyzers are starting
            if progress_callback:
                analyzer_names = [name.replace('_', ' ').title() for name in self.analyzers.keys()]
                progress_callback(0, total_count, f"Starting: {', '.join(analyzer_names[:3])}{'...' if len(analyzer_names) > 3 else ''}")
            
            # Collect results as they complete with timeout
            try:
                for future in concurrent.futures.as_completed(future_to_analyzer, timeout=900):  # 15 minute total timeout
                    # Check for cancellation
                    if self.cancellation_token and self.cancellation_token.is_cancelled():
                        print("DEBUG: Cancellation detected, stopping remaining tasks")
                        # Cancel remaining futures
                        for remaining_future in future_to_analyzer:
                            if not remaining_future.done():
                                remaining_future.cancel()
                        
                        # Add cancelled status to remaining analyzers
                        for remaining_future, remaining_analyzer in future_to_analyzer.items():
                            if not remaining_future.done():
                                results[remaining_analyzer] = {
                                    "analyzer": remaining_analyzer,
                                    "error": "Operation was cancelled",
                                    "success": False,
                                    "cancelled": True
                                }
                        break
                    
                    analyzer_name = future_to_analyzer[future]
                    print(f"DEBUG: {analyzer_name} completed")
                    
                    try:
                        result = future.result(timeout=5)  # Short timeout since future is already done
                        results[analyzer_name] = result
                        completed_count += 1
                        
                        # Update progress if callback provided
                        if progress_callback:
                            # Show which analyzers are still running
                            remaining_analyzers = [name for f, name in future_to_analyzer.items() if not f.done()]
                            if remaining_analyzers:
                                progress_callback(completed_count, total_count, f"Running: {', '.join(remaining_analyzers[:2])}{'...' if len(remaining_analyzers) > 2 else ''}")
                            else:
                                progress_callback(completed_count, total_count, "Finalizing results")
                            
                    except concurrent.futures.TimeoutError:
                        print(f"DEBUG: {analyzer_name} result timed out")
                        results[analyzer_name] = {
                            "analyzer": analyzer_name,
                            "error": "Result retrieval timed out",
                            "success": False
                        }
                        completed_count += 1
                    except Exception as e:
                        print(f"DEBUG: {analyzer_name} failed with error: {str(e)}")
                        results[analyzer_name] = {
                            "analyzer": analyzer_name,
                            "error": str(e),
                            "success": False
                        }
                        completed_count += 1
                        
            except concurrent.futures.TimeoutError:
                print("DEBUG: Overall analysis timed out")
                # Handle any remaining futures that didn't complete
                for future, analyzer_name in future_to_analyzer.items():
                    if analyzer_name not in results:
                        results[analyzer_name] = {
                            "analyzer": analyzer_name,
                            "error": "Analysis timed out",
                            "success": False
                        }
        
        print(f"DEBUG: Parallel analysis completed. Results: {len(results)} analyzers")
        return results

def main():
    st.set_page_config(
        page_title="AI Codebase Analyzer",
        page_icon="🔍",
        layout="wide"
    )
    
    # Hide Streamlit's default deploy button and menu + Fix styling
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none !important;}
    .stActionButton {display:none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    .stApp > header {display: none !important;}
    .stApp > .main .block-container {padding-top: 2rem !important;}
    footer {visibility: hidden !important;}
    #stDecoration {display:none !important;}
    button[title="Deploy this app"] {display: none !important;}
    .css-1rs6os {display: none !important;}
    .css-17eq0hr {display: none !important;}
    
    /* Fix text input styling - remove red border and improve appearance */
    .stTextInput > div > div > input {
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        background-color: white !important;
        box-sizing: border-box !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
        outline: none !important;
    }
    
    /* Ensure text input container stays within sidebar bounds - more aggressive approach */
    [data-testid="stSidebar"] .stTextInput {
        max-width: calc(100% - 2rem) !important;
        width: calc(100% - 2rem) !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > div {
        max-width: 100% !important;
        width: 100% !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div {
        max-width: 100% !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Force sidebar content to respect boundaries */
    [data-testid="stSidebar"] > div {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        box-sizing: border-box !important;
    }
    
    /* Fix sidebar spacing and alignment */
    [data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Improve checkbox alignment */
    .stCheckbox {
        margin-bottom: 0.5rem !important;
    }
    
    /* Fix button styling */
    .stButton > button {
        width: 100% !important;
        margin-top: 1rem !important;
    }
    
    /* Clean up form elements */
    .stSelectbox, .stTextInput {
        margin-bottom: 1rem !important;
    }
    
    /* Remove any error styling on inputs */
    .stTextInput [data-baseweb="input"]:not(:focus):not(:hover) {
        border-color: #d1d5db !important;
    }
    
    .stTextInput [data-baseweb="input"] {
        background-color: white !important;
    }
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Hide default Streamlit sidebar controls completely and add custom CSS for our toggle button
    st.markdown("""
    <style>
    /* Hide all default Streamlit sidebar collapse/expand controls */
    [data-testid="collapsedControl"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    .css-1outpf7 {display: none !important;}
    .css-vk3wp9 {display: none !important;}
    .css-14xtw13 {display: none !important;}
    .css-1lcbmhc {display: none !important;}
    .css-17eq0hr {display: none !important;}
    button[kind="header"] {display: none !important;}
    button[title="Expand sidebar"] {display: none !important;}
    button[title="Collapse sidebar"] {display: none !important;}
    button[aria-label="Expand sidebar"] {display: none !important;}
    button[aria-label="Collapse sidebar"] {display: none !important;}
    .stSidebar button[kind="header"] {display: none !important;}
    
    /* Additional targeting for any remaining default controls */
    [data-testid="stSidebar"] > div > div:first-child button:not([key="toggle_sidebar"]) {
        display: none !important;
    }
    
    /* Main content area adjustments - more aggressive targeting */
    .main, .main .block-container, .stApp > .main, [data-testid="stAppViewContainer"] .main {
        transition: margin-left 0.3s ease, max-width 0.3s ease, width 0.3s ease !important;
    }
    
    /* Target Streamlit's main content wrapper more specifically */
    .stApp > .main {
        margin-left: 21rem !important;
        width: calc(100vw - 21rem) !important;
        transition: all 0.3s ease !important;
    }
    
    /* When sidebar is collapsed - main content expands to full width */
    .sidebar-collapsed ~ .main,
    body:has(.sidebar-collapsed) .main,
    .stApp:has(.sidebar-collapsed) > .main {
        margin-left: 0 !important;
        width: 100vw !important;
        max-width: 100vw !important;
    }
    
    .sidebar-collapsed ~ .main .block-container,
    body:has(.sidebar-collapsed) .main .block-container {
        max-width: none !important;
        width: 100% !important;
        padding-left: 4rem !important;
        padding-right: 2rem !important;
    }
    
    /* Completely hide sidebar when collapsed - show only toggle button */
    [data-testid="stSidebar"].sidebar-collapsed {
        width: 60px !important;
        min-width: 60px !important;
        max-width: 60px !important;
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        transition: width 0.3s ease !important;
        position: fixed !important;
        z-index: 999999 !important;
    }
    
    /* Normal sidebar with smooth transition */
    [data-testid="stSidebar"] {
        transition: width 0.3s ease !important;
    }
    
    /* Hide the gray sidebar container completely when collapsed */
    [data-testid="stSidebar"].sidebar-collapsed > div {
        display: none !important;
    }
    
    /* Hide all sidebar content except toggle button when collapsed */
    [data-testid="stSidebar"].sidebar-collapsed .element-container:not(:first-child) {
        display: none !important;
    }
    
    /* Make toggle button float and be visible when collapsed */
    [data-testid="stSidebar"].sidebar-collapsed .element-container:first-child {
        position: fixed !important;
        top: 1rem !important;
        left: 1rem !important;
        z-index: 999999 !important;
        background: transparent !important;
        width: auto !important;
        display: block !important;
    }
    
    /* Style the toggle button to be prominent and accessible */
    [data-testid="stSidebar"] button[key="toggle_sidebar"] {
        width: 45px !important;
        height: 45px !important;
        padding: 5px !important;
        font-size: 16px !important;
        background-color: #007bff !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        margin: 2px auto !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    [data-testid="stSidebar"] button[key="toggle_sidebar"]:hover {
        background-color: #0056b3 !important;
        transform: scale(1.05) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main app header
    st.title("🔍 AI-Powered Codebase Analyzer")
    st.markdown("Accelerate codebase onboarding and architectural discovery")
    
    # Initialize session state
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'results' not in st.session_state:
        st.session_state.results = {}
    if 'sidebar_collapsed' not in st.session_state:
        st.session_state.sidebar_collapsed = False
    
    # Apply CSS class conditionally for sidebar collapse with ultra-aggressive DOM manipulation
    if st.session_state.sidebar_collapsed:
        st.markdown("""
        <script>
        (function() {
            // Force immediate execution
            function collapseInterface() {
                const sidebar = document.querySelector('[data-testid="stSidebar"]');
                const main = document.querySelector('.main');
                const mainContainer = document.querySelector('.main .block-container');
                const stApp = document.querySelector('.stApp');
                
                // Completely hide sidebar - only show toggle button
                if (sidebar) {
                    sidebar.classList.add('sidebar-collapsed');
                    sidebar.style.width = '60px !important';
                    sidebar.style.minWidth = '60px !important';
                    sidebar.style.maxWidth = '60px !important';
                    sidebar.style.position = 'fixed';
                    sidebar.style.zIndex = '999999';
                    sidebar.style.background = 'transparent';
                    sidebar.style.border = 'none';
                    sidebar.style.transition = 'width 0.3s ease';
                }
                
                // Expand main content to full width (with small margin for floating button)
                if (main) {
                    main.classList.add('sidebar-collapsed');
                    main.style.marginLeft = '0 !important';
                    main.style.width = '100vw !important';
                    main.style.maxWidth = '100vw !important';
                    main.style.transition = 'all 0.3s ease !important';
                    main.style.position = 'relative';
                    main.style.left = '0px';
                }
                
                // Also target the inner container
                if (mainContainer) {
                    mainContainer.style.maxWidth = '100% !important';
                    mainContainer.style.width = '100% !important';
                    mainContainer.style.paddingLeft = '4rem !important';
                    mainContainer.style.paddingRight = '2rem !important';
                    mainContainer.style.marginLeft = '0 !important';
                }
                
                // Set body class for global styling
                document.body.classList.add('sidebar-collapsed');
                document.body.style.overflow = 'auto';
                
                console.log('COLLAPSED: Sidebar completely hidden, main content expanded to full width');
            }
            
            // Execute immediately and with delays to force layout
            collapseInterface();
            setTimeout(collapseInterface, 50);
            setTimeout(collapseInterface, 200);
            setTimeout(collapseInterface, 500);
        })();
        </script>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <script>
        (function() {
            // Force immediate execution
            function expandInterface() {
                const sidebar = document.querySelector('[data-testid="stSidebar"]');
                const main = document.querySelector('.main');
                const mainContainer = document.querySelector('.main .block-container');
                
                // Expand sidebar back to normal
                if (sidebar) {
                    sidebar.classList.remove('sidebar-collapsed');
                    sidebar.style.width = '';
                    sidebar.style.minWidth = '';
                    sidebar.style.maxWidth = '';
                    sidebar.style.position = '';
                    sidebar.style.zIndex = '';
                    sidebar.style.background = '';
                    sidebar.style.borderRight = '';
                }
                
                // Move main content back to normal position
                if (main) {
                    main.classList.remove('sidebar-collapsed');
                    main.style.marginLeft = '21rem !important';
                    main.style.width = 'calc(100vw - 21rem) !important';
                    main.style.maxWidth = 'calc(100vw - 21rem) !important';
                    main.style.transition = 'all 0.4s ease !important';
                    main.style.position = '';
                    main.style.left = '';
                }
                
                // Reset container styles
                if (mainContainer) {
                    mainContainer.style.maxWidth = '';
                    mainContainer.style.width = '';
                    mainContainer.style.paddingLeft = '';
                    mainContainer.style.paddingRight = '';
                    mainContainer.style.marginLeft = '';
                }
                
                // Remove body class
                document.body.classList.remove('sidebar-collapsed');
                
                console.log('EXPANDED: Sidebar restored to full width, main content returned to normal');
            }
            
            // Execute immediately and with delays to force layout
            expandInterface();
            setTimeout(expandInterface, 50);
            setTimeout(expandInterface, 200);
            setTimeout(expandInterface, 500);
        })();
        </script>
        """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        # Custom toggle button - always visible at the top
        toggle_icon = "▶" if st.session_state.sidebar_collapsed else "◀"
        toggle_help = "Expand sidebar" if st.session_state.sidebar_collapsed else "Collapse sidebar"
        
        if st.button(toggle_icon, key="toggle_sidebar", help=toggle_help):
            st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
            st.rerun()
        
        # Only show content when not collapsed
        if not st.session_state.sidebar_collapsed:
            st.header("Repository Configuration")
            
            # Repository path input
            repo_path = st.text_input(
                "Repository Path",
                value="/path/to/your/repo",
                help="Enter the full path to your Git repository"
            )
            
            # Add instruction text positioned directly under the input field
            st.markdown(
                '<div style="margin-top: -20px; margin-bottom: 15px; color: #666; font-size: 12px; font-style: italic; text-align: right; padding-right: 2px;">Press Enter to Apply</div>', 
                unsafe_allow_html=True
            )
            
            st.markdown("---")
            
            # Analysis selection
            st.header("Select Analyses")
            analysis_options = {
                'expertise': '👥 Team Expertise Mapping',
                'timeline': '📅 Timeline Analysis',
                'api_contracts': '🔗 API Contracts',
                'ai_context': '🤖 AI Context Analysis',
                'risk_analysis': '⚠️ Risk Analysis',
                'development_patterns': '🔄 Development Patterns',
                'version_governance': '📦 Version Governance',
                'tech_debt': '🔧 Technical Debt Detection',
                'design_patterns': '🏗️ Design Patterns'
            }
            
            selected_analyses = {}
            for key, label in analysis_options.items():
                selected_analyses[key] = st.checkbox(label, value=True, key=f"check_{key}")
            
            st.markdown("---")
            
            # Run analysis button
        else:
            # When collapsed, we still need these variables for the button logic
            repo_path = "/path/to/your/repo"
            selected_analyses = {key: True for key in ['expertise', 'timeline', 'api_contracts', 'ai_context', 'risk_analysis', 'development_patterns', 'version_governance', 'tech_debt', 'design_patterns']}
            analysis_options = {
                'expertise': '👥 Team Expertise Mapping',
                'timeline': '📅 Timeline Analysis',
                'api_contracts': '🔗 API Contracts',
                'ai_context': '🤖 AI Context Analysis',
                'risk_analysis': '⚠️ Risk Analysis',
                'development_patterns': '🔄 Development Patterns',
                'version_governance': '📦 Version Governance',
                'tech_debt': '🔧 Technical Debt Detection',
                'design_patterns': '🏗️ Design Patterns'
            }
        
        # Show run button only when expanded
        if not st.session_state.sidebar_collapsed and st.button("🚀 Run Selected Analyses", type="primary", use_container_width=True):
            if not repo_path or repo_path == "/path/to/your/repo":
                st.error("Please enter a valid repository path!")
            elif not os.path.exists(repo_path):
                st.error(f"Repository path does not exist: {repo_path}")
            elif not any(selected_analyses.values()):
                st.error("Please select at least one analysis to run!")
            else:
                # Run the analysis
                st.session_state.analysis_complete = False
                st.session_state.results = {}
                
                with st.spinner("Initializing analysis..."):
                    try:
                        analyzer = ParallelAIAnalyzer(repo_path)
                        
                        # Filter analyzers based on selection
                        analyzer.analyzers = {
                            k: v for k, v in analyzer.analyzers.items() 
                            if selected_analyses.get(k, False)
                        }
                        
                        # Progress tracking
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        def progress_callback(completed, total, status):
                            progress = completed / total if total > 0 else 0
                            progress_bar.progress(progress)
                            status_text.text(f"Progress: {completed}/{total} - {status}")
                        
                        # Run analysis
                        results = analyzer.run_parallel_analysis(progress_callback)
                        
                        st.session_state.results = results
                        st.session_state.analysis_complete = True
                        
                        progress_bar.progress(1.0)
                        status_text.text("Analysis complete!")
                        st.success("✅ Analysis completed successfully!")
                        
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")
    
    # Main content area
    if not st.session_state.analysis_complete:
        st.markdown("## 🚀 Welcome to AI Codebase Analyzer")
        
        st.markdown("""
        This tool helps you quickly understand and analyze any Git repository using AI-powered insights.
        
        **Getting Started:**
        
        1. 👈 Enter your repository path in the sidebar
        2. 🎯 Select the analyses you want to run
        3. 🚀 Click "Run Selected Analyses" to get AI insights
        4. 📊 View results in the tabs that appear
        
        **What you'll get:**
        
        • Deep insights into code structure and patterns
        • Team expertise mapping and collaboration analysis  
        • Risk assessment and technical debt detection
        • API contracts and integration analysis
        • Timeline and development velocity insights
        """)
        
    else:
        # Show results in tabs
        results = st.session_state.results
        successful_results = {k: v for k, v in results.items() if v.get('success', False)}
        
        if successful_results:
            # Create tabs for successful analyses
            tab_names = []
            tab_data = []
            
            for analyzer_name, result in successful_results.items():
                display_name = analyzer_name.replace('_', ' ').title()
                tab_names.append(display_name)
                tab_data.append((analyzer_name, result))
            
            tabs = st.tabs(tab_names)
            
            for i, (tab, (analyzer_name, result)) in enumerate(zip(tabs, tab_data)):
                with tab:
                    st.header(f"{analysis_options.get(analyzer_name, analyzer_name.replace('_', ' ').title())}")
                    
                    if 'insight' in result:
                        st.markdown(result['insight'])
                    else:
                        st.error("No AI insight available for this analysis")
                    
                    # Show raw data in expander if available
                    if 'analysis_data' in result:
                        with st.expander("📊 Raw Analysis Data"):
                            st.json(result['analysis_data'])
        
        # Show any failures
        failed_results = {k: v for k, v in results.items() if not v.get('success', False)}
        if failed_results:
            st.error("❌ Some analyses failed:")
            for analyzer_name, result in failed_results.items():
                st.error(f"**{analyzer_name.replace('_', ' ').title()}**: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
