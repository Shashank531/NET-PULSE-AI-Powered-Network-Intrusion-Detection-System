# NET PULSE — AI-Powered Network Intrusion Detection System

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)

[![Streamlit](https://img.shields.io/badge/Streamlit-App-orange)](https://streamlit.io/)

[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

NET PULSE is a deep learning–based Network Intrusion Detection System (NIDS) built using a hybrid CNN–LSTM fusion architecture trained on the UNSW-NB15 dataset.

The system models both statistical flow-level features and temporal packet behavior, and provides an interactive Streamlit dashboard for real-time traffic analysis and threat visualization.

---

## Overview

Traditional intrusion detection systems rely on rule-based signatures that fail against modern and evolving attack patterns. NET PULSE uses deep learning to detect anomalies and malicious traffic by learning patterns directly from network flow data.

The model classifies traffic into:

- Normal  
- Suspicious  
- Malicious  

Overall multi-class accuracy: **~82%**

---

## System Architecture

The model follows a dual-branch fusion design:

Flow Features → Dense Layers  
Packet Sequences → CNN → LSTM  
Fusion Layer → Softmax Output  

This structure allows the system to learn both:

- Statistical traffic patterns  
- Temporal packet-level behavior  

---

## Implementation Details

### 1. Data Preprocessing Pipeline

Before training or inference, the following preprocessing steps are applied:

#### Categorical Encoding
The categorical columns:
- `proto`
- `service`
- `state`

are encoded into numerical format using label encoding.

#### Feature Scaling
All numerical flow-level features are standardized using a pre-trained `StandardScaler`.  
This ensures training and inference distributions remain consistent.

#### Feature Alignment
Incoming CSV data is reindexed to match the exact feature order used during model training to prevent shape mismatches during prediction.

---

### 2. Flow-to-Sequence Engineering

The original dataset provides aggregated flow-level statistics.  
To introduce temporal modeling, synthetic packet sequences are reconstructed.

For each flow:

- Packet counts (`spkts`, `dpkts`) are extracted
- Average packet sizes are estimated from byte counts
- Synthetic timestamps are derived from flow duration
- Direction encoding:
  - 0 → Source to Destination
  - 1 → Destination to Source

This produces a structured packet-level sequence for each flow.

These sequences are padded or truncated to a fixed length before being passed to the neural network.

---

### 3. Fusion CNN–LSTM Model

The model consists of two parallel branches:

#### Flow Branch
- Input: Scaled numerical flow features
- Architecture: Fully connected dense layers
- Purpose: Capture statistical relationships between features

#### Sequence Branch
- Input: Packet-level engineered sequences
- 1D CNN: Extract local packet patterns
- LSTM: Model temporal dependencies across packets
- Purpose: Learn attack behavior progression over time

#### Fusion Layer
Outputs from both branches are concatenated and passed through final dense layers with Softmax activation for multi-class classification.

---

### 4. Inference Pipeline

During prediction:

1. CSV file is uploaded via Streamlit
2. Data is preprocessed
3. Flow features are scaled
4. Packet sequences are generated
5. Both branches receive inputs
6. Model outputs:
   - Predicted class
   - Confidence score
   - Threat probability distribution

---

## Streamlit Dashboard Features

The application provides:

- Batch CSV analysis  
- Real-time monitoring mode  
- Threat scoring and confidence estimation  
- Interactive visualizations:
  - Threat distribution (pie and bar charts)
  - Confidence histogram
  - Timeline analysis
  - Feature correlation heatmap
  - Packet sequence visualization
  - 3D traffic pattern analysis  
- Risk-level summary dashboard  

The interface allows intuitive inspection of network behavior without needing direct code interaction.

---

## Dataset

Dataset: **UNSW-NB15**

- Modern normal and attack traffic
- Includes multiple attack categories
- Contains flow-level statistical features

Preprocessing includes:

- Categorical encoding
- Feature scaling
- Sequence generation from aggregated statistics

The dataset is not included in this repository due to size constraints.

---

## How to Run

Clone the repository:

```
git clone https://github.com/Shashank531/NET-PULSE-AI-Powered-Network-Intrusion-Detection-System.git
cd NET-PULSE-AI-Powered-Network-Intrusion-Detection-System
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the application:

```
streamlit run app.py
```

Upload a network traffic CSV file and begin analysis.

---

## Technologies Used

- Python  
- TensorFlow / Keras  
- Scikit-learn  
- Pandas  
- NumPy  
- Streamlit  
- Plotly  
- Matplotlib  
- Seaborn  

---

## Results

- Multi-class classification (Normal / Suspicious / Malicious)  
- ~82% accuracy on UNSW-NB15  
- Confidence-based threat scoring  
- Dual-branch fusion deep learning model  
- Interactive threat analytics dashboard  

---

## Future Improvements

- Model explainability (SHAP or attention visualization)
- Docker containerization
- Real-time packet capture integration
- CI/CD deployment pipeline
- Online model updating
- Attack-type granular classification

---

## License

This project is licensed under the MIT License.

---

## Author

Shashank Jha  
AI/ML Engineer
