"""pyUltrasonic Sensor Module."""
import RPi.GPIO as GPIO
import time

class UltrasonicSensor():

    def __init__(self, gpio_trigger, gpio_echo, depth, compensation=0):
        """Initialize the sensor object."""
        self.distance = None
        self.startTime = None
        self.distance = None
        self.gpio_trigger = gpio_trigger
        self.gpio_echo = gpio_echo
        self.depth = depth
        self.compensation = compensation

        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        #set GPIO direction (IN / OUT)
        GPIO.setup(self.gpio_trigger, GPIO.OUT)
        GPIO.setup(self.gpio_echo, GPIO.IN)

    def __del__(self):
        """clean up all the ports you’ve used."""
        GPIO.cleanup()  

    def retrieveDistance(self):
        """Retrieve the distance."""
        # set Trigger to HIGH
        GPIO.output(self.gpio_trigger, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.gpio_trigger, False)

        self.startTime = time.time()
        startElapsed = time.perf_counter()
        stopElapsed = time.perf_counter()
     
        # save StartTime
        while GPIO.input(self.gpio_echo) == 0 and (time.perf_counter() - startElapsed) < 30:
            startElapsed = time.perf_counter()
        if (time.perf_counter() - startElapsed) >= 30:
            pass
            #TODO: Raise an Error
     
        # save time of arrival
        while GPIO.input(self.gpio_echo) == 1 and (time.perf_counter() - stopElapsed) < 30:
            stopElapsed = time.perf_counter()
        if (time.perf_counter() - stopElapsed) >= 30:
            pass
            #TODO: Raise an Error
     
        # time difference between start and arrival
        disdistance = ((stopElapsed - startElapsed) * 34300) / 2 + self.compensation
        self.distance = round(disdistance, 0)

    def getDistance(self):
        """Return the distance value."""
        if self.distance is None:
            self.retrieveDistance()

        return self.distance

    def waterLevel(self):
        """Return the water level value."""
        if self.distance is None:
            self.retrieveDistance()

        return self.depth - self.distance

    def waterLevelPercent(self):
        """Return the water level in percentage."""
        if self.distance is None:
            self.retrieveDistance()

        return round((self.depth - self.distance) / self.depth * 100 ,0)
