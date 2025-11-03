# Raspberry Pi Camera Shutter Tester

A Raspberry Pi-based tool for testing camera shutter speeds using a photoresistor circuit and ADS1115 ADC converter.

## Hardware Requirements

- Raspberry Pi 3 (or newer)
- ADS1115 16-bit ADC converter
- Photoresistor (LDR)
- Resistor (10kΩ recommended)
- Breadboard and jumper wires

## Circuit Diagram

```
Photoresistor --- ADS1115 A0
       |
    10kΩ Resistor
       |
      GND

ADS1115 Connections:
- VDD → 3.3V
- GND → GND  
- SCL → GPIO 3 (SCL)
- SDA → GPIO 2 (SDA)
```

## Installation

1. Enable I2C on your Raspberry Pi:
```bash
sudo raspi-config
# Navigate to Interface Options > I2C > Enable
```

2. Install required Python libraries:
```bash
pip3 install adafruit-circuitpython-ads1x15
```

3. Clone this repository:
```bash
git clone https://github.com/yourusername/raspberry-pi-shutter-tester.git
cd raspberry-pi-shutter-tester
```

## Usage

### Live Monitor
Run the live monitor to see real-time ADC readings:

```bash
python3 src/live_monitor.py
```

### Shutter Speed Tester
Run the main shutter tester program:

```bash
python3 src/shutter_tester.py
```

1. **Calibration**: Follow prompts to set reference values for closed/open shutter
2. **Measurement**: Program continuously measures shutter duration and displays closest standard shutter speed
3. Press `Ctrl+C` to stop

The output shows:
- **High values (near 32767)**: Shutter closed (dark)
- **Low values (near 0)**: Shutter open (light)
- **Duration**: Measured time and closest camera shutter speed (e.g., 1/125, 1/500)

## How It Works

The photoresistor changes resistance based on light exposure. When the camera shutter opens, light hits the photoresistor, reducing its resistance and lowering the ADC reading. When closed, the resistance increases, raising the ADC value.

## Limitations

ADS1115 provides 860 samples per second so the fastest shutter speed you can measure is 1/860. Roughly 1/1000. 

## Contributing

Feel free to submit issues and pull requests to improve this project.

## License

MIT License - see LICENSE file for details.