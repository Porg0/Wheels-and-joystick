# Code for servo arm control
# This is codde framing out how to control a servo arm
# Pin values may be incorrect but it is a starting point
# Most is just the movement code but arranged and some values are changed

from machine import Pin, ADC, PWM
import time

# Joystick Pins
x_axis = ADC(Pin(26))  # HORZ (X-axis) connected to GP26 (ADC0)
y_axis = ADC(Pin(27))  # VERT (Y-axis) connected to GP27 (ADC1)
z_axis = ADC(Pin(28))  # Z-axis (rotation) connected to GP28 (ADC2)

# Servos
servos = {
    "front_right": PWM(Pin(28)),
    "middle_right": PWM(Pin(27)),
    "rear_right": PWM(Pin(26)),
    "front_left": PWM(Pin(16)),
    "middle_left": PWM(Pin(17)),
    "rear_left": PWM(Pin(18)),
}

FullForward = 100  # Full Forward speed value for servos
ModerateForward = 50  # Faster Forward speed value for servos
NormForward = 25  # Slow Forward speed value for servos
FullBackward = -100  # Full Backward speed value for servos
ModerateBackward = -50  # Faster Backward speed value for servos
NormBackward = -25  # Slow Backward speed value for servos
Stopall = 0  # Stop value for servos

# Set servo frequency to 50Hz
# for servo in servos.values():
#     servo.freq(50)

# Function to map values from one range to another
def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Function to set servo speed
def set_servo_speed(servo, speed):
    neutral = 32768  # Neutral position for servos
    if speed > 0:
        duty = neutral + int(speed * 32768 / 100)  # Forward
    elif speed < 0:
        duty = neutral - int(abs(speed) * 32768 / 100)  # Backward
    else:
        duty = neutral  # Stop
    servo.duty_u16(duty)

# Main loop
try:
    while True:
        # Read joystick analog values
        x_value = x_axis.read_u16()  # X-axis value (0-65535)
        y_value = y_axis.read_u16()  # Y-axis value (0-65535)
        z_value = z_axis.read_u16()

        # Map joystick values to speed (-100 to 100)
        x_speed = map_value(x_value, 0, 65535, -100, 100)  # Turning
        y_speed = map_value(y_value, 0, 65535, -100, 100)  # Forward/Backward
        z_speed = map_value(z_value, 0, 65535, -100, 100)  # Rotation

        # Debugging: Print joystick values
        print(f"Raw X: {x_value}, Raw Y: {y_value}, Raw Z: {z_value}")

        # Maybe add a check here for if arm is maxed out in any direction
        
        if x_speed > 0: # Adjust to be higher input values if wanted
            print(f"X Speed: {x_speed} (Right)") # Add in loop for all servos
            set_servo_speed(servos, x_speed)
        elif x_speed < 0:   
            print(f"X Speed: {x_speed} (Left)")
            set_servo_speed(servos, x_speed)
        else:
            print("X Speed: 0 (Neutral)")
        if y_speed > 0:
            print(f"Y Speed: {y_speed} (Forward)")
            set_servo_speed(servos, x_speed)
        elif y_speed < 0:
            print(f"Y Speed: {y_speed} (Backward)")
            set_servo_speed(servos, x_speed)
        else:
            print("Y Speed: 0 (Neutral)")
        if z_speed > 0:
            print(f"Z Speed: {z_speed} (Clockwise)")
            set_servo_speed(servos, x_speed)
        elif z_speed < 0:
            print(f"Z Speed: {z_speed} (Counterclockwise)")
            set_servo_speed(servos, x_speed)
        else:
            print("Z Speed: 0 (Neutral)")

        # Small delay for smooth control
        time.sleep(0.1)
except KeyboardInterrupt:  # Stop Program
    print("Keyboard interrupt detected. Stopping all servos.")
    set_servo_speed(servos, Stopall)
