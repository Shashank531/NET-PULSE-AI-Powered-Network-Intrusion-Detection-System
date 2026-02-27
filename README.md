# NET-PULSE-AI-Powered-Network-Intrusion-Detection-System

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-orange)](https://streamlit.io/)

NET PULSE is a deep learning-based Network Intrusion Detection System (NIDS) built using a hybrid CNN–LSTM fusion architecture trained on the UNSW-NB15 dataset.

The system combines flow-level statistical features with packet-sequence modeling and provides an interactive Streamlit dashboard for traffic analysis and threat visualization.

---

## Overview

Modern network attacks are increasingly sophisticated and difficult to detect using traditional rule-based systems. NET PULSE approaches intrusion detection using deep learning by modeling both statistical behavior and temporal packet patterns.

The model classifies traffic into:

- Normal  
- Suspicious  
- Malicious  

Overall multi-class accuracy: **~82%**

---

## Model Architecture

The architecture follows a fusion-based design:

### Flow Branch
- Numerical flow-level features
- Scaled using StandardScaler
- Processed through fully connected layers

### Sequence Branch
- Packet-level sequence representation
- Engineered using:
  - Packet size
  - Time gap
  - Direction
- 1D CNN for local pattern extraction
- LSTM for temporal modeling

### Fusion
Outputs from both branches are concatenated and passed to final dense layers for multi-class classification.

This design allows the model to learn both statistical and temporal attack behavior.

---

## Dataset

**Dataset:** UNSW-NB15  

- Contains modern normal and attack traffic  
- Includes flow-level features and attack categories  

Preprocessing includes:
- Label encoding of categorical features (`proto`, `service`, `state`)
- Feature scaling
- Custom packet-sequence generation

The dataset is not included in this repository due to size constraints.

---

## Key Features

- Batch CSV analysis  
- Real-time monitoring mode  
- Threat score and confidence scoring  
- Interactive visualizations:
  - Threat distribution (pie and bar charts)
  - Confidence histogram
  - Timeline analysis
  - Feature correlation heatmap
  - Packet sequence visualization
  - 3D traffic pattern analysis
- Risk-level summary dashboard  
- Modular model loading system  

---

## How to Run

Clone the repository:
git clone https://github.com/your-username/netpulse-ai-nids.git
cd netpulse-ai-nids

Install dependencies:
pip install -r requirements.txt

Run the application:
streamlit run app.py



Upload a CSV file containing network traffic data and begin analysis.

---

## Technologies Used

- Python  
- TensorFlow / Keras  
- Scikit-learn  
- Pandas  
- NumPy  
- Streamlit  
- Plotly  

---

## Results

- Multi-class classification (Normal / Suspicious / Malicious)
- ~82% accuracy
- Confidence-based threat scoring
- Interactive threat analytics dashboard

---

## Future Improvements

- Model explainability (SHAP or attention visualization)
- Docker containerization
- Real-time packet capture integration
- CI/CD deployment pipeline
- Online model updating

---

## Author

Shashank Jha  
AI/ML Engineer 
