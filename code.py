import rtc, time, board, busio, random
import adafruit_framebuf
import adafruit_is31fl3731

#Randomly pick something to display as text
def chatty():
    thingsToSay = ["BE INSPIRED",
                "DRINK WATER",
                "KEEP GOING",
                "HANG IN THERE",
                "TAKE IT EASY",                
                "YOU GOT THIS",                                                                
                "ROCK ON!",                
                "DON'T YEET ME!",                
                "HELLO WORLD!"]
    line = random.choice(thingsToSay)
    return line

#Stringify the current time and add 0 if a single digit
def clockfix(number):
    if number < 10:
        numFixed = "0"+str(number)
    else:
        numFixed = str(number)
    return numFixed

#Return the name of current day because the datetime returns only an intger between 0-6 for day of week
def dayOfWeek(dow):
    dayDict = {0:"MON",1:"TUE",2:"WED",3:"THU",4:"FRI",5:"SAT",6:"SUN"}
    day = dayDict.get(dow)
    return day

#The Adafruit ScrollingText example now a function we can call over and over
#Just feed it a string and watch the text fly
def textEvent(text_to_show):
    try:
        frame = 0
        for i in range(len(text_to_show) * 9):
            fb.fill(0)
            fb.text(text_to_show, -i + display.width, 0, color=1)
            display.frame(frame, show=False)
            display.fill(0)
            for x in range(display.width):
                # using the FrameBuffer text result
                bite = buf[x]
                for y in range(display.height):
                    bit = 1 << y & bite
                    # if bit > 0 then set the pixel brightness
                    if bit:
                        display.pixel(x, y, 20)

            display.frame(frame, show=True)
            frame = 0 if frame else 1
    Exception as e:
        print("Error: " + str(e))
    return

# Setup frames 4-7 so we can call them later as needed 
# Saves on processing to redraw what we want to display
def animateEvent():
    for z in range(random.randint(1,2)):
            for ani in range(4,8):
                display.frame(ani, show=True)
                time.sleep(1)
    return

# initialize display for the Feather CharlieWing LED 15 x 7
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_is31fl3731.CharlieWing(i2c)

# Create a framebuffer for our display
# Charilewing has 8 frames avaiable
buf = bytearray(32)  # 2 bytes tall x 16 wide = 32 bytes (9 bits is 2 bytes)
fb = adafruit_framebuf.FrameBuffer(buf, display.width, display.height, adafruit_framebuf.MVLSB)

#Time Setup - intialize the RTC and pass to it a hardcoded date
#You will need to adjust the date each time you update the code
r = rtc.RTC()
r.datetime = time.struct_time((2020, 1, 1, 0, 00, 0, 0, -1, -1))

#Dict of the face animation FRAME:[LEDS]
face = {4:[[10,0,2],[10,0,3],[10,0,4],[10,0,10],[10,0,11],[10,0,12],[10,1,1],[10,1,5],[10,1,9],[10,1,13],[10,2,1],[10,2,3],[10,2,5],[10,2,9],[10,2,11],[10,2,13],
            [10,3,1],[10,3,5],[10,3,9],[10,3,13],[10,4,2],[10,4,3],[10,4,4],[10,4,10],[10,4,11],[10,4,12],[10,5,6],[10,5,7],[10,5,8],[10,6,6],[10,6,7],[10,6,8]],
        5:[[10,0,2],[10,0,3],[10,0,4],[10,0,10],[10,0,11],[10,0,12],[10,1,1],[10,1,5],[10,1,9],[10,1,13],[10,2,1],[10,2,2],[10,2,5],[10,2,9],[10,2,10],[10,2,13],
            [10,3,1],[10,3,5],[10,3,9],[10,3,13],[10,4,2],[10,4,3],[10,4,4],[10,4,10],[10,4,11],[10,4,12],[10,5,6],[10,5,7],[10,5,8],[10,6,6],[10,6,7],[10,6,8]],
        6:[[10,0,2],[10,0,3],[10,0,4],[10,0,10],[10,0,11],[10,0,12],[10,1,1],[10,1,5],[10,1,9],[10,1,13],[10,2,1],[10,2,4],[10,2,5],[10,2,9],[10,2,12],[10,2,13],
            [10,3,1],[10,3,5],[10,3,9],[10,3,13],[10,4,2],[10,4,3],[10,4,4],[10,4,10],[10,4,11],[10,4,12],[10,5,6],[10,5,7],[10,5,8],[10,6,6],[10,6,7],[10,6,8]],
        7:[[10,0,2],[10,0,3],[10,0,4],[10,0,10],[10,0,11],[10,0,12],[10,1,1],[10,1,5],[10,1,9],[10,1,13],[10,2,1],[10,2,3],[10,2,5],[10,2,9],[10,2,11],[10,2,13],
            [10,3,1],[10,3,4],[10,3,10],[10,3,13],[10,4,2],[10,4,3],[10,4,11],[10,4,12],[10,5,5],[10,5,9],[10,6,6],[10,6,7],[10,6,8]]}

# PreRender frames 4-7 with our pixel ART
for y in range(4,8):
    display.frame(y, show=False)
    display.fill(0)
    for cur_led in face.get(y):
        display.pixel(cur_led[2], cur_led[1], cur_led[0])

#The main loop
while True:
    try:
        #Get the current time and format it to a string
        curDay = dayOfWeek(r.datetime[6])
        curHour = r.datetime[3]
        curMin = clockfix(r.datetime[4])
        curSec = clockfix(r.datetime[5])
        clockFace = "  {0}  {1}:{2}:{3}   ".format(curDay, curHour, curMin, curSec)

        #Rendering the display
        textEvent(clockFace)
        textEvent(chatty())        
        animateEvent()

    except Exception as e:
        print("Error: " + str(e))