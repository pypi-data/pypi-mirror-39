from .Raspi_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x6F)
pwm.setPWMFreq(50)

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 50                       # 50 Hz
  pulseLength /= 4096                     # 12 bits of resolution
  pulse /= pulseLength
  pwm.setPWM(channel, 0, int(pulse))

