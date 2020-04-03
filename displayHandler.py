import RPi.GPIO as GPIO
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class SerialOLEDDisplay: 
    def __init__(self, WIDTH, HEIGHT): 
        i2c = busio.I2C(SCL, SDA)

        self.display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

        self.buffer = Image.new("1", (WIDTH, HEIGHT))
        self.draw   = ImageDraw.Draw(self.buffer)

        self.clear_display()

    def display_string (self, x, y, string, fontSize=10, fontPath="./fonts/truetype/dejavu/DejaVuSans.ttf"):
        font   = ImageFont.truetype(fontPath, size=fontSize)

        (font_width, font_height) = font.getsize(string)
        self.draw.rectangle((x, y, x+font_height, y+font_width), fill=0)
        self.draw.text((x, y), string, font=font, fill=128)
        self.display.image(self.buffer)
        self.display.show()

    def clear_display(self):
        #Draws a black rectangle over everything. 
        #Effectively clears the display. 
        self.draw.rectangle((0, 0, self.display.width, self.display.height), fill=0)
        self.display.image(self.buffer)
        self.display.show()