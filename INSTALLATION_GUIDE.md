# EduScan Somalia - Installation Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
streamlit run app.py --server.port 5000
```

### 3. Access the Application
Open your browser and go to: `http://localhost:5000`

## Project Structure
```
eduscan_complete_package/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── pages/                      # Streamlit pages
│   ├── 01_Prediction.py       # Risk assessment page
│   ├── 02_Teacher_Resources.py # Educational resources
│   ├── 03_Parent_Tracker.py   # Parent observation tracker
│   └── 04_Educational_Content.py # Educational content
├── utils/                      # Utility modules
│   ├── model_utils.py         # ML model functions
│   └── data_utils.py          # Data management
├── database/                   # Database components
│   ├── models.py              # Database models
│   └── database_utils.py      # Database utilities
├── data/                       # Data files
│   └── learning_difficulty_detector.pkl # Your trained ML model
└── .streamlit/                 # Streamlit configuration
    └── config.toml            # App configuration
```

## Features
- Learning risk assessment using your trained ML model
- Multilingual support (English, Somali, Arabic)
- Parent observation tracking
- Educational resources for teachers
- Professional dashboard interface
- Database integration with PostgreSQL fallback

## System Requirements
- Python 3.11 or higher
- 4GB RAM recommended
- Modern web browser

## Configuration
The application is pre-configured to work with:
- Your trained machine learning model
- Professional Somali-themed styling
- Database connectivity (PostgreSQL with JSON fallback)

## Support
For questions or issues, refer to the application documentation or contact support.