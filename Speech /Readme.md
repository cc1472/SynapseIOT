# Dysarthric Speech Classification Using TORGO Dataset
### MFCC- and Pitch-Based Machine Learning Pipeline

## 1. Purpose
This module implements a classical machine learning pipeline for detecting dysarthric speech using audio recordings from the **TORGO dataset**. 

**Primary Objectives:**
* Extract clinically meaningful acoustic features.
* Train a binary classifier (**Control vs. Dysarthric**).
* Provide an objective speech-quality assessment baseline.
* Serve as the speech-analysis backbone for the **Neuro-Kinematic Rehab Coach**.

> **Note:** This model focuses on **speech motor impairment** (how the sound is produced) rather than linguistic content (what is being said).

---

## 2. Dataset & Labeling
### TORGO Speech Dataset
The TORGO corpus contains recordings from healthy control speakers and speakers with dysarthria (associated with cerebral palsy or ALS).

**Label Mapping:**
* **Control Speech:** Label 0
* **Dysarthric Speech:** Label 1

The system includes both male and female speakers to ensure the classifier generalizes across different vocal characteristics.



---

## 3. Feature Extraction Pipeline
To transform raw audio into a format suitable for Machine Learning, a 30-dimensional feature vector is computed for every sample.

### Acoustic Feature Set
1. **MFCCs (Mel-Frequency Cepstral Coefficients):** * 13 coefficients + Standard Deviations (26 features total).
   * Represents spectral envelope and articulatory consistency.
2. **Pitch (F0):** * Mean + Standard Deviation.
   * Captures monotonicity and voicing control issues.
3. **Energy (RMS):** * Represents speech loudness and respiratory strength.
4. **Duration:** * Captures slowed speech rate and prolonged phonation.



### Preprocessing Steps
* **Resampling:** All audio is normalized to 16 kHz.
* **Trimming:** Silence is removed using an energy-based threshold to ensure the model only analyzes active speech.

---

## 4. Model Architecture
The system utilizes a **Support Vector Machine (SVM)** within a scikit-learn pipeline.

### Why SVM?
SVMs are exceptionally effective for clinical datasets that are small-to-medium in size and contain high-dimensional features.

| Component | Function |
| :--- | :--- |
| **StandardScaler** | Normalizes features to zero mean and unit variance. |
| **SVM Classifier** | Uses an **RBF (Radial Basis Function) Kernel**. |
| **Probability Mapping** | Enabled to provide a "confidence score" for impairment. |



---

## 5. Evaluation & Persistence
* **Split:** 80% Training / 20% Testing (Stratified).
* **Metrics:** Accuracy, Precision, Recall, and F1-score.
* **Persistence:** The trained model is saved as `torgo_speech_classifier.pkl` using `joblib` for real-time deployment.

---

## 6. Integration: Neuro-Kinematic Rehab Coach
In the context of your broader project, this module provides the **Speech Motor Quality Score (SMQS)**.

### System Integration Flow
1. **Audio Input:** Captured via wearable or stationary microphone.
2. **Feature Analysis:** This SVM pipeline classifies the degree of dysarthria.
3. **Multimodal Fusion:** The speech prediction is combined with **IMU-based motor analysis** and breathing signals.
4. **Feedback:** The system provides corrective prompts if speech quality drops due to fatigue.

---

## 7. Limitations & Future Extensions
* **Current:** Binary classification (Yes/No).
* **Future:** Regression modeling for **Severity Scoring** (1–10 scale).
* **Future:** Integration of **Delta/Delta-Delta MFCCs** to capture temporal dynamics.
* **Future:** Fusion with **Torso IMU data** to correlate speech quality with posture.

---

## Bottom Line
This module provides a clean, interpretable, and clinically grounded pipeline. It moves the Rehab Coach from a movement-only system to a **multimodal rehabilitation platform**.
