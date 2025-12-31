# Neuro-Kinematic Rehab Coach
A Camera-Free, Closed-Loop Motor and Speech Rehabilitation System for MCA Stroke Recovery

---

## Overview
The Neuro-Kinematic Rehab Coach is an intelligent, wearable, camera-free rehabilitation system designed for Middle Cerebral Artery (MCA) stroke patients. It functions as a digital physiotherapist, providing real-time movement and speech correction using wearable sensors, haptic feedback, and adaptive control logic.

Unlike conventional rehabilitation systems that rely on cameras and delayed visual feedback, this project implements a true closed-loop control architecture that actively guides, corrects, and adapts therapy in real time. The system is optimized for unsupervised home-based rehabilitation, prioritizing safety, privacy, and clinical relevance.

---

## Problems Addressed
MCA stroke patients commonly experience:
- Upper-limb motor impairment
- Loss of proprioception
- Trunk compensation and shoulder hiking
- Abnormal movement synergies
- Rapid neuromuscular fatigue
- Dysarthria and impaired speech–breathing coordination

Most existing rehabilitation systems are passive, camera-dependent, and screen-centric, making them poorly suited for neurological motor relearning.

---

## System Philosophy
The system follows a control-systems-driven rehabilitation loop:

Sense → Analyze → Correct → Adapt → Learn

This approach enables continuous motor and speech quality improvement rather than simple activity tracking.

---

## Hardware Architecture

### Wearable IMU Configuration (5 IMUs)

| Location | Function |
|--------|---------|
| Torso (sternum) | Posture, trunk compensation, breathing motion |
| Affected upper arm | Shoulder kinematics, abnormal synergy detection |
| Affected wrist | End-effector control, tremor, fatigue |
| Unaffected upper arm | Healthy motion reference |
| Unaffected wrist | Baseline movement template |

This configuration enables relative kinematic analysis, symmetry assessment, and compensation detection.

---

### Haptic Feedback System
Each IMU is paired with a vibration motor to provide localized, real-time corrective feedback.

- Directional vibration indicates specific movement errors
- Silence acts as positive reinforcement
- Eliminates dependence on screens and visual attention

Example mappings:
- Torso vibration: trunk lean
- Upper arm vibration: shoulder hiking
- Wrist vibration: endpoint drift
- Rapid pulses: fatigue warning

---

### Speech Rehabilitation Hardware
- Mouth-mounted microphone: articulation clarity, pitch, speech rate
- Chest-mounted microphone with torso IMU: breath flow, voice onset timing, speech–breath coordination

---

## Motor Rehabilitation Intelligence

### Real-Time Kinematic Analysis
The system continuously computes:
- Joint angles and angular velocity
- Movement smoothness (jerk)
- Symmetry between affected and unaffected limbs
- Arm-to-torso motion ratio
- Tremor and micro-vibration patterns

---

### Compensation Awareness Module
Explicit detection of:
- Trunk compensation
- Shoulder hiking
- Abnormal joint coupling

This prevents false progress and enforces neurologically correct movement patterns.

---

### Motor Quality Score (MQS)
Each repetition and session is assigned a Motor Quality Score (0–100) computed from:
- Smoothness
- Symmetry
- Compensation magnitude
- Fatigue trend

MQS emphasizes movement quality rather than task completion.

---

## Fatigue Detection and Safety
Fatigue is inferred from:
- IMU micro-vibrations
- Declining movement smoothness
- Increasing compensation frequency

A Predictive Fatigue Risk Index enables:
- Pre-emptive rest prompts
- Automatic session tapering
- Injury and overuse prevention

---

## Closed-Loop Haptic Guidance
The system provides real-time, error-specific haptic feedback during movement execution, enabling immediate motor correction and reinforcing proper neural pathways.

---

## Adaptive Therapy Engine
Therapy parameters are dynamically adjusted, including:
- Range of motion
- Movement speed
- Hold duration
- Repetition count
- Session length and sequencing

Progression is performance-driven rather than time-based.

---

## Abnormal Synergy Detection
Classic MCA stroke movement synergies (e.g., shoulder abduction with elbow flexion coupling) are detected in real time. When identified:
- Task difficulty is reduced
- Feedback intensity is increased
- Progression is temporarily paused

---

## Speech Rehabilitation Module

### Speech Feature Extraction
- Pitch
- Intensity
- Speech rate
- Pause duration
- Voice onset time
- Spectral stability

---

### Breathing–Speech Coordination
Using torso IMU and chest microphone data, the system analyzes:
- Inhale–phonation timing
- Speech per breath cycle
- Vocal endurance

---

### Speech Motor Quality Score (SMQS)
Speech performance is quantified using a Speech Motor Quality Score based on:
- Articulation clarity
- Rhythm and timing
- Breath coordination
- Fatigue resistance

---

## Clinical Intelligence Layer
- Metrics mapped to standard clinical assessment principles
- Replay and explain mode for therapist review
- Dominant vs non-dominant hand–aware thresholds and progression logic

This ensures clinical interpretability and trust.

---

## System Architecture Summary
Wearable IMUs and microphones feed into multimodal analysis pipelines for compensation detection, fatigue prediction, and quality scoring. These outputs drive an adaptive control engine and a haptic feedback system, forming a continuous closed-loop rehabilitation cycle.

---

## Project Outcomes
- Real-time motor and speech correction
- Objective, quantitative quality metrics
- Fatigue-aware and safety-aware therapy
- Privacy-preserving, camera-free operation
- MCA-specific clinical relevance

---

## Final Positioning
The Neuro-Kinematic Rehab Coach is a multimodal, closed-loop neuro-rehabilitation platform that embeds therapist reasoning into wearable hardware and adaptive intelligence. It is engineered for real-world, unsupervised home rehabilitation with a strong foundation in control systems, biomechanics, and clinical neuro-rehabilitation principles.
