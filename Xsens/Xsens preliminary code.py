import matplotlib
matplotlib.use("TkAgg")

import sys
import time
import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt

from xdpchandler import *
import movelladot_pc_sdk

# =========================================================
# TAG → ROLE MAP (EXACT TAGS)
# =========================================================
ROLE_BY_TAG = {
    "Shoulder": "LEFT_UPPER_ARM",
    "Forearms": "LEFT_FOREARM",
    "Right wrist": "RIGHT_FOREARM",
    "Right Ankle": "RIGHT_UPPER_ARM"
}

SEGMENT = {
    "UPPER_ARM": 0.30,
    "FOREARM": 0.25
}

# Calibration: Xsens DOTs typically have Z-up when flat on table
# We need Z-down along limb, so rotate 180° around X-axis
CALIBRATION_ROT = R.from_euler('x', 180, degrees=True)

# =========================================================
# INIT SDK
# =========================================================
print("Initializing Xsens DOT SDK...")
xdpc = XdpcHandler()
if not xdpc.initialize():
    sys.exit("ERROR: SDK initialization failed")

print("Scanning for DOTs...")
xdpc.scanForDots()

print("Connecting to DOTs...")
xdpc.connectDots()

devices = xdpc.connectedDots()
if not devices:
    sys.exit("ERROR: No DOTs connected")

device_map = {}  # Maps role -> device object
addr_to_role = {}  # Maps bluetooth address -> role

print("\n" + "="*50)
print("CONNECTED DOT TAGS")
print("="*50)
for d in devices:
    tag = d.deviceTagName()
    addr = d.portInfo().bluetoothAddress()
    print(f"Tag: '{tag}' | Address: {addr}")
    
    if tag in ROLE_BY_TAG:
        role = ROLE_BY_TAG[tag]
        device_map[role] = d
        addr_to_role[addr] = role
        print(f"  ✓ Mapped to: {role}")
    else:
        print(f"  ✗ Not in mapping (ignored)")

print("="*50 + "\n")

if not device_map:
    sys.exit("ERROR: No usable DOTs mapped. Check your ROLE_BY_TAG dictionary.")

# =========================================================
# START STREAMING - CRITICAL: Set output rate BEFORE measurement
# =========================================================
print("Configuring and starting measurement...")
for role, device in device_map.items():
    try:
        # Set output rate first
        if not device.setOutputRate(60):
            print(f"  ✗ Failed to set output rate for {role}")
            continue
        
        # Then start measurement
        if not device.startMeasurement(movelladot_pc_sdk.XsPayloadMode_OrientationQuaternion):
            print(f"  ✗ Failed to start measurement for {role}: {device.lastResultText()}")
            continue
            
        print(f"  ✓ {role} streaming at 60 Hz")
    except Exception as e:
        print(f"  ✗ Error starting {role}: {e}")

time.sleep(1.0)  # Allow sensors to stabilize

# =========================================================
# STATE TRACKING
# =========================================================
last_q = {role: None for role in device_map.keys()}
packet_count = {role: 0 for role in device_map.keys()}
last_update_time = time.time()

# =========================================================
# MATPLOTLIB SETUP
# =========================================================
print("\nStarting visualization...")
plt.ion()
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")
plt.show(block=False)

def setup_axes():
    ax.set_xlim(-0.6, 0.6)
    ax.set_ylim(-0.6, 0.6)
    ax.set_zlim(0.0, 1.4)
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.set_title("Xsens DOT – Real-Time Upper Body Tracking")
    ax.view_init(elev=20, azim=45)

# =========================================================
# MAIN LOOP - FIXED QUATERNION HANDLING
# =========================================================
frame_count = 0
start_time = time.time()

print("\nMain loop started. Move your arms to see visualization...")
print("-" * 50)

try:
    while True:
        loop_start = time.time()
        updated = False
        
        # CRITICAL: Use the SDK's packetsAvailable() method correctly
        if xdpc.packetsAvailable():
            # Retrieve packets for each device using bluetooth address
            for role, device in device_map.items():
                addr = device.portInfo().bluetoothAddress()
                
                try:
                    # Get packet for this specific device
                    packet = xdpc.getNextPacket(addr)
                    
                    if packet and packet.containsOrientation():
                        q = packet.orientationQuaternion()
                        
                        # CRITICAL FIX: Handle numpy array quaternion
                        # Xsens returns [w, x, y, z], scipy needs [x, y, z, w]
                        if isinstance(q, np.ndarray):
                            last_q[role] = [q[1], q[2], q[3], q[0]]
                        else:
                            # Fallback for SDK object (has .x(), .y() methods)
                            last_q[role] = [q.x(), q.y(), q.z(), q.w()]
                        
                        packet_count[role] += 1
                        updated = True
                        
                except Exception as e:
                    # Only print first error per role to avoid spam
                    if packet_count[role] == 0:
                        print(f"Error getting packet for {role}: {e}")
        
        # Print status every second
        if time.time() - last_update_time > 1.0:
            total = sum(packet_count.values())
            if total > 0:
                print(f"Packets received: {total} | Per device: {dict(packet_count)}")
            last_update_time = time.time()
        
        # =========================================================
        # DRAW FRAME
        # =========================================================
        ax.cla()
        setup_axes()
        
        # Virtual torso anchor (shoulder level)
        torso = np.array([0.0, 0.0, 0.9])
        ax.scatter(*torso, c="black", s=80, marker='o', label="Torso")
        
        # LEFT ARM (Blue)
        if last_q.get("LEFT_UPPER_ARM") is not None:
            try:
                # Apply calibration rotation
                r_raw = R.from_quat(last_q["LEFT_UPPER_ARM"])
                r = CALIBRATION_ROT * r_raw
                
                # Upper arm: shoulder to elbow
                elbow = torso + r.apply([0, 0, -SEGMENT["UPPER_ARM"]])
                ax.plot([torso[0], elbow[0]],
                       [torso[1], elbow[1]],
                       [torso[2], elbow[2]], 
                       color="blue", linewidth=4, label="L Upper Arm")
                ax.scatter(*elbow, c="blue", s=60, marker='o')
                
                # Forearm: elbow to wrist
                if last_q.get("LEFT_FOREARM") is not None:
                    r2_raw = R.from_quat(last_q["LEFT_FOREARM"])
                    r2 = CALIBRATION_ROT * r2_raw
                    
                    wrist = elbow + r2.apply([0, 0, -SEGMENT["FOREARM"]])
                    ax.plot([elbow[0], wrist[0]],
                           [elbow[1], wrist[1]],
                           [elbow[2], wrist[2]], 
                           color="cyan", linewidth=4, label="L Forearm")
                    ax.scatter(*wrist, c="cyan", s=60, marker='o')
            except Exception as e:
                print(f"Error drawing left arm: {e}")
        
        # RIGHT ARM (Red)
        if last_q.get("RIGHT_UPPER_ARM") is not None:
            try:
                # Apply calibration rotation
                r_raw = R.from_quat(last_q["RIGHT_UPPER_ARM"])
                r = CALIBRATION_ROT * r_raw
                
                # Upper arm: shoulder to elbow
                elbow = torso + r.apply([0, 0, -SEGMENT["UPPER_ARM"]])
                ax.plot([torso[0], elbow[0]],
                       [torso[1], elbow[1]],
                       [torso[2], elbow[2]], 
                       color="red", linewidth=4, label="R Upper Arm")
                ax.scatter(*elbow, c="red", s=60, marker='o')
                
                # Forearm: elbow to wrist
                if last_q.get("RIGHT_FOREARM") is not None:
                    r2_raw = R.from_quat(last_q["RIGHT_FOREARM"])
                    r2 = CALIBRATION_ROT * r2_raw
                    
                    wrist = elbow + r2.apply([0, 0, -SEGMENT["FOREARM"]])
                    ax.plot([elbow[0], wrist[0]],
                           [elbow[1], wrist[1]],
                           [elbow[2], wrist[2]], 
                           color="orange", linewidth=4, label="R Forearm")
                    ax.scatter(*wrist, c="orange", s=60, marker='o')
            except Exception as e:
                print(f"Error drawing right arm: {e}")
        
        # Add legend
        if any(q is not None for q in last_q.values()):
            ax.legend(loc='upper right', fontsize=8)
        
        # Refresh display
        plt.pause(0.016)  # ~60 FPS
        
        if updated:
            frame_count += 1

except KeyboardInterrupt:
    print("\n\nStopping visualization...")

finally:
    # =========================================================
    # CLEANUP
    # =========================================================
    print("\nStopping measurements...")
    for role, device in device_map.items():
        try:
            if not device.stopMeasurement():
                print(f"  ✗ Failed to stop {role}")
            else:
                print(f"  ✓ Stopped {role}")
        except Exception as e:
            print(f"  ✗ Error stopping {role}: {e}")
    
    print("\nClosing connection manager...")
    xdpc.cleanup()
    plt.close('all')
    
    print(f"\nSession summary:")
    print(f"  Total frames: {frame_count}")
    print(f"  Packets per device:")
    for role, count in packet_count.items():
        print(f"    {role}: {count}")
    print("\nDone.")