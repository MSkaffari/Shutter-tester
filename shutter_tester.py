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

# Standard camera shutter speeds (in seconds)
SHUTTER_SPEEDS = [
    1/1000, 1/500, 1/250, 1/125, 1/60, 1/30, 1/15, 1/8, 1/4, 1/2, 1
]

def setup_adc():
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        ads.gain = 1
        ads.data_rate = 860  # Fastest sampling for accurate timing
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
    
    threshold = (closed_ref + open_ref) / 2
    print(f"Closed: {closed_ref:.0f}, Open: {open_ref:.0f}, Threshold: {threshold:.0f}")
    return threshold

def find_closest_shutter_speed(duration):
    closest = min(SHUTTER_SPEEDS, key=lambda x: abs(x - duration))
    if closest >= 1:
        return f"{closest:.0f}s"
    else:
        return f"1/{int(1/closest)}"

def measure_shutter(channel, threshold):
    print("\n=== MEASURING ===")
    print("Press Ctrl+C to stop")
    
    while True:
        try:
            # Wait for shutter to close (high value)
            while channel.value < threshold:
                time.sleep(0.001)
            
            # Wait for shutter to open (low value)
            while channel.value >= threshold:
                time.sleep(0.001)
            
            start_time = time.time()
            
            # Wait for shutter to close again
            while channel.value < threshold:
                time.sleep(0.001)
            
            duration = time.time() - start_time
            closest_speed = find_closest_shutter_speed(duration)
            print(f"Duration: {duration:.4f}s → {closest_speed}")
            
        except KeyboardInterrupt:
            print("\nStopped.")
            break

def main():
    channel = setup_adc()
    threshold = calibrate(channel)
    measure_shutter(channel, threshold)

if __name__ == "__main__":
    main()