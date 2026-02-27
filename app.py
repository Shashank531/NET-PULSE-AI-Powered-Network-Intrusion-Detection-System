import streamlit as st
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time

# ========================= 
# Global Color Map 
# ========================= 
COLOR_MAP = {
    "Normal": "#17b724",     # green
    "Suspicious": "#ffae00",  # yellow
    "Malicious": "#ff2a2a"    # red
}

# Set page config
st.set_page_config(
    page_title="NET PULSE - AI-Powered NIDS",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with sophisticated dark theme and improved visualizations
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main Background - Sophisticated Dark */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 50%, #0f1419 100%);
    }
    
    /* Remove default Streamlit styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide the top toolbar and streamlit branding */
    .stApp > header {
        display: none !important;
    }
    
    /* Hide streamlit's default top right buttons */
    .stApp > div:first-child > div:first-child > div:first-child {
        display: none !important;
    }
    
    /* Remove padding from main container */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Hide empty containers */
    div[data-testid="column"] {
        min-height: 0 !important;
    }
    
    div[data-testid="column"]:empty {
        display: none !important;
    }
    
    /* Aggressively hide top-left boxes */
    section[data-testid="stSidebar"] + div {
        padding-left: 0 !important;
    }
    
    /* Hide decoration containers */
    .stApp [data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Remove top spacer */
    .stApp .block-container {
        padding-top: 1rem !important;
    }
    
    /* Hide any empty divs at the top */
    .main .block-container > div:first-child:empty {
        display: none !important;
    }
    
    /* Target and hide the specific gray boxes */
    div[class*="st-emotion-cache"] > div:empty {
        display: none !important;
    }
    
    /* Custom Header */
    .main-header {
        background: linear-gradient(135deg, rgba(23, 183, 36, 0.1) 0%, rgba(26, 31, 46, 0.9) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #17b724 20%, 
            #ffae00 50%, 
            #ff2a2a 80%, 
            transparent 100%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    .header-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #a0aec0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .header-subtitle {
        color: #a0aec0;
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 300;
        letter-spacing: 0.05em;
    }
    
    /* Metric Cards - Smart Home Inspired */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at top right, rgba(23, 183, 36, 0.1), transparent 60%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(23, 183, 36, 0.3);
        box-shadow: 0 12px 40px rgba(23, 183, 36, 0.15);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    /* Enhanced Chart Container */
    .chart-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at center, rgba(23, 183, 36, 0.05), transparent 70%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .chart-container:hover::before {
        opacity: 1;
    }
    
    .chart-container:hover {
        border-color: rgba(23, 183, 36, 0.2);
        box-shadow: 0 8px 32px rgba(23, 183, 36, 0.1);
    }
    
    /* Chart Title */
    .chart-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .chart-title::before {
        content: '📊';
        font-size: 1.5rem;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.02);
        padding: 0.75rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 14px;
        color: #a0aec0;
        font-weight: 500;
        padding: 0.85rem 1.75rem;
        transition: all 0.3s ease;
        border: 1px solid transparent;
        font-size: 0.95rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.05);
        color: #ffffff;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(23, 183, 36, 0.25) 0%, rgba(23, 183, 36, 0.15) 100%) !important;
        color: #17b724 !important;
        border-color: rgba(23, 183, 36, 0.4) !important;
        box-shadow: 0 4px 16px rgba(23, 183, 36, 0.2);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 20, 25, 0.95) 0%, rgba(26, 31, 46, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    [data-testid="stSidebar"] .element-container {
        transition: all 0.3s ease;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #17b724 0%, #15a020 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(23, 183, 36, 0.3);
        letter-spacing: 0.02em;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(23, 183, 36, 0.4);
        background: linear-gradient(135deg, #19c928 0%, #17b724 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.02);
        border: 2px dashed rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(23, 183, 36, 0.4);
        background: rgba(23, 183, 36, 0.05);
    }
    
    /* Data Frames */
    .dataframe {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(23, 183, 36, 0.2);
        transform: translateX(4px);
    }
    
    /* Alerts */
    .stAlert {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        border-left: 4px solid;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    /* Success Alert */
    [data-testid="stNotificationContentSuccess"] {
        border-left-color: #17b724;
        background: linear-gradient(135deg, rgba(23, 183, 36, 0.1) 0%, rgba(23, 183, 36, 0.05) 100%);
    }
    
    /* Error Alert */
    [data-testid="stNotificationContentError"] {
        border-left-color: #ff2a2a;
        background: linear-gradient(135deg, rgba(255, 42, 42, 0.1) 0%, rgba(255, 42, 42, 0.05) 100%);
    }
    
    /* Warning Alert */
    [data-testid="stNotificationContentWarning"] {
        border-left-color: #ffae00;
        background: linear-gradient(135deg, rgba(255, 174, 0, 0.1) 0%, rgba(255, 174, 0, 0.05) 100%);
    }
    
    /* Info Alert */
    [data-testid="stNotificationContentInfo"] {
        border-left-color: #4a9eff;
        background: linear-gradient(135deg, rgba(74, 158, 255, 0.1) 0%, rgba(74, 158, 255, 0.05) 100%);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #a0aec0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a0aec0;
        font-size: 0.85rem;
        font-weight: 500;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: rgba(23, 183, 36, 0.2);
    }
    
    .stSlider > div > div > div > div {
        background: #17b724;
        box-shadow: 0 0 16px rgba(23, 183, 36, 0.5);
    }
    
    /* Radio Buttons */
    .stRadio > label {
        color: #a0aec0;
        font-weight: 500;
    }
    
    .stRadio > div {
        background: rgba(255, 255, 255, 0.02);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    /* Checkboxes */
    .stCheckbox > label {
        color: #a0aec0;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .stCheckbox > label:hover {
        color: #ffffff;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: rgba(23, 183, 36, 0.3);
        background: rgba(255, 255, 255, 0.05);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #17b724 0%, #19c928 100%);
        box-shadow: 0 2px 12px rgba(23, 183, 36, 0.4);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #17b724 !important;
    }
    
    /* Threat Level Badge */
    .threat-badge {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .threat-badge:hover {
        transform: scale(1.05);
    }
    
    .threat-normal {
        background: rgba(23, 183, 36, 0.15);
        color: #17b724;
        border: 1px solid rgba(23, 183, 36, 0.3);
        box-shadow: 0 4px 12px rgba(23, 183, 36, 0.2);
    }
    
    .threat-suspicious {
        background: rgba(255, 174, 0, 0.15);
        color: #ffae00;
        border: 1px solid rgba(255, 174, 0, 0.3);
        box-shadow: 0 4px 12px rgba(255, 174, 0, 0.2);
    }
    
    .threat-malicious {
        background: rgba(255, 42, 42, 0.15);
        color: #ff2a2a;
        border: 1px solid rgba(255, 42, 42, 0.3);
        box-shadow: 0 4px 12px rgba(255, 42, 42, 0.2);
    }
    
    /* Threat Detail Container */
    .threat-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        backdrop-filter: blur(20px);
        border-left: 4px solid;
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .threat-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .threat-container:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .threat-container-normal {
        border-left-color: #17b724;
    }
    
    .threat-container-normal:hover::before {
        background: radial-gradient(circle at left, rgba(23, 183, 36, 0.1), transparent 70%);
        opacity: 1;
    }
    
    .threat-container-suspicious {
        border-left-color: #ffae00;
    }
    
    .threat-container-suspicious:hover::before {
        background: radial-gradient(circle at left, rgba(255, 174, 0, 0.1), transparent 70%);
        opacity: 1;
    }
    
    .threat-container-malicious {
        border-left-color: #ff2a2a;
    }
    
    .threat-container-malicious:hover::before {
        background: radial-gradient(circle at left, rgba(255, 42, 42, 0.1), transparent 70%);
        opacity: 1;
    }
    
    .threat-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    
    .threat-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
    }
    
    .confidence-bar {
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        overflow: hidden;
        margin-top: 0.75rem;
    }
    
    .confidence-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 16px currentColor;
        animation: fillBar 1.5s ease-out;
    }
    
    @keyframes fillBar {
        from { width: 0 !important; }
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.6rem;
        font-weight: 600;
        color: #ffffff;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    /* Feature Card */
    .feature-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at center, rgba(23, 183, 36, 0.1), transparent 70%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        border-color: rgba(23, 183, 36, 0.4);
        box-shadow: 0 12px 40px rgba(23, 183, 36, 0.2);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.25rem;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover .feature-icon {
        transform: scale(1.1) rotate(5deg);
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.75rem;
    }
    
    .feature-description {
        font-size: 0.95rem;
        color: #a0aec0;
        line-height: 1.6;
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 2.5rem 0;
        color: #6b7280;
        font-size: 0.9rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 4rem;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(23, 183, 36, 0.3);
        border-radius: 6px;
        transition: background 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(23, 183, 36, 0.5);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.6;
        }
    }
    
    @keyframes glow {
        0%, 100% {
            box-shadow: 0 0 20px rgba(23, 183, 36, 0.3);
        }
        50% {
            box-shadow: 0 0 30px rgba(23, 183, 36, 0.6);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    .slide-in {
        animation: slideIn 0.6s ease-out;
    }
    
    /* Loading Animation */
    .loading-pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Plotly Chart Containers */
    .js-plotly-plot {
        border-radius: 20px;
        overflow: hidden;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, rgba(74, 158, 255, 0.2) 0%, rgba(74, 158, 255, 0.1) 100%);
        color: #4a9eff;
        border: 1px solid rgba(74, 158, 255, 0.3);
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, rgba(74, 158, 255, 0.3) 0%, rgba(74, 158, 255, 0.2) 100%);
        border-color: rgba(74, 158, 255, 0.5);
        box-shadow: 0 4px 16px rgba(74, 158, 255, 0.3);
        transform: translateY(-2px);
    }
    
    /* Interactive Data Table */
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    
    /* Interactive Filter Panel */
    .filter-panel {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Stat Card with Icon */
    .stat-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.25rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(23, 183, 36, 0.15);
        border-color: rgba(23, 183, 36, 0.2);
    }
    
    /* Number Input */
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        color: #ffffff;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: rgba(23, 183, 36, 0.4);
        box-shadow: 0 0 0 2px rgba(23, 183, 36, 0.1);
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        color: #ffffff;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(23, 183, 36, 0.4);
        box-shadow: 0 0 0 2px rgba(23, 183, 36, 0.1);
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stMultiSelect > div > div:hover {
        border-color: rgba(23, 183, 36, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ========================= 
# Load Artifacts 
# ========================= 
@st.cache_resource
def load_artifacts():
    try:
        fusion = tf.keras.models.load_model("netpulse_fusion_v2.h5")
        with open("scaler3.pkl", "rb") as f:
            scaler3 = pickle.load(f)
        with open("class_map.pkl", "rb") as f:
            class_map = pickle.load(f)
        with open("config.pkl", "rb") as f:
            config = pickle.load(f)
        return fusion, scaler3, class_map, config
    except Exception as e:
        st.error(f"Error loading artifacts: {str(e)}")
        return None, None, None, None

fusion, scaler3, class_map, config = load_artifacts()

if fusion:
    SEQ_LEN = config.get("SEQ_LEN", 50)

# ========================= 
# UI Header 
# ========================= 
# Load and encode logo
import base64
import os

logo_base64 = ""
try:
    if os.path.exists("netpulse_logo.png"):
        with open("netpulse_logo.png", "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
    elif os.path.exists("/mnt/user-data/uploads/netpulse_logo.png"):
        with open("/mnt/user-data/uploads/netpulse_logo.png", "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
except:
    pass

# Display logo centered using pure CSS - NO COLUMNS AT ALL
if logo_base64:
    st.markdown(f"""
    <div style='display: flex; justify-content: center; align-items: center; margin-bottom: 1.5rem;'>
        <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
                    backdrop-filter: blur(20px);
                    border: 1px solid rgba(255, 255, 255, 0.15);
                    border-radius: 24px;
                    padding: 2rem 4rem;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    text-align: center;'>
            <img src="data:image/png;base64,{logo_base64}" width="450" style="display: block; margin: 0 auto;"/>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('''
<div class="main-header fade-in">
    <div class="header-title">NET PULSE</div>
    <div class="header-subtitle">Advanced Network Intrusion Detection System • AI-Powered Security Platform</div>
</div>
''', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Logo/Icon section with background
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 16px;
                padding: 1rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
                text-align: center;'>
    """, unsafe_allow_html=True)
    try:
        st.image("netpulse_logo.png", width=180)
    except:
        try:
            st.image("/mnt/user-data/uploads/netpulse_logo.png", width=180)
        except:
            try:
                st.image("/mnt/user-data/uploads/1769091506209_image.png", width=180)
            except:
                st.markdown("""
                <div style='text-align: center; padding: 0.5rem 0;'>
                    <div style='font-size: 2rem;'>🛡️</div>
                    <div style='font-size: 1rem; font-weight: 700; color: #17b724; margin-top: 0.5rem;'>NET PULSE</div>
                </div>
                """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("#### 🎯 Detection Mode")
    detection_mode = st.radio(
        "Select Mode:",
        ["Batch Analysis", "Real-time Monitor", "Threat Hunting"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("#### 🎨 Visualization Options")
    show_sequence_viz = st.checkbox("Packet Sequence Analysis", value=True)
    show_heatmap = st.checkbox("Feature Correlation", value=True)
    show_timeline = st.checkbox("Timeline Analysis", value=True)
    show_3d = st.checkbox("3D Pattern Analysis", value=False)
    
    st.markdown("---")
    
    st.markdown("#### ⚡ Alert Settings")
    alert_threshold = st.slider(
        "Sensitivity Level", 
        0.0, 1.0, 0.7, 0.05,
        help="Lower values = more sensitive detection"
    )
    
    auto_export = st.checkbox("Auto-export Reports", value=False)
    
    st.markdown("---")
    
    # Model Info Card
    st.markdown("""
    <div style='background: rgba(255, 255, 255, 0.03); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08);'>
        <div style='font-size: 0.85rem; color: #a0aec0; margin-bottom: 0.5rem;'>MODEL INFO</div>
        <div style='font-weight: 600; color: #ffffff; margin-bottom: 0.25rem;'>Fusion CNN-LSTM</div>
        <div style='font-size: 0.85rem; color: #a0aec0;'>Dataset: UNSW-NB15</div>
        <div style='font-size: 0.85rem; color: #17b724; font-weight: 600; margin-top: 0.5rem;'>82% Accuracy</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    if 'summary_stats' in st.session_state:
        st.markdown("---")
        st.markdown("#### 📊 Session Stats")
        
        stats = st.session_state.summary_stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Flows", f"{stats.get('total_flows', 0):,}")
        with col2:
            st.metric("Threats", stats.get('malicious_count', 0))
        
        # Risk level indicator
        total = stats.get('total_flows', 1)
        malicious = stats.get('malicious_count', 0)
        risk_pct = (malicious / total * 100) if total > 0 else 0
        
        if risk_pct > 5:
            risk_color = "#ff2a2a"
            risk_label = "HIGH RISK"
        elif risk_pct > 1:
            risk_color = "#ffae00"
            risk_label = "MEDIUM"
        else:
            risk_color = "#17b724"
            risk_label = "LOW RISK"
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
                    padding: 0.75rem 1rem; border-radius: 10px; border-left: 3px solid {risk_color};
                    margin-top: 0.5rem;'>
            <div style='font-size: 0.75rem; color: #a0aec0; margin-bottom: 0.25rem;'>RISK LEVEL</div>
            <div style='font-size: 1.1rem; font-weight: 700; color: {risk_color};'>{risk_label}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========================= 
# Flow → Sequence Conversion 
# ========================= 
def flow_to_sequence(row):
    spkts = int(row.get('spkts', row.get('src_pkts', 0)))
    dpkts = int(row.get('dpkts', row.get('dst_pkts', 0)))
    sbytes = float(row.get('sbytes', row.get('src_bytes', 0)))
    dbytes = float(row.get('dbytes', row.get('dst_bytes', 0)))
    dur = float(row.get('dur', row.get('duration', 0.001)) or 0.001)
    
    src_sizes = [sbytes/spkts] * spkts if spkts > 0 else []
    dst_sizes = [dbytes/dpkts] * dpkts if dpkts > 0 else []
    src_times = np.linspace(0, dur, len(src_sizes)) if len(src_sizes) else []
    dst_times = np.linspace(0, dur, len(dst_sizes)) if len(dst_sizes) else []
    src_dir = [+1] * len(src_sizes)
    dst_dir = [-1] * len(dst_sizes)
    
    packets = list(zip(src_times, src_sizes, src_dir)) + \
              list(zip(dst_times, dst_sizes, dst_dir))
    packets.sort(key=lambda x: x[0])
    
    seq = []
    prev_t = 0
    for t, size, d in packets:
        gap = t - prev_t
        prev_t = t
        seq.append([size, gap, d])
    
    if len(seq) < SEQ_LEN:
        seq += [[0, 0, 0]] * (SEQ_LEN - len(seq))
    else:
        seq = seq[:SEQ_LEN]
    
    return np.array(seq)

# ========================= 
# Enhanced Visualization Functions 
# ========================= 
def create_pie_chart(pred_counts):
    pred_counts = pred_counts.reindex(["Normal", "Suspicious", "Malicious"]).dropna()
    
    fig = px.pie(
        values=pred_counts.values,
        names=pred_counts.index,
        title="<b>Threat Distribution</b>",
        color=pred_counts.index,
        color_discrete_map=COLOR_MAP,
        hole=0.5
    )
    
    fig.update_traces(
        textposition='outside',
        textinfo='percent+label',
        marker=dict(
            line=dict(color='rgba(0,0,0,0.5)', width=2)
        ),
        pull=[0, 0.05, 0.1],
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        height=450,
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Outfit', size=13, color='#a0aec0'),
        title_font=dict(size=18, color='#ffffff', family='Outfit'),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.1,
            bgcolor='rgba(255,255,255,0.03)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1,
            font=dict(size=12)
        ),
        margin=dict(l=20, r=150, t=60, b=20)
    )
    
    return fig

def create_bar_chart(pred_counts):
    fig = px.bar(
        x=pred_counts.index,
        y=pred_counts.values,
        title="<b>Threat Count by Category</b>",
        color=pred_counts.index,
        color_discrete_map=COLOR_MAP,
        labels={'x': 'Threat Category', 'y': 'Count'},
        text=pred_counts.values
    )
    
    fig.update_traces(
        marker=dict(
            line=dict(color='rgba(0,0,0,0.5)', width=1.5),
            pattern_shape="/"
        ),
        texttemplate='<b>%{text}</b>',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Count: %{y}<br><extra></extra>'
    )
    
    fig.update_layout(
        height=450,
        showlegend=False,
        xaxis_title="<b>Threat Category</b>",
        yaxis_title="<b>Count</b>",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Outfit', color='#a0aec0', size=12),
        title_font=dict(size=18, color='#ffffff', family='Outfit'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            showline=True,
            linecolor='rgba(255,255,255,0.1)',
            linewidth=2,
            tickfont=dict(size=13, color='#ffffff')
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            showline=True,
            linecolor='rgba(255,255,255,0.1)',
            linewidth=2,
            tickfont=dict(size=12)
        ),
        margin=dict(l=60, r=40, t=60, b=60)
    )
    
    return fig

def create_threat_timeline(df):
    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'])
        timeline_df = df.groupby([df['time'].dt.floor('H'), 'prediction_label']).size().reset_index(name='count')
        
        fig = px.line(
            timeline_df,
            x='time',
            y='count',
            color='prediction_label',
            title="<b>Threat Activity Timeline</b>",
            color_discrete_map=COLOR_MAP,
            markers=True
        )
        
        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=10, line=dict(width=2, color='rgba(0,0,0,0.5)')),
            hovertemplate='<b>%{fullData.name}</b><br>Time: %{x}<br>Count: %{y}<extra></extra>'
        )
        
        fig.update_layout(
            height=450,
            xaxis_title="<b>Time</b>",
            yaxis_title="<b>Threat Count</b>",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Outfit', color='#a0aec0', size=12),
            title_font=dict(size=18, color='#ffffff', family='Outfit'),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                showline=True,
                linecolor='rgba(255,255,255,0.1)',
                linewidth=2,
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                showline=True,
                linecolor='rgba(255,255,255,0.1)',
                linewidth=2,
                tickfont=dict(size=12)
            ),
            legend=dict(
                bgcolor='rgba(255,255,255,0.03)',
                bordercolor='rgba(255,255,255,0.1)',
                borderwidth=1,
                font=dict(size=12)
            ),
            hovermode='x unified',
            margin=dict(l=60, r=40, t=60, b=60)
        )
        
        return fig
    return None

def create_heatmap(df):
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numerical_cols) > 1:
        corr_matrix = df[numerical_cols[:10]].corr()
        
        fig = px.imshow(
            corr_matrix,
            title="<b>Feature Correlation Heatmap</b>",
            color_continuous_scale='RdBu_r',
            aspect='auto',
            zmin=-1,
            zmax=1,
            text_auto='.2f'
        )
        
        fig.update_traces(
            hovertemplate='<b>%{x}</b> × <b>%{y}</b><br>Correlation: %{z:.3f}<extra></extra>'
        )
        
        fig.update_layout(
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Outfit', color='#a0aec0', size=11),
            title_font=dict(size=18, color='#ffffff', family='Outfit'),
            xaxis=dict(tickfont=dict(size=11)),
            yaxis=dict(tickfont=dict(size=11)),
            margin=dict(l=100, r=40, t=60, b=100)
        )
        
        return fig
    return None

def create_packet_sequence_viz(sequence):
    seq_array = np.array(sequence)
    
    fig = go.Figure()
    
    # Packet Size Bars with gradient
    fig.add_trace(go.Bar(
        x=list(range(len(seq_array))),
        y=seq_array[:, 0],
        name='Packet Size',
        marker=dict(
            color=seq_array[:, 0],
            colorscale='Viridis',
            line=dict(color='rgba(0,0,0,0.3)', width=1)
        ),
        opacity=0.9,
        hovertemplate='<b>Packet %{x}</b><br>Size: %{y:.2f} bytes<extra></extra>'
    ))
    
    # Time Gap Line
    fig.add_trace(go.Scatter(
        x=list(range(len(seq_array))),
        y=seq_array[:, 1] * 100,
        name='Time Gap (scaled)',
        yaxis='y2',
        line=dict(color='#ff2a2a', width=4, shape='spline'),
        mode='lines+markers',
        marker=dict(size=8, line=dict(width=2, color='rgba(255,255,255,0.5)')),
        fill='tozeroy',
        fillcolor='rgba(255, 42, 42, 0.1)',
        hovertemplate='<b>Packet %{x}</b><br>Time Gap: %{y:.2f} ms<extra></extra>'
    ))
    
    fig.update_layout(
        title="<b>Packet Sequence Analysis</b>",
        height=450,
        xaxis_title="<b>Packet Number</b>",
        yaxis_title="<b>Packet Size (bytes)</b>",
        yaxis2=dict(
            title="<b>Time Gap (ms)</b>",
            overlaying='y',
            side='right',
            gridcolor='rgba(255,255,255,0.05)',
            tickfont=dict(size=12, color='#ff2a2a')
        ),
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Outfit', color='#a0aec0', size=12),
        title_font=dict(size=18, color='#ffffff', family='Outfit'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            showline=True,
            linecolor='rgba(255,255,255,0.1)',
            linewidth=2,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            showline=True,
            linecolor='rgba(255,255,255,0.1)',
            linewidth=2,
            tickfont=dict(size=12, color='#17b724')
        ),
        legend=dict(
            bgcolor='rgba(255,255,255,0.03)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1,
            font=dict(size=12),
            x=0.02,
            y=0.98
        ),
        hovermode='x unified',
        margin=dict(l=60, r=80, t=60, b=60)
    )
    
    return fig

def create_threat_radar(df):
    threat_stats = df.groupby('prediction_label').agg({
        'spkts': 'mean',
        'dpkts': 'mean',
        'sbytes': 'mean',
        'dbytes': 'mean',
        'dur': 'mean'
    }).reset_index()
    
    categories = ['Source Pkts', 'Dest Pkts', 'Source Bytes', 'Dest Bytes', 'Duration']
    original_categories = ['spkts', 'dpkts', 'sbytes', 'dbytes', 'dur']
    
    fig = go.Figure()
    
    for threat in threat_stats['prediction_label'].unique():
        values = threat_stats[threat_stats['prediction_label'] == threat][original_categories].values[0]
        values = values / np.max(values) * 100 if np.max(values) > 0 else values
        
        color = COLOR_MAP.get(threat, '#ffffff')
        
        fig.add_trace(go.Scatterpolar(
            r=values.tolist() + [values[0]],
            theta=categories + [categories[0]],
            name=threat,
            fill='toself',
            line=dict(color=color, width=3),
            marker=dict(size=10, line=dict(width=2, color='rgba(255,255,255,0.3)')),
            hovertemplate='<b>%{fullData.name}</b><br>%{theta}: %{r:.1f}<extra></extra>'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(color='#a0aec0', size=11),
                linecolor='rgba(255,255,255,0.1)'
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(color='#ffffff', size=12),
                linecolor='rgba(255,255,255,0.1)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        title="<b>Threat Characteristics Radar</b>",
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Outfit', color='#a0aec0', size=12),
        title_font=dict(size=18, color='#ffffff', family='Outfit'),
        legend=dict(
            bgcolor='rgba(255,255,255,0.03)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1,
            font=dict(size=12)
        ),
        margin=dict(l=80, r=80, t=80, b=80)
    )
    
    return fig

def create_3d_scatter(df):
    if 'spkts' in df.columns and 'dpkts' in df.columns and 'sbytes' in df.columns:
        sample_df = df.head(200)
        
        fig = px.scatter_3d(
            sample_df,
            x='spkts',
            y='dpkts',
            z='sbytes',
            color='prediction_label',
            title="<b>3D Traffic Pattern Analysis</b>",
            color_discrete_map=COLOR_MAP,
            opacity=0.8,
            size_max=10,
            hover_data=['confidence']
        )
        
        fig.update_traces(
            marker=dict(
                size=6,
                line=dict(width=0.8, color='rgba(0,0,0,0.5)')
            ),
            hovertemplate='<b>%{fullData.name}</b><br>Src Pkts: %{x}<br>Dst Pkts: %{y}<br>Src Bytes: %{z}<br>Confidence: %{customdata[0]:.2%}<extra></extra>'
        )
        
        fig.update_layout(
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Outfit', color='#a0aec0', size=12),
            title_font=dict(size=18, color='#ffffff', family='Outfit'),
            scene=dict(
                bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='rgba(255,255,255,0.1)',
                    title=dict(text='<b>Source Packets</b>', font=dict(size=13, color='#ffffff')),
                    tickfont=dict(size=11, color='#a0aec0')
                ),
                yaxis=dict(
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='rgba(255,255,255,0.1)',
                    title=dict(text='<b>Dest Packets</b>', font=dict(size=13, color='#ffffff')),
                    tickfont=dict(size=11, color='#a0aec0')
                ),
                zaxis=dict(
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='rgba(255,255,255,0.1)',
                    title=dict(text='<b>Source Bytes</b>', font=dict(size=13, color='#ffffff')),
                    tickfont=dict(size=11, color='#a0aec0')
                )
            ),
            legend=dict(
                bgcolor='rgba(255,255,255,0.03)',
                bordercolor='rgba(255,255,255,0.1)',
                borderwidth=1,
                font=dict(size=12)
            ),
            margin=dict(l=0, r=0, t=60, b=0)
        )
        
        return fig
    return None

# ========================= 
# Main Content 
# ========================= 
uploaded = st.file_uploader("", type=["csv"], help="Upload your network traffic data in CSV format")

if uploaded:
    df = pd.read_csv(uploaded)
    st.session_state.original_df = df.copy()
    
    # File info cards
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 0.85rem; color: #a0aec0; margin-bottom: 0.5rem;'>TOTAL FLOWS</div>
            <div style='font-size: 2rem; font-weight: 700; color: #ffffff;'>{:,}</div>
        </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 0.85rem; color: #a0aec0; margin-bottom: 0.5rem;'>FEATURES</div>
            <div style='font-size: 2rem; font-weight: 700; color: #ffffff;'>{}</div>
        </div>
        """.format(len(df.columns)), unsafe_allow_html=True)
    
    with col3:
        time_range = "N/A" if 'time' not in df.columns else "Available"
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 0.85rem; color: #a0aec0; margin-bottom: 0.5rem;'>TIME DATA</div>
            <div style='font-size: 1.5rem; font-weight: 700; color: #ffffff;'>{}</div>
        </div>
        """.format(time_range), unsafe_allow_html=True)
    
    with col4:
        memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 0.85rem; color: #a0aec0; margin-bottom: 0.5rem;'>MEMORY</div>
            <div style='font-size: 1.5rem; font-weight: 700; color: #ffffff;'>{:.1f} MB</div>
        </div>
        """.format(memory_mb), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.success(f"✅ File loaded successfully: **{uploaded.name}**")
    
    # Processing
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner("🔍 Analyzing network traffic..."):
        status_text.text("🔄 Preprocessing data...")
        progress_bar.progress(20)
        
        flows = df.copy()
        
        # Encode categorical columns
        cat_cols = ['proto', 'service', 'state']
        for col in cat_cols:
            if col in flows.columns:
                le = LabelEncoder()
                flows[col] = le.fit_transform(flows[col].astype(str))
        
        status_text.text("🔄 Removing unnecessary columns...")
        progress_bar.progress(40)
        
        drop_cols = ['id', 'attack_cat', 'label', 'class3']
        flows = flows.drop(columns=drop_cols, errors='ignore')
        
        if scaler3 and hasattr(scaler3, 'feature_names_in_'):
            expected_features = scaler3.feature_names_in_
            flows = flows.reindex(columns=expected_features)
        
        status_text.text("🔄 Building packet sequences...")
        progress_bar.progress(60)
        
        sequences = np.array([flow_to_sequence(r) for _, r in df.iterrows()])
        
        status_text.text("🔄 Scaling features...")
        progress_bar.progress(70)
        
        if scaler3:
            flows_scaled = scaler3.transform(flows)
        
        status_text.text("🤖 Running AI prediction...")
        progress_bar.progress(80)
        
        if fusion:
            preds = fusion.predict([flows_scaled, sequences], verbose=0)
            confidence_scores = np.max(preds, axis=1)
            pred_classes = preds.argmax(axis=1)
            
            df['prediction'] = pred_classes
            df['prediction_label'] = df['prediction'].map(class_map)
            df['confidence'] = confidence_scores
            df['threat_score'] = df['prediction'].apply(lambda x: 0 if x == 0 else 0.5 if x == 1 else 1.0)
            
            status_text.text("✅ Analysis complete!")
            progress_bar.progress(100)
            
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
            
            pred_counts = df['prediction_label'].value_counts()
            st.session_state.summary_stats = {
                'total_flows': len(df),
                'malicious_count': pred_counts.get('Malicious', 0),
                'suspicious_count': pred_counts.get('Suspicious', 0),
                'normal_count': pred_counts.get('Normal', 0),
                'avg_confidence': df['confidence'].mean()
            }
            
            # Success message with stats
            malicious_count = pred_counts.get('Malicious', 0)
            suspicious_count = pred_counts.get('Suspicious', 0)
            
            if malicious_count > 0:
                st.error(f"🚨 **ALERT:** Found **{malicious_count}** malicious and **{suspicious_count}** suspicious flows")
            elif suspicious_count > 0:
                st.warning(f"⚠️ **WARNING:** Found **{suspicious_count}** suspicious flows")
            else:
                st.success(f"✅ **ALL CLEAR:** No threats detected in {len(df):,} analyzed flows")
            
            # ========================= 
            # Tabs for different views 
            # ========================= 
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Overview Dashboard",
                "🔍 Detailed Analysis",
                "📈 Visualizations",
                "🚨 Threat Details",
                "📋 Raw Data"
            ])
            
            with tab1:
                st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                
                # KPI Cards
                col1, col2, col3, col4 = st.columns(4)
                
                total_threats = pred_counts.get('Malicious', 0) + pred_counts.get('Suspicious', 0)
                threat_severity = (pred_counts.get('Malicious', 0) / len(df) * 100) if len(df) > 0 else 0
                avg_confidence = df['confidence'].mean() * 100
                
                if pred_counts.get('Malicious', 0) > 0:
                    risk_level = "HIGH"
                    risk_color = "#ff2a2a"
                elif pred_counts.get('Suspicious', 0) > 0:
                    risk_level = "MEDIUM"
                    risk_color = "#ffae00"
                else:
                    risk_level = "LOW"
                    risk_color = "#17b724"
                
                with col1:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div style='font-size: 0.85rem; color: #a0aec0; margin-bottom: 0.5rem;'>TOTAL THREATS</div>
                        <div style='font-size: 2.5rem; font-weight: 700; color: #ff2a2a;'>{total_threats}</div>
                        <div style='font-size: 0.75rem; color: #a0aec0; margin-top: 0.5rem;'>Malicious + Suspicious</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div style='font-size: 0.85rem; color: #a0aec0; margin-bottom: 0.5rem;'>THREAT SEVERITY</div>
                        <div style='font-size: 2.5rem; font-weight: 700; color: #ff2a2a;'>{threat_severity:.1f}%</div>
                        <div style='font-size: 0.75rem; color: #a0aec0; margin-top: 0.5rem;'>of total traffic</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div style='font-size: 0.85rem; color: #a0aec0; margin-bottom: 0.5rem;'>AVG CONFIDENCE</div>
                        <div style='font-size: 2.5rem; font-weight: 700; color: #17b724;'>{avg_confidence:.1f}%</div>
                        <div style='font-size: 0.75rem; color: #a0aec0; margin-top: 0.5rem;'>detection accuracy</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div style='font-size: 0.85rem; color: #a0aec0; margin-bottom: 0.5rem;'>RISK LEVEL</div>
                        <div style='font-size: 2.5rem; font-weight: 700; color: {risk_color};'>{risk_level}</div>
                        <div style='font-size: 0.75rem; color: #a0aec0; margin-top: 0.5rem;'>security status</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Main charts in containers
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    fig_pie = create_pie_chart(pred_counts)
                    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    fig_bar = create_bar_chart(pred_counts)
                    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Timeline
                if 'time' in df.columns and show_timeline:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    fig_timeline = create_threat_timeline(df)
                    if fig_timeline:
                        st.plotly_chart(fig_timeline, use_container_width=True, config={'displayModeBar': False})
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'proto' in df.columns:
                        proto_counts = df['proto'].value_counts().head(10)
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        fig_proto = px.bar(
                            x=proto_counts.index,
                            y=proto_counts.values,
                            title="<b>Top Protocols</b>",
                            color=proto_counts.values,
                            color_continuous_scale='Viridis',
                            labels={'x': 'Protocol', 'y': 'Count'},
                            text=proto_counts.values
                        )
                        fig_proto.update_traces(
                            texttemplate='%{text}',
                            textposition='outside',
                            hovertemplate='<b>Protocol %{x}</b><br>Count: %{y}<extra></extra>'
                        )
                        fig_proto.update_layout(
                            height=450,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(family='Outfit', color='#a0aec0', size=12),
                            title_font=dict(size=18, color='#ffffff', family='Outfit'),
                            xaxis=dict(
                                gridcolor='rgba(255,255,255,0.05)',
                                tickfont=dict(size=12)
                            ),
                            yaxis=dict(
                                gridcolor='rgba(255,255,255,0.05)',
                                tickfont=dict(size=12)
                            ),
                            margin=dict(l=60, r=40, t=60, b=60)
                        )
                        st.plotly_chart(fig_proto, use_container_width=True, config={'displayModeBar': False})
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    fig_conf = px.histogram(
                        df,
                        x='confidence',
                        color='prediction_label',
                        title="<b>Confidence Score Distribution</b>",
                        color_discrete_map=COLOR_MAP,
                        nbins=30,
                        marginal="box"
                    )
                    fig_conf.update_traces(
                        hovertemplate='Confidence: %{x:.2%}<br>Count: %{y}<extra></extra>'
                    )
                    fig_conf.update_layout(
                        height=450,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='Outfit', color='#a0aec0', size=12),
                        title_font=dict(size=18, color='#ffffff', family='Outfit'),
                        xaxis=dict(
                            gridcolor='rgba(255,255,255,0.05)',
                            tickfont=dict(size=12),
                            title='<b>Confidence Score</b>'
                        ),
                        yaxis=dict(
                            gridcolor='rgba(255,255,255,0.05)',
                            tickfont=dict(size=12),
                            title='<b>Count</b>'
                        ),
                        legend=dict(
                            bgcolor='rgba(255,255,255,0.03)',
                            bordercolor='rgba(255,255,255,0.1)',
                            borderwidth=1,
                            font=dict(size=12)
                        ),
                        margin=dict(l=60, r=40, t=60, b=60)
                    )
                    st.plotly_chart(fig_conf, use_container_width=True, config={'displayModeBar': False})
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if show_sequence_viz and len(sequences) > 0:
                    st.markdown("---")
                    st.markdown("### 📦 Packet Sequence Analysis")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        seq_idx = st.slider(
                            "Select Flow Index",
                            0,
                            min(100, len(sequences)-1),
                            0
                        )
                    with col2:
                        if seq_idx < len(df):
                            threat_label = df.iloc[seq_idx]['prediction_label']
                            threat_class = threat_label.lower()
                            st.markdown(f"""
                            <div class='threat-badge threat-{threat_class}'>
                                {threat_label}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    fig_seq = create_packet_sequence_viz(sequences[seq_idx])
                    st.plotly_chart(fig_seq, use_container_width=True, config={'displayModeBar': False})
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab3:
                st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    fig_radar = create_threat_radar(df)
                    st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    if show_heatmap:
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        fig_heatmap = create_heatmap(df)
                        if fig_heatmap:
                            st.plotly_chart(fig_heatmap, use_container_width=True, config={'displayModeBar': False})
                        st.markdown('</div>', unsafe_allow_html=True)
                
                if show_3d:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    fig_3d = create_3d_scatter(df)
                    if fig_3d:
                        st.plotly_chart(fig_3d, use_container_width=True, config={'displayModeBar': True})
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab4:
                st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                
                # Filter options
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    threat_filter = st.multiselect(
                        "🎯 Filter by Threat Type:",
                        ["Normal", "Suspicious", "Malicious"],
                        default=["Malicious", "Suspicious"]
                    )
                
                with col2:
                    sort_by = st.selectbox(
                        "📊 Sort by:",
                        ["Confidence (High to Low)", "Confidence (Low to High)", "Threat Score"]
                    )
                
                with col3:
                    max_display = st.number_input(
                        "Show top:",
                        min_value=5,
                        max_value=100,
                        value=20,
                        step=5
                    )
                
                if threat_filter:
                    threat_df = df[df['prediction_label'].isin(threat_filter)]
                    
                    # Sort
                    if "High to Low" in sort_by:
                        threat_df_sorted = threat_df.sort_values('confidence', ascending=False)
                    elif "Low to High" in sort_by:
                        threat_df_sorted = threat_df.sort_values('confidence', ascending=True)
                    else:
                        threat_df_sorted = threat_df.sort_values('threat_score', ascending=False)
                    
                    threat_df_sorted = threat_df_sorted.head(max_display)
                    
                    st.markdown(f"### 🔍 Top {len(threat_df_sorted)} Threats")
                    
                    for idx, row in threat_df_sorted.iterrows():
                        threat_level = row['prediction_label']
                        confidence = row['confidence']
                        threat_class = threat_level.lower()
                        color = COLOR_MAP[threat_level]
                        
                        confidence_pct = confidence * 100
                        
                        st.markdown(f"""
                        <div class='threat-container threat-container-{threat_class}'>
                            <div class='threat-header'>
                                <div>
                                    <span class='threat-badge threat-{threat_class}'>{threat_level}</span>
                                    <span style='color: #a0aec0; font-size: 0.85rem; margin-left: 1rem;'>
                                        Flow ID: {idx}
                                    </span>
                                </div>
                                <div style='font-size: 1.2rem; font-weight: 700; color: {color};'>
                                    {confidence_pct:.1f}%
                                </div>
                            </div>
                            <div class='confidence-bar'>
                                <div class='confidence-fill' style='width: {confidence_pct}%; background: {color};'></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("📋 View Details", expanded=False):
                            detail_cols = [c for c in df.columns if c not in ['prediction', 'prediction_label', 'confidence', 'threat_score']]
                            
                            col1, col2, col3 = st.columns(3)
                            
                            for i, col in enumerate(detail_cols[:9]):
                                with [col1, col2, col3][i % 3]:
                                    st.metric(col, f"{row[col]}")
                    
                    # Export
                    st.markdown("---")
                    csv = threat_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Threat Report (CSV)",
                        data=csv,
                        file_name=f"threat_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                else:
                    st.info("👆 Please select at least one threat type to display")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab5:
                st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                
                # Filter options
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    filter_threat = st.multiselect(
                        "🎯 Filter by Threat Level:",
                        ["Normal", "Suspicious", "Malicious"],
                        default=["Normal", "Suspicious", "Malicious"]
                    )
                
                with col2:
                    min_confidence = st.slider(
                        "🎚️ Minimum Confidence:",
                        0.0, 1.0, 0.0, 0.05
                    )
                
                with col3:
                    search_term = st.text_input("🔍 Search in data:", "")
                
                # Apply filters
                filtered_df = df[
                    (df['prediction_label'].isin(filter_threat)) &
                    (df['confidence'] >= min_confidence)
                ]
                
                if search_term:
                    filtered_df = filtered_df[
                        filtered_df.astype(str).apply(
                            lambda row: row.str.contains(search_term, case=False).any(),
                            axis=1
                        )
                    ]
                
                st.markdown(f"**Showing {len(filtered_df):,} of {len(df):,} flows**")
                
                # Display data
                st.dataframe(
                    filtered_df,
                    height=500,
                    use_container_width=True
                )
                
                # Pagination
                TOTAL = len(df)
                PAGE_SIZE = 250
                pages = max(1, TOTAL // PAGE_SIZE)
                
                col1, col2 = st.columns(2)
                with col1:
                    page = st.number_input(
                        "📄 Page",
                        min_value=1,
                        max_value=pages,
                        value=1
                    )
                with col2:
                    st.metric("Total Pages", pages)
                
                start = (page-1)*PAGE_SIZE
                end = start + PAGE_SIZE
                df_page = df.iloc[start:end]
                
                st.dataframe(df_page, use_container_width=True)
                
                # Export
                st.markdown("---")
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download Full Results (CSV)",
                    csv,
                    file_name=f"netpulse_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # ========================= 
            # Alert System 
            # ========================= 
            st.markdown("---")
            
            if pred_counts.get('Malicious', 0) > 0:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(255, 42, 42, 0.2) 0%, rgba(255, 42, 42, 0.1) 100%);
                            backdrop-filter: blur(20px);
                            border: 1px solid rgba(255, 42, 42, 0.3);
                            border-radius: 16px;
                            padding: 1.5rem;
                            margin: 1rem 0;'>
                    <div style='font-size: 1.5rem; font-weight: 700; color: #ff2a2a; margin-bottom: 0.5rem;'>
                        🚨 CRITICAL ALERT
                    </div>
                    <div style='color: #ffffff; font-size: 1.1rem;'>
                        {pred_counts.get('Malicious', 0)} malicious flows detected in your network traffic
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("🛡️ Recommended Actions", expanded=True):
                    st.markdown("""
                    <div style='line-height: 1.8;'>
                        <p style='color: #ffffff; font-weight: 600; margin-bottom: 1rem;'>Immediate Response Required:</p>
                        <ol style='color: #a0aec0;'>
                            <li><strong style='color: #ffffff;'>Immediate Isolation:</strong> Block source IPs of malicious flows</li>
                            <li><strong style='color: #ffffff;'>Forensic Analysis:</strong> Capture packet data for investigation</li>
                            <li><strong style='color: #ffffff;'>Alert Escalation:</strong> Notify security team immediately</li>
                            <li><strong style='color: #ffffff;'>Rule Update:</strong> Add new patterns to firewall rules</li>
                            <li><strong style='color: #ffffff;'>Network Monitoring:</strong> Increase monitoring frequency</li>
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)
            
            elif pred_counts.get('Suspicious', 0) > 0:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(255, 174, 0, 0.2) 0%, rgba(255, 174, 0, 0.1) 100%);
                            backdrop-filter: blur(20px);
                            border: 1px solid rgba(255, 174, 0, 0.3);
                            border-radius: 16px;
                            padding: 1.5rem;
                            margin: 1rem 0;'>
                    <div style='font-size: 1.5rem; font-weight: 700; color: #ffae00; margin-bottom: 0.5rem;'>
                        ⚠️ WARNING
                    </div>
                    <div style='color: #ffffff; font-size: 1.1rem;'>
                        {pred_counts.get('Suspicious', 0)} suspicious flows detected - investigation recommended
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("🔍 Investigation Suggestions"):
                    st.markdown("""
                    <div style='line-height: 1.8;'>
                        <ol style='color: #a0aec0;'>
                            <li><strong style='color: #ffffff;'>Monitor:</strong> Increase monitoring for affected IPs</li>
                            <li><strong style='color: #ffffff;'>Log Review:</strong> Check system logs for anomalies</li>
                            <li><strong style='color: #ffffff;'>Traffic Analysis:</strong> Deep packet inspection recommended</li>
                            <li><strong style='color: #ffffff;'>Pattern Analysis:</strong> Look for similar traffic patterns</li>
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)
            
            else:
                st.markdown("""
                <div style='background: linear-gradient(135deg, rgba(23, 183, 36, 0.2) 0%, rgba(23, 183, 36, 0.1) 100%);
                            backdrop-filter: blur(20px);
                            border: 1px solid rgba(23, 183, 36, 0.3);
                            border-radius: 16px;
                            padding: 1.5rem;
                            margin: 1rem 0;'>
                    <div style='font-size: 1.5rem; font-weight: 700; color: #17b724; margin-bottom: 0.5rem;'>
                        ✅ ALL CLEAR
                    </div>
                    <div style='color: #ffffff; font-size: 1.1rem;'>
                        No threats detected in analyzed traffic - network appears secure
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.error("❌ Model not loaded properly. Please check your model file.")

else:
    # Welcome screen
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Load and encode logo for welcome screen
    welcome_logo_base64 = ""
    try:
        if os.path.exists("netpulse_logo.png"):
            with open("netpulse_logo.png", "rb") as f:
                welcome_logo_base64 = base64.b64encode(f.read()).decode()
        elif os.path.exists("/mnt/user-data/uploads/netpulse_logo.png"):
            with open("/mnt/user-data/uploads/netpulse_logo.png", "rb") as f:
                welcome_logo_base64 = base64.b64encode(f.read()).decode()
    except:
        pass
    
    # Display logo centered - NO COLUMNS
    if welcome_logo_base64:
        st.markdown(f"""
        <div style='display: flex; justify-content: center; align-items: center; margin: 2rem 0 1.5rem 0;'>
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
                        backdrop-filter: blur(20px);
                        border: 1px solid rgba(255, 255, 255, 0.15);
                        border-radius: 24px;
                        padding: 2.5rem 4rem;
                        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                        text-align: center;'>
                <img src="data:image/png;base64,{welcome_logo_base64}" width="400" style="display: block; margin: 0 auto;"/>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 3rem 0;'>
        <div style='font-size: 2rem; font-weight: 600; color: #ffffff; margin-bottom: 0.75rem;'>
            Welcome to NET PULSE
        </div>
        <div style='font-size: 1.1rem; color: #a0aec0; line-height: 1.6;'>
            Upload your network traffic data to begin AI-powered threat analysis
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📊</div>
            <div class='feature-title'>Dashboard Includes</div>
            <div class='feature-description'>
                • Threat Distribution Charts<br>
                • Timeline Analysis<br>
                • Confidence Scores<br>
                • Exportable Reports
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🎯</div>
            <div class='feature-title'>Supported Formats</div>
            <div class='feature-description'>
                • CSV files (UNSW-NB15)<br>
                • Network Flow Data<br>
                • PCAP (coming soon)<br>
                • NetFlow (coming soon)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🔍</div>
            <div class='feature-title'>Detection Capabilities</div>
            <div class='feature-description'>
                • DDoS Attacks<br>
                • Port Scanning<br>
                • Data Exfiltration<br>
                • Malware Traffic
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>⚡</div>
            <div class='feature-title'>Performance</div>
            <div class='feature-description'>
                • Real-time Analysis<br>
                • Batch Processing<br>
                • Low Latency<br>
                • Scalable Architecture
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature highlights
    st.markdown("### 🌟 Key Features")
    
    feat_cols = st.columns(4)
    
    with feat_cols[0]:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🧠</div>
            <div class='feature-title'>AI-Powered</div>
            <div class='feature-description'>Fusion CNN-LSTM model for accurate detection</div>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_cols[1]:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📈</div>
            <div class='feature-title'>Real-time</div>
            <div class='feature-description'>Live monitoring capability with instant alerts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_cols[2]:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🎯</div>
            <div class='feature-title'>Accurate</div>
            <div class='feature-description'>82%+ detection accuracy on UNSW-NB15</div>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_cols[3]:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📊</div>
            <div class='feature-title'>Visual</div>
            <div class='feature-description'>Interactive dashboards and comprehensive reports</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='custom-footer'>
    <div style='font-size: 1.1rem; font-weight: 600; color: #ffffff; margin-bottom: 0.75rem;'>
        NET PULSE AI Security Platform
    </div>
    <div style='font-size: 0.95rem;'>
        Version 2.0 | Built with TensorFlow & Streamlit | Powered by UNSW-NB15 Dataset
    </div>
    <div style='margin-top: 0.75rem; font-size: 0.85rem;'>
        © 2026 NET PULSE | All Rights Reserved
    </div>
</div>
""", unsafe_allow_html=True)