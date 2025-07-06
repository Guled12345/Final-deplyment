import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
import json
from utils.data_utils import load_student_data, load_parent_observations, save_prediction_data, save_parent_observation
from utils.model_utils import load_model, make_prediction

def get_text(key, language='English'):
    """Get localized text based on language setting"""
    translations = {
        'English': {
            # Navigation
            'dashboard': 'Dashboard',
            'assessment': 'Assessment',
            'resources': 'Resources', 
            'tracker': 'Tracker',
            'analytics': 'Analytics',
            
            # Basic Info
            'student_name': 'Student Name',
            'grade_level': 'Grade Level',
            'child_name': "Child's Name",
            'observation_date': 'Observation Date',
            
            # Academic Scores
            'math_score': 'Mathematics Score (%)',
            'reading_score': 'Reading Score (%)',
            'writing_score': 'Writing Score (%)',
            'attendance': 'Attendance (%)',
            'behavior_rating': 'Behavior Rating',
            'literacy_level': 'Literacy Level',
            
            # Assessment Page
            'learning_risk_assessment': 'Learning Risk Assessment',
            'student_information': 'Student Information',
            'academic_performance': 'Academic Performance',
            'behavioral_assessment': 'Behavioral Assessment',
            'assessment_results': 'Assessment Results',
            'analyze_learning_risk': 'Analyze Learning Risk',
            'performance_profile': 'Performance Profile',
            'recommendations': 'Recommendations',
            
            # Parent Tracker
            'daily_observation_log': 'Daily Observation Log',
            'academic_observations': 'Academic Observations',
            'behavioral_observations': 'Behavioral Observations',
            'homework_completion': 'Homework Completion (%)',
            'reading_time': 'Reading Time (minutes)',
            'focus_level': 'Focus Level',
            'subjects_struggled': 'Subjects Struggled With',
            'mood_rating': 'Mood Rating',
            'sleep_hours': 'Sleep Hours',
            'energy_level': 'Energy Level',
            'learning_wins': 'Learning Wins Today',
            'challenges_faced': 'Challenges Faced',
            'save_observation': 'Save Observation',
            'progress_insights': 'Progress Insights',
            
            # Dashboard
            'system_overview': 'System Overview',
            'total_students': 'Total Students',
            'on_track': 'On Track',
            'at_risk': 'At Risk',
            'intervention': 'Intervention',
            'class_performance': 'Class Performance Overview',
            'recent_assessments': 'Recent Assessments',
            'students_needing_attention': 'Students Needing Attention',
            'quick_actions': 'Quick Actions',
            'system_status': 'System Status',
            
            # Actions/Buttons
            'save_assessment': 'Save Assessment',
            'export_data': 'Export Data',
            'offline_mode': 'Toggle Offline Mode',
            'settings': 'Settings',
            'help': 'Help & Support',
            'reset': 'Reset Application',
            'save_settings': 'Save Settings',
            'close_settings': 'Close Settings',
            
            # Risk Levels
            'low_risk': 'Low Risk',
            'medium_risk': 'Medium Risk',
            'high_risk': 'High Risk',
            
            # Levels/Options
            'low': 'Low',
            'medium': 'Medium',
            'high': 'High',
            'excellent': 'Excellent',
            'good': 'Good',
            'average': 'Average',
            'below_average': 'Below Average',
            'poor': 'Poor'
        },
        'Somali': {
            # Navigation
            'dashboard': 'Xarunta Xogta',
            'assessment': 'Qiimayn',
            'resources': 'Agabka',
            'tracker': 'Dabagal',
            'analytics': 'Falanqayn',
            
            # Basic Info
            'student_name': 'Magaca Ardayga',
            'grade_level': 'Heerka Fasalka',
            'child_name': 'Magaca Ilmaha',
            'observation_date': 'Taariikhda Daawashada',
            
            # Academic Scores
            'math_score': 'Buunka Xisaabta (%)',
            'reading_score': 'Buunka Akhriska (%)',
            'writing_score': 'Buunka Qorista (%)',
            'attendance': 'Soo Galitaanka (%)',
            'behavior_rating': 'Qiimaynta Dhaqanka',
            'literacy_level': 'Heerka Aqrinta',
            
            # Assessment Page
            'learning_risk_assessment': 'Qiimaynta Khatarta Barashada',
            'student_information': 'Macluumaadka Ardayga',
            'academic_performance': 'Waxqabadka Waxbarashada',
            'behavioral_assessment': 'Qiimaynta Dhaqanka',
            'assessment_results': 'Natiijada Qiimaynta',
            'analyze_learning_risk': 'Falanqee Khatarta Barashada',
            'performance_profile': 'Astaanta Waxqabadka',
            'recommendations': 'Talooyinka',
            
            # Parent Tracker
            'daily_observation_log': 'Buugga Daawashada Maalinta',
            'academic_observations': 'Daawasho Waxbarasho',
            'behavioral_observations': 'Daawasho Dhaqan',
            'homework_completion': 'Dhammaynta Shaqada Guriga (%)',
            'reading_time': 'Waqtiga Akhriska (daqiiqado)',
            'focus_level': 'Heerka Diiradda',
            'subjects_struggled': 'Maadooyinka Ku Adkaadey',
            'mood_rating': 'Qiimaynta Dareenka',
            'sleep_hours': 'Saacadaha Hurdada',
            'energy_level': 'Heerka Tamarku',
            'learning_wins': 'Guusha Barashada Maanta',
            'challenges_faced': 'Caqabadaha la Kulmay',
            'save_observation': 'Kaydi Daawashada',
            'progress_insights': 'Aragti Horumar',
            
            # Dashboard
            'system_overview': 'Dulmar Nidaamka',
            'total_students': 'Wadarta Ardayda',
            'on_track': 'Jidka Saxda ah',
            'at_risk': 'Khatar ku jira',
            'intervention': 'Faragelin',
            'class_performance': 'Waxqabadka Fasalka Guud',
            'recent_assessments': 'Qiimaynaha Dhawaan',
            'students_needing_attention': 'Ardayda u Baahan Feejignaan',
            'quick_actions': 'Ficillo Degdeg ah',
            'system_status': 'Xaalada Nidaamka',
            
            # Actions/Buttons
            'save_assessment': 'Kaydi Qiimaynta',
            'export_data': 'Soo Saari Xogta',
            'offline_mode': 'Bedel Qaabka Offline',
            'settings': 'Dejinta',
            'help': 'Caawimaad',
            'reset': 'Cusboonaysii Barnaamijka',
            'save_settings': 'Kaydi Dejinta',
            'close_settings': 'Xir Dejinta',
            
            # Risk Levels
            'low_risk': 'Khatar Yar',
            'medium_risk': 'Khatar Dhexdhexaad ah',
            'high_risk': 'Khatar Weyn',
            
            # Levels/Options
            'low': 'Hoose',
            'medium': 'Dhexdhexaad',
            'high': 'Sare',
            'excellent': 'Aad u Fiican',
            'good': 'Fiican',
            'average': 'Caadi',
            'below_average': 'Ka hooseeya Celceliska',
            'poor': 'Liita'
        },
        'Arabic': {
            # Navigation
            'dashboard': 'لوحة القيادة',
            'assessment': 'التقييم',
            'resources': 'الموارد',
            'tracker': 'المتتبع',
            'analytics': 'التحليلات',
            
            # Basic Info
            'student_name': 'اسم الطالب',
            'grade_level': 'مستوى الصف',
            'child_name': 'اسم الطفل',
            'observation_date': 'تاريخ الملاحظة',
            
            # Academic Scores
            'math_score': 'نتيجة الرياضيات (%)',
            'reading_score': 'نتيجة القراءة (%)',
            'writing_score': 'نتيجة الكتابة (%)',
            'attendance': 'الحضور (%)',
            'behavior_rating': 'تقييم السلوك',
            'literacy_level': 'مستوى القراءة والكتابة',
            
            # Assessment Page
            'learning_risk_assessment': 'تقييم مخاطر التعلم',
            'student_information': 'معلومات الطالب',
            'academic_performance': 'الأداء الأكاديمي',
            'behavioral_assessment': 'التقييم السلوكي',
            'assessment_results': 'نتائج التقييم',
            'analyze_learning_risk': 'تحليل مخاطر التعلم',
            'performance_profile': 'ملف الأداء',
            'recommendations': 'التوصيات',
            
            # Parent Tracker
            'daily_observation_log': 'سجل الملاحظات اليومية',
            'academic_observations': 'الملاحظات الأكاديمية',
            'behavioral_observations': 'الملاحظات السلوكية',
            'homework_completion': 'إكمال الواجبات المنزلية (%)',
            'reading_time': 'وقت القراءة (دقائق)',
            'focus_level': 'مستوى التركيز',
            'subjects_struggled': 'المواد التي واجه صعوبة فيها',
            'mood_rating': 'تقييم المزاج',
            'sleep_hours': 'ساعات النوم',
            'energy_level': 'مستوى الطاقة',
            'learning_wins': 'إنجازات التعلم اليوم',
            'challenges_faced': 'التحديات التي واجهها',
            'save_observation': 'حفظ الملاحظة',
            'progress_insights': 'رؤى التقدم',
            
            # Dashboard
            'system_overview': 'نظرة عامة على النظام',
            'total_students': 'إجمالي الطلاب',
            'on_track': 'على المسار الصحيح',
            'at_risk': 'في خطر',
            'intervention': 'التدخل',
            'class_performance': 'أداء الفصل العام',
            'recent_assessments': 'التقييمات الحديثة',
            'students_needing_attention': 'الطلاب الذين يحتاجون انتباه',
            'quick_actions': 'الإجراءات السريعة',
            'system_status': 'حالة النظام',
            
            # Actions/Buttons
            'save_assessment': 'حفظ التقييم',
            'export_data': 'تصدير البيانات',
            'offline_mode': 'تبديل الوضع دون اتصال',
            'settings': 'الإعدادات',
            'help': 'المساعدة والدعم',
            'reset': 'إعادة تعيين التطبيق',
            'save_settings': 'حفظ الإعدادات',
            'close_settings': 'إغلاق الإعدادات',
            
            # Risk Levels
            'low_risk': 'خطر منخفض',
            'medium_risk': 'خطر متوسط',
            'high_risk': 'خطر عالي',
            
            # Levels/Options
            'low': 'منخفض',
            'medium': 'متوسط',
            'high': 'عالي',
            'excellent': 'ممتاز',
            'good': 'جيد',
            'average': 'متوسط',
            'below_average': 'دون المتوسط',
            'poor': 'ضعيف'
        }
    }
    return translations.get(language, translations['English']).get(key, key)

def get_recommendations(risk_level):
    """Get recommendations based on risk level"""
    if risk_level == "Low Risk":
        return ["Maintain current study routine", "Provide enrichment activities", "Monitor progress regularly"]
    elif risk_level == "Medium Risk":
        return ["Provide targeted tutoring", "Increase parent-teacher communication", "Monitor attendance closely"]
    else:
        return ["Implement individualized learning plan", "Consider specialized support services", "Increase monitoring and feedback"]

def load_app_settings():
    """Load application settings from file"""
    try:
        with open('data/app_settings.json', 'r') as f:
            settings = json.load(f)
            return settings
    except:
        return {'language': 'English', 'theme': 'Light', 'autosave_interval': 5}

def apply_theme(theme):
    """Apply the selected theme to the application"""
    if theme == "Dark":
        st.markdown("""
        <style>
        .stApp { 
            background-color: #1e1e1e !important; 
            color: white !important; 
        }
        .desktop-container { 
            background: #2d2d2d !important; 
            border: 1px solid #444 !important;
        }
        .nav-tab {
            background: #333 !important;
            color: white !important;
        }
        .nav-tab.active {
            background: #2563eb !important;
        }
        .metric-card {
            background: #333 !important;
            color: white !important;
        }
        .stSelectbox > div > div {
            background-color: #333 !important;
            color: white !important;
        }
        .stTextInput > div > div > input {
            background-color: #333 !important;
            color: white !important;
        }
        .stNumberInput > div > div > input {
            background-color: #333 !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp { 
            background-color: #ffffff !important; 
            color: #1f2937 !important; 
        }
        .desktop-container { 
            background: #ffffff !important; 
            border: 1px solid #e5e7eb !important;
        }
        .nav-tab {
            background: #f8fafc !important;
            color: #1f2937 !important;
        }
        .nav-tab.active {
            background: #2563eb !important;
            color: white !important;
        }
        .metric-card {
            background: #ffffff !important;
            color: #1f2937 !important;
        }
        </style>
        """, unsafe_allow_html=True)

# Configure Streamlit page
st.set_page_config(
    page_title="EduScan Somalia - Professional Learning Assessment System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Check offline mode
@st.cache_data
def check_offline_mode():
    """Check if application can work offline"""
    try:
        # Try to load model and data
        model = load_model()
        data = load_student_data()
        return False, "Online Mode"
    except:
        return True, "Offline Mode"

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'
if 'offline_mode' not in st.session_state:
    st.session_state.offline_mode, st.session_state.mode_status = check_offline_mode()

# Professional Desktop-Style CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Reset and Base */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        background-attachment: fixed;
    }
    
    /* Hide all Streamlit UI elements */
    .stDeployButton, #MainMenu, .stHeader, .stToolbar, 
    header[data-testid="stHeader"], .stDecoration, .css-1d391kg, 
    .css-1lcbmhc, [data-testid="stSidebar"], .css-1outpf7, .css-17eq0hr {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Desktop Application Container */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        margin: 20px !important;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Application Header */
    .app-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
        pointer-events: none;
    }
    
    .app-title {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #e3f2fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        margin: 0;
    }
    
    .app-subtitle {
        font-size: 14px;
        opacity: 0.9;
        font-weight: 400;
        margin-top: 5px;
    }
    
    .app-status {
        display: flex;
        align-items: center;
        gap: 15px;
        font-size: 12px;
        opacity: 0.9;
    }
    
    .status-indicator {
        width: 8px;
        height: 8px;
        background: #4CAF50;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    .offline-indicator {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 8px 15px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Navigation Tabs */
    .nav-tabs {
        background: #f8fafc;
        border-bottom: 1px solid #e2e8f0;
        padding: 0 40px;
        display: flex;
        gap: 2px;
        overflow-x: auto;
    }
    
    .nav-tab {
        background: transparent;
        border: none;
        padding: 15px 25px;
        cursor: pointer;
        color: #64748b;
        font-weight: 500;
        font-size: 14px;
        border-radius: 8px 8px 0 0;
        transition: all 0.3s ease;
        position: relative;
        white-space: nowrap;
    }
    
    .nav-tab:hover {
        background: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
    }
    
    .nav-tab.active {
        background: white;
        color: #1e40af;
        font-weight: 600;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .nav-tab.active::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    }
    
    /* Content Area */
    .content-area {
        background: white;
        padding: 40px;
        min-height: calc(100vh - 250px);
        overflow-y: auto;
    }
    
    /* Professional Cards */
    .dashboard-card {
        background: white;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.05);
        margin-bottom: 30px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    }
    
    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* Metric Cards Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 25px;
        margin-bottom: 40px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--accent-color, #3b82f6);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: 800;
        color: #1e293b;
        margin: 10px 0 5px 0;
        background: linear-gradient(135deg, #1e293b 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 14px;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Professional Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
    }
    
    /* Bottom Navigation */
    .bottom-nav {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 20px 40px;
        display: flex;
        justify-content: center;
        gap: 30px;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .bottom-nav-btn {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        min-width: 120px !important;
    }
    
    .bottom-nav-btn:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Form Elements */
    .stSelectbox > div > div, .stNumberInput > div > div > input {
        background: white !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .app-header { padding: 15px 20px; }
        .app-title { font-size: 22px; }
        .content-area { padding: 20px; }
        .nav-tabs { padding: 0 20px; }
        .metrics-grid { grid-template-columns: 1fr; gap: 15px; }
        .bottom-nav { padding: 15px 20px; gap: 15px; flex-wrap: wrap; }
    }
</style>
""", unsafe_allow_html=True)

def render_app_header():
    """Render professional desktop application header"""
    mode_status = st.session_state.mode_status
    is_offline = st.session_state.offline_mode
    
    status_class = "offline-indicator" if is_offline else "app-status"
    indicator_color = "#f59e0b" if is_offline else "#4CAF50"
    
    st.markdown(f"""
    <div class="app-header">
        <div>
            <h1 class="app-title">EduScan Somalia</h1>
            <p class="app-subtitle">Professional Learning Assessment System</p>
        </div>
        <div class="{status_class}">
            <div class="status-indicator" style="background: {indicator_color};"></div>
            <span>{mode_status}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_navigation():
    """Render desktop-style navigation tabs"""
    # Get current language setting
    current_language = st.session_state.get('app_language', 'English')
    
    pages = ['Dashboard', 'Assessment', 'Resources', 'Tracker', 'Analytics']
    page_keys = ['dashboard', 'assessment', 'resources', 'tracker', 'analytics']
    
    # Simple tab display without onclick handlers
    nav_html = '<div class="nav-tabs">'
    for i, page in enumerate(pages):
        active_class = 'active' if st.session_state.current_page == page else ''
        localized_name = get_text(page_keys[i], current_language)
        nav_html += f'<div class="nav-tab {active_class}">{localized_name}</div>'
    nav_html += '</div>'
    
    st.markdown(nav_html, unsafe_allow_html=True)
    
    # Handle page navigation with buttons in a clean layout
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button(get_text('dashboard', current_language), key="nav_dashboard", use_container_width=True):
            st.session_state.current_page = 'Dashboard'
            st.rerun()
    with col2:
        if st.button(get_text('assessment', current_language), key="nav_assessment", use_container_width=True):
            st.session_state.current_page = 'Assessment'
            st.rerun()
    with col3:
        if st.button(get_text('resources', current_language), key="nav_resources", use_container_width=True):
            st.session_state.current_page = 'Resources'
            st.rerun()
    with col4:
        if st.button(get_text('tracker', current_language), key="nav_tracker", use_container_width=True):
            st.session_state.current_page = 'Tracker'
            st.rerun()
    with col5:
        if st.button(get_text('analytics', current_language), key="nav_analytics", use_container_width=True):
            st.session_state.current_page = 'Analytics'
            st.rerun()

def create_metric_card(title, value, description, color="#3b82f6"):
    """Create a professional metric card"""
    return f"""
    <div class="metric-card" style="--accent-color: {color};">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{title}</div>
        <div style="font-size: 12px; color: #9ca3af; margin-top: 8px;">{description}</div>
    </div>
    """

def render_dashboard():
    """Render the main dashboard"""
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    
    # Dashboard title
    st.markdown("## System Overview")
    
    # Metrics grid
    try:
        data = load_student_data()
        total_students = len(data) if data else 0
        at_risk = int(total_students * 0.25) if total_students > 0 else 0
        on_track = total_students - at_risk
        interventions = int(at_risk * 0.6) if at_risk > 0 else 0
    except:
        total_students, at_risk, on_track, interventions = 0, 0, 0, 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card("Total Students", total_students, "Currently enrolled", "#3b82f6"), 
                   unsafe_allow_html=True)
    with col2:
        st.markdown(create_metric_card("On Track", on_track, "Performing well", "#16a34a"), 
                   unsafe_allow_html=True)
    with col3:
        st.markdown(create_metric_card("At Risk", at_risk, "Need attention", "#dc2626"), 
                   unsafe_allow_html=True)
    with col4:
        st.markdown(create_metric_card("Interventions", interventions, "Active support", "#d97706"), 
                   unsafe_allow_html=True)
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Performance Overview")
        # Create sample performance chart
        subjects = ['Mathematics', 'Reading', 'Writing', 'Science']
        scores = [75, 82, 68, 79]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=subjects,
            y=scores,
            marker_color=['#3b82f6', '#16a34a', '#dc2626', '#d97706']
        ))
        fig.update_layout(
            height=300,
            showlegend=False,
            margin=dict(l=0, r=0, t=30, b=0),
            yaxis_title="Average Score (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Risk Distribution")
        # Create risk distribution pie chart
        labels = ['Low Risk', 'Medium Risk', 'High Risk']
        values = [60, 25, 15]
        colors = ['#16a34a', '#d97706', '#dc2626']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values,
            marker_colors=colors,
            hole=0.4
        )])
        fig.update_layout(
            height=300,
            showlegend=True,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_assessment():
    """Render the assessment page"""
    # Get current language setting
    current_language = st.session_state.get('app_language', 'English')
    
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    
    st.markdown(f"## {get_text('learning_risk_assessment', current_language)}")
    st.markdown("Evaluate student learning risks using advanced machine learning analysis.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {get_text('student_information', current_language)}")
        
        # Student data input
        student_name = st.text_input(get_text('student_name', current_language), placeholder="Enter student name")
        grade_level = st.selectbox(get_text('grade_level', current_language), ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6"])
        
        st.markdown(f"### {get_text('academic_performance', current_language)}")
        st.caption("Enter scores as percentages (0-100)")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            math_score = st.number_input(get_text('math_score', current_language), min_value=0, max_value=100, value=75, 
                                       help="Student's mathematics performance percentage")
        with col_b:
            reading_score = st.number_input(get_text('reading_score', current_language), min_value=0, max_value=100, value=80,
                                          help="Student's reading comprehension percentage")
        with col_c:
            writing_score = st.number_input(get_text('writing_score', current_language), min_value=0, max_value=100, value=70,
                                          help="Student's writing skills percentage")
        
        # Show average score indicator
        avg_score = (math_score + reading_score + writing_score) / 3
        if avg_score >= 80:
            score_color = "#16a34a"
            score_status = "Excellent"
        elif avg_score >= 70:
            score_color = "#d97706"
            score_status = "Good"
        elif avg_score >= 60:
            score_color = "#dc2626"
            score_status = "Needs Improvement"
        else:
            score_color = "#991b1b"
            score_status = "Critical"
        
        st.markdown(f"""
        <div style="background: {score_color}20; border-left: 4px solid {score_color}; padding: 10px; margin: 10px 0; border-radius: 4px;">
            <strong>Academic Average: {avg_score:.1f}% - {score_status}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"### {get_text('behavioral_assessment', current_language)}")
        
        col_d, col_e, col_f = st.columns(3)
        with col_d:
            attendance = st.number_input(get_text('attendance', current_language), min_value=0, max_value=100, value=90,
                                       help="Percentage of school days attended")
        with col_e:
            behavior = st.selectbox(get_text('behavior_rating', current_language), [1, 2, 3, 4, 5], index=3,
                                  help="1=Poor, 2=Below Average, 3=Average, 4=Good, 5=Excellent")
        with col_f:
            literacy = st.selectbox(get_text('literacy_level', current_language), list(range(1, 11)), index=5,
                                  help="Reading level from 1 (beginner) to 10 (advanced)")
        
        # Real-time risk indicator
        st.markdown("### Quick Risk Indicator")
        risk_factors = []
        if avg_score < 70:
            risk_factors.append("Low academic performance")
        if attendance < 80:
            risk_factors.append("Poor attendance")
        if behavior <= 2:
            risk_factors.append("Behavioral concerns")
        if literacy <= 3:
            risk_factors.append("Low literacy level")
        
        if risk_factors:
            st.warning(f"⚠️ Risk factors detected: {', '.join(risk_factors)}")
        else:
            st.success("✅ No immediate risk factors detected")
        
        if st.button(get_text('analyze_learning_risk', current_language), type="primary", use_container_width=True):
            try:
                # Prepare student data
                student_data = {
                    'math_score': math_score,
                    'reading_score': reading_score,
                    'writing_score': writing_score,
                    'attendance': attendance,
                    'behavior': behavior,
                    'literacy': literacy
                }
                
                # Make prediction
                if not st.session_state.offline_mode:
                    prediction, probability = make_prediction(student_data)
                    
                    # Determine risk level
                    if probability < 0.3:
                        risk_level = "Low Risk"
                        risk_color = "#16a34a"
                    elif probability < 0.7:
                        risk_level = "Medium Risk"
                        risk_color = "#d97706"
                    else:
                        risk_level = "High Risk"
                        risk_color = "#dc2626"
                    
                    st.session_state.last_prediction = {
                        'student_name': student_name,
                        'risk_level': risk_level,
                        'probability': probability,
                        'risk_color': risk_color,
                        'student_data': student_data
                    }
                else:
                    # Offline mode - simple rule-based assessment
                    avg_score = (math_score + reading_score + writing_score) / 3
                    if avg_score >= 75 and attendance >= 85 and behavior >= 4:
                        risk_level = "Low Risk"
                        probability = 0.2
                        risk_color = "#16a34a"
                    elif avg_score >= 60 and attendance >= 70:
                        risk_level = "Medium Risk"
                        probability = 0.5
                        risk_color = "#d97706"
                    else:
                        risk_level = "High Risk"
                        probability = 0.8
                        risk_color = "#dc2626"
                    
                    st.session_state.last_prediction = {
                        'student_name': student_name,
                        'risk_level': risk_level,
                        'probability': probability,
                        'risk_color': risk_color,
                        'student_data': student_data
                    }
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Error during assessment: {str(e)}")
    
    with col2:
        st.markdown(f"### {get_text('assessment_results', current_language)}")
        
        if 'last_prediction' in st.session_state:
            result = st.session_state.last_prediction
            
            # Risk level indicator with gauge chart
            st.markdown(f"""
            <div style="background: {result['risk_color']}; color: white; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
                <h3 style="margin: 0; font-size: 24px;">{result['risk_level']}</h3>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">Risk Probability: {result['probability']:.1%}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Risk probability gauge
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = result['probability'] * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Risk Level (%)"},
                delta = {'reference': 50},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': result['risk_color']},
                    'steps': [
                        {'range': [0, 30], 'color': "rgba(22, 163, 74, 0.2)"},
                        {'range': [30, 70], 'color': "rgba(217, 119, 6, 0.2)"},
                        {'range': [70, 100], 'color': "rgba(220, 38, 38, 0.2)"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Performance radar chart
            st.markdown("### Performance Profile")
            categories = ['Mathematics', 'Reading', 'Writing', 'Attendance', 'Behavior', 'Literacy']
            values = [
                result['student_data']['math_score'],
                result['student_data']['reading_score'],
                result['student_data']['writing_score'],
                result['student_data']['attendance'],
                result['student_data']['behavior'] * 20,  # Scale to 100
                result['student_data']['literacy'] * 10   # Scale to 100
            ]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                marker_color=result['risk_color']
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=False,
                height=300,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            
            # Recommendations
            st.markdown("### Recommendations")
            
            if result['risk_level'] == "Low Risk":
                st.success("Student is performing well. Continue current learning approach.")
                st.markdown("**Suggested Actions:**")
                st.markdown("✓ Maintain current study routine")
                st.markdown("✓ Provide enrichment activities")
                st.markdown("✓ Monitor progress regularly")
                st.markdown("✓ Consider advanced placement opportunities")
            
            elif result['risk_level'] == "Medium Risk":
                st.warning("Student may benefit from additional support.")
                st.markdown("**Suggested Actions:**")
                st.markdown("• Provide targeted tutoring in weak areas")
                st.markdown("• Increase parent-teacher communication")
                st.markdown("• Monitor attendance closely")
                st.markdown("• Implement weekly progress checks")
            
            else:
                st.error("Student requires immediate intervention.")
                st.markdown("**Urgent Actions Required:**")
                st.markdown("⚠️ Implement individualized learning plan")
                st.markdown("⚠️ Consider specialized support services")
                st.markdown("⚠️ Increase monitoring and feedback")
                st.markdown("⚠️ Schedule parent conference immediately")
            
            # Save assessment button
            if st.button("Save Assessment", type="secondary", use_container_width=True):
                try:
                    # Prepare assessment data
                    assessment_data = {
                        'student_name': result['student_name'],
                        'grade_level': result['student_data'].get('grade_level', ''),
                        'math_score': result['student_data']['math_score'],
                        'reading_score': result['student_data']['reading_score'],
                        'writing_score': result['student_data']['writing_score'],
                        'attendance': result['student_data']['attendance'],
                        'behavior': result['student_data']['behavior'],
                        'literacy': result['student_data']['literacy'],
                        'prediction': 1 if result['risk_level'] == 'High Risk' else 0,
                        'probability': result['probability'],
                        'risk_level': result['risk_level'],
                        'timestamp': datetime.now().isoformat(),
                        'recommendations': get_recommendations(result['risk_level'])
                    }
                    
                    # Save to JSON file
                    from utils.data_utils import save_prediction_data
                    save_prediction_data(assessment_data)
                    
                    # Add to session state for immediate display
                    if 'saved_assessments' not in st.session_state:
                        st.session_state.saved_assessments = []
                    st.session_state.saved_assessments.append(assessment_data)
                    
                    st.success(f"Assessment for {result['student_name']} saved successfully!")
                    
                except Exception as e:
                    st.error(f"Error saving assessment: {str(e)}")
                
        else:
            st.info("Complete the assessment form to view results.")
            
            # Sample visualization placeholder
            st.markdown("### Sample Analysis")
            fig_sample = go.Figure()
            fig_sample.add_trace(go.Bar(
                x=['Math', 'Reading', 'Writing'],
                y=[0, 0, 0],
                marker_color='#e5e7eb'
            ))
            fig_sample.update_layout(
                height=200,
                title="Subject Performance",
                showlegend=False,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig_sample, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_resources():
    """Render the resources page with comprehensive teacher tools"""
    # Get current language setting
    current_language = st.session_state.get('app_language', 'English')
    
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    
    st.markdown(f"## {get_text('resources', current_language)} - Teacher Tools & Guides")
    st.markdown("Comprehensive educational resources for effective teaching and learning support.")
    
    # Create tabs for different resource categories
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Teaching Guides", 
        "Lesson Plans", 
        "Educational Games", 
        "Real-Life Activities",
        "My Saved Resources"
    ])
    
    with tab1:
        render_teaching_guides(current_language)
    
    with tab2:
        render_lesson_plans(current_language)
    
    with tab3:
        render_educational_games(current_language)
    
    with tab4:
        render_real_life_activities(current_language)
    
    with tab5:
        render_saved_resources(current_language)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_teaching_guides(language):
    """Render teaching guides and strategies"""
    st.markdown("### Teaching Guides & Strategies")
    
    # Categories of teaching guides
    guide_type = st.selectbox("Select Guide Category", [
        "Learning Difficulty Support",
        "Classroom Management", 
        "Assessment Strategies",
        "Differentiated Instruction",
        "Student Engagement",
        "Parent Communication"
    ])
    
    if guide_type == "Learning Difficulty Support":
        st.markdown("""
        #### Identifying Learning Difficulties
        **Early Warning Signs:**
        - Difficulty following multi-step instructions
        - Problems with reading comprehension or math concepts
        - Inconsistent academic performance
        - Avoidance of reading or writing tasks
        - Trouble organizing thoughts or materials
        
        **Intervention Strategies:**
        - Break down complex tasks into smaller steps
        - Use visual aids and hands-on learning materials
        - Provide extra time for assignments and tests
        - Offer alternative ways to demonstrate knowledge
        - Create structured learning environments
        
        **External Resources & Professional Development:**
        - **International Dyslexia Association**: dyslexiaida.org - Research-based resources
        - **Learning Disabilities Association**: ldaamerica.org - Support strategies
        - **Understood.org**: understood.org - Comprehensive learning difference guide
        - **CAST UDL Guidelines**: udlguidelines.cast.org - Universal Design for Learning
        - **RTI Action Network**: rtinetwork.org - Response to Intervention resources
        """)
        
    elif guide_type == "Classroom Management":
        st.markdown("""
        #### Effective Classroom Management
        **Creating Positive Environment:**
        - Establish clear, consistent rules and expectations
        - Use positive reinforcement and praise
        - Create predictable daily routines
        - Provide calm-down spaces for overwhelmed students
        
        **Managing Challenging Behaviors:**
        - Address issues privately before escalating
        - Use restorative practices instead of punishment
        - Teach emotional regulation skills
        - Collaborate with parents and support staff
        
        **External Resources & Training:**
        - **Positive Behavioral Interventions & Supports**: pbis.org - Evidence-based strategies
        - **Responsive Classroom**: responsiveclassroom.org - Social-emotional learning approach
        - **Teaching Tolerance**: tolerance.org - Classroom management resources
        - **Edutopia**: edutopia.org/classroom-management - Research-based practices
        - **ASCD**: ascd.org - Professional development resources
        """)
        
    elif guide_type == "Assessment Strategies":
        st.markdown("""
        #### Comprehensive Assessment Approaches
        **Formative Assessment:**
        - Daily check-ins and exit tickets
        - Peer and self-assessment activities
        - Learning journals and reflection
        - Quick diagnostic quizzes
        
        **Accommodations for Struggling Learners:**
        - Extended time for assessments
        - Alternative formats (oral, visual, hands-on)
        - Reduced question quantities
        - Use of assistive technology
        
        **External Assessment Resources:**
        - **Educational Testing Service**: ets.org - Assessment development guidance
        - **National Center on Educational Outcomes**: nceo.info - Inclusive assessment
        - **Smarter Balanced**: smarterbalanced.org - Assessment tools and resources
        - **Council of Chief State School Officers**: ccsso.org - Assessment standards
        - **Assessment & Teaching of 21st Century Skills**: atc21s.org - Modern assessment
        """)
    
    # Add remaining guide categories
    elif guide_type == "Differentiated Instruction":
        st.markdown("""
        #### Differentiated Instruction Strategies
        **Content Differentiation:**
        - Provide materials at multiple reading levels
        - Use multimedia resources (videos, audio, interactive)
        - Offer choice in topics within curriculum standards
        - Create tiered assignments with varying complexity
        
        **Process Differentiation:**
        - Flexible grouping strategies
        - Learning stations and centers
        - Independent study options
        - Collaborative learning opportunities
        
        **Product Differentiation:**
        - Multiple ways to demonstrate learning
        - Portfolio assessments
        - Performance-based tasks
        - Student choice in final products
        
        **External Resources for Differentiation:**
        - **Carol Ann Tomlinson Resources**: carolannntomlinson.com - Differentiation expert
        - **Association for Supervision and Curriculum Development**: ascd.org/differentiation
        - **Differentiated Instruction Network**: differentiatedinstruction.com
        - **Teaching Channel**: teachingchannel.org - Video examples of differentiation
        - **Edutopia Differentiation**: edutopia.org/differentiated-instruction-resources
        """)
    
    elif guide_type == "Student Engagement":
        st.markdown("""
        #### Student Engagement Techniques
        **Active Learning Strategies:**
        - Think-pair-share activities
        - Hands-on experiments and projects
        - Role-playing and simulations
        - Interactive technology integration
        
        **Motivation Techniques:**
        - Connect learning to student interests
        - Provide choice and autonomy
        - Set achievable goals with clear progress markers
        - Celebrate effort and improvement, not just achievement
        
        **External Engagement Resources:**
        - **Student Engagement Institute**: studentengagementinstitute.org
        - **Gallup Student Engagement**: gallup.com/education/student-engagement
        - **Buck Institute for Education**: pblworks.org - Project-based learning
        - **Facing History and Ourselves**: facinghistory.org - Engaging curriculum
        - **Teaching Kids to Love Learning**: scholastic.com/teachers/teaching-resources
        """)
    
    elif guide_type == "Parent Communication":
        st.markdown("""
        #### Effective Parent Communication
        **Building Partnerships:**
        - Regular, proactive communication about student progress
        - Share positive news, not just concerns
        - Provide specific suggestions for home support
        - Respect cultural differences and family circumstances
        
        **Communication Methods:**
        - Weekly newsletters or emails
        - Parent-teacher conferences with clear agendas
        - Home visits when appropriate and welcomed
        - Digital platforms for ongoing communication
        
        **External Parent Engagement Resources:**
        - **National PTA**: pta.org - Parent engagement standards
        - **Harvard Family Research Project**: hfrp.org - Research-based strategies
        - **Center for Parent Information**: parentcenterhub.org
        - **National Association of Elementary School Principals**: naesp.org/parent-engagement
        - **Colorin Colorado**: colorincolorado.org - Resources for ELL families
        """)
    
    # Save guide button
    if st.button("Save This Guide"):
        save_resource_to_file("teaching_guide", guide_type, f"Teaching guide for {guide_type}")
        st.success("Guide saved to your resources!")

def render_lesson_plans(language):
    """Render lesson plan creation and management"""
    st.markdown("### Lesson Plan Creator & Manager")
    
    # Lesson plan creator
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Create New Lesson Plan")
        
        lesson_title = st.text_input("Lesson Title")
        subject = st.selectbox("Subject", ["Mathematics", "Reading", "Writing", "Science", "Social Studies", "Art"])
        grade_level = st.selectbox("Grade Level", ["Pre-K", "K", "1", "2", "3", "4", "5", "6"])
        duration = st.selectbox("Duration", ["30 minutes", "45 minutes", "60 minutes", "90 minutes"])
        
        learning_objectives = st.text_area("Learning Objectives", 
                                         placeholder="What will students learn by the end of this lesson?")
        
        materials_needed = st.text_area("Materials Needed", 
                                       placeholder="List all materials, resources, and tools needed")
        
        lesson_activities = st.text_area("Lesson Activities & Procedures", 
                                        placeholder="Step-by-step activities and procedures", height=150)
        
        assessment_method = st.text_area("Assessment Method", 
                                        placeholder="How will you assess student understanding?")
        
        differentiation = st.text_area("Differentiation Strategies", 
                                      placeholder="How will you support different learning needs?")
        
        if st.button("Save Lesson Plan"):
            if lesson_title and learning_objectives:
                lesson_plan = {
                    "title": lesson_title,
                    "subject": subject,
                    "grade_level": grade_level,
                    "duration": duration,
                    "objectives": learning_objectives,
                    "materials": materials_needed,
                    "activities": lesson_activities,
                    "assessment": assessment_method,
                    "differentiation": differentiation,
                    "created_date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                save_resource_to_file("lesson_plan", lesson_title, lesson_plan)
                st.success("Lesson plan saved successfully!")
            else:
                st.error("Please fill in at least the title and learning objectives.")
        
        # External lesson planning resources
        st.markdown("#### External Lesson Planning Resources")
        st.markdown("""
        **Professional Lesson Plan Sites:**
        - **Teachers Pay Teachers**: teacherspayteachers.com - Teacher-created lesson plans
        - **Lesson Planet**: lessonplanet.com - Comprehensive lesson plan database
        - **Education.com**: education.com - Standards-aligned lesson plans
        - **Scholastic Teachers**: scholastic.com/teachers - Grade-level resources
        - **Common Core Resources**: corestandards.org - Standards-based planning
        
        **Subject-Specific Resources:**
        - **ReadWriteThink**: readwritethink.org - Language arts lesson plans
        - **Illuminations**: illuminations.nctm.org - Math lesson plans and activities
        - **NSTA Learning Center**: learningcenter.nsta.org - Science lesson plans
        - **C3 Teachers**: c3teachers.org - Social studies inquiry lessons
        - **Arts Integration**: kennedy-center.org/education - Arts-integrated lessons
        """)
    
    with col2:
        st.markdown("#### Quick Templates")
        
        template_type = st.selectbox("Choose Template", [
            "Reading Comprehension",
            "Math Problem Solving", 
            "Science Experiment",
            "Writing Workshop",
            "Group Project"
        ])
        
        if st.button("Load Template"):
            templates = get_lesson_templates()
            if template_type in templates:
                template = templates[template_type]
                st.text_area("Template Content", value=template, height=200)

def render_educational_games(language):
    """Render educational games and interactive activities"""
    st.markdown("### Educational Games & Interactive Activities")
    
    # Game categories
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Skill-Building Games")
        
        skill_area = st.selectbox("Select Skill Area", [
            "Reading & Literacy",
            "Math & Numbers", 
            "Memory & Attention",
            "Problem Solving",
            "Social Skills"
        ])
        
        difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
        
        if st.button("Generate Game Activity"):
            games = get_educational_games(skill_area, difficulty)
            for game in games:
                st.markdown(f"**{game['name']}**")
                st.markdown(f"*Age Group:* {game['age_group']}")
                st.markdown(f"*Duration:* {game['duration']}")
                st.markdown(f"*Materials:* {game['materials']}")
                st.markdown(f"*Instructions:* {game['instructions']}")
                st.markdown("---")
    
    with col2:
        st.markdown("#### Online Educational Game Platforms")
        
        st.markdown("""
        **Free Educational Game Websites:**
        - **Khan Academy Kids**: khanacademykids.org - Interactive lessons for K-5
        - **PBS Kids Games**: pbskids.org/games - Educational games by subject
        - **Funbrain**: funbrain.com - Math, reading, and problem-solving games
        - **Cool Math Games**: coolmathgames.com - Logic and math puzzle games
        - **National Geographic Kids**: kids.nationalgeographic.com - Science and geography games
        - **Scratch**: scratch.mit.edu - Programming and creative projects
        - **Code.org**: code.org - Computer science education games
        
        **Premium Educational Platforms:**
        - **ABCmouse**: abcmouse.com - Comprehensive early learning platform
        - **Prodigy Math**: prodigygame.com - Adaptive math game platform
        - **Epic Books**: getepic.com - Digital library with interactive books
        - **BrainPOP**: brainpop.com - Educational games and videos
        - **IXL Learning**: ixl.com - Personalized learning with game elements
        
        **Game Creation Tools for Teachers:**
        - **Kahoot**: kahoot.com - Create interactive quizzes and games
        - **Quizizz**: quizizz.com - Gamified assessment platform
        - **Blooket**: blooket.com - Question-based learning games
        - **Gimkit**: gimkit.com - Live learning games for classrooms
        - **Wordwall**: wordwall.net - Create custom educational games
        """)
        
        if st.button("Save Game Resources"):
            save_resource_to_file("games", "Educational Games Collection", 
                                "Collection of educational games and online resources")
            st.success("Game resources saved!")

def render_real_life_activities(language):
    """Render real-life learning activities"""
    st.markdown("### Real-Life Learning Activities")
    
    # Activity categories
    activity_category = st.selectbox("Activity Category", [
        "Home & Family Activities",
        "Community Connections",
        "Nature & Outdoor Learning", 
        "Cultural Activities",
        "Life Skills Practice"
    ])
    
    if activity_category == "Home & Family Activities":
        st.markdown("""
        #### Learning at Home
        
        **Kitchen Math:**
        - Measuring ingredients while cooking
        - Calculating recipe portions
        - Counting and sorting utensils
        - Reading recipe instructions
        
        **Household Reading:**
        - Reading labels and instructions
        - Creating grocery lists together
        - Reading mail and discussing content
        - Writing family journals
        
        **Daily Life Science:**
        - Observing weather patterns
        - Growing plants or herbs
        - Simple cooking experiments
        - Exploring how household items work
        """)
        
    elif activity_category == "Community Connections":
        st.markdown("""
        #### Learning in the Community
        
        **Local Business Visits:**
        - Library storytimes and research
        - Bank visits to learn about money
        - Post office to understand mail system
        - Grocery store math and budgeting
        
        **Community Service Learning:**
        - Helping elderly neighbors
        - Participating in cleanup activities
        - Volunteering at local charities
        - Creating community art projects
        """)
        
    elif activity_category == "Nature & Outdoor Learning":
        st.markdown("""
        #### Outdoor Education
        
        **Nature Exploration:**
        - Identifying plants and animals
        - Weather observation journals
        - Collecting and categorizing natural items
        - Understanding seasonal changes
        
        **Outdoor Math & Science:**
        - Measuring tree heights and distances
        - Counting and comparing natural objects
        - Understanding ecosystems
        - Simple physics with playground equipment
        """)
    
    # Add external resources for real-life activities
    elif activity_category == "Cultural Activities":
        st.markdown("""
        #### Cultural Learning Experiences
        **Museum and Cultural Site Visits:**
        - Local history museums for timeline activities
        - Art galleries for creative expression discussions
        - Cultural centers for community heritage learning
        - Historical sites for hands-on history lessons
        
        **Multicultural Learning:**
        - Celebrating different cultural holidays and traditions
        - Exploring various languages spoken in the community
        - Learning traditional games from different cultures
        - Cooking traditional foods from various cultures
        """)
    
    elif activity_category == "Life Skills Practice":
        st.markdown("""
        #### Practical Life Skills Learning
        **Financial Literacy:**
        - Setting up a classroom store for money math
        - Budget planning for class parties or field trips
        - Comparing prices while shopping with families
        - Learning about saving and spending decisions
        
        **Communication Skills:**
        - Writing thank-you notes to community helpers
        - Conducting interviews with family members
        - Presenting research projects to classmates
        - Participating in community meetings or events
        """)
    
    # External resources for real-life activities
    st.markdown("#### External Resources for Real-Life Learning")
    st.markdown("""
    **Organizations Supporting Experiential Learning:**
    - **Place-based Education Cooperative**: promiseofplace.org - Community-based learning
    - **Children & Nature Network**: childrenandnature.org - Outdoor education resources
    - **4-H Youth Development**: 4-h.org - Hands-on learning projects and activities
    - **Junior Achievement**: ja.org - Economic education and entrepreneurship
    - **National Environmental Education Foundation**: neefusa.org - Environmental learning
    
    **Community Partnership Resources:**
    - **Points of Light**: pointsoflight.org - Community service learning projects
    - **Learning for Justice**: learningforjustice.org - Social justice education activities
    - **National Art Education Association**: arteducators.org - Arts integration ideas
    - **National Council for Social Studies**: socialstudies.org - Community-based social studies
    - **Project Learning Tree**: plt.org - Environmental education activities
    """)
    
    # Activity planner
    st.markdown("#### Activity Planner")
    
    col1, col2 = st.columns(2)
    with col1:
        activity_name = st.text_input("Activity Name")
        learning_goals = st.text_area("Learning Goals")
        
    with col2:
        materials_required = st.text_area("Materials Required") 
        estimated_time = st.selectbox("Estimated Time", ["15 min", "30 min", "1 hour", "2+ hours"])
    
    activity_steps = st.text_area("Activity Steps", height=100)
    
    if st.button("Save Activity Plan"):
        if activity_name and learning_goals:
            activity_plan = {
                "name": activity_name,
                "goals": learning_goals,
                "materials": materials_required,
                "time": estimated_time,
                "steps": activity_steps,
                "created_date": datetime.now().strftime("%Y-%m-%d")
            }
            save_resource_to_file("activity", activity_name, activity_plan)
            st.success("Activity plan saved!")

def render_saved_resources(language):
    """Render saved resources management"""
    st.markdown("### My Saved Resources")
    
    # Load saved resources
    saved_resources = load_saved_resources()
    
    if not saved_resources:
        st.info("No saved resources yet. Create and save resources from other tabs to see them here.")
        return
    
    # Filter by resource type
    resource_types = list(set([r['type'] for r in saved_resources]))
    selected_type = st.selectbox("Filter by Type", ["All"] + resource_types)
    
    # Display resources
    filtered_resources = saved_resources if selected_type == "All" else [r for r in saved_resources if r['type'] == selected_type]
    
    for i, resource in enumerate(filtered_resources):
        with st.expander(f"{resource['type'].title()}: {resource['name']}"):
            st.markdown(f"**Created:** {resource.get('created_date', 'Unknown')}")
            st.markdown(f"**Type:** {resource['type'].title()}")
            
            if isinstance(resource['content'], dict):
                for key, value in resource['content'].items():
                    if value:
                        st.markdown(f"**{key.title()}:** {value}")
            else:
                st.markdown(resource['content'])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Export", key=f"export_{i}"):
                    export_resource_as_pdf(resource)
                    st.success("Resource exported!")
            
            with col2:
                if st.button(f"Delete", key=f"delete_{i}"):
                    delete_saved_resource(resource['name'])
                    st.success("Resource deleted!")
                    st.rerun()

def save_resource_to_file(resource_type, name, content):
    """Save resource to file"""
    from utils.data_utils import get_data_directory
    import json
    import os
    
    data_dir = get_data_directory()
    resources_file = os.path.join(data_dir, "saved_resources.json")
    
    # Load existing resources
    try:
        if os.path.exists(resources_file):
            with open(resources_file, 'r', encoding='utf-8') as f:
                resources = json.load(f)
        else:
            resources = []
    except:
        resources = []
    
    # Add new resource
    new_resource = {
        "type": resource_type,
        "name": name,
        "content": content,
        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    resources.append(new_resource)
    
    # Save updated resources
    try:
        with open(resources_file, 'w', encoding='utf-8') as f:
            json.dump(resources, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving resource: {e}")

def load_saved_resources():
    """Load saved resources from file"""
    from utils.data_utils import get_data_directory
    import json
    import os
    
    data_dir = get_data_directory()
    resources_file = os.path.join(data_dir, "saved_resources.json")
    
    try:
        if os.path.exists(resources_file):
            with open(resources_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    
    return []

def get_lesson_templates():
    """Get lesson plan templates"""
    return {
        "Reading Comprehension": """
**Lesson Objective:** Students will improve reading comprehension skills through guided practice.

**Activities:**
1. Pre-reading discussion (5 min)
2. Guided reading of selected text (15 min)
3. Comprehension questions and discussion (15 min)
4. Independent practice (10 min)

**Assessment:** Exit ticket with 3 comprehension questions
        """,
        "Math Problem Solving": """
**Lesson Objective:** Students will apply problem-solving strategies to word problems.

**Activities:**
1. Review problem-solving steps (5 min)
2. Model problem-solving with think-aloud (10 min)
3. Guided practice in pairs (20 min)
4. Independent problem solving (10 min)

**Assessment:** Problem-solving rubric
        """,
        "Science Experiment": """
**Lesson Objective:** Students will observe and record scientific phenomena.

**Activities:**
1. Hypothesis formation (10 min)
2. Conduct experiment with observation (20 min)
3. Record and analyze results (15 min)
4. Draw conclusions (10 min)

**Assessment:** Lab report with observations and conclusions
        """
    }

def get_educational_games(skill_area, difficulty):
    """Get educational games based on skill area and difficulty"""
    games_db = {
        "Reading & Literacy": {
            "Easy": [
                {
                    "name": "Letter Hunt",
                    "age_group": "4-6 years",
                    "duration": "15-20 minutes",
                    "materials": "Magazines, scissors, glue, paper",
                    "instructions": "Have children find and cut out specific letters from magazines to create alphabet collages."
                }
            ],
            "Medium": [
                {
                    "name": "Story Building Blocks",
                    "age_group": "6-8 years", 
                    "duration": "20-30 minutes",
                    "materials": "Story prompt cards, timer",
                    "instructions": "Children take turns adding sentences to build a collaborative story using prompt cards."
                }
            ]
        },
        "Math & Numbers": {
            "Easy": [
                {
                    "name": "Number Line Hopscotch",
                    "age_group": "5-7 years",
                    "duration": "15-25 minutes", 
                    "materials": "Chalk, number cards",
                    "instructions": "Create a number line on the ground. Call out numbers and have children hop to them."
                }
            ]
        }
    }
    
    return games_db.get(skill_area, {}).get(difficulty, [{"name": "Custom Activity", "age_group": "All ages", "duration": "Variable", "materials": "As needed", "instructions": "Create your own activity for this skill area."}])

def delete_saved_resource(resource_name):
    """Delete a saved resource"""
    from utils.data_utils import get_data_directory
    import json
    import os
    
    data_dir = get_data_directory()
    resources_file = os.path.join(data_dir, "saved_resources.json")
    
    try:
        if os.path.exists(resources_file):
            with open(resources_file, 'r', encoding='utf-8') as f:
                resources = json.load(f)
            
            resources = [r for r in resources if r['name'] != resource_name]
            
            with open(resources_file, 'w', encoding='utf-8') as f:
                json.dump(resources, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error deleting resource: {e}")

def export_resource_as_pdf(resource):
    """Export resource as downloadable content"""
    # For now, just copy to clipboard or show export message
    st.info("Resource content copied for export. In a full implementation, this would generate a PDF download.")

def render_tracker():
    """Render the parent tracker page"""
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    
    st.markdown("## Parent Observation Tracker")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Daily Observation Log")
        
        # Child information
        child_name = st.text_input("Child's Name")
        observation_date = st.date_input("Observation Date", datetime.now())
        
        st.markdown("### Academic Observations")
        
        col_a, col_b = st.columns(2)
        with col_a:
            homework_completion = st.slider("Homework Completion (%)", 0, 100, 75)
            reading_time = st.number_input("Reading Time (minutes)", min_value=0, max_value=120, value=20)
        with col_b:
            focus_level = st.selectbox("Focus Level", ["Low", "Medium", "High"])
            subjects_struggled = st.multiselect("Subjects Struggled With", ["Math", "Reading", "Writing", "Science"])
        
        st.markdown("### Behavioral Observations")
        
        col_c, col_d = st.columns(2)
        with col_c:
            behavior_rating = st.selectbox("Behavior Rating", [1, 2, 3, 4, 5], index=3)
            mood_rating = st.selectbox("Mood Rating", [1, 2, 3, 4, 5], index=3)
        with col_d:
            sleep_hours = st.number_input("Sleep Hours", min_value=0.0, max_value=12.0, value=8.0, step=0.5)
            energy_level = st.selectbox("Energy Level", ["Low", "Medium", "High"])
        
        # Additional observations
        learning_wins = st.text_area("Learning Wins Today", placeholder="What did your child do well today?")
        challenges_faced = st.text_area("Challenges Faced", placeholder="What difficulties did your child encounter?")
        
        if st.button("Save Observation", type="primary"):
            observation_data = {
                'child_name': child_name,
                'date': observation_date.isoformat(),
                'homework_completion': homework_completion,
                'reading_time': reading_time,
                'focus_level': focus_level,
                'subjects_struggled': subjects_struggled,
                'behavior_rating': behavior_rating,
                'mood_rating': mood_rating,
                'sleep_hours': sleep_hours,
                'energy_level': energy_level,
                'learning_wins': learning_wins,
                'challenges_faced': challenges_faced,
                'timestamp': datetime.now().isoformat()
            }
            
            try:
                # Save observation to file
                save_parent_observation(observation_data)
                
                # Add to session state for immediate display
                if 'saved_observations' not in st.session_state:
                    st.session_state.saved_observations = []
                st.session_state.saved_observations.append(observation_data)
                
                st.success(f"Observation for {child_name} saved successfully!")
                st.balloons()
                
            except Exception as e:
                st.error(f"Error saving observation: {str(e)}")
    
    with col2:
        st.markdown("### Progress Insights")
        
        # Sample progress data
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        homework_progress = np.random.normal(75, 10, 30)
        reading_progress = np.random.normal(20, 5, 30)
        
        # Homework completion trend
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=homework_progress,
            mode='lines+markers',
            name='Homework Completion %',
            line=dict(color='#3b82f6')
        ))
        fig.update_layout(
            title="Homework Completion Trend",
            height=200,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Reading time trend
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=dates,
            y=reading_progress,
            mode='lines+markers',
            name='Reading Time (minutes)',
            line=dict(color='#16a34a')
        ))
        fig2.update_layout(
            title="Daily Reading Time",
            height=200,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_analytics():
    """Render the analytics page"""
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    
    st.markdown("## Analytics & Reports")
    
    # Analytics overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Assessments", "245", "+12 this week")
    with col2:
        st.metric("Average Risk Score", "0.34", "-0.05 vs last month")
    with col3:
        st.metric("Intervention Success", "78%", "+5% improvement")
    
    # Detailed analytics
    tab1, tab2, tab3 = st.tabs(["Performance Trends", "Risk Analysis", "Intervention Tracking"])
    
    with tab1:
        st.markdown("### Performance Trends Over Time")
        
        # Generate sample trend data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        math_scores = [72, 74, 76, 75, 78, 80]
        reading_scores = [68, 70, 72, 74, 76, 78]
        writing_scores = [65, 67, 69, 71, 73, 75]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=math_scores, mode='lines+markers', name='Mathematics'))
        fig.add_trace(go.Scatter(x=months, y=reading_scores, mode='lines+markers', name='Reading'))
        fig.add_trace(go.Scatter(x=months, y=writing_scores, mode='lines+markers', name='Writing'))
        
        fig.update_layout(
            title="Average Subject Scores by Month",
            xaxis_title="Month",
            yaxis_title="Average Score (%)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Risk Level Distribution")
        
        # Risk analysis by grade
        grades = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6']
        low_risk = [25, 30, 28, 32, 29, 26]
        medium_risk = [8, 10, 12, 9, 11, 10]
        high_risk = [3, 2, 4, 3, 2, 3]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Low Risk', x=grades, y=low_risk, marker_color='#16a34a'))
        fig.add_trace(go.Bar(name='Medium Risk', x=grades, y=medium_risk, marker_color='#d97706'))
        fig.add_trace(go.Bar(name='High Risk', x=grades, y=high_risk, marker_color='#dc2626'))
        
        fig.update_layout(
            title="Risk Distribution by Grade Level",
            xaxis_title="Grade Level",
            yaxis_title="Number of Students",
            barmode='stack',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Intervention Effectiveness")
        
        interventions = ['Tutoring', 'Parent Support', 'Special Resources', 'Counseling']
        success_rates = [85, 72, 68, 79]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=interventions,
            y=success_rates,
            marker_color=['#3b82f6', '#16a34a', '#d97706', '#8b5cf6']
        ))
        
        fig.update_layout(
            title="Intervention Success Rates",
            xaxis_title="Intervention Type",
            yaxis_title="Success Rate (%)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_bottom_navigation():
    """Render bottom navigation with offline toggle and reset"""
    st.markdown("""
    <div class="bottom-nav">
    </div>
    """, unsafe_allow_html=True)
    
    # Get current language setting
    current_language = st.session_state.get('app_language', 'English')
    
    # Bottom navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button(get_text('offline_mode', current_language), key="offline_toggle", help="Switch between online and offline modes"):
            st.session_state.offline_mode = not st.session_state.offline_mode
            st.session_state.mode_status = "Offline Mode" if st.session_state.offline_mode else "Online Mode"
            st.toast(f"Switched to {st.session_state.mode_status}")
            st.rerun()
    
    with col2:
        if st.button(get_text('export_data', current_language), key="export_data", help="Export assessment data as CSV"):
            try:
                # Load actual saved data
                student_data = load_student_data()
                parent_data = load_parent_observations()
                
                if student_data or parent_data:
                    # Create comprehensive export data
                    export_records = []
                    
                    # Add assessment data
                    for record in student_data:
                        export_records.append({
                            'Type': 'Assessment',
                            'Date': record.get('timestamp', ''),
                            'Student_Name': record.get('student_name', ''),
                            'Grade_Level': record.get('grade_level', ''),
                            'Math_Score': record.get('math_score', ''),
                            'Reading_Score': record.get('reading_score', ''),
                            'Writing_Score': record.get('writing_score', ''),
                            'Attendance': record.get('attendance', ''),
                            'Behavior': record.get('behavior', ''),
                            'Literacy': record.get('literacy', ''),
                            'Risk_Level': record.get('risk_level', ''),
                            'Probability': record.get('probability', ''),
                            'Recommendations': ', '.join(record.get('recommendations', []))
                        })
                    
                    # Add parent tracker data
                    for record in parent_data:
                        export_records.append({
                            'Type': 'Parent_Tracker',
                            'Date': record.get('date', ''),
                            'Student_Name': record.get('child_name', ''),
                            'Homework_Completion': record.get('homework_completion', ''),
                            'Reading_Time': record.get('reading_time', ''),
                            'Focus_Level': record.get('focus_level', ''),
                            'Behavior_Rating': record.get('behavior_rating', ''),
                            'Mood_Rating': record.get('mood_rating', ''),
                            'Sleep_Hours': record.get('sleep_hours', ''),
                            'Energy_Level': record.get('energy_level', ''),
                            'Screen_Time': record.get('screen_time', ''),
                            'Physical_Activity': record.get('physical_activity', ''),
                            'Learning_Wins': record.get('learning_wins', ''),
                            'Challenges_Faced': record.get('challenges_faced', '')
                        })
                    
                    if export_records:
                        df = pd.DataFrame(export_records)
                        csv = df.to_csv(index=False)
                        # Combined data download
                        st.download_button(
                            label="Download All Data (CSV)",
                            data=csv,
                            file_name=f'eduscan_all_data_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
                            mime='text/csv',
                            key="download_csv_all"
                        )
                        
                        # Separate downloads for each data type
                        if student_data:
                            assessment_df = pd.DataFrame([r for r in export_records if r['Type'] == 'Assessment'])
                            assessment_csv = assessment_df.to_csv(index=False)
                            st.download_button(
                                label="Download Assessments Only (CSV)",
                                data=assessment_csv,
                                file_name=f'eduscan_assessments_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
                                mime='text/csv',
                                key="download_assessments"
                            )
                        
                        if parent_data:
                            tracker_df = pd.DataFrame([r for r in export_records if r['Type'] == 'Parent_Tracker'])
                            tracker_csv = tracker_df.to_csv(index=False)
                            st.download_button(
                                label="Download Parent Tracker Data (CSV)",
                                data=tracker_csv,
                                file_name=f'eduscan_parent_tracker_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
                                mime='text/csv',
                                key="download_tracker"
                            )
                        
                        st.success(f"Ready to download {len(export_records)} total records!")
                        st.info(f"📊 {len(student_data)} assessments | 👨‍👩‍👧‍👦 {len(parent_data)} tracker entries")
                    else:
                        st.warning("No data available to export")
                else:
                    st.info("No saved data found. Complete some assessments or tracker entries first.")
                    
            except Exception as e:
                st.error(f"Export failed: {str(e)}")
    
    with col3:
        if st.button(get_text('settings', current_language), key="settings", help="Application settings and preferences"):
            st.session_state.show_settings = not st.session_state.get('show_settings', False)
            st.rerun()
        
        # Show settings panel if toggled
        if st.session_state.get('show_settings', False):
            st.markdown("### Settings Panel")
            
            # Create clean settings layout
            st.markdown("---")
            
            # Language setting
            current_language = st.session_state.get('app_language', 'English')
            st.markdown("**Language / Luuqadda / اللغة**")
            new_language = st.selectbox("Select Language", ["English", "Somali", "Arabic"], 
                                      index=["English", "Somali", "Arabic"].index(current_language),
                                      key="language_selector")
            
            st.markdown("---")
            
            # Theme setting
            current_theme = st.session_state.get('app_theme', 'Light')
            st.markdown("**Theme / Duco / المظهر**")
            new_theme = st.selectbox("Choose Theme", ["Light", "Dark"], 
                                   index=["Light", "Dark"].index(current_theme),
                                   key="theme_selector")
            
            # Show immediate theme preview
            if new_theme != current_theme:
                apply_theme(new_theme)
            
            st.markdown("---")
            
            # Auto-save setting
            current_interval = st.session_state.get('autosave_interval', 5)
            st.markdown("**Auto-save Interval**")
            new_interval = st.slider("Minutes between auto-saves", 1, 30, current_interval, key="interval_slider")
            
            st.markdown("---")
            
            # Action buttons in clean layout
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("💾 Save Settings", key="save_settings_btn", use_container_width=True):
                    # Update session state with new settings
                    st.session_state.app_language = new_language
                    st.session_state.app_theme = new_theme
                    st.session_state.autosave_interval = new_interval
                    
                    # Apply theme changes
                    apply_theme(new_theme)
                    
                    # Save to file for persistence
                    settings_data = {
                        'language': new_language,
                        'theme': new_theme,
                        'autosave_interval': new_interval,
                        'saved_at': datetime.now().isoformat()
                    }
                    
                    try:
                        with open('data/app_settings.json', 'w') as f:
                            json.dump(settings_data, f, indent=2)
                    except:
                        pass  # Continue without file save if directory doesn't exist
                    
                    st.success(f"✅ Settings saved! Language: {new_language}, Theme: {new_theme}")
                    st.balloons()
                    st.session_state.show_settings = False
                    st.rerun()
            
            with col2:
                if st.button("🔄 Reset to Default", key="reset_settings_btn", use_container_width=True):
                    st.session_state.app_language = 'English'
                    st.session_state.app_theme = 'Light'
                    st.session_state.autosave_interval = 5
                    apply_theme('Light')
                    st.success("🔄 Settings reset to default!")
                    st.rerun()
            
            with col3:
                if st.button("❌ Close Panel", key="close_settings_btn", use_container_width=True):
                    st.session_state.show_settings = False
                    st.rerun()
    
    with col4:
        if st.button(get_text('help', current_language), key="help", help="Documentation and support resources"):
            with st.expander("Help & Documentation", expanded=True):
                st.markdown("### Quick Start Guide")
                st.markdown("1. **Dashboard**: View overall system statistics")
                st.markdown("2. **Assessment**: Evaluate student learning risks")
                st.markdown("3. **Resources**: Access educational materials")
                st.markdown("4. **Tracker**: Log daily observations")
                st.markdown("5. **Analytics**: Review progress reports")
                
                st.markdown("### Support Contacts")
                st.markdown("📧 support@eduscan-somalia.edu")
                st.markdown("📞 +252-xx-xxxxxxx")
    
    with col5:
        # Reset button with proper state management
        reset_clicked = st.button(get_text('reset', current_language), key="reset_app", help="Clear all data and restart")
        
        if reset_clicked:
            if 'reset_confirm_step' not in st.session_state:
                st.session_state.reset_confirm_step = 1
                st.rerun()
            elif st.session_state.reset_confirm_step == 1:
                st.session_state.reset_confirm_step = 2
                st.rerun()
        
        # Show confirmation dialog
        if 'reset_confirm_step' in st.session_state:
            if st.session_state.reset_confirm_step == 1:
                st.warning("⚠️ This will clear all data. Click Reset again to confirm.")
            elif st.session_state.reset_confirm_step == 2:
                # Actually reset the application
                keys_to_delete = [key for key in st.session_state.keys() if key != 'reset_confirm_step']
                for key in keys_to_delete:
                    del st.session_state[key]
                
                # Reinitialize core state
                st.session_state.current_page = 'Dashboard'
                st.session_state.offline_mode, st.session_state.mode_status = check_offline_mode()
                
                # Clear reset confirmation
                if 'reset_confirm_step' in st.session_state:
                    del st.session_state.reset_confirm_step
                
                st.success("✅ Application reset successfully!")
                st.balloons()
                st.rerun()

# Main application logic
def main():
    """Main application function"""
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Dashboard'
    
    if 'offline_mode' not in st.session_state:
        st.session_state.offline_mode, st.session_state.mode_status = check_offline_mode()
    
    # Load and apply saved settings
    if 'settings_loaded' not in st.session_state:
        saved_settings = load_app_settings()
        st.session_state.app_language = saved_settings.get('language', 'English')
        st.session_state.app_theme = saved_settings.get('theme', 'Light')
        st.session_state.autosave_interval = saved_settings.get('autosave_interval', 5)
        st.session_state.settings_loaded = True
        
        # Apply the saved theme
        apply_theme(st.session_state.app_theme)
    
    # Render header
    render_app_header()
    
    # Render navigation
    render_navigation()
    
    # Render current page content
    if st.session_state.current_page == 'Dashboard':
        render_dashboard()
    elif st.session_state.current_page == 'Assessment':
        render_assessment()
    elif st.session_state.current_page == 'Resources':
        render_resources()
    elif st.session_state.current_page == 'Tracker':
        render_tracker()
    elif st.session_state.current_page == 'Analytics':
        render_analytics()
    
    # Render bottom navigation
    render_bottom_navigation()

if __name__ == "__main__":
    main()