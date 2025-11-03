import board
import busio
import time
import sys
try:
    # Attempt to import the required libraries
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
except ImportError:
    # Exit cleanly if the library is missing
    print("Error: The 'adafruit-circuitpython-ads1x15' library is not installed.")
    print("Please run: pip3 install adafruit-circuitpython-ads1x15")
    sys.exit(1)

# --- Configuration ---
try:
    # Initialize the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create the ADS1115 object
    ads = ADS.ADS1115(i2c)
except ValueError:
    print("I2C initialization failed. Ensure the I2C interface is enabled on your Raspberry Pi.")
    sys.exit(1)


# Set the gain. GAIN=1 provides a +/- 4.096V measurement range.
ads.gain = 1
# Set the data rate to 128 samples per second (a good balance for monitoring)
ads.data_rate = 128 
channel = AnalogIn(ads, 0) # Use the A0 channel

def main_monitor():
    """Reads and prints the ADC value and voltage periodically."""
    print("--- ADS1115 Live Data Monitor ---")
    print("Press Ctrl+C to stop.")
    print("-" * 35)
    print("Dark (Shutter Closed) values should be HIGH (near 32767).")
    print("Light (Shutter Open) values should be LOW (near 0).")
    print("-" * 35)

    while True:
        try:
            # Read the raw 16-bit value (0 to 32767)
            raw_value = channel.value
            
            # Read the measured voltage
            voltage = channel.voltage

            # Print the readings
            print(f"Raw ADC: {raw_value:<5} | Voltage: {voltage:.3f} V")
            
            # Wait for half a second before the next reading
            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nExiting Live Monitor.")
            break
        except Exception as e:
            print(f"\nAn error occurred during reading: {e}")
            time.sleep(1) 

if __name__ == "__main__":
    main_monitor()