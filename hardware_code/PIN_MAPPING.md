# Raspberry Pi 5 Pin Mapping

## Motor Driver 1 (Drivetrain - WASD Control)
| Signal | BCM GPIO | Physical Pin |
|--------|----------|--------------|
| LEFT_IN1 | 17 | 11 |
| LEFT_IN2 | 27 | 13 |
| RIGHT_IN3 | 23 | 16 |
| RIGHT_IN4 | 24 | 18 |

## Motor Driver 2 (Auxiliary Motors - 1/2/3/4 Control)
| Signal | BCM GPIO | Physical Pin |
|--------|----------|--------------|
| LEFT_IN1 | 5 | 29 |
| LEFT_IN2 | 6 | 31 |
| RIGHT_IN3 | 12 | 32 |
| RIGHT_IN4 | 13 | 33 |

## Temperature Sensor
| Signal | BCM GPIO | Physical Pin |
|--------|----------|--------------|
| DHT22 | 21 | 40 |

## Ultrasonic Sensors (HC-SR04)
| Direction | TRIG | ECHO | TRIG Pin | ECHO Pin |
|-----------|------|------|----------|----------|
| Front | 2 | 3 | 3 | 5 |
| Right | 4 | 14 | 7 | 8 |
| Back | 15 | 18 | 10 | 12 |
| Left | 22 | 25 | 15 | 22 |

## Power & Ground
- **5V**: Pins 2, 4 (use for motor driver logic power if needed)
- **3.3V**: Pins 1, 17 (use for DHT22 and ultrasonic ECHO level-shifting)
- **GND**: Pins 6, 9, 14, 20, 25, 30, 34, 39 (use multiple for current distribution)

## Notes
- Motor drivers require 5V power supply (separate from RPi)
- Ultrasonic ECHO pins need level-shifter (5V → 3.3V) or voltage divider
- DHT22 requires pull-up resistor (~4.7kΩ) between data pin and 3.3V
- All GPIO pins are in BCM numbering mode
