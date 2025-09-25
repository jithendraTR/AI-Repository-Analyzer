@echo off
echo Starting AI-Powered Repository Analyzer...
echo.
echo Python version:
python --version
echo.
echo Streamlit version:
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
echo.
echo Starting Streamlit application...
python -m streamlit run repo_analyzer/main.py --server.port 8501 --server.address localhost
pause
