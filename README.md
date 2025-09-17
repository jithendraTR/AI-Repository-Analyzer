# AI-Powered Codebase Analyzer

An AI-powered solution to analyze the codebase and provide one spot detailed analysis on Commits Mapping, Timeline Analysis, API Analysis, AI Integration Analysis and Risk Analysis

## Features

The analyzer provides comprehensive analysis across 9 different tabs:

1. **👥 Commits Mapping** - Commits mapping to developers
2. **📅 Timeline Analysis** - Codebase timelines
3. **🔌 API Analysis** - API endpoints details
4. **🤖 AI Integration Analysis** - AI-powered Integration analysis
5. **⚠️ Risk Analysis** - Test coverage gaps and security vulnerabilities

## Setup

### Prerequisites

- Python 3.8 or higher
- Access to Thomson Reuters Open Arena AI API
- Valid ESSO token

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   
4. Edit `.env` file with your credentials:
   ```
   OPEN_ARENA_THOMSON_REUTERS_URL=https://aiopenarena.gcs.int.thomsonreuters.com/v1/inference
   AI_ARENA_WORKFLOW_ID=eded8958-bd45-4cbf-bf44-5de6c0b00c7c
   ESSO_TOKEN=your_actual_esso_token_here
   ```

### Running the Application

1. Navigate to the project directory
2. Run the Streamlit application:
   ```bash
   streamlit run repo_analyzer/main.py
   ```

3. Open your browser to `http://localhost:8501`

## Usage

1. **Select Repository**: Choose the repository you want to analyze (defaults to current directory)
2. **Choose Analysis Tab**: Select from the 9 available analysis types
3. **Run Analysis**: Each analyzer will scan your codebase and provide insights
4. **AI Insights**: Use the AI-powered recommendations for deeper analysis

## API Configuration

The application uses Thomson Reuters Open Arena AI API with the following pattern:

```python
import requests

url = "https://aiopenarena.gcs.int.thomsonreuters.com/v1/inference"
headers = {
    "Authorization": "Bearer <your_esso_token>",
    "Content-Type": "application/json"
}

payload = {
    "workflow_id": "eded8958-bd45-4cbf-bf44-5de6c0b00c7c",
    "query": "Your analysis query here",
    "is_persistence_allowed": False
}

response = requests.post(url, headers=headers, json=payload)
```

## Analysis Details

### Commits Mapping
- Identifies contributors and their areas of expertise
- Maps code ownership and knowledge distribution
- Highlights key maintainers for different modules

### Timeline Analysis
- Tracks recent changes and development velocity
- Identifies active development areas
- Shows project evolution patterns

### API Analysis
- Discovers REST endpoints and API definitions
- Maps integration points and external dependencies
- Analyzes API versioning and compatibility

### AI Integration Analysis
- Suggests optimal locations for new features
- Identifies architectural patterns and conventions
- Provides context-aware development guidance

### Risk Analysis
- Identifies test coverage gaps
- Highlights potential security vulnerabilities
- Assesses code quality metrics

## Project Structure

```
repo_analyzer/
├── repo_analyzer/
│   └── main.py              # Main Streamlit application
├── utils/
│   └── ai_client.py         # Thomson Reuters AI API client
├── analyzers/
│   ├── base_analyzer.py     # Base analyzer class
│   ├── commits_mapping.py # Commits mapping analyzer
│   ├── timeline_analysis.py # Timeline analysis analyzer
│   ├── api_analysis.py     # API analysis analyzer
│   ├── ai_integration_analysis.py        # AI integration analysis analyzer
│   ├── risk_analysis.py     # Risk analysis analyzer
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md              # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for internal Thomson Reuters use.

## Support

For issues or questions, please contact the development team.
