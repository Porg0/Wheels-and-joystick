# Code for controlling servos using a joystick
# Has Variable speed implemented
# Has Variable turning as well
# Uses pins 26, 27 for joystick and pin 22 for button
# Servos are connected to pins 28, 27, 26, 16, 17, 18


from machine import Pin, ADC, PWM
import time

# Joystick Pins
x_axis = ADC(Pin(26))  # HORZ (X-axis) connected to GP26 (ADC0)
y_axis = ADC(Pin(27))  # VERT (Y-axis) connected to GP27 (ADC1)
button = Pin(22, Pin.IN, Pin.PULL_UP)  # SEL (button) connected to GP22

FullForward = 100  # Full Forward speed value for servos
ModerateForward = 50  # Faster Forward speed value for servos
NormForward = 25  # Slow Forward speed value for servos
FullBackward = -100  # Full Backward speed value for servos
ModerateBackward = -50  # Faster Backward speed value for servos
NormBackward = -25  # Slow Backward speed value for servos
Stopall = 0  # Stop value for servos

# Servo Pins
servos = {
    "front_right": PWM(Pin(28)),
    "middle_right": PWM(Pin(27)),
    "rear_right": PWM(Pin(26)),
    "front_left": PWM(Pin(16)),
    "middle_left": PWM(Pin(17)),
    "rear_left": PWM(Pin(18)),
}

# Set servo frequency to 50Hz
for servo in servos.values():
    servo.freq(50)

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
        button_pressed = not button.value()  # Button pressed = True, released = False

        # Map joystick values to speed (-100 to 100)
        x_speed = map_value(x_value, 0, 65535, -100, 100)  # Turning
        y_speed = map_value(y_value, 0, 65535, -100, 100)  # Forward/Backward

        # Turning logic
        if x_speed > 60:  # Hard Right turn
            # Stop right-side servos
            for servo_name in ["front_right", "middle_right", "rear_right"]:
                set_servo_speed(servos[servo_name], FullBackward) # Move rightside backwards
                print("Right-side servos Backwards at 100")
            # Move left-side servos forward
            for servo_name in ["front_left", "middle_left", "rear_left"]:
                set_servo_speed(servos[servo_name], FullForward)  # Fixed forward speed
                print(f"{servo_name}: Moving forward at speed 100")
        elif x_speed > 20:  # Right turn
            # Stop right-side servos
            for servo_name in ["front_right", "middle_right", "rear_right"]:
                set_servo_speed(servos[servo_name], ModerateBackward) # Move rightside backwards
                print("Right-side servos Backwards at 50")
            # Move left-side servos forward
            for servo_name in ["front_left", "middle_left", "rear_left"]:
                set_servo_speed(servos[servo_name], ModerateForward)  # Fixed forward speed
                print(f"{servo_name}: Moving forward at speed 50")
        elif x_speed < -20:  # Left turn
            # Stop left-side servos
            for servo_name in ["front_left", "middle_left", "rear_left"]:
                set_servo_speed(servos[servo_name], ModerateBackward) # Move leftside backwards
                print("Left-side servos Backwards at 50")
            # Move right-side servos forward
            for servo_name in ["front_right", "middle_right", "rear_right"]:
                set_servo_speed(servos[servo_name], ModerateForward)  # Fixed forward speed
                print(f"{servo_name}: Moving forward at speed 50")
        elif x_speed < -60:  # Hard Left turn
            for servo_name in ["front_left", "middle_left", "rear_left"]:
                set_servo_speed(servos[servo_name], FullBackward)
                print(f"{servo_name}: Moving backward at speed 100")
            for servo_name in ["front_right", "middle_right", "rear_right"]:
                set_servo_speed(servos[servo_name], FullForward)
                print(f"{servo_name}: Moving forward at speed 100")

        if y_speed > 75: # Full speed forward
            for servo_name, servo in servos.items():
                set_servo_speed(servo, FullForward)
                print(f"{servo_name}: Moving forward at speed 100")
        elif y_speed > 50: # Moderate speed forward
            for servo_name, servo in servos.items():
                set_servo_speed(servo, ModerateForward)
                print(f"{servo_name}: Moving forward at speed 50")
        elif y_speed > 25: # Slow speed forward
            for servo_name, servo in servos.items():
                set_servo_speed(servo, NormForward)
                print(f"{servo_name}: Moving forward at speed 25")
        else:  # Joystick centered, normal forward/backward control
            for servo_name, servo in servos.items():
                set_servo_speed(servo, Stopall)
                print("All servos stopped")

        # Debugging: Print joystick values
        print(f"Raw X: {x_value}, Raw Y: {y_value}, Button Pressed: {button_pressed}")

        # Small delay for smooth control
        time.sleep(0.1)
except KeyboardInterrupt:  # Stop Program
    print("Keyboard interrupt detected. Stopping all servos.")
    for servo_name, servo in servos.items():
        set_servo_speed(servo, Stopall)
        print(f"{servo_name}: Stopped")
