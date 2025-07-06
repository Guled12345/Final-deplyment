# EduScan Somalia - Learning Risk Assessment Application

A professional desktop-style Streamlit application designed to predict and support learning difficulties for students in Somalia, leveraging advanced machine learning techniques for educational intervention.

## Features

- **Machine Learning Risk Assessment**: Advanced ML-powered learning difficulty prediction
- **Professional Desktop Interface**: Modern, clean UI suitable for educational institutions
- **Offline Mode Capability**: Can function without internet connectivity
- **Real-time Visualizations**: Interactive charts and performance analytics
- **Export Functionality**: Download assessment data for analysis
- **Multi-language Support**: Built for Somali educational context

## Quick Start

1. Install dependencies:
   ```bash
   pip install streamlit pandas numpy scikit-learn plotly psycopg2-binary sqlalchemy
   ```

2. Run the application:
   ```bash
   streamlit run app_desktop.py
   ```

3. Access the application at `http://localhost:8501`

## Deployment

This application is optimized for deployment on Streamlit Community Cloud.

### Streamlit Community Cloud Deployment

1. Fork/clone this repository to your GitHub account
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy using `app_desktop.py` as the main file

## Application Structure

- `app_desktop.py` - Main desktop application with professional UI
- `utils/model_utils.py` - Machine learning model utilities
- `utils/data_utils.py` - Data management and persistence
- `database/` - Database models and utilities
- `data/` - Training data and model files
- `.streamlit/config.toml` - Streamlit configuration

## Requirements

- Python 3.11+
- Streamlit 1.28.0+
- scikit-learn 1.3.0+
- pandas 2.0.0+
- plotly 5.15.0+
- numpy 1.24.0+

## License

Educational use license for Somalia educational institutions.

## Contact

For support and inquiries: support@eduscan-somalia.edu