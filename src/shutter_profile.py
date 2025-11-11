import board
import busio
import time
import sys

try:
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
except ImportError:
    print("Error: Install with 'pip3 install adafruit-circuitpython-ads1x15'")
    sys.exit(1)

def setup_adc():
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        ads.gain = 1
        ads.data_rate = 860  # Fastest sampling
        return AnalogIn(ads, 0)
    except ValueError:
        print("I2C initialization failed. Enable I2C interface.")
        sys.exit(1)

def calibrate(channel):
    print("=== CALIBRATION ===")
    
    input("Close shutter and press Enter...")
    closed_values = [channel.value for _ in range(10)]
    closed_ref = sum(closed_values) / len(closed_values)
    
    input("Open shutter and press Enter...")
    open_values = [channel.value for _ in range(10)]
    open_ref = sum(open_values) / len(open_values)
    
    # Set threshold close to closed value to catch slow ramp up
    threshold = closed_ref - (closed_ref - open_ref) * 0.1
    print(f"Closed: {closed_ref:.0f}, Open: {open_ref:.0f}, Threshold: {threshold:.0f}")
    return threshold, closed_ref, open_ref

def record_shutter_profile(channel):
    import threading
    
    print("\n=== SHUTTER PROFILE RECORDER ===")
    print("Press Enter to START recording, then press Enter again to STOP")
    
    input("Press Enter to start recording...")
    
    measurements = []
    recording = True
    start_time = time.time()
    
    def stop_recording():
        nonlocal recording
        input()  # Wait for Enter press
        recording = False
    
    # Start background thread to listen for stop command
    stop_thread = threading.Thread(target=stop_recording)
    stop_thread.daemon = True
    stop_thread.start()
    
    print("Recording started! Press Enter to stop...")
    
    # Record measurements until stopped
    while recording:
        current_time = time.time()
        value = channel.value
        measurements.append((current_time - start_time, value))
    
    # Display results
    total_time = measurements[-1][0]
    print(f"\nRecording stopped!")
    print(f"Duration: {total_time:.4f}s")
    print(f"Measurements: {len(measurements)}")
    print("\nTime(ms) | ADC Value")
    print("-" * 20)
    
    for t, val in measurements:
        print(f"{t*1000:7.1f} | {val:5.0f}")
    
    print(f"\nTotal duration: {total_time:.4f}s")

def main():
    channel = setup_adc()
    threshold, closed_ref, open_ref = calibrate(channel)
    record_shutter_profile(channel)

if __name__ == "__main__":
    main()