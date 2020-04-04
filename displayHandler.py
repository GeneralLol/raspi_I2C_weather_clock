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
    #x and y specify which coordinates to start inserting the text at. 
    #maxX and maxY specify the boundaries of the text box. Default to 
    #   arbitrary large values. 
    #Returns: A list of tuples containing the coordinates of the four 
    #   vertecies in clockwise direction starting from the one on the 
    #   top left. 
    def add_string (self, startx=0, starty=0, maxX=1000, maxY=1000, string="", \
                    fontSize=10, fontPath="./fonts/truetype/dejavu/DejaVuSans.ttf"):

        font   = ImageFont.truetype(fontPath, size=fontSize)

        (textWidth, textHeight) = font.getsize(string)
        lineHeight = textHeight
        stringsToDisplay = []
        #Check if the text will go out of bound. 
        #If x goes out of bound, reduce font size, split the string into two and place into two lines. 
        #TODO: There is a mathemetical method to make a rectangle into a less long rectangle. 
        #   Implement that when there is time. 
        if (startx + textWidth > maxX):
            font = ImageFont.truetype(fontPath, size=int(fontSize))
            stringsToDisplay.append(string[:int(len(string)/2)])
            stringsToDisplay.append(string[int(len(string)/2):])
            #Check if a word was split. If there is, add a hyphen. 
            if (stringsToDisplay[0][1:] != " " and stringsToDisplay[1][:1] != " "):
                stringsToDisplay[0] = stringsToDisplay[0] + "-"
            (textWidth, lineHeight) = font.getsize(stringsToDisplay[0])
            textHeight = lineHeight*2    #To account for the two lines
        #If y goes out of bound, do nothing. 

        #Draw a black rectangle as a backgound to cover up whatever
        #   that might overlap. 
        self.draw.rectangle((startx, starty, startx+textWidth, starty+textHeight), fill=0)
        #Display the text
        lineCounter = 0
        for y in range(starty, maxY, lineHeight): 
            self.draw.text((startx, y), stringsToDisplay[lineCounter], font=font, fill=128)
            lineCounter += 1
        
        return [(startx, starty), (startx+textWidth, starty), \
                (startx+textWidth, starty+textHeight), (startx, starty+textHeight)]

    def clear_buffer(self):
        #Draws a black rectangle over everything. 
        #Effectively clears the display. 
        self.draw.rectangle((0, 0, self.display.width, self.display.height), fill=0)
    
    def display_everything(self):
        self.display.image(self.buffer)
        self.display.show()

    #Changes the brightness of the OLED display. 
    def config_brightness(self, brightness):
        self.display.write_cmd(0x81)
        self.display.write_cmd(brightness)