"""
Dev Assistance Chatbot Analyzer
Provides a simple chatbot interface for repository questions
"""

import streamlit as st
import os
from typing import Dict, Any
from .base_analyzer import BaseAnalyzer
from utils.ai_client import OpenArenaClient

class DevAssistanceChatbotAnalyzer(BaseAnalyzer):
    """Dev Assistance Chatbot for repository questions"""
    
    def __init__(self, repo_path: str):
        super().__init__(repo_path)
        self.ai_client = OpenArenaClient()
        self.repo_info = self._get_repo_info()
    
    def _get_repo_info(self) -> str:
        """Get basic repository information for context"""
        try:
            # Get file structure
            files = []
            for root, dirs, filenames in os.walk(self.repo_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for filename in filenames:
                    if not filename.startswith('.'):
                        rel_path = os.path.relpath(os.path.join(root, filename), self.repo_path)
                        files.append(rel_path)
            
            # Get most modified files (by counting)
            file_extensions = {}
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext:
                    file_extensions[ext] = file_extensions.get(ext, 0) + 1
            
            return f"""Repository Path: {self.repo_path}
Total Files: {len(files)}
Main File Types: {dict(sorted(file_extensions.items(), key=lambda x: x[1], reverse=True)[:5])}
Key Files: {files[:10]}"""
        except Exception as e:
            return f"Repository Path: {self.repo_path}\nError getting repo info: {str(e)}"
    
    def analyze(self, **kwargs) -> Dict[str, Any]:
        """This analyzer doesn't need traditional analysis - it's interactive"""
        return {
            "repo_info": self.repo_info,
            "status": "ready"
        }
    
    def render(self):
        """Render the chatbot interface"""
        st.markdown("### 🛠️ Development Setup Assistant")
        st.markdown("Get help with tool installation, IDE setup, and project requirements for this repository.")
        
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Quick action buttons
        st.markdown("#### 🚀 Quick Help")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔧 What tools do I need?", use_container_width=True):
                self._process_question("What tools and software do I need to install for this project?")
        
        with col2:
            if st.button("💻 Which IDE should I use?", use_container_width=True):
                self._process_question("Which IDE is best for this project and how do I set it up?")
        
        with col3:
            if st.button("📦 How to install dependencies?", use_container_width=True):
                self._process_question("How do I install all the required dependencies and packages?")
        
        st.markdown("---")
        
        # Chat input
        user_question = st.text_input(
            "Ask about installation, setup, or tools:",
            placeholder="e.g., How do I install Python? Which IDE is best? What dependencies do I need?",
            key="dev_chat_input"
        )
        
        # Buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🚀 Ask", type="primary", use_container_width=True):
                if user_question.strip():
                    self._process_question(user_question)
                else:
                    st.warning("Please enter a question!")
        
        with col2:
            if st.button("🗑️ Clear", type="secondary", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("---")
            st.markdown("### 💬 Chat History")
            
            for i, (question, answer) in enumerate(st.session_state.chat_history):
                with st.expander(f"Q{i+1}: {question[:50]}..." if len(question) > 50 else f"Q{i+1}: {question}", expanded=(i == len(st.session_state.chat_history) - 1)):
                    st.markdown(f"**Question:** {question}")
                    st.markdown(f"**Answer:** {answer}")
    
    def _process_question(self, question: str):
        """Process user question and get AI response"""
        try:
            # Check for tool installation questions
            if any(keyword in question.lower() for keyword in ['what tools', 'tools do i need', 'software do i need', 'install', 'setup', 'requirements']):
                response = self._handle_tool_installation_query(question)
            # Check for IDE-specific questions
            elif any(keyword in question.lower() for keyword in ['which ide', 'best ide', 'ide should i use', 'editor', 'development environment']):
                response = self._handle_ide_recommendation_query(question)
            # Check for dependency installation questions
            elif any(keyword in question.lower() for keyword in ['dependencies', 'packages', 'install dependencies', 'requirements.txt', 'package.json']):
                response = self._handle_dependency_installation_query(question)
            # Check if this is a "how to run" question
            elif any(keyword in question.lower() for keyword in ['how to run', 'how do i run', 'start the project', 'run this project', 'execute', 'launch']):
                response = self._handle_run_project_query_with_ai(question)
            # Check if this is a "most committed files" question
            elif any(keyword in question.lower() for keyword in ['most committed', 'most changed', 'frequently modified', 'file changes', 'commit history', 'most modified']):
                response = self._handle_most_committed_files_query(question)
            else:
                # Create context-aware prompt for installation and setup focused questions
                prompt = f"""You are a development setup assistant analyzing a code repository. 

Repository Information:
{self.repo_info}

User Question: {question}

Please provide a helpful, specific answer about this repository. Focus on:
- Tool installation requirements and steps
- IDE recommendations and setup
- Development environment configuration
- Prerequisites and dependencies
- Step-by-step installation guides

Provide detailed installation instructions with specific commands and download links where possible. Keep your response practical and actionable."""

                with st.spinner("🔧 Analyzing setup requirements..."):
                    response = self.ai_client.query(prompt)
            
            if response and response.strip():
                # Add to chat history
                st.session_state.chat_history.append((question, response))
                st.rerun()
            else:
                st.error("Sorry, I couldn't generate a response. Please try again.")
                
        except Exception as e:
            st.error(f"Error processing question: {str(e)}")
    
    def _handle_run_project_query(self, question: str) -> str:
        """Handle 'how to run the project' queries with complete structured response"""
        try:
            # Detect tech stack and find scripts
            tech_stack = self._detect_tech_stack()
            run_instructions = self._find_run_instructions()
            batch_scripts = self._find_batch_scripts()
            
            # Build comprehensive response
            response_parts = []
            
            # Title
            response_parts.append("## 🚀 How to Run This Project")
            response_parts.append("")
            
            # Detected Technology Stack
            if tech_stack:
                response_parts.append(f"**Detected Technology Stack:** {', '.join(tech_stack)}")
            else:
                response_parts.append("**Detected Technology Stack:** Mixed/Unknown")
            response_parts.append("")
            
            # Batch Scripts Section
            if batch_scripts:
                response_parts.append("### 📜 Available Scripts")
                for script_name, script_path in batch_scripts:
                    response_parts.append(f"• **{script_name}** - `{script_path}`")
                response_parts.append("")
                response_parts.append("**Quick Start:** Double-click `start_app.bat` or run it from command line")
                response_parts.append("")
            
            # IDE Recommendations
            response_parts.append("### 💻 Recommended IDEs")
            ide_recommendations = self._get_ide_recommendations(tech_stack)
            for ide_rec in ide_recommendations:
                response_parts.append(ide_rec)
            response_parts.append("")
            
            # Prerequisites
            response_parts.append("### 📋 Prerequisites")
            prereqs = self._get_prerequisites(tech_stack)
            for prereq in prereqs:
                response_parts.append(prereq)
            response_parts.append("")
            
            # Setup Instructions
            response_parts.append("### ⚙️ Setup Instructions")
            setup_instructions = self._get_setup_instructions(tech_stack)
            for instruction in setup_instructions:
                response_parts.append(instruction)
            response_parts.append("")
            
            # Run Commands
            response_parts.append("### 🏃 Run Commands")
            if batch_scripts:
                response_parts.append("**Option 1: Use the provided script (Recommended)**")
                response_parts.append("```batch")
                response_parts.append("start_app.bat")
                response_parts.append("```")
                response_parts.append("")
                response_parts.append("**Option 2: Manual commands**")
            
            run_commands = self._get_run_commands(tech_stack)
            for command in run_commands:
                response_parts.append(command)
            response_parts.append("")
            
            # Found Instructions
            if run_instructions:
                response_parts.append("### 📖 Found Documentation")
                response_parts.append(run_instructions)
                response_parts.append("")
            
            # Notes
            response_parts.append("### 📝 Notes")
            response_parts.append("• This project appears to be a **Streamlit-based AI Repository Analyzer**")
            response_parts.append("• The main entry point is `repo_analyzer/main.py`")
            response_parts.append("• Make sure you have all required Python packages installed")
            response_parts.append("• The application will open in your default web browser")
            
            return '\n'.join(response_parts)
                
        except Exception as e:
            return f"Sorry, I encountered an error while analyzing how to run the project: {str(e)}"
    
    def _find_run_instructions(self) -> str:
        """Search for explicit run instructions in the repository"""
        instructions = []
        
        try:
            # Files to check for run instructions
            instruction_files = [
                'README.md', 'readme.md', 'README.txt',
                'INSTALL.md', 'SETUP.md', 'GETTING_STARTED.md',
                'docs/README.md', 'docs/setup.md', 'docs/installation.md'
            ]
            
            # Batch files and scripts
            script_files = []
            for root, dirs, files in os.walk(self.repo_path):
                for file in files:
                    if file.endswith(('.bat', '.sh', '.cmd', '.ps1')):
                        script_files.append(os.path.join(root, file))
            
            # Check instruction files
            for file_name in instruction_files:
                file_path = os.path.join(self.repo_path, file_name)
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            # Look for run-related sections
                            if any(keyword in content.lower() for keyword in ['how to run', 'running', 'start', 'execute', 'launch', 'usage']):
                                # Extract relevant sections (first 500 chars of run-related content)
                                lines = content.split('\n')
                                run_section = []
                                capture = False
                                for line in lines:
                                    if any(keyword in line.lower() for keyword in ['## run', '# run', 'how to run', 'running', '## usage', '# usage', '## start', '# start']):
                                        capture = True
                                    if capture:
                                        run_section.append(line)
                                        if len('\n'.join(run_section)) > 500:
                                            break
                                    if capture and line.startswith('#') and len(run_section) > 1:
                                        # Stop at next major section
                                        if not any(keyword in line.lower() for keyword in ['run', 'start', 'usage', 'execute']):
                                            break
                                
                                if run_section:
                                    instructions.append(f"**From {file_name}:**\n" + '\n'.join(run_section[:10]))
                    except Exception:
                        continue
            
            # Check script files
            if script_files:
                script_info = []
                for script in script_files[:5]:  # Limit to first 5 scripts
                    rel_path = os.path.relpath(script, self.repo_path)
                    script_info.append(f"• `{rel_path}`")
                
                if script_info:
                    instructions.append(f"**Found executable scripts:**\n" + '\n'.join(script_info))
            
            return '\n\n'.join(instructions) if instructions else ""
            
        except Exception as e:
            return f"Error searching for run instructions: {str(e)}"
    
    def _detect_tech_stack(self) -> list:
        """Detect the technology stack from repository files"""
        tech_stack = []
        
        try:
            # Check for specific files and patterns
            for root, dirs, files in os.walk(self.repo_path):
                for file in files:
                    file_lower = file.lower()
                    
                    # .NET/C#
                    if file.endswith(('.sln', '.csproj', '.vbproj', '.fsproj')):
                        if '.NET/C#' not in tech_stack:
                            tech_stack.append('.NET/C#')
                    
                    # Java
                    elif file.endswith(('.java', '.jar')) or file in ['pom.xml', 'build.gradle']:
                        if 'Java' not in tech_stack:
                            tech_stack.append('Java')
                    
                    # Python
                    elif file.endswith('.py') or file in ['requirements.txt', 'setup.py', 'pyproject.toml']:
                        if 'Python' not in tech_stack:
                            tech_stack.append('Python')
                    
                    # Node.js/JavaScript
                    elif file in ['package.json', 'yarn.lock', 'package-lock.json']:
                        if 'Node.js' not in tech_stack:
                            tech_stack.append('Node.js')
                    
                    # PHP
                    elif file.endswith('.php') or file == 'composer.json':
                        if 'PHP' not in tech_stack:
                            tech_stack.append('PHP')
                    
                    # Ruby
                    elif file.endswith('.rb') or file == 'Gemfile':
                        if 'Ruby' not in tech_stack:
                            tech_stack.append('Ruby')
                    
                    # Go
                    elif file.endswith('.go') or file == 'go.mod':
                        if 'Go' not in tech_stack:
                            tech_stack.append('Go')
                    
                    # Rust
                    elif file.endswith('.rs') or file == 'Cargo.toml':
                        if 'Rust' not in tech_stack:
                            tech_stack.append('Rust')
            
            return tech_stack
            
        except Exception:
            return []
    
    def _find_batch_scripts(self) -> list:
        """Find batch scripts and executable files in the repository"""
        scripts = []
        
        try:
            for root, dirs, files in os.walk(self.repo_path):
                for file in files:
                    if file.endswith(('.bat', '.sh', '.cmd', '.ps1')):
                        rel_path = os.path.relpath(os.path.join(root, file), self.repo_path)
                        script_name = os.path.splitext(file)[0].replace('_', ' ').title()
                        scripts.append((script_name, rel_path))
            
            return scripts
            
        except Exception:
            return []
    
    def _get_ide_recommendations(self, tech_stack: list) -> list:
        """Get IDE recommendations based on detected tech stack"""
        recommendations = []
        
        if 'Python' in tech_stack:
            recommendations.append("**For Python Development:**")
            recommendations.append("• **VS Code** with Python extension (Recommended)")
            recommendations.append("• **PyCharm** (Professional IDE)")
            recommendations.append("• **Jupyter Notebook** (for data analysis)")
        
        if '.NET/C#' in tech_stack:
            recommendations.append("**For .NET/C# Development:**")
            recommendations.append("• **Visual Studio** (Windows - Full IDE)")
            recommendations.append("• **VS Code** with C# Dev Kit (Cross-platform)")
            recommendations.append("• **JetBrains Rider** (Cross-platform)")
        
        if 'Java' in tech_stack:
            recommendations.append("**For Java Development:**")
            recommendations.append("• **IntelliJ IDEA** (Recommended)")
            recommendations.append("• **Eclipse IDE**")
            recommendations.append("• **VS Code** with Java extensions")
        
        if 'Node.js' in tech_stack:
            recommendations.append("**For Node.js/JavaScript Development:**")
            recommendations.append("• **VS Code** (Recommended)")
            recommendations.append("• **WebStorm** (JetBrains)")
            recommendations.append("• **Sublime Text** with packages")
        
        if 'Ruby' in tech_stack:
            recommendations.append("**For Ruby Development:**")
            recommendations.append("• **RubyMine** (JetBrains)")
            recommendations.append("• **VS Code** with Ruby extensions")
            recommendations.append("• **Atom** with Ruby packages")
        
        if not recommendations:
            recommendations.append("**General Purpose IDEs:**")
            recommendations.append("• **VS Code** (Lightweight, extensible)")
            recommendations.append("• **Sublime Text** (Fast, customizable)")
            recommendations.append("• **Atom** (Hackable text editor)")
        
        return recommendations
    
    def _get_prerequisites(self, tech_stack: list) -> list:
        """Get prerequisites based on detected tech stack"""
        prereqs = []
        
        if 'Python' in tech_stack:
            prereqs.append("**Python Requirements:**")
            prereqs.append("• Python 3.8+ installed")
            prereqs.append("• pip package manager")
            prereqs.append("• Virtual environment (recommended)")
        
        if '.NET/C#' in tech_stack:
            prereqs.append("**-.NET Requirements:**")
            prereqs.append("• .NET SDK 6.0 or later")
            prereqs.append("• Visual Studio or VS Code")
        
        if 'Java' in tech_stack:
            prereqs.append("**Java Requirements:**")
            prereqs.append("• JDK 11 or later")
            prereqs.append("• Maven or Gradle (if applicable)")
        
        if 'Node.js' in tech_stack:
            prereqs.append("**Node.js Requirements:**")
            prereqs.append("• Node.js LTS version")
            prereqs.append("• npm or yarn package manager")
        
        if 'Ruby' in tech_stack:
            prereqs.append("**Ruby Requirements:**")
            prereqs.append("• Ruby 2.7+ installed")
            prereqs.append("• Bundler gem manager")
        
        if not prereqs:
            prereqs.append("**General Requirements:**")
            prereqs.append("• Git (for version control)")
            prereqs.append("• Text editor or IDE")
            prereqs.append("• Command line access")
        
        return prereqs
    
    def _get_setup_instructions(self, tech_stack: list) -> list:
        """Get setup instructions based on detected tech stack"""
        instructions = []
        
        if 'Python' in tech_stack:
            instructions.append("**Python Setup:**")
            instructions.append("1. Clone the repository")
            instructions.append("2. Create virtual environment: `python -m venv venv`")
            instructions.append("3. Activate virtual environment:")
            instructions.append("   - Windows: `venv\\Scripts\\activate`")
            instructions.append("   - macOS/Linux: `source venv/bin/activate`")
            instructions.append("4. Install dependencies: `pip install -r requirements.txt`")
        
        if '.NET/C#' in tech_stack:
            instructions.append("**-.NET Setup:**")
            instructions.append("1. Clone the repository")
            instructions.append("2. Restore packages: `dotnet restore`")
            instructions.append("3. Build project: `dotnet build`")
        
        if 'Java' in tech_stack:
            instructions.append("**Java Setup:**")
            instructions.append("1. Clone the repository")
            instructions.append("2. Install dependencies:")
            instructions.append("   - Maven: `mvn clean install`")
            instructions.append("   - Gradle: `./gradlew build`")
        
        if 'Node.js' in tech_stack:
            instructions.append("**Node.js Setup:**")
            instructions.append("1. Clone the repository")
            instructions.append("2. Install dependencies: `npm install` or `yarn install`")
        
        if 'Ruby' in tech_stack:
            instructions.append("**Ruby Setup:**")
            instructions.append("1. Clone the repository")
            instructions.append("2. Install gems: `bundle install`")
        
        if not instructions:
            instructions.append("**General Setup:**")
            instructions.append("1. Clone the repository")
            instructions.append("2. Follow any README instructions")
            instructions.append("3. Install required dependencies")
        
        return instructions
    
    def _get_run_commands(self, tech_stack: list) -> list:
        """Get run commands based on detected tech stack"""
        commands = []
        
        if 'Python' in tech_stack:
            commands.append("**Python Commands:**")
            commands.append("```bash")
            commands.append("# For Streamlit apps")
            commands.append("streamlit run repo_analyzer/main.py")
            commands.append("")
            commands.append("# Alternative Python commands")
            commands.append("python repo_analyzer/main.py")
            commands.append("python -m streamlit run repo_analyzer/main.py")
            commands.append("```")
        
        if '.NET/C#' in tech_stack:
            commands.append("**-.NET Commands:**")
            commands.append("```bash")
            commands.append("dotnet run")
            commands.append("dotnet run --project <project-name>")
            commands.append("```")
        
        if 'Java' in tech_stack:
            commands.append("**Java Commands:**")
            commands.append("```bash")
            commands.append("# Maven")
            commands.append("mvn spring-boot:run")
            commands.append("mvn exec:java")
            commands.append("")
            commands.append("# Gradle")
            commands.append("./gradlew run")
            commands.append("./gradlew bootRun")
            commands.append("```")
        
        if 'Node.js' in tech_stack:
            commands.append("**Node.js Commands:**")
            commands.append("```bash")
            commands.append("npm start")
            commands.append("npm run dev")
            commands.append("yarn start")
            commands.append("```")
        
        if 'Ruby' in tech_stack:
            commands.append("**Ruby Commands:**")
            commands.append("```bash")
            commands.append("bundle exec rails server")
            commands.append("ruby app.rb")
            commands.append("```")
        
        if not commands:
            commands.append("**General Commands:**")
            commands.append("```bash")
            commands.append("# Check for main files and run accordingly")
            commands.append("python main.py")
            commands.append("node index.js")
            commands.append("```")
        
        return commands
    
    def _generate_fallback_run_suggestions(self, tech_stack: list) -> str:
        """Generate fallback run suggestions based on detected tech stack"""
        suggestions = []
        
        for tech in tech_stack:
            if tech == '.NET/C#':
                suggestions.append("""**For .NET/C# Projects:**
• Open the `.sln` file in Visual Studio and press F5 to run
• Or use command line: `dotnet run` (in project directory)
• For web projects: `dotnet run --urls="https://localhost:5001"`""")
            
            elif tech == 'Java':
                suggestions.append("""**For Java Projects:**
• Maven: `mvn spring-boot:run` or `mvn exec:java`
• Gradle: `gradle run` or `./gradlew run`
• Direct: `java -jar target/your-app.jar` (after building)
• IDE: Open in IntelliJ/Eclipse and run main class""")
            
            elif tech == 'Python':
                suggestions.append("""**For Python Projects:**
• General: `python main.py` or `python app.py`
• Streamlit: `streamlit run app.py` or `streamlit run main.py`
• Flask: `python app.py` or `flask run`
• Django: `python manage.py runserver`
• FastAPI: `uvicorn main:app --reload`""")
            
            elif tech == 'Node.js':
                suggestions.append("""**For Node.js Projects:**
• `npm start` (if start script is defined)
• `npm run dev` (for development)
• `node app.js` or `node server.js` or `node index.js`
• `yarn start` (if using Yarn)""")
            
            elif tech == 'PHP':
                suggestions.append("""**For PHP Projects:**
• `php -S localhost:8000` (built-in server)
• Set up Apache/Nginx virtual host
• `composer install` then access via web server""")
            
            elif tech == 'Ruby':
                suggestions.append("""**For Ruby Projects:**
• Rails: `rails server` or `bundle exec rails server`
• Sinatra: `ruby app.rb`
• General: `bundle install` then `ruby main.rb`""")
            
            elif tech == 'Go':
                suggestions.append("""**For Go Projects:**
• `go run main.go`
• `go build` then run the executable
• `go run .` (if main.go is in current directory)""")
            
            elif tech == 'Rust':
                suggestions.append("""**For Rust Projects:**
• `cargo run`
• `cargo build --release` then run the executable
• `cargo run --bin <binary_name>` for specific binaries""")
        
        if not suggestions:
            suggestions.append("""**General Suggestions:**
• Look for main entry files: `main.*`, `app.*`, `index.*`, `server.*`
• Check for configuration files that might indicate the framework
• Look for build scripts or package managers
• Try common commands like `npm start`, `python main.py`, `dotnet run`""")
        
        return '\n\n'.join(suggestions)
    
    def _handle_run_project_query_with_ai(self, question: str) -> str:
        """Handle 'how to run the project' queries using AI assistant"""
        try:
            # Create AI prompt for how to run the project
            ai_prompt = f"""You are an expert developer assistant. Analyze this repository and provide detailed instructions on how to run the project.

Repository Information:
{self.repo_info}

User Question: {question}

Please provide a comprehensive response that includes:
1. **Detected Technology Stack** - What technologies/frameworks are used
2. **Prerequisites** - What needs to be installed
3. **IDE Recommendations** - Best IDEs for this project
4. **Setup Instructions** - Step-by-step setup process
5. **Run Commands** - Exact commands to run the project
6. **Available Scripts** - Any batch files or scripts found
7. **Notes** - Important additional information

Format your response with clear sections and code blocks where appropriate. Be specific and actionable."""

            with st.spinner("🤖 Consulting AI assistant for run instructions..."):
                response = self.ai_client.query(ai_prompt)
            
            return response if response and response.strip() else "Sorry, I couldn't generate AI-powered run instructions. Please try asking more specifically about your setup."
                
        except Exception as e:
            return f"Sorry, I encountered an error while getting AI assistance: {str(e)}"
    
    def _handle_most_committed_files_query(self, question: str) -> str:
        """Handle queries about most committed/modified files"""
        try:
            # Get most committed files using git log
            most_committed_files = self._get_most_committed_files()
            
            if not most_committed_files:
                return "Sorry, I couldn't retrieve commit information. This might not be a git repository or git is not available."
            
            # Build response
            response_parts = []
            response_parts.append("## 📊 Most Committed Files Analysis")
            response_parts.append("")
            response_parts.append("Here are the top 10 most frequently modified files in this repository:")
            response_parts.append("")
            
            for i, (file_path, commit_count) in enumerate(most_committed_files[:10], 1):
                response_parts.append(f"### {i}. `{file_path}` ({commit_count} commits)")
                
                # Get file summary using AI
                file_summary = self._get_file_summary(file_path)
                response_parts.append(f"**What this file does:** {file_summary}")
                response_parts.append("")
            
            response_parts.append("### 📝 Summary")
            response_parts.append("These files are the most actively developed parts of the codebase. They likely contain:")
            response_parts.append("• Core business logic")
            response_parts.append("• Frequently updated features")
            response_parts.append("• Bug fixes and improvements")
            response_parts.append("• Configuration changes")
            
            return '\n'.join(response_parts)
                
        except Exception as e:
            return f"Sorry, I encountered an error while analyzing commit history: {str(e)}"
    
    def _get_most_committed_files(self) -> list:
        """Get the most committed files using git log"""
        try:
            import subprocess
            
            # Run git log to get file change statistics
            cmd = ['git', 'log', '--name-only', '--pretty=format:', '--since=1 year ago']
            result = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                return []
            
            # Count file occurrences
            file_counts = {}
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line and not line.startswith('.'):  # Skip empty lines and hidden files
                    file_counts[line] = file_counts.get(line, 0) + 1
            
            # Sort by count and return top files
            sorted_files = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)
            return sorted_files
            
        except Exception:
            # Fallback: analyze file modification times
            return self._get_recently_modified_files()
    
    def _get_recently_modified_files(self) -> list:
        """Fallback method to get recently modified files"""
        try:
            import os
            import time
            
            file_times = []
            for root, dirs, files in os.walk(self.repo_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for file in files:
                    if not file.startswith('.'):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.repo_path)
                        try:
                            mtime = os.path.getmtime(file_path)
                            file_times.append((rel_path, mtime))
                        except:
                            continue
            
            # Sort by modification time and convert to count format
            sorted_files = sorted(file_times, key=lambda x: x[1], reverse=True)
            return [(file_path, int(time.time() - mtime)) for file_path, mtime in sorted_files]
            
        except Exception:
            return []
    
    def _get_file_summary(self, file_path: str) -> str:
        """Get AI-generated summary of what a file does"""
        try:
            full_path = os.path.join(self.repo_path, file_path)
            
            if not os.path.exists(full_path):
                return "File not found or inaccessible."
            
            # Read file content (first 1000 characters for analysis)
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(1000)
            except:
                return "Unable to read file content."
            
            # Create AI prompt for file summary
            ai_prompt = f"""Analyze this code file and provide a brief, plain text summary of what it does.

File: {file_path}
Content (first 1000 characters):
{content}

Provide a concise 1-2 sentence summary in plain text explaining the purpose and functionality of this file. Focus on what the file does, not how it's implemented."""

            summary = self.ai_client.query(ai_prompt)
            
            if summary and summary.strip():
                # Clean up the summary (remove quotes, extra formatting)
                summary = summary.strip().strip('"').strip("'")
                return summary
            else:
                return "Unable to generate summary for this file."
                
        except Exception as e:
            return f"Error analyzing file: {str(e)}"
    
    def _handle_tool_installation_query(self, question: str) -> str:
        """Handle tool installation queries with detailed installation guides"""
        try:
            tech_stack = self._detect_tech_stack()
            
            response_parts = []
            response_parts.append("## 🔧 Tool Installation Guide")
            response_parts.append("")
            
            if 'Python' in tech_stack:
                response_parts.append("### 🐍 Python Installation")
                response_parts.append("**Download & Install Python:**")
                response_parts.append("1. Visit https://python.org/downloads/")
                response_parts.append("2. Download Python 3.8+ (Latest recommended)")
                response_parts.append("3. Run installer and **check 'Add Python to PATH'**")
                response_parts.append("4. Verify: `python --version` in command prompt")
                response_parts.append("")
                response_parts.append("**Install pip (if not included):**")
                response_parts.append("```bash")
                response_parts.append("python -m ensurepip --upgrade")
                response_parts.append("```")
                response_parts.append("")
                
            if '.NET/C#' in tech_stack:
                response_parts.append("### 🔷 .NET SDK Installation")
                response_parts.append("**Download & Install .NET SDK:**")
                response_parts.append("1. Visit https://dotnet.microsoft.com/download")
                response_parts.append("2. Download .NET 6.0+ SDK")
                response_parts.append("3. Run installer")
                response_parts.append("4. Verify: `dotnet --version`")
                response_parts.append("")
                
            if 'Node.js' in tech_stack:
                response_parts.append("### 🟢 Node.js Installation")
                response_parts.append("**Download & Install Node.js:**")
                response_parts.append("1. Visit https://nodejs.org/")
                response_parts.append("2. Download LTS version")
                response_parts.append("3. Run installer")
                response_parts.append("4. Verify: `node --version` and `npm --version`")
                response_parts.append("")
                
            if 'Java' in tech_stack:
                response_parts.append("### ☕ Java JDK Installation")
                response_parts.append("**Download & Install JDK:**")
                response_parts.append("1. Visit https://adoptium.net/ (recommended)")
                response_parts.append("2. Download JDK 11+ (LTS version)")
                response_parts.append("3. Run installer")
                response_parts.append("4. Set JAVA_HOME environment variable")
                response_parts.append("5. Verify: `java --version`")
                response_parts.append("")
            
            # Git installation
            response_parts.append("### 📚 Git Installation")
            response_parts.append("**Download & Install Git:**")
            response_parts.append("1. Visit https://git-scm.com/downloads")
            response_parts.append("2. Download for your OS")
            response_parts.append("3. Run installer (use default settings)")
            response_parts.append("4. Verify: `git --version`")
            response_parts.append("")
            
            # Additional tools
            response_parts.append("### 🛠️ Additional Recommended Tools")
            response_parts.append("**Package Managers:**")
            if 'Python' in tech_stack:
                response_parts.append("• **pip** (included with Python)")
                response_parts.append("• **pipenv** or **poetry** for dependency management")
            if 'Node.js' in tech_stack:
                response_parts.append("• **npm** (included with Node.js)")
                response_parts.append("• **yarn** (alternative package manager)")
            response_parts.append("")
            
            response_parts.append("**Command Line Tools:**")
            response_parts.append("• **Windows Terminal** (Windows users)")
            response_parts.append("• **PowerShell** (cross-platform)")
            response_parts.append("• **WSL2** (Windows Subsystem for Linux)")
            
            return '\n'.join(response_parts)
            
        except Exception as e:
            return f"Sorry, I encountered an error while generating tool installation guide: {str(e)}"
    
    def _handle_ide_recommendation_query(self, question: str) -> str:
        """Handle IDE recommendation queries with specific setup instructions"""
        try:
            tech_stack = self._detect_tech_stack()
            
            response_parts = []
            response_parts.append("## 💻 IDE Recommendations & Setup")
            response_parts.append("")
            
            if 'Python' in tech_stack:
                response_parts.append("### 🐍 For Python Development")
                response_parts.append("")
                response_parts.append("#### 🥇 **VS Code (Highly Recommended)**")
                response_parts.append("**Download:** https://code.visualstudio.com/")
                response_parts.append("**Required Extensions:**")
                response_parts.append("• Python (by Microsoft)")
                response_parts.append("• Pylance (Python language server)")
                response_parts.append("• Python Debugger")
                response_parts.append("")
                response_parts.append("**Setup Steps:**")
                response_parts.append("1. Install VS Code")
                response_parts.append("2. Open Extensions (Ctrl+Shift+X)")
                response_parts.append("3. Search and install 'Python' extension")
                response_parts.append("4. Open your project folder")
                response_parts.append("5. Select Python interpreter (Ctrl+Shift+P → 'Python: Select Interpreter')")
                response_parts.append("")
                
                response_parts.append("#### 🥈 **PyCharm (Professional IDE)**")
                response_parts.append("**Download:** https://jetbrains.com/pycharm/")
                response_parts.append("• **Community Edition** (Free)")
                response_parts.append("• **Professional Edition** (Paid, more features)")
                response_parts.append("")
                
            if '.NET/C#' in tech_stack:
                response_parts.append("### 🔷 For .NET/C# Development")
                response_parts.append("")
                response_parts.append("#### 🥇 **Visual Studio (Windows)**")
                response_parts.append("**Download:** https://visualstudio.microsoft.com/")
                response_parts.append("• **Community Edition** (Free)")
                response_parts.append("• **Professional/Enterprise** (Paid)")
                response_parts.append("")
                response_parts.append("#### 🥈 **VS Code (Cross-platform)**")
                response_parts.append("**Required Extensions:**")
                response_parts.append("• C# Dev Kit (by Microsoft)")
                response_parts.append("• .NET Install Tool")
                response_parts.append("")
                
            if 'Java' in tech_stack:
                response_parts.append("### ☕ For Java Development")
                response_parts.append("")
                response_parts.append("#### 🥇 **IntelliJ IDEA**")
                response_parts.append("**Download:** https://jetbrains.com/idea/")
                response_parts.append("• **Community Edition** (Free)")
                response_parts.append("• **Ultimate Edition** (Paid)")
                response_parts.append("")
                response_parts.append("#### 🥈 **Eclipse IDE**")
                response_parts.append("**Download:** https://eclipse.org/downloads/")
                response_parts.append("• Free and open-source")
                response_parts.append("")
                
            if 'Node.js' in tech_stack:
                response_parts.append("### 🟢 For Node.js/JavaScript Development")
                response_parts.append("")
                response_parts.append("#### 🥇 **VS Code**")
                response_parts.append("**Required Extensions:**")
                response_parts.append("• JavaScript (ES6) code snippets")
                response_parts.append("• Node.js Extension Pack")
                response_parts.append("• ESLint")
                response_parts.append("• Prettier")
                response_parts.append("")
            
            # General recommendations
            response_parts.append("### 🌟 This Project Specifically")
            response_parts.append("Based on the detected technology stack, here's what I recommend:")
            response_parts.append("")
            
            if 'Python' in tech_stack:
                response_parts.append("**🎯 Best Choice: VS Code with Python Extension**")
                response_parts.append("• Perfect for Streamlit applications")
                response_parts.append("• Excellent debugging support")
                response_parts.append("• Integrated terminal")
                response_parts.append("• Git integration")
                response_parts.append("• Free and lightweight")
                response_parts.append("")
                response_parts.append("**Setup for this project:**")
                response_parts.append("1. Install VS Code")
                response_parts.append("2. Install Python extension")
                response_parts.append("3. Open project folder in VS Code")
                response_parts.append("4. Create/activate virtual environment")
                response_parts.append("5. Install requirements: `pip install -r requirements.txt`")
                response_parts.append("6. Run: `streamlit run repo_analyzer/main.py`")
            
            return '\n'.join(response_parts)
            
        except Exception as e:
            return f"Sorry, I encountered an error while generating IDE recommendations: {str(e)}"
    
    def _handle_dependency_installation_query(self, question: str) -> str:
        """Handle dependency installation queries"""
        try:
            tech_stack = self._detect_tech_stack()
            
            response_parts = []
            response_parts.append("## 📦 Dependency Installation Guide")
            response_parts.append("")
            
            if 'Python' in tech_stack:
                response_parts.append("### 🐍 Python Dependencies")
                response_parts.append("")
                response_parts.append("**Step 1: Create Virtual Environment (Recommended)**")
                response_parts.append("```bash")
                response_parts.append("# Create virtual environment")
                response_parts.append("python -m venv venv")
                response_parts.append("")
                response_parts.append("# Activate virtual environment")
                response_parts.append("# Windows:")
                response_parts.append("venv\\Scripts\\activate")
                response_parts.append("")
                response_parts.append("# macOS/Linux:")
                response_parts.append("source venv/bin/activate")
                response_parts.append("```")
                response_parts.append("")
                response_parts.append("**Step 2: Install Dependencies**")
                response_parts.append("```bash")
                response_parts.append("# Install from requirements.txt")
                response_parts.append("pip install -r requirements.txt")
                response_parts.append("")
                response_parts.append("# Or install individual packages")
                response_parts.append("pip install streamlit pandas numpy")
                response_parts.append("```")
                response_parts.append("")
                response_parts.append("**Step 3: Verify Installation**")
                response_parts.append("```bash")
                response_parts.append("pip list")
                response_parts.append("```")
                response_parts.append("")
                
            if '.NET/C#' in tech_stack:
                response_parts.append("### 🔷 .NET Dependencies")
                response_parts.append("```bash")
                response_parts.append("# Restore NuGet packages")
                response_parts.append("dotnet restore")
                response_parts.append("")
                response_parts.append("# Build project")
                response_parts.append("dotnet build")
                response_parts.append("```")
                response_parts.append("")
                
            if 'Node.js' in tech_stack:
                response_parts.append("### 🟢 Node.js Dependencies")
                response_parts.append("```bash")
                response_parts.append("# Install dependencies")
                response_parts.append("npm install")
                response_parts.append("")
                response_parts.append("# Or using Yarn")
                response_parts.append("yarn install")
                response_parts.append("```")
                response_parts.append("")
                
            if 'Java' in tech_stack:
                response_parts.append("### ☕ Java Dependencies")
                response_parts.append("**Maven:**")
                response_parts.append("```bash")
                response_parts.append("mvn clean install")
                response_parts.append("```")
                response_parts.append("")
                response_parts.append("**Gradle:**")
                response_parts.append("```bash")
                response_parts.append("./gradlew build")
                response_parts.append("```")
                response_parts.append("")
            
            # Troubleshooting section
            response_parts.append("### 🔧 Troubleshooting")
            response_parts.append("**Common Issues:**")
            response_parts.append("")
            
            if 'Python' in tech_stack:
                response_parts.append("**Python Issues:**")
                response_parts.append("• **Permission denied:** Run as administrator or use `--user` flag")
                response_parts.append("• **Package not found:** Update pip: `python -m pip install --upgrade pip`")
                response_parts.append("• **Virtual environment issues:** Deactivate and recreate: `deactivate` then create new venv")
                response_parts.append("")
                
            response_parts.append("**General Issues:**")
            response_parts.append("• **Network issues:** Check firewall/proxy settings")
            response_parts.append("• **Version conflicts:** Use virtual environments")
            response_parts.append("• **Path issues:** Ensure tools are in system PATH")
            
            return '\n'.join(response_parts)
            
        except Exception as e:
            return f"Sorry, I encountered an error while generating dependency installation guide: {str(e)}"
