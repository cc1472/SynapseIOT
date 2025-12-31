# Wokwi ESP32-S3 + MPU6050 Simulation
### Hardware Validation & Diagnostics Prototype

## 1. Overview of This Simulation
This simulation represents a low-level hardware validation and diagnostics prototype built using an **ESP32-S3**, four **MPU6050 IMUs**, and two **RGB LEDs**, simulated in Wokwi.

**Primary Goals:**
* Verify multi-IMU communication on a shared $I^2C$ bus.
* Validate **AD0-based address multiplexing** (switching between 0x68 and 0x69).
* Confirm basic motion and posture detection logic.
* Provide immediate visual (LED) and serial feedback.

> **Note:** This simulation focuses on embedded feasibility and signal sanity, not rehabilitation intelligence.

---

## 2. What This Simulation Demonstrates

### Hardware-Level Capabilities
* **Address Multiplexing:** Multiple MPU6050 IMUs share the same $I^2C$ address (0x69).
* **Sensor Selection:** AD0 pin multiplexing selects one IMU at a time using GPIO-controlled lines.
* **Stable Communication:** Reliable $I^2C$ communication via custom SDA/SCL pins.
* **Data Acquisition:** Real-time accelerometer and gyroscope data acquisition.

[Image of ESP32-S3 and multiple MPU6050 I2C wiring diagram]

### Embedded Signal Processing
The firmware performs fundamental calculations without complex filters:
* **Raw Readings:** Accelerometer ($a_x, a_y, a_z$) and Gyroscope ($g_x, g_y, g_z$).
* **Unit Conversion:** LSB to $g$ and LSB to $dps$ (degrees per second).
* **Tilt Estimation:** Simple pitch and roll estimation using trigonometry.
* **Intensity Estimation:** Motion magnitude calculation using gyroscope data.

---

## 3. Feedback Logic & Output

### LED-Based Indicators
Two RGB LEDs serve as coarse state indicators:

| Component | Target | Color | Logic |
| :--- | :--- | :--- | :--- |
| **LED 1** | Posture (IMU 1) | **Green** | Stable posture detected |
| | | **Red** | Posture deviation detected |
| **LED 2** | Motion (IMU 3) | **Blue** | Active motion detected |
| | | **Off** | Low or no motion |

### Serial Diagnostics
The serial output provides developer-facing data for inspection:
* Per-IMU accelerometer and gyroscope values.
* Estimated pitch and roll.
* Motion intensity classifications: `STATIONARY`, `MOVING`, or `ACTIVE`.

---

## 4. Architectural Scope
This simulation operates entirely at the device and firmware level:
* **Single Microcontroller:** No external compute power.
* **Deterministic Logic:** No learning, adaptation, or patient-specific modeling.
* **Open-Loop:** No closed-loop correction logic or biomechanical feedback.

---

## 5. Key Differences: Simulation vs. Rehab Coach Project

| Feature | Wokwi Simulation | Neuro-Kinematic Rehab Coach |
| :--- | :--- | :--- |
| **Purpose** | Hardware & $I^2C$ Validation | Stroke-specific Motor Relearning |
| **Abstraction** | Raw Sensor Space | Kinematic Space & Quality Metrics |
| **Sensor Interpretation** | Raw thresholds (no fusion) | IMU Fusion & Joint Relationships |
| **Feedback** | Binary LEDs / Serial Logs | Haptics, Audio, & Performance Scores |
| **Loop Structure** | Open-Loop | Closed-Loop Adaptive Control |
| **Clinical Intelligence** | None | Motor Quality Score (MQS) |
| **Target User** | Embedded Developer | Patient & Physiotherapist |

[Image of 3D skeletal arm model tracking limb orientation]

---

## 6. Evolution Path
This simulation sits at **Step 0–1** of the pipeline. To evolve into the full **Rehab Coach**, the following transitions are planned:

1.  **Sensor Fusion:** Replace threshold logic with Madgwick/Kalman filters.
2.  **Actuation:** Transition from LEDs to localized vibration motors for haptic feedback.
3.  **Kinematics:** Implement limb-to-torso relationship analysis and compensation detection.
4.  **Integration:** Move computation to a high-level processing unit and add speech/breathing analysis.

---

## Bottom Line
* **The Simulation** proves you can read the sensors.
* **The Project** proves you understand rehabilitation.
