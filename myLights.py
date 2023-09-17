from openrgb.utils import RGBColor, LEDData
from openrgb.network import NetworkClient
from openrgb import OpenRGBClient
import keyboard
import time
import random
import math
import threading
import struct


cli = OpenRGBClient()
#print(cli.devices)

root = cli.get_devices_by_name('Z590 AORUS ELITE')[0]

motherboard_components = root.zones[2]

gigabyte_logo = cli.get_devices_by_name('Gigabyte RTX3060 Gaming OC 12G')[0]
all_fans = root.zones[1]
#all_fans.leds[0..4].set_color(white)
middle_fan = motherboard_components.leds[1]
auros_logo = motherboard_components.leds[2]
back_light = motherboard_components.leds[3]
right_led_strip = motherboard_components.leds[4]
left_ballistix = cli.get_devices_by_name('Crucial DRAM')[0]
right_ballistix = cli.get_devices_by_name('Crucial DRAM')[1]
#left_ballistix.leds[0..7].set_color(red)

red = RGBColor(255, 0, 0)
green = RGBColor(0, 255, 0)
blue = RGBColor(0, 0, 255)
black = RGBColor(0, 0, 0)
white = RGBColor(255, 255, 255)
yellow = RGBColor(255, 255, 0)
purple = RGBColor(128, 0, 128)
orange = RGBColor(255, 165, 0)
pink = RGBColor(255, 192, 203)
brown = RGBColor(139, 69, 19)
gray = RGBColor(128, 128, 128)


color_array = [red,green,blue,black,white,yellow,purple,orange,pink,brown,gray]
color_array_index = 0

#cli.clear()

#left_ballistix.clear()
#right_ballistix.clear()

left_ballistix.set_mode('Direct')
right_ballistix.set_mode('Direct')


for led in all_fans.leds:
    led.set_color(white)

for led in left_ballistix.leds:
    led.set_color(white)

for led in right_ballistix.leds:
    led.set_color(white)

middle_fan.set_color(white)
right_led_strip.set_color(white)
gigabyte_logo.set_color(white)
auros_logo.set_color(white)

def validate_secret_code(code):
    global secret_code
    code_length = len(secret_code)
    i = 0 
    while i < code_length:
        if i == 0 and secret_code[i] != 'up':
            secret_code.clear()
        if i == 1 and secret_code[i] != 'up':
            secret_code.clear()
        if i == 2 and secret_code[i] != 'down':
            secret_code.clear()
        if i == 3 and secret_code[i] != 'down':
            secret_code.clear()
        if i == 4 and secret_code[i] != 'left':
            secret_code.clear()
        if i == 5 and secret_code[i] != 'right':
            secret_code.clear()
        if i == 6 and secret_code[i] != 'left':
            secret_code.clear()
        if i == 7 and secret_code[i] != 'right':
            secret_code.clear()
        if i == 8 and secret_code[i] != 'b':
            secret_code.clear()
        if i == 9 and secret_code[i] != 'a':
            secret_code.clear()
        if i == 9:
            code_is_cracked()
            secret_code.clear()
        i += 1

def code_is_cracked():
    global color_array, color_array_index
    while color_array_index < 11:
        for led in all_fans.leds:
            led.set_color(color_array[color_array_index])
            time.sleep(.07)
        color_array_index += 1
    color_array_index = 0


checkered_index = 0 
checkered_index_fast = 0 
prev = 999
position = 0
reverseChecker = False
is_green = True

def set_led_color(device,index):
    global checkered_index, checkered_index_fast, position, prev, reverseChecker, is_green

    lightSetting = 3

    if index > 6:
        is_green = not is_green

    if lightSetting == 1:
        #checkered setting

        fan_layout = [
            [3, 2, 1],
            [4, 0, 0],
            [5, 6, 7]
        ]

        position = fan_layout[checkered_index][checkered_index_fast]

        if checkered_index == 1 and checkered_index_fast == 2:
            position = 5
            checkered_index += 1
            checkered_index_fast = 0

        if reverseChecker:
            if position % 2 == 0:
                #even
                device.leds[position].set_color(yellow)
            else:
                device.leds[position].set_color(orange)
                #odd
            middle_fan.set_color(green)
        else:
            if position % 2 == 0:
                #even
                device.leds[position].set_color(brown)
            else:
                device.leds[position].set_color(green)
                #odd
            middle_fan.set_color(yellow)

        if len(fan_layout[checkered_index]) - 1 == checkered_index_fast:
            checkered_index += 1
            checkered_index_fast = 0
        else:
            checkered_index_fast += 1


        if index > 6:
            checkered_index = 0 
            checkered_index_fast = 0
            reverseChecker = not reverseChecker
            position = 0
    elif lightSetting == 2:
        #generic circle
        if is_green:
            all_fans.leds[i].set_color(green)
        else:
            all_fans.leds[i].set_color(yellow)






def set_simon_color_animation(position,speed):
    if position == 1:
        all_fans.leds[1].set_color(red)
        all_fans.leds[0].set_color(red)
        all_fans.leds[7].set_color(red)
        time.sleep(speed)
        all_fans.leds[1].set_color(white)
        all_fans.leds[0].set_color(white)
        all_fans.leds[7].set_color(white)
        time.sleep(speed)
    if position == 2:
        all_fans.leds[3].set_color(green)
        all_fans.leds[2].set_color(green)
        all_fans.leds[1].set_color(green)
        time.sleep(speed)
        all_fans.leds[3].set_color(white)
        all_fans.leds[2].set_color(white)
        all_fans.leds[1].set_color(white)
        time.sleep(speed)
    if position == 3:
        all_fans.leds[3].set_color(blue)
        all_fans.leds[4].set_color(blue)
        all_fans.leds[5].set_color(blue)
        time.sleep(speed)
        all_fans.leds[3].set_color(white)
        all_fans.leds[4].set_color(white)
        all_fans.leds[5].set_color(white)
        time.sleep(speed)
    if position == 4:
        all_fans.leds[5].set_color(yellow)
        all_fans.leds[6].set_color(yellow)
        all_fans.leds[7].set_color(yellow)
        time.sleep(speed)
        all_fans.leds[5].set_color(white)
        all_fans.leds[6].set_color(white)
        all_fans.leds[7].set_color(white)
        time.sleep(speed)



simonStarted = False
simonArray = []
userArray = []
simon_array_index = 0
def simonsTurn():
    randumNum = random.randint(1,4)
    simonArray.append(randumNum)
    #Simon goes
    for number in simonArray:
        set_simon_color_animation(number,.5)

def startSimonGame(e):
    global simonStarted, userArray, simon_array_index

    if not e.name == 'f16':
        if e.name == 'right':
            userArray.append(1)
        if e.name == 'up':
            userArray.append(2)
        if e.name == 'left':
            userArray.append(3)
        if e.name == 'down':
            userArray.append(4)

    if len(userArray) > 0:
        if userArray[simon_array_index] == simonArray[simon_array_index]:
            set_simon_color_animation(userArray[simon_array_index],.1)
            simon_array_index += 1
        else:
            simon_array_index = 0
            userArray.clear()
            simonArray.clear()
            simonStarted = False
            all_fans.set_color(red)
            time.sleep(.5)
            all_fans.set_color(black)
            time.sleep(.5)
            all_fans.set_color(red)
            time.sleep(.5)
            all_fans.set_color(white)

    if len(userArray) == len(simonArray) and simonStarted:
        time.sleep(1)
        simonsTurn()
        userArray.clear()
        simon_array_index = 0

def count_words(text):
    words = text.split()
    return len(words)





secret_code = []
i = 0
j = 0 
full_press_bool = True
left_right_ball_bool = True
ballistix_green = True

input_text = []
word_count = 0
tick_rate = True
elapsed_time_4_thread = 0 
tick = False
exit_flag = False

wpm = 1
base_speed = 10
target_wpm = 999


start_time = time.time()
character_count = 0
time_is_ticking = False

# iggs

def on_key_event(e):
    global i, j, secret_code, full_press_bool, device_id_array, left_right_ball_bool, ballistix_green, simonStarted, character_count,  input_text, word_count, start_time, time_is_ticking,tick, base_speed, wpm

    # Below if for key press not just up or down
    if e.event_type == keyboard.KEY_DOWN:
        full_press_bool = False
    elif e.event_type == keyboard.KEY_UP:
        full_press_bool = True
        

    if full_press_bool:

        input_text.append(e.name)

        elapsed_time = round(time.time() - start_time)

        if elapsed_time > 0:
            wpm = (len(input_text) / elapsed_time) * 60
        else:
            start_time = time.time()
            input_text = []
            character_count = 0
            if  wpm == 0:
                elapsed_time = 1

        if elapsed_time > 0:
            character_count += 1

            if e.name == 'f16':
                simonStarted = True

            if simonStarted:
                all_fans.set_color(white)
                startSimonGame(e)
            else:
                #if i < 8:
                #    set_led_color(all_fans,i)
                #    i += 1
                #else:
                #    #resets main index maybe play an animation? 
                #    i = 0

                    #if j == 8:
                    #    j = 0
                    #    left_right_ball_bool = not left_right_ball_bool
                    #    if left_right_ball_bool:
                    #        ballistix_green = not ballistix_green

                    #if left_right_ball_bool:
                    #    if ballistix_green:
                    #        set_led_color(left_ballistix,green,j)
                    #    else:
                    #        set_led_color(left_ballistix,white,j)
                    #else:
                    #    if ballistix_green:
                    #        set_led_color(right_ballistix,green,j)
                    #    else:
                    #        set_led_color(right_ballistix,white,j)
                    #j += 1

                if(e.name == 'up'):
                    secret_code.append('up')
                if(e.name == 'down'):
                    secret_code.append('down')
                if(e.name == 'left'):
                    secret_code.append('left')
                if(e.name == 'right'):
                    secret_code.append('right')
                if(e.name == 'b'):
                    secret_code.append('b')
                if(e.name == 'a'):
                    secret_code.append('a')

                validate_secret_code(secret_code)



def increment_time():
    global exit_flag, tick, i, wpm
    while not exit_flag:

        base_sleep_time = .1

        if wpm < 0: 
            wpm = 1
        elif wpm > 300:
            wpm = 1


        sleep_time = base_sleep_time / (1 + math.sqrt(round(wpm) / 50))

        sleep_timer = max(sleep_time, 0.01)

        if sleep_timer < 0:
            sleep_timer = 1
        else:
            time.sleep(round(sleep_timer,2))

            if wpm > 0:
                wpm -= .5

            if i < 8:
                a = (i + 1) % 8
                b = (i + 2) % 8
                c = (i + 3) % 8
                d = (i + 4) % 8
                e = (i + 5) % 8
                f = (i + 6) % 8
                g = (i + 7) % 8
                h = (i + 8) % 8
                #fan_layout = [
                #    [d, c, b],
                #    [e, 0, a],
                #    [f, g, h]
                #]

                cyan = RGBColor(0, 255, 255)
                light_aqua = RGBColor(0, 239, 255)
                aqua = RGBColor(0, 223, 255)
                light_blue = RGBColor(0, 207, 255)
                sky_blue = RGBColor(0, 191, 255)
                deep_sky_blue = RGBColor(0, 175, 255)
                dodger_blue = RGBColor(0, 159, 255)
                steel_blue = RGBColor(0, 143, 255)
                blue = RGBColor(0, 127, 255)
                medium_blue = RGBColor(0, 95, 255)
                dark_blue = RGBColor(0, 63, 255)
                navy_blue = RGBColor(0, 31, 255)
                blue_navy = RGBColor(0, 0, 255)
                indigo = RGBColor(51, 0, 204)
                purple_blue = RGBColor(102, 0, 153)
                dark_purple = RGBColor(153, 0, 102)
                reddish_purple = RGBColor(204, 0, 51)
                red = RGBColor(255, 0, 0)
                orange_red = RGBColor(255, 127, 0)
                yellow = RGBColor(255, 255, 0) 


                index = 0
                color_array = [cyan,light_aqua,aqua,light_blue,sky_blue,deep_sky_blue,dodger_blue,steel_blue,blue,medium_blue,dark_blue,navy_blue,blue_navy,indigo,purple_blue,dark_purple,reddish_purple,red,orange_red,yellow]

                index = round(wpm / 10)
                if index < 0:
                    index = 0
                elif index > 19:
                    index = 19



                all_fans.leds[a].set_color(color_array[index])
                all_fans.leds[b].set_color(black)
                all_fans.leds[c].set_color(black)
                all_fans.leds[d].set_color(black)
                all_fans.leds[e].set_color(color_array[index])
                all_fans.leds[f].set_color(black)
                all_fans.leds[g].set_color(black)
                all_fans.leds[h].set_color(black)
                time.sleep(round(sleep_timer,2))
                all_fans.leds[a].set_color(black)
                all_fans.leds[b].set_color(color_array[index])
                all_fans.leds[c].set_color(black)
                all_fans.leds[d].set_color(black)
                all_fans.leds[e].set_color(black)
                all_fans.leds[f].set_color(color_array[index])
                all_fans.leds[g].set_color(black)
                all_fans.leds[h].set_color(black)
                time.sleep(round(sleep_timer,2))
                all_fans.leds[a].set_color(black)
                all_fans.leds[b].set_color(black)
                all_fans.leds[c].set_color(color_array[index])
                all_fans.leds[d].set_color(black)
                all_fans.leds[e].set_color(black)
                all_fans.leds[f].set_color(black)
                all_fans.leds[g].set_color(color_array[index])
                all_fans.leds[h].set_color(black)
                time.sleep(round(sleep_timer,2))
                all_fans.leds[a].set_color(black)
                all_fans.leds[b].set_color(black)
                all_fans.leds[c].set_color(black)
                all_fans.leds[d].set_color(color_array[index])
                all_fans.leds[e].set_color(black)
                all_fans.leds[f].set_color(black)
                all_fans.leds[g].set_color(black)
                all_fans.leds[h].set_color(color_array[index])
                time.sleep(round(sleep_timer,2))
                all_fans.leds[a].set_color(color_array[index])
                all_fans.leds[b].set_color(black)
                all_fans.leds[c].set_color(black)
                all_fans.leds[d].set_color(black)
                all_fans.leds[e].set_color(color_array[index])
                all_fans.leds[f].set_color(black)
                all_fans.leds[g].set_color(black)
                all_fans.leds[h].set_color(black)

                i += 1
            else:
                i = 0 


time_thread = threading.Thread(target=increment_time)

time_thread.start()


keyboard.hook(on_key_event)
try:
    # Wait for keyboard events
    keyboard.wait()
except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C)
    pass
finally:
    # Set the exit flag to True to stop the thread
    exit_flag = True
    time_thread.join()  # Wait for the thread to finish before exiting




#name='Direct',
#name='Shift',
#name='Gradient Shift',
#name='Fill',
#name='Stack',
#name='Double Stack',
#name='Breathing',
#name='Motion Point',
#name='Inside Out',
#name='Color Step',
#name='Water Wave (Color Blending)',




