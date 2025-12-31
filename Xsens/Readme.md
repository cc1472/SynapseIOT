# Xsens DOT Real-Time Upper-Body Visualization
### Quaternion-Based Skeletal Arm Tracking Using Xsens DOT IMUs and Matplotlib

## 1. Purpose
This module implements a real-time upper-body skeletal visualization using Xsens DOT IMUs. It streams orientation quaternions from multiple wearable sensors, converts them into anatomically meaningful limb vectors, and renders a live 3D arm model using Matplotlib.

The code serves as a foundational layer for **camera-free neuro-rehabilitation systems**, enabling:
* Limb orientation tracking
* Compensation analysis (trunk vs. limb motion)
* Kinematic quality assessment
* Real-time feedback visualization for patients and clinicians

---

## 2. Core Functionalities
* **SDK Integration:** Initializes the Xsens DOT PC SDK for seamless communication.
* **Device Management:** Scans, connects, and maps DOT sensors using customizable device tags.
* **High-Frequency Streaming:** Streams orientation quaternions at 60 Hz.
* **Anatomical Alignment:** Applies calibration to align sensor local frames with anatomical limb frames.
* **Vector Kinematics:** Converts quaternions into 3D limb vectors using a two-link model.
* **Live Rendering:** Renders left and right arms in real time using Matplotlib (TkAgg backend).
* **Robustness:** Handles packet synchronization, diagnostics, and graceful shutdown.

---

## 3. System Requirements & Dependencies
* **Python:** 3.9–3.11
* **SDKs:** `movelladot_pc_sdk`, `xdpchandler` (Xsens SDK helper)
* **Math/Science:** `numpy`, `scipy`
* **Visualization:** `matplotlib` (Requires **TkAgg** backend for interactive 3D rendering)

---

## 4. Hardware Mapping & Modeling

### Sensor-to-Body Role Mapping
Each sensor must be tagged in the Xsens DOT App to ensure correct mapping:

| Device Tag | Anatomical Role |
| :--- | :--- |
| `LEFT_UPPER_ARM` | Left Shoulder / Humerus |
| `LEFT_FOREARM` | Left Forearm / Radius-Ulna |
| `RIGHT_UPPER_ARM` | Right Shoulder / Humerus |
| `RIGHT_FOREARM` | Right Forearm / Radius-Ulna |

### Anatomical Segment Model (Standard Anthropometry)
* **Upper Arm Length:** 0.30 m
* **Forearm Length:** 0.25 m
* *Note: These are adjustable for subject-specific calibration.*



---

## 5. Technical Implementation Details

### Coordinate System Calibration
Xsens DOT sensors report orientation in a local frame (Z-axis up when flat). To ensure limb vectors point downward naturally:
* **Calibration Rotation:** A **180-degree rotation about the X-axis** is applied to all sensor orientations to align the sensor frame with the anatomical limb frame.

### Quaternion Handling
* **Input Format (Xsens):** `[w, x, y, z]`
* **Processing Format (SciPy):** `[x, y, z, w]`
* **Constraint:** The code explicitly reorders components to prevent invalid rotations and visualization "flipping."

### Kinematic Chain Construction
1.  **Upper Arm:** Rotates a downward unit vector by the calibrated humerus quaternion $\to$ Scaled by length $\to$ Anchored at the Torso.
2.  **Forearm:** Rotates a downward unit vector by the calibrated forearm quaternion $\to$ Scaled by length $\to$ Anchored at the Elbow position.

---

## 6. Visualization Conventions
The 3D environment uses the following color-coding for immediate segment identification:

* **Left Arm:** Blue (Upper) / Cyan (Forearm)
* **Right Arm:** Red (Upper) / Orange (Forearm)
* **Torso Anchor:** Black Dot

---

## 7. Performance & Runtime Behavior
* **Data Rate:** 60 FPS/Hz visualization and sampling.
* **Packet Integrity:** Periodic diagnostic prints; missing packets trigger a "last-known-state" hold to prevent jitter.
* **Cleanup:** Safe measurement stop and SDK connection closure on `KeyboardInterrupt` to prevent device locking.

---

## 8. Limitations & Future Extensions
### Current Limitations
* No Inverse Kinematics (Forward Kinematics only).
* Fixed segment lengths (Non-dynamic).
* No active drift correction or joint constraint enforcement.

### Recommended Extensions
* **Joint Angle Computation:** Calculate Euler angles for clinical range-of-motion (ROM) reports.
* **Haptic Integration:** Trigger feedback (via Arduino/ESP32) when compensation is detected.
* **GPU Rendering:** Migrate to PyOpenGL or Open3D for higher-fidelity visualization.
