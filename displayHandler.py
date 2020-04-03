import RPi.GPIO as GPIO
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class SerialOLEDDisplay: 
    def __init__(self, WIDTH, HEIGHT): 
        i2c = busio.I2C(SCL, SDA)
        self.width  = WIDTH
        self.height = HEIGHT

        self.display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

        self.buffer = Image.new("1", (WIDTH, HEIGHT))
        self.draw   = ImageDraw.Draw(self.buffer)

        self.clear_buffer()
        self.display_everything() 

    #Adds a string to the buffer to the specified coordinates. 
    #Returns: A list of tuples containing the coordinates of the four 
    #   vertecies in clockwise direction starting from the one on the 
    #   top left. 
    def add_string (self, x, y, string, fontSize=10, fontPath="./fonts/truetype/dejavu/DejaVuSans.ttf"):
        font   = ImageFont.truetype(fontPath, size=fontSize)

        (text_width, text_height) = font.getsize(string)
        #Draw a black rectangle as a backgound to cover up whatever
        #   that might overlap. 
        self.draw.rectangle((x, y, x+text_width, y+text_height), fill=0)
        self.draw.text((x, y), string, font=font, fill=128)
        
        return [(x, y), (x+text_width, y), (x+text_width, y+text_height), (x, y+text_height)]

    def clear_buffer(self):
        #Draws a black rectangle over everything. 
        #Effectively clears the display. 
        self.draw.rectangle((0, 0, self.display.width, self.display.height), fill=0)
    
    def display_everything(self):
        self.display.image(self.buffer)
        self.display.show()