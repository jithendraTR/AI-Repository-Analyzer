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
from analyzers.singular_product_vision import SingularProductVisionAnalyzer
from utils.ai_client import OpenArenaClient
from utils.git_handler import validate_and_prepare_repository, git_handler

class CancellationToken:
    """Simple cancellation token for stopping analysis"""
    def __init__(self):
        self.cancelled = False
        
    
    def cancel(self):
        self.cancelled = True
    
    def is_cancelled(self):
        return self.cancelled
        
    def check_cancellation(self):
        """Raise an exception if cancelled"""
        if self.is_cancelled():
            raise Exception("Operation was cancelled")

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
            'design_patterns': DesignPatternAnalyzer(repo_path),
            'singular_product_vision': SingularProductVisionAnalyzer(repo_path)
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
                # Check for cancellation during progress updates
                if self.cancellation_token and self.cancellation_token.is_cancelled():
                    raise Exception("Operation was cancelled during analysis")
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
            
            # Get AI insight with more frequent cancellation checks
            try:
                insight = self.ai_client.query(prompt)
                
                # Final cancellation check
                if self.cancellation_token and self.cancellation_token.is_cancelled():
                    return {
                        "analyzer": analyzer_name,
                        "error": "Operation was cancelled",
                        "success": False,
                        "cancelled": True
                    }
                
                # If AI insight was successful, return with insight
                if insight and insight.strip():
                    return {
                        "analyzer": analyzer_name,
                        "insight": insight,
                        "success": True,
                        "analysis_data": analysis_data  # Include raw analysis data
                    }
                else:
                    # AI insight failed but analysis data is still valid - mark as success
                    return {
                        "analyzer": analyzer_name,
                        "insight": "⚠️ AI insight generation failed, but analysis data is available. Check the Raw Analysis Data section below for detailed results.",
                        "success": True,  # Still mark as success!
                        "analysis_data": analysis_data,  # Raw data is still valuable
                        "ai_insight_failed": True
                    }
            except Exception as ai_error:
                # AI insight failed but analysis data is still valid - mark as success
                print(f"DEBUG: AI insight generation failed for {analyzer_name}: {ai_error}")
                return {
                    "analyzer": analyzer_name,
                    "insight": f"⚠️ AI insight generation failed ({str(ai_error)}), but analysis data is available. Check the Raw Analysis Data section below for detailed results.",
                    "success": True,  # Still mark as success!
                    "analysis_data": analysis_data,  # Raw data is still valuable
                    "ai_insight_failed": True
                }
        except Exception as e:
            # Check if it's a cancellation
            if "cancelled" in str(e).lower() or (self.cancellation_token and self.cancellation_token.is_cancelled()):
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
            """,
            
            'singular_product_vision': f"""
            Analyze the product vision coherence and strategic alignment:
            {str(analysis_data)[:2000]}
            
            Provide:
            1. Product vision clarity and consistency assessment
            2. Feature alignment with strategic goals analysis
            3. Areas where vision could be strengthened
            4. Recommendations for maintaining product focus
            5. Strategic suggestions for better feature coherence
            6. Potential risks to product direction
            """
        }
        
        return prompts.get(analyzer_name, f"Analyze this data: {str(analysis_data)[:2000]}")
    
    def run_parallel_analysis(self, progress_callback=None) -> Dict[str, Any]:
        """Run AI analysis for all analyzers sequentially with immediate cancellation support"""
        results = {}
        completed_count = 0
        total_count = len(self.analyzers)
        
        # Immediate cancellation check before starting anything
        if self.cancellation_token and self.cancellation_token.is_cancelled():
            print("DEBUG: Analysis was cancelled before starting")
            # Return cancelled results for all analyzers
            for analyzer_name in self.analyzers.keys():
                results[analyzer_name] = {
                    "analyzer": analyzer_name,
                    "error": "Operation was cancelled",
                    "success": False,
                    "cancelled": True
                }
            return results
        
        # Debug: Print what analyzers we're about to run
        print(f"DEBUG: Starting sequential analysis for {total_count} analyzers: {list(self.analyzers.keys())}")
        
        # Run analyzers sequentially for immediate cancellation
        for name, analyzer in self.analyzers.items():
            # Check cancellation before each analyzer
            if self.cancellation_token and self.cancellation_token.is_cancelled():
                print(f"DEBUG: Cancellation detected before starting {name}")
                # Mark this analyzer as cancelled
                results[name] = {
                    "analyzer": name,
                    "error": "Operation was cancelled",
                    "success": False,
                    "cancelled": True
                }
                # Mark all remaining analyzers as cancelled too
                remaining_analyzers = list(self.analyzers.keys())[list(self.analyzers.keys()).index(name)+1:]
                for remaining_name in remaining_analyzers:
                    results[remaining_name] = {
                        "analyzer": remaining_name,
                        "error": "Operation was cancelled",
                        "success": False,
                        "cancelled": True
                    }
                break
            
            print(f"DEBUG: Starting {name}")
            
            # Update progress
            if progress_callback:
                progress_callback(completed_count, total_count, f"Running: {name.replace('_', ' ').title()}")
            
            # Run single analysis with frequent cancellation checks
            result = self.run_single_analysis(name, analyzer)
            results[name] = result
            completed_count += 1
            
            # Check if this analyzer was cancelled
            if result.get('cancelled', False):
                print(f"DEBUG: {name} was cancelled, stopping remaining analyzers")
                # Mark all remaining analyzers as cancelled
                remaining_analyzers = list(self.analyzers.keys())[list(self.analyzers.keys()).index(name)+1:]
                for remaining_name in remaining_analyzers:
                    results[remaining_name] = {
                        "analyzer": remaining_name,
                        "error": "Operation was cancelled",
                        "success": False,
                        "cancelled": True
                    }
                break
        
        print(f"DEBUG: Sequential analysis completed. Results: {len(results)} analyzers")
        return results

def main():
    st.set_page_config(
        page_title="AI Codebase Analyzer",
        page_icon="🔍",
        layout="wide"
    )
    
    # Hide Streamlit's default deploy button and menu + Fix styling + HIDE CHAIN LINK ICONS
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
    
    /* HIDE ALL CHAIN LINK ICONS FROM HEADERS AND SUBHEADERS */
    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a, .stMarkdown h4 a, .stMarkdown h5 a, .stMarkdown h6 a {
        display: none !important;
        visibility: hidden !important;
    }
    [data-testid="stHeader"] a, [data-testid="stSubheader"] a {
        display: none !important;
        visibility: hidden !important;
    }
    .element-container h1 a, .element-container h2 a, .element-container h3 a {
        display: none !important;
        visibility: hidden !important;
    }
    h1 a[href^="#"], h2 a[href^="#"], h3 a[href^="#"], h4 a[href^="#"], h5 a[href^="#"], h6 a[href^="#"] {
        display: none !important;
        visibility: hidden !important;
    }
    /* Target any link icon specifically */
    .stMarkdown a[href^="#"]:before, .stMarkdown a[href^="#"]:after {
        display: none !important;
    }
    /* Hide anchor links completely */
    a.anchor-link, .anchor-link {
        display: none !important;
        visibility: hidden !important;
    }
    /* Additional comprehensive targeting */
    [data-testid="element-container"] a[href^="#"] {
        display: none !important;
    }
    
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
    
    # Main app header with summary button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🔍 AI-Powered Codebase Analyzer")
        st.markdown("Accelerate codebase onboarding and architectural discovery")
    
    with col2:
        # Summary button positioned at top right
        if st.button("📋 Summary", type="secondary", help="Show comprehensive project analysis", key="summary_button"):
            if st.session_state.get('actual_repo_path'):
                st.session_state.show_summary_popup = True
            else:
                st.error("Please load a repository first!")
    
# Summary popup display - True modal overlay
    if st.session_state.get('show_summary_popup', False):
        display_summary_modal()
    
    # Initialize session state
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'results' not in st.session_state:
        st.session_state.results = {}
    if 'sidebar_collapsed' not in st.session_state:
        st.session_state.sidebar_collapsed = False
    if 'analysis_running' not in st.session_state:
        st.session_state.analysis_running = False
    if 'current_analyzer' not in st.session_state:
        st.session_state.current_analyzer = None
    if 'last_repo_path' not in st.session_state:
        st.session_state.last_repo_path = ""
    if 'success_message' not in st.session_state:
        st.session_state.success_message = ""
    if 'success_message_time' not in st.session_state:
        st.session_state.success_message_time = 0
    if 'cancellation_token' not in st.session_state:
        st.session_state.cancellation_token = None
    if 'prepared_repo_info' not in st.session_state:
        st.session_state.prepared_repo_info = None
    if 'actual_repo_path' not in st.session_state:
        st.session_state.actual_repo_path = ""
    
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
        
        # Initialize repo_path from session state (always available)
        repo_path = st.session_state.get('last_repo_path', '')
        
        # Only show content when not collapsed
        if not st.session_state.sidebar_collapsed:
            st.header("Repository Configuration")
            
            # Repository path input with session state value
            repo_path = st.text_input(
                "Repository Path",
                value=st.session_state.get('last_repo_path', ''),
                placeholder="C:\\path\\to\\your\\repo",
                help="Enter the full path to your Git repository",
                key="repo_path_input"
            )
            
            # Add commit time frame selection
            st.subheader("⏱️ Commit Time Frame")
            time_frame_options = {
                "all": "All commits",
                "1_year": "Last 1 year",
                "2_years": "Last 2 years", 
                "3_years": "Last 3 years",
                "5_years": "Last 5 years"
            }
            
            selected_time_frame = st.selectbox(
                "Select analysis time period",
                options=list(time_frame_options.keys()),
                format_func=lambda x: time_frame_options[x],
                index=0,  # Default to "all"
                help="Choose how far back in commit history to analyze",
                key="time_frame_selection"
            )
            
            # Store time frame in session state
            st.session_state['selected_time_frame'] = selected_time_frame
            
            # Add Apply button
            col1, col2 = st.columns([1.2, 2.8])
            with col1:
                apply_clicked = st.button("🔄 Apply", type="secondary", help="Load the repository", use_container_width=True)
            with col2:
                st.markdown(
                    '<div style="margin-top: 8px; color: #888; font-size: 13px; font-style: italic;">Click Apply to load repository</div>', 
                    unsafe_allow_html=True
                )
            
            # Check if repository should be loaded (Apply button only)
            repo_should_load = False
            if apply_clicked:
                repo_should_load = True
            
            # Show immediate validation feedback for any valid path entered
            if repo_should_load:
                if repo_path and repo_path.strip() and repo_path not in ["/path/to/your/repo", "C:\\path\\to\\your\\repo"]:
                    # Fast path detection: check if it's a Git URL first
                    is_git_url = (repo_path.startswith('https://github.com/') or 
                                 repo_path.startswith('git@github.com:') or
                                 repo_path.startswith('https://gitlab.com/') or
                                 repo_path.startswith('git@gitlab.com:'))
                    
                    if is_git_url:
                        # It's a Git URL - use the full validation and cloning process
                        validation_result = validate_and_prepare_repository(repo_path)
                        
                        if validation_result['success']:
                            # Clone the repository
                            clone_result = git_handler.clone_repository(repo_path)
                            if clone_result['success']:
                                success_msg = f"✅ Git repository cloned successfully! {clone_result.get('info', '')}"
                                # Store both original URL and local path
                                st.session_state.prepared_repo_info = clone_result
                                st.session_state.actual_repo_path = clone_result['local_path']
                                st.session_state.last_repo_path = repo_path  # Keep original URL for display
                            else:
                                st.error(f"❌ Failed to clone Git repository: {clone_result['error']}")
                                return  # Exit early on clone failure
                        else:
                            st.error(f"❌ Repository validation failed: {validation_result['error']}")
                            return
                    else:
                        # It's a local path - use the original fast validation (PRESERVE ORIGINAL PERFORMANCE)
                        if os.path.exists(repo_path):
                            # Check if it's a git repository
                            if os.path.exists(os.path.join(repo_path, '.git')):
                                success_msg = "✅ Repository loaded successfully! Valid Git repository detected"
                            else:
                                success_msg = "✅ Repository loaded successfully! Directory found (not a Git repository)"
                            
                            # For local paths, actual path is the same as input path (no cloning needed)
                            st.session_state.prepared_repo_info = None
                            st.session_state.actual_repo_path = repo_path
                            st.session_state.last_repo_path = repo_path
                        else:
                            st.error("❌ Repository path does not exist. Please check the path and try again.")
                            return
                    
                    # Show success message
                    st.session_state.success_message = success_msg
                    st.session_state.success_message_time = time.time()
                    st.success(success_msg)
                else:
                    st.error("❌ Please enter a valid repository path or Git URL.")
            
            # Show stored success message if within time limit
            elif st.session_state.get('success_message') and time.time() - st.session_state.get('success_message_time', 0) < 3:
                st.success(st.session_state.get('success_message'))
            
            st.markdown("---")
            
            # Analysis selection
            st.header("🎯 Select Analysis")
            analysis_options = {
                'expertise': '👥 Team Expertise Mapping',
                'timeline': '📅 Timeline Analysis',
                'api_contracts': 'API Contracts',
                'ai_context': '🤖 AI Context Analysis',
                'risk_analysis': '⚠️ Risk Analysis',
                'development_patterns': '🔄 Development Patterns',
                'version_governance': '📦 Version Governance',
                'tech_debt': '🔧 Technical Debt Detection',
                'design_patterns': '🏗️ Design Patterns',
                'singular_product_vision': '🎯 Singular Product Vision'
            }
            
            st.markdown("Choose which analyses to run on your repository")
            
            # Add Select All / Clear All buttons side by side
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Select All", key="select_all"):
                    for key in analysis_options.keys():
                        st.session_state[f"selected_{key}"] = True
                    # Increment counter to force multiselect refresh
                    if 'multiselect_refresh_counter' not in st.session_state:
                        st.session_state.multiselect_refresh_counter = 0
                    st.session_state.multiselect_refresh_counter += 1
            
            with col2:
                if st.button("🗑️ Clear All", key="clear_all"):
                    for key in analysis_options.keys():
                        st.session_state[f"selected_{key}"] = False
                    # Increment counter to force multiselect refresh
                    if 'multiselect_refresh_counter' not in st.session_state:
                        st.session_state.multiselect_refresh_counter = 0
                    st.session_state.multiselect_refresh_counter += 1
            
            # Initialize selected analyses in session state if not present
            for key in analysis_options.keys():
                if f"selected_{key}" not in st.session_state:
                    st.session_state[f"selected_{key}"] = False
            
            # Display multiselect with current selection
            st.markdown("Select analyses to run:")
            
            # Create a multiselect for analyses
            options = list(analysis_options.values())
            keys = list(analysis_options.keys())
            
            # Get default selections based on session state
            default_selections = [
                options[i] for i, key in enumerate(keys) 
                if st.session_state.get(f"selected_{key}", False)
            ]
            
            selected_options = st.multiselect(
                "Select analyses",
                options=options,
                default=default_selections,
                label_visibility="collapsed",
                key=f"multiselect_analyses_{st.session_state.get('multiselect_refresh_counter', 0)}"
            )
            
            # Update session state based on selection
            selected_analyses = {}
            for key, label in analysis_options.items():
                is_selected = label in selected_options
                selected_analyses[key] = is_selected
                # Only update session state if there's a change to avoid conflicts
                current_state = st.session_state.get(f"selected_{key}", False)
                if current_state != is_selected:
                    st.session_state[f"selected_{key}"] = is_selected
            
            # Show count of selected analyses in the run button
            selected_count = sum(1 for v in selected_analyses.values() if v)
            
            # Debug: Show what's actually selected
            print(f"DEBUG: UI Selection State: {selected_analyses}")
            print(f"DEBUG: Selected count: {selected_count}")
            
            st.markdown("---")
        else:
            # When collapsed, get selected analyses from session state
            selected_analyses = {}
            analysis_options = {
                'expertise': '👥 Team Expertise Mapping',
                'timeline': '📅 Timeline Analysis',
                'api_contracts': 'API Contracts',
                'ai_context': '🤖 AI Context Analysis',
                'risk_analysis': '⚠️ Risk Analysis',
                'development_patterns': '🔄 Development Patterns',
                'version_governance': '📦 Version Governance',
                'tech_debt': '🔧 Technical Debt Detection',
                'design_patterns': '🏗️ Design Patterns',
                'singular_product_vision': '🎯 Singular Product Vision'
            }
            # Get selections from session state
            for key in analysis_options.keys():
                selected_analyses[key] = st.session_state.get(f"selected_{key}", False)
            selected_count = sum(1 for v in selected_analyses.values() if v)
        
        # Show run button only when expanded and not running
        if not st.session_state.sidebar_collapsed:
            if st.session_state.analysis_complete:
                # Show completed analysis button and option to run new analysis
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.button("✅ Completed Analysis!", type="primary", use_container_width=True, disabled=True)
                with col2:
                    if st.button("🔄 New", type="secondary", use_container_width=True, help="Run new analysis"):
                        st.session_state.analysis_complete = False
                        st.session_state.results = {}
                        st.rerun()
            elif not st.session_state.analysis_running:
                if st.button(f"🚀 Run {selected_count} Selected Analyses", type="primary", use_container_width=True):
                    # Check if repository is properly loaded
                    actual_repo_path = st.session_state.get('actual_repo_path', '')
                    original_repo_path = st.session_state.get('last_repo_path', '')
                    
                    if not original_repo_path or not original_repo_path.strip():
                        st.error("Please enter a repository path and click Apply button to load it first!")
                    elif not actual_repo_path or not actual_repo_path.strip():
                        st.error("Repository not properly loaded. Please click Apply button to load the repository first!")
                    elif not os.path.exists(actual_repo_path):
                        st.error(f"Repository path does not exist: {actual_repo_path}")
                    elif not any(selected_analyses.values()):
                        st.error("Please select at least one analysis to run!")
                    else:
                        # Start the analysis
                        st.session_state.analysis_running = True
                        st.session_state.analysis_complete = False
                        st.session_state.results = {}
                        # Store selected analyses for the execution phase
                        st.session_state.selected_analyses = selected_analyses
                        st.rerun()
            else:
                # Show stop button when analysis is running with improved styling
                if st.button(f"⛔ Stop Analysis", type="secondary", use_container_width=True, key="stop_analysis_btn"):
                    # Immediately stop the analysis
                    st.session_state.analysis_running = False
                    st.session_state.analysis_complete = False
                    
                    # Cancel the current analysis if it exists
                    if st.session_state.cancellation_token:
                        st.session_state.cancellation_token.cancel()
                    
                    if st.session_state.current_analyzer and hasattr(st.session_state.current_analyzer, 'cancellation_token'):
                        if st.session_state.current_analyzer.cancellation_token:
                            st.session_state.current_analyzer.cancellation_token.cancel()
                    
                    # Cleanup Git repository if it was cloned
                    if st.session_state.get('prepared_repo_info') and st.session_state.prepared_repo_info.get('temp_dir'):
                        temp_dir = st.session_state.prepared_repo_info['temp_dir']
                        if git_handler.cleanup_repository(temp_dir):
                            print(f"DEBUG: Cleaned up temporary Git repository: {temp_dir}")
                        st.session_state.prepared_repo_info = None
                        st.session_state.actual_repo_path = ""
                    
                    # Clear analyzer reference
                    st.session_state.current_analyzer = None
                    st.session_state.cancellation_token = None
                    
                    # Show immediate feedback
                    st.error("🛑 Analysis stopped by user!")
                    st.rerun()
                
                # Also add a disabled run button to show it's not available
                st.button(f"🚀 Run {selected_count} Selected Analyses", type="primary", disabled=True, use_container_width=True, 
                         help="Analysis is currently running. Click 'Stop Analysis' to cancel.")
    
    # Handle analysis execution
    if st.session_state.analysis_running and not st.session_state.analysis_complete:
        st.markdown("## 🔄 Analysis in Progress")
        st.markdown("Running AI-powered analysis on your repository...")
        
        try:
            # Get the actual local repository path (could be original local path or cloned Git repo path)
            actual_repo_path = st.session_state.get('actual_repo_path', '')
            original_repo_path = st.session_state.get('last_repo_path', '')
            
            if not actual_repo_path or not actual_repo_path.strip():
                st.error("Invalid repository path! Please enter a valid path in the sidebar and click Apply.")
                st.session_state.analysis_running = False
                st.rerun()
            elif not os.path.exists(actual_repo_path):
                st.error(f"Repository path does not exist: {actual_repo_path}")
                st.session_state.analysis_running = False
                st.rerun()
            
            # Create analyzer
            analyzer = ParallelAIAnalyzer(actual_repo_path)
            st.session_state.current_analyzer = analyzer
            
            # Create and set cancellation token
            cancellation_token = CancellationToken()
            st.session_state.cancellation_token = cancellation_token
            analyzer.set_cancellation_token(cancellation_token)
            
            # Filter analyzers based on selection
            if hasattr(st.session_state, 'selected_analyses') and st.session_state.selected_analyses:
                # Filter to only run selected analyses
                selected_analyzer_keys = [k for k, v in st.session_state.selected_analyses.items() if v]
                if selected_analyzer_keys:
                    # Only filter if there are actually selected analyzers
                    print(f"DEBUG: Running {len(selected_analyzer_keys)} selected analyzers: {selected_analyzer_keys}")
                    analyzer.analyzers = {
                        k: v for k, v in analyzer.analyzers.items() 
                        if k in selected_analyzer_keys
                    }
                else:
                    # If no analyzers are explicitly selected, run all analyzers (DON'T FILTER)
                    print(f"DEBUG: No analyzers selected, running all {len(analyzer.analyzers)} analyzers by default")
            else:
                # If no selection state exists, run all analyzers (DON'T FILTER)
                print(f"DEBUG: No selection state found, running all {len(analyzer.analyzers)} analyzers by default")
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def progress_callback(completed, total, status):
                # Check if analysis was stopped
                if not st.session_state.analysis_running:
                    return
                progress = completed / total if total > 0 else 0
                progress_bar.progress(progress)
                status_text.text(f"Progress: {completed}/{total} - {status}")
            
            # Run analysis with immediate cancellation check
            if st.session_state.analysis_running:  # Double-check before starting
                with st.spinner("Running analysis..."):
                    results = analyzer.run_parallel_analysis(progress_callback)
            else:
                # Analysis was cancelled before it could start
                results = {}
                for analyzer_name in analyzer.analyzers.keys():
                    results[analyzer_name] = {
                        "analyzer": analyzer_name,
                        "error": "Operation was cancelled",
                        "success": False,
                        "cancelled": True
                    }
            
            # Store results and complete
            st.session_state.results = results
            st.session_state.analysis_complete = True
            st.session_state.analysis_running = False
            st.session_state.current_analyzer = None
            
            progress_bar.progress(1.0)
            status_text.text("Analysis complete!")
            st.success("✅ Analysis completed successfully!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.session_state.analysis_running = False
            st.session_state.current_analyzer = None
    
    # Main content area
    elif not st.session_state.analysis_complete:
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
                    
                    # First check if we should render with analyzer-specific UI
                    analyzer_instance = None
                    # Use actual_repo_path (could be local path or cloned Git repo path)
                    actual_path = st.session_state.get('actual_repo_path', '')
                    if actual_path and analyzer_name == 'timeline':
                        analyzer_instance = TimelineAnalyzer(actual_path)
                    elif actual_path and analyzer_name == 'expertise':
                        analyzer_instance = ExpertiseMapper(actual_path)
                    elif actual_path and analyzer_name == 'api_contracts':
                        analyzer_instance = APIContractAnalyzer(actual_path)
                    elif actual_path and analyzer_name == 'ai_context':
                        analyzer_instance = AIContextAnalyzer(actual_path)
                    elif actual_path and analyzer_name == 'risk_analysis':
                        analyzer_instance = RiskAnalysisAnalyzer(actual_path)
                    elif actual_path and analyzer_name == 'development_patterns':
                        analyzer_instance = DevelopmentPatternsAnalyzer(actual_path)
                    elif actual_path and analyzer_name == 'version_governance':
                        analyzer_instance = VersionGovernanceAnalyzer(actual_path)
                    elif actual_path and analyzer_name == 'tech_debt':
                        analyzer_instance = TechDebtDetectionAnalyzer(actual_path)
                    elif actual_path and analyzer_name == 'design_patterns':
                        analyzer_instance = DesignPatternAnalyzer(actual_path)
                    elif actual_path and analyzer_name == 'singular_product_vision':
                        analyzer_instance = SingularProductVisionAnalyzer(actual_path)
                    
                    if analyzer_instance and hasattr(analyzer_instance, 'render'):
                        # Store the analysis data in session state so the renderer can access it
                        if 'analysis_data' in result:
                            st.session_state[f"{analyzer_name}_analysis_data"] = result['analysis_data']
                        # Render using the analyzer's custom renderer
                        analyzer_instance.render()
                    else:
                        # Fallback to default rendering
                        if 'insight' in result:
                            st.markdown(result['insight'])
                        else:
                            st.error("No AI insight available for this analysis")
                        
                        # Show raw data in expander if available
                        if 'analysis_data' in result:
                            with st.expander("📊 Raw Analysis Data"):
                                st.json(result['analysis_data'])
        
        # Show any failures (excluding cancelled operations)
        failed_results = {k: v for k, v in results.items() 
                         if not v.get('success', False) and not v.get('cancelled', False)}
        if failed_results:
            st.error("❌ Some analyses failed:")
            for analyzer_name, result in failed_results.items():
                st.error(f"**{analyzer_name.replace('_', ' ').title()}**: {result.get('error', 'Unknown error')}")
        
        # Show cancelled operations separately if any
        cancelled_results = {k: v for k, v in results.items() if v.get('cancelled', False)}
        if cancelled_results:
            st.warning("⚠️ Some analyses were cancelled:")
            for analyzer_name, result in cancelled_results.items():
                st.info(f"**{analyzer_name.replace('_', ' ').title()}**: Operation was stopped by user")

# Cleanup function to be called on app exit
@st.dialog("📋 Comprehensive Project Summary")
def display_summary_modal():
    """Display comprehensive project analysis as a true modal popup"""
    
    actual_repo_path = st.session_state.get('actual_repo_path', '')
    
    if not actual_repo_path or not os.path.exists(actual_repo_path):
        st.error("❌ Repository not loaded. Please load a repository first!")
        if st.button("Close", type="primary"):
            st.rerun()
        return
    
    try:
        with st.spinner("🔍 Analyzing repository structure and generating comprehensive summary..."):
            # Generate summary data
            summary_data = generate_project_summary(actual_repo_path)
        
        # Display sections using native Streamlit components
        st.subheader("🎯 Project Summary")
        st.info(summary_data['project_summary'])
        
        st.subheader("🏗️ Architecture")
        st.info(summary_data['architecture'])
        
        st.subheader("💻 Languages and Frameworks")
        st.code(summary_data['languages_frameworks'], language='text')
        
        st.subheader("📁 Project Structure")
        st.code(summary_data['project_structure'], language='text')
        
        if summary_data['authentication_authorization']:
            st.subheader("🔐 Authentication and Authorization")
            st.info(summary_data['authentication_authorization'])
        
        # Close button at bottom
        if st.button("✅ Close Summary", type="primary", use_container_width=True):
            st.rerun()
            
    except Exception as e:
        st.error(f"❌ Error generating summary: {str(e)}")
        if st.button("Close", type="primary"):
            st.rerun()


def generate_project_summary(repo_path: str) -> dict:
    """Generate comprehensive project summary by analyzing repository structure"""
    
    try:
        print(f"DEBUG: Starting summary generation for: {repo_path}")
        
        # Initialize summary data
        summary_data = {
            'project_summary': '',
            'architecture': '',
            'languages_frameworks': '',
            'project_structure': '',
            'authentication_authorization': ''
        }
        
        # Analyze project files and structure
        project_files = []
        language_stats = {}
        framework_indicators = {
            'React': ['package.json', 'src/App.js', 'src/App.tsx', 'public/index.html'],
            'Angular': ['angular.json', 'src/app', 'package.json'],
            'Vue': ['vue.config.js', 'src/main.js', 'src/App.vue'],
            'Django': ['manage.py', 'settings.py', 'models.py', 'views.py'],
            'Flask': ['app.py', 'flask', '__init__.py'],
            'Spring Boot': ['pom.xml', 'Application.java', 'src/main/java'],
            'Express.js': ['package.json', 'server.js', 'app.js'],
            'Next.js': ['next.config.js', 'pages/', '_app.js'],
            'FastAPI': ['main.py', 'uvicorn', 'pydantic'],
            'Laravel': ['composer.json', 'artisan', 'app/Http'],
            'Ruby on Rails': ['Gemfile', 'config/routes.rb', 'app/controllers'],
            'ASP.NET': ['.csproj', 'Program.cs', 'Controllers/'],
            '.NET Core': ['.csproj', 'appsettings.json', 'Startup.cs'],
            'Streamlit': ['streamlit', 'app.py', 'main.py'],
            'Python': ['main.py', 'app.py', '__init__.py'],
            'AI/ML': ['requirements.txt', 'setup.py', 'analyzers/']
        }
        
        detected_frameworks = []
        auth_indicators = []
        
        # Walk through repository - fixed to handle file paths properly
        print(f"DEBUG: Walking through directory: {os.path.abspath(repo_path)}")
        file_count = 0
        for root, dirs, files in os.walk(repo_path):
            # Skip hidden directories and common build/cache directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'build', 'dist', 'venv', 'env']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, repo_path)
                project_files.append(relative_path)
                file_count += 1
                
                # Count file extensions for language detection
                _, ext = os.path.splitext(file)
                if ext:
                    language_stats[ext] = language_stats.get(ext, 0) + 1
                
                # Check for framework indicators
                for framework, indicators in framework_indicators.items():
                    for indicator in indicators:
                        if (indicator in relative_path.lower() or 
                            file.lower() == indicator.lower() or
                            file.lower() in indicator.lower()):
                            if framework not in detected_frameworks:
                                detected_frameworks.append(framework)
                
                # Check for authentication/authorization indicators
                file_lower = file.lower()
                path_lower = relative_path.lower()
                if any(keyword in file_lower or keyword in path_lower for keyword in 
                      ['auth', 'login', 'user', 'token', 'jwt', 'oauth', 'security', 'permission', 'role']):
                    auth_indicators.append(relative_path)
        
        print(f"DEBUG: Found {file_count} files, {len(language_stats)} language types")
        print(f"DEBUG: Language stats: {dict(list(language_stats.items())[:5])}")
        print(f"DEBUG: Detected frameworks: {detected_frameworks}")
        
        # Generate project summary with better error handling
        main_languages = sorted(language_stats.items(), key=lambda x: x[1], reverse=True)[:3]
        lang_names = {'.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.java': 'Java', 
                     '.cs': 'C#', '.cpp': 'C++', '.go': 'Go', '.rs': 'Rust', '.php': 'PHP', 
                     '.rb': 'Ruby', '.html': 'HTML', '.css': 'CSS', '.json': 'JSON',
                     '.md': 'Markdown', '.txt': 'Text', '.yml': 'YAML', '.yaml': 'YAML'}
        
        primary_languages = []
        for ext, count in main_languages:
            if ext in lang_names:
                primary_languages.append(lang_names[ext])
            elif ext.startswith('.'):
                primary_languages.append(ext[1:].upper())
        
        print(f"DEBUG: Primary languages: {primary_languages}")
        
        # Generate project summary
        if len(project_files) == 0:
            summary_data['project_summary'] = "No files detected in the repository. Please check if the path is correct and contains files."
        elif detected_frameworks:
            summary_data['project_summary'] = f"""This repository represents a {', '.join(detected_frameworks[:2])} application primarily built with {', '.join(primary_languages[:2]) if primary_languages else 'multiple technologies'}. The project contains {len(project_files)} files across various modules and demonstrates {detected_frameworks[0] if detected_frameworks else 'modern'} development practices. The codebase appears to be structured for {'web development' if any(fw in detected_frameworks for fw in ['React', 'Angular', 'Vue', 'Django', 'Flask']) else 'software development'} with clear separation of concerns and modular architecture."""
        else:
            summary_data['project_summary'] = f"""This repository is a software project primarily written in {', '.join(primary_languages[:2]) if primary_languages else 'multiple programming languages'}. The project contains {len(project_files)} files organized in a structured manner following standard development practices. The codebase demonstrates good organization with clear file hierarchy and separation of different components and functionalities."""
        
        # Get directory structure
        dir_structure = []
        try:
            for root, dirs, files in os.walk(repo_path):
                if root == repo_path:
                    dir_structure = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
                    break
        except Exception as e:
            print(f"DEBUG: Error getting directory structure: {e}")
            dir_structure = ['src', 'analyzers', 'utils', 'repo_analyzer']  # Default fallback
        
        print(f"DEBUG: Directory structure: {dir_structure}")
        
        # Generate architecture
        architecture_patterns = []
        if any('mvc' in f.lower() or 'model' in f.lower() or 'view' in f.lower() or 'controller' in f.lower() for f in project_files):
            architecture_patterns.append("MVC (Model-View-Controller)")
        if any('component' in f.lower() for f in project_files):
            architecture_patterns.append("Component-based architecture")
        if any('service' in f.lower() or 'api' in f.lower() for f in project_files):
            architecture_patterns.append("Service-oriented architecture")
        if any('module' in f.lower() or 'analyzer' in f.lower() for f in project_files):
            architecture_patterns.append("Modular architecture")
        
        summary_data['architecture'] = f"""The project follows a {', '.join(architecture_patterns) if architecture_patterns else 'layered'} architectural pattern. The codebase is organized into {len(dir_structure)} main directories: {', '.join(dir_structure[:5])}{'...' if len(dir_structure) > 5 else ''}. {'This structure indicates a ' + detected_frameworks[0] + ' application' if detected_frameworks else 'The architectural approach'} with clear separation between different layers of the application. The organization suggests a focus on maintainability and scalability, with dedicated areas for different concerns such as business logic, data handling, and user interface components."""
        
        # Generate languages and frameworks
        if main_languages:
            language_list = []
            for ext, count in main_languages[:5]:
                lang_name = lang_names.get(ext, ext[1:].upper() if ext.startswith('.') else ext.upper())
                language_list.append(f"{lang_name}: {count} files")
        else:
            language_list = ["No languages detected"]
        
        summary_data['languages_frameworks'] = f"""**Primary Languages:**
{chr(10).join(f"• {lang}" for lang in language_list)}

**Detected Frameworks and Technologies:**
{chr(10).join(f"• {framework}" for framework in detected_frameworks) if detected_frameworks else "• Standard development tools and libraries"}

**Key Technologies Identified:**
{chr(10).join(f"• {ext[1:].upper()} ecosystem" for ext, count in main_languages[:3] if count > 5)}"""
        
        # Generate project structure explanation
        summary_data['project_structure'] = f"""The project is organized in a hierarchical structure with {len(dir_structure)} main directories at the root level.

**Key Directory Structure:**
{chr(10).join(f"• **{dir}/** - {get_directory_purpose(dir)}" for dir in dir_structure[:8])}

The structure follows {'framework conventions' if detected_frameworks else 'standard development practices'} with clear separation of source code, configuration files, documentation, and build artifacts. This organization facilitates easy navigation, promotes code maintainability, and supports collaborative development by providing a predictable project layout."""
        
        # Generate authentication/authorization if detected
        if auth_indicators:
            auth_files = [f for f in auth_indicators[:5]]  # Limit to 5 files
            summary_data['authentication_authorization'] = f"""The repository contains authentication and authorization mechanisms as evidenced by {len(auth_indicators)} security-related files.

**Key Security Files Detected:**
{chr(10).join(f"• {file}" for file in auth_files)}

The presence of these files indicates the application implements user management, access control, and security features. This suggests a multi-user system with role-based permissions and secure authentication protocols, likely including features such as user login, session management, and protected resource access."""
        
        print(f"DEBUG: Summary generation completed successfully")
        return summary_data
        
    except Exception as e:
        print(f"DEBUG: Error in summary generation: {e}")
        # Fallback summary if analysis fails
        return {
            'project_summary': f"This repository contains a software project located at {repo_path}. The project structure and contents are being analyzed to provide comprehensive insights.",
            'architecture': "The architectural analysis is in progress. The system appears to follow standard software development patterns with organized code structure.",
            'languages_frameworks': "Language and framework detection is being performed based on file analysis and project structure.",
            'project_structure': "The project follows a structured organization with multiple directories and files arranged for optimal development workflow.",
            'authentication_authorization': ""
        }


def get_directory_purpose(directory_name: str) -> str:
    """Get the likely purpose of a directory based on its name"""
    
    purposes = {
        'src': 'Source code and main application files',
        'app': 'Application core logic and components',
        'lib': 'Library files and shared utilities', 
        'components': 'Reusable UI components and modules',
        'pages': 'Page components and routing logic',
        'utils': 'Utility functions and helper methods',
        'services': 'Business logic and API service layers',
        'api': 'API endpoints and server-side logic',
        'models': 'Data models and database schemas',
        'views': 'View layer and presentation logic',
        'controllers': 'Request handling and business flow control',
        'config': 'Configuration files and settings',
        'public': 'Static assets and public files',
        'assets': 'Images, styles, and static resources',
        'styles': 'CSS and styling files',
        'css': 'Stylesheet files',
        'js': 'JavaScript files and scripts',
        'tests': 'Test files and testing utilities',
        'test': 'Unit and integration tests',
        'docs': 'Documentation and project guides',
        'build': 'Build artifacts and compiled files',
        'dist': 'Distribution and deployment files',
        'node_modules': 'Node.js dependencies',
        'venv': 'Python virtual environment',
        'migrations': 'Database migration files',
        'static': 'Static files for web serving',
        'templates': 'Template files and layouts',
        'middleware': 'Middleware and request processing',
        'helpers': 'Helper functions and utilities',
        'hooks': 'Custom hooks and lifecycle methods',
        'store': 'State management and data store',
        'reducers': 'State reducers and actions',
        'actions': 'Action creators and dispatchers',
        'schemas': 'Data validation and schema definitions',
        'types': 'Type definitions and interfaces',
        'interfaces': 'Interface definitions and contracts',
        'enums': 'Enumeration definitions',
        'constants': 'Application constants and configuration',
        'locales': 'Internationalization and language files',
        'i18n': 'Internationalization resources'
    }
    
    dir_lower = directory_name.lower()
    return purposes.get(dir_lower, 'Project files and resources')


def cleanup_on_exit():
    """Clean up any temporary Git repositories on app exit"""
    try:
        if hasattr(st.session_state, 'prepared_repo_info') and st.session_state.get('prepared_repo_info'):
            if st.session_state.prepared_repo_info.get('temp_dir'):
                temp_dir = st.session_state.prepared_repo_info['temp_dir']
                if git_handler.cleanup_repository(temp_dir):
                    print(f"DEBUG: Cleaned up temporary Git repository on exit: {temp_dir}")
        
        # Also cleanup any other temporary directories tracked by git_handler
        git_handler.cleanup_all()
    except Exception as e:
        print(f"Warning: Error during cleanup on exit: {e}")

if __name__ == "__main__":
    # Register cleanup function
    import atexit
    atexit.register(cleanup_on_exit)
    
    main()
