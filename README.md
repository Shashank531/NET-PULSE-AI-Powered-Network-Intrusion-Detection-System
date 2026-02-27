# NET-PULSE-AI-Powered-Network-Intrusion-Detection-System
Built a Fusion CNN-LSTM model on UNSW-NB15 dataset achieving 82% accuracy. Engineered packet-sequence representation from raw flow data. Developed interactive Streamlit dashboard for real-time threat visualization. Implemented feature scaling, categorical encoding, and sequence modeling pipeline.


NET PULSE — AI-Powered Network Intrusion Detection System

NET PULSE is a deep learning-based Network Intrusion Detection System (NIDS) designed to detect malicious and suspicious network traffic using a hybrid CNN–LSTM architecture.

The system combines engineered flow-level features with packet-sequence modeling and provides an interactive Streamlit dashboard for analysis and visualization.

Overview

Modern network attacks are increasingly complex and difficult to detect using rule-based systems. NET PULSE approaches intrusion detection using deep learning, modeling both statistical flow features and temporal packet behavior.

The system classifies network traffic into three categories:

Normal

Suspicious

Malicious

The model is trained on the UNSW-NB15 dataset and achieves approximately 82% multi-class accuracy.

Model Architecture

The architecture follows a fusion-based design:

Flow Features → Dense Layers
Packet Sequences → CNN → LSTM
Fusion Layer → Softmax Output

Flow Branch

Numerical flow-level features

Scaled using StandardScaler

Passed through fully connected layers

Sequence Branch

Packet-level sequence representation

Engineered using packet size, time gap, and direction

1D CNN for local pattern extraction

LSTM for temporal modeling

Fusion

Outputs from both branches are concatenated and passed to final dense layers for multi-class classification.

This design allows the model to learn both statistical and temporal attack patterns.

Dataset

Dataset: UNSW-NB15

Contains modern normal and attack traffic

Includes flow-level features and attack categories

Preprocessing includes:

Label encoding of categorical features (proto, service, state)

Feature scaling

Custom packet sequence generation

The dataset is not included in this repository due to size constraints.

Key Features

Batch CSV analysis

Real-time monitoring mode

Threat score and confidence scoring

Interactive visualizations:

Threat distribution (pie and bar charts)

Confidence histogram

Timeline analysis

Feature correlation heatmap

Packet sequence visualization

3D traffic pattern analysis

Risk level summary dashboard

Modular model loading system

Project Structure
netpulse-ai-nids/
│
├── app.py
├── requirements.txt
├── README.md
│
├── assets/
│   └── netpulse_logo.png
│
├── models/
│   ├── netpulse_fusion_v2.h5
│   ├── scaler3.pkl
│   ├── class_map.pkl
│   └── config.pkl
│
└── notebooks/
    └── training_pipeline.ipynb
How to Run

Clone the repository

git clone https://github.com/your-username/netpulse-ai-nids.git
cd netpulse-ai-nids

Install dependencies

pip install -r requirements.txt

Run the application

streamlit run app.py

Upload a network traffic CSV file and analyze.

Technologies Used

Python

TensorFlow / Keras

Scikit-learn

Pandas / NumPy

Streamlit

Plotly

Results

Multi-class classification (Normal / Suspicious / Malicious)

~82% accuracy

Confidence-based threat scoring

Clear visual threat breakdown in dashboard

Future Improvements

Model explainability (SHAP or attention visualization)

Online learning for continuous model updates

Docker containerization

Real-time packet capture integration

CI/CD deployment pipeline

Author

Shashank Jha

AI/ML Engineering | Deep Learning | Systems Design
