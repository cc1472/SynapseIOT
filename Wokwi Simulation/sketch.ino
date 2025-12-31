#include <Wire.h>
#include <math.h>

#define SDA_PIN 8
#define SCL_PIN 9
#define MPU_ADDR 0x69

// AD0 pins
int ad0Pins[4] = {4, 5, 6, 7};

// RGB LED 1 (Posture)
#define R1 35
#define G1 36
#define B1 37

// RGB LED 2 (Motion)
#define R2 38
#define G2 39
#define B2 40

void selectIMU(int index) {
  for (int i = 0; i < 4; i++) digitalWrite(ad0Pins[i], LOW);
  digitalWrite(ad0Pins[index], HIGH);
  delay(2);   // REQUIRED for MPU6050 AD0 switching
}

void writeMPU(uint8_t reg, uint8_t data) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(reg);
  Wire.write(data);
  Wire.endTransmission();
}

void readMPU(int16_t &ax, int16_t &ay, int16_t &az,
             int16_t &gx, int16_t &gy, int16_t &gz) {

  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 14);

  ax = Wire.read() << 8 | Wire.read();
  ay = Wire.read() << 8 | Wire.read();
  az = Wire.read() << 8 | Wire.read();
  Wire.read(); Wire.read(); // temperature ignored
  gx = Wire.read() << 8 | Wire.read();
  gy = Wire.read() << 8 | Wire.read();
  gz = Wire.read() << 8 | Wire.read();
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n===== Neuro-Kinematic Rehab Coach : Sensor Diagnostics =====");

  Wire.begin(SDA_PIN, SCL_PIN);

  for (int i = 0; i < 4; i++) {
    pinMode(ad0Pins[i], OUTPUT);
    digitalWrite(ad0Pins[i], LOW);
  }

  pinMode(R1, OUTPUT); pinMode(G1, OUTPUT); pinMode(B1, OUTPUT);
  pinMode(R2, OUTPUT); pinMode(G2, OUTPUT); pinMode(B2, OUTPUT);

  for (int i = 0; i < 4; i++) {
    selectIMU(i);
    writeMPU(0x6B, 0x00); // wake
    writeMPU(0x1C, 0x00); // ±2g
    writeMPU(0x1B, 0x00); // ±250 dps
    writeMPU(0x1A, 0x03); // DLPF
    Serial.print("IMU "); Serial.print(i + 1); Serial.println(" initialized");
  }

  Serial.println("------------------------------------------------------------");
}

void printIMUData(int imuIndex) {
  int16_t ax, ay, az, gx, gy, gz;
  selectIMU(imuIndex);
  readMPU(ax, ay, az, gx, gy, gz);

  // Convert accel to g (approx)
  float axg = ax / 16384.0;
  float ayg = ay / 16384.0;
  float azg = az / 16384.0;

  // Simple tilt estimation
  float pitch = atan2(axg, sqrt(ayg * ayg + azg * azg)) * 57.3;
  float roll  = atan2(ayg, sqrt(axg * axg + azg * azg)) * 57.3;

  // Motion intensity
  float motionEnergy = sqrt(gx * gx + gy * gy + gz * gz);

  Serial.print("IMU "); Serial.print(imuIndex + 1); Serial.println(":");
  Serial.print("  Accel (g)   → X: "); Serial.print(axg, 2);
  Serial.print(" Y: "); Serial.print(ayg, 2);
  Serial.print(" Z: "); Serial.println(azg, 2);

  Serial.print("  Gyro (dps)  → X: "); Serial.print(gx / 131.0, 1);
  Serial.print(" Y: "); Serial.print(gy / 131.0, 1);
  Serial.print(" Z: "); Serial.println(gz / 131.0, 1);

  Serial.print("  Tilt (deg)  → Pitch: "); Serial.print(pitch, 1);
  Serial.print(" Roll: "); Serial.println(roll, 1);

  Serial.print("  Motion Intensity → "); Serial.println(motionEnergy, 1);

  Serial.print("  State → ");
  if (motionEnergy < 1000) Serial.println("STATIONARY");
  else if (motionEnergy < 4000) Serial.println("MOVING");
  else Serial.println("ACTIVE");

  Serial.println();
}

void loop() {

  // ---- IMU 1 : Posture + LED 1 ----
  int16_t ax, ay, az, gx, gy, gz;
  selectIMU(0);
  readMPU(ax, ay, az, gx, gy, gz);

  bool stablePosture = (abs(ax) < 1600 && abs(ay) < 1600);

  digitalWrite(G1, stablePosture);
  digitalWrite(R1, !stablePosture);
  digitalWrite(B1, LOW);

  // ---- IMU 3 : Motion + LED 2 ----
  selectIMU(2);
  readMPU(ax, ay, az, gx, gy, gz);

  bool activeMotion = (abs(gx) > 2600);
  digitalWrite(B2, activeMotion);
  digitalWrite(R2, LOW);
  digitalWrite(G2, LOW);

  // ---- VERBOSE SENSOR PRINT ----
  printIMUData(0); // Torso
  printIMUData(2); // Wrist

  Serial.println("============================================================");
  delay(500);
}
