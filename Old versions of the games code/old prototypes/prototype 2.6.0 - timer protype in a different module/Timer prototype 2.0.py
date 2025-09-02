import time#import time module

# Variables to keep track of different measures of time
Minutes = 0
Seconds = 0
Centiseconds = 0# one 100ths of seconds

while True:
    print(str(Minutes) + " Mins " + str(Seconds) + " Sec " + str(Centiseconds) + ' Centiseconds ' )#prints time passed over and over
    Centiseconds += 1#increase centiseconds by one
    time.sleep(.01)#wait one 100th of a second
    if Centiseconds == 100:#if a second has passed
        Seconds += 1#increase a second by 1
        Centiseconds = 0#reset Centiseconds to 0
        if Seconds == 60:#if a minute has passed
            Seconds = 0#reset seconds to 0
            Minutes += 1#increase minute by 1
            

