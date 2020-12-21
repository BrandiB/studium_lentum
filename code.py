import time
import random
import terminalio
import json
from adafruit_magtag.magtag import MagTag

SHOW_LIGHTS = False
PLAY_SOUNDS = False
MAX_LEVEL =  40
NUMBER_CORRECT = 0
CORRECT_ANSWER = 1
SHOW_EXTRA = True
WHICH_QUESTION = 0

magtag = MagTag()

# main text, index 0
magtag.add_text(
    text_font ="Arial-Bold-24.bdf",
    text_position=(
        magtag.graphics.display.width // 2,
        5,
    ),
    text_scale = 1,
    line_spacing=1,
    text_anchor_point=(0.5, 0),
)

# button labels, add all 4 in one loop
for x_coord in (5, 92, 166, 220):
    magtag.add_text(
        text_font = "Arial-12.bdf",
        text_position=(x_coord, magtag.graphics.display.height - 3),
        line_spacing=1.0,
        text_anchor_point=(0, 1),
    )

# Extra
magtag.add_text(
    text_font = "Arial-12.bdf",
    text_position=(
        magtag.graphics.display.width // 2,
        38,
    ),
    text_scale = 1,
    line_spacing=1,
    text_anchor_point=(0.5, 0),
)

# Answer A
magtag.add_text(
    text_font = "Arial-18.bdf",
    text_position=(
        magtag.graphics.display.width // 2,
        56,
    ),
    text_scale = 1,
    line_spacing=1,
    text_anchor_point=(0.5, 0),
)

# Answer B
magtag.add_text(
    text_font = "Arial-18.bdf",
    text_position=(
        magtag.graphics.display.width // 2,
        83,
    ),
    text_scale = 1,
    line_spacing=1,
    text_anchor_point=(0.5, 0),
)

quizQuestions = json.loads(open("latin.json").read())

def displayNextQuestion():
    global MAX_LEVEL
    global CORRECT_ANSWER
    global WHICH_QUESTION
    global SHOW_EXTRA
    magtag.set_background("background_menu.bmp")
    magtag.set_text("SETUP", 1, False)
    magtag.set_text("A", 2, False)
    magtag.set_text("B", 3, False)
    magtag.set_text("EXTRA", 4, False)
    questionLevel = 41
    while questionLevel > MAX_LEVEL:
        WHICH_QUESTION = random.randint(0, len(quizQuestions)-1)
        questionLevel = quizQuestions[WHICH_QUESTION]['lesson']
    magtag.set_text(quizQuestions[WHICH_QUESTION]['question'], 0, False)
    CORRECT_ANSWER = random.randint(1,2)
    wrongAnswer = quizQuestions[WHICH_QUESTION]['answer']
    while wrongAnswer == quizQuestions[WHICH_QUESTION]['answer']:
        whichWrong = random.randint(0, len(quizQuestions)-1)
        wrongAnswer = quizQuestions[whichWrong]['answer']
    if SHOW_EXTRA == True:
        magtag.set_text(quizQuestions[WHICH_QUESTION]['parts'], 5, False)
    if SHOW_EXTRA == False:
        magtag.set_text("", 5, False)
    if CORRECT_ANSWER == 1:
        magtag.set_text('A: ' + quizQuestions[WHICH_QUESTION]['answer'], 6, False)
        magtag.set_text('B: ' + wrongAnswer, 7, False)
    if CORRECT_ANSWER == 2:
        magtag.set_text('A: ' + wrongAnswer, 6, False)
        magtag.set_text('B: ' + quizQuestions[WHICH_QUESTION]['answer'], 7, False)
    magtag.refresh()

magtag.peripherals.neopixels.brightness = 0.1
magtag.set_background("background.bmp")
magtag.set_text("STUDIUM\n LENTUM")
magtag.refresh()
if SHOW_LIGHTS == True:
    magtag.peripherals.neopixels.fill(0xFF4500)
if PLAY_SOUNDS == True:
    song = ((262, 2),(262, 2),(349,6))
    for notepair in song:
        magtag.peripherals.play_tone(notepair[0], notepair[1] * 0.2)
if SHOW_LIGHTS == True:
    magtag.peripherals.neopixels.fill(0xffffff)
else:
    magtag.peripherals.neopixels.fill(0x000000)

def changeSettings():
        # Setup Screen
        magtag.set_text('Setup', 0, False)
        magtag.set_text('   1', 1, False)
        magtag.set_text('2', 2, False)
        magtag.set_text('3', 3, False)
        magtag.set_text('BACK', 4, False)
        magtag.set_text(' 1: Light \n 2: Sound \n 3: Level', 5, False)
        magtag.set_text('', 6, False)
        magtag.set_text('', 7, True)
        while magtag.peripherals.buttons[0].value and magtag.peripherals.buttons[1].value and magtag.peripherals.buttons[2].value and magtag.peripherals.buttons[3].value:
            time.sleep(0.1)
        if not magtag.peripherals.buttons[0].value:
            changeLights()
        if not magtag.peripherals.buttons[1].value:
            changeSound()
        if not magtag.peripherals.buttons[2].value:
            changeLevel()
        if not magtag.peripherals.buttons[3].value:
            displayNextQuestion()

def changeLevel():
    # Level
    global MAX_LEVEL
    newMaxLevel = MAX_LEVEL
    magtag.set_text('Max Level',0,False)
    magtag.set_text('SAVE',1,False)
    if MAX_LEVEL > 1:
        magtag.set_text('v',2,False)
    else:
        magtag.set_text('',2,False)
    if MAX_LEVEL < 41:
        magtag.set_text('^',3,False)
    else:
        magtag.set_text('',3,False)
    magtag.set_text('(1 - 40)', 5, False)
    magtag.set_text('Current: ' + str(newMaxLevel), 6, True)
    keepLooking = True
    while keepLooking:
        if not magtag.peripherals.buttons[0].value:
            MAX_LEVEL = newMaxLevel
            keepLooking = False
        if not magtag.peripherals.buttons[1].value:
            if newMaxLevel > 1:
                newMaxLevel = newMaxLevel - 5
                if newMaxLevel <= 5:
                    newMaxLevel = 5
                    magtag.set_text('',2,False)
                else:
                    magtag.set_text('v',2,False)
                if newMaxLevel >= 40:
                    newMaxLevel = 40
                    magtag.set_text('',3,False)
                else:
                    magtag.set_text('^',3,False)
                magtag.set_text('Current: ' + str(newMaxLevel), 6, True)
        if not magtag.peripherals.buttons[2].value:
            if newMaxLevel < MAX_LEVEL:
                newMaxLevel = newMaxLevel + 5
                if newMaxLevel <= 5:
                    newMaxLevel = 5
                    magtag.set_text('',2,False)
                else:
                    magtag.set_text('v',2,False)
                if newMaxLevel >= 40:
                    newMaxLevel = 40
                    magtag.set_text('',3,False)
                else:
                    magtag.set_text('^',3,False)
                magtag.set_text('Current: ' + str(newMaxLevel), 6, True)
        if not magtag.peripherals.buttons[3].value:
            changeSettings()
        time.sleep(0.1)
    displayNextQuestion()

def changeSound():
    # Sound
    global PLAY_SOUNDS
    magtag.set_text('Sounds',0,False)
    magtag.set_text('CHANGE',1,False)
    magtag.set_text('',2,False)
    magtag.set_text('',3,False)
    if PLAY_SOUNDS == True:
        magtag.set_text('Sounds are on.',5,True)
    else:
        magtag.set_text('Sounds are off.',5,True)
    while magtag.peripherals.buttons[0].value and magtag.peripherals.buttons[3].value:
        time.sleep(0.1)
    if not magtag.peripherals.buttons[0].value:
        if PLAY_SOUNDS == True:
            PLAY_SOUNDS = False
        else:
            PLAY_SOUNDS = True
            song = ((262, 2),(262, 2),(349,6))
            for notepair in song:
                magtag.peripherals.play_tone(notepair[0], notepair[1] * 0.2)
        displayNextQuestion()
    if not magtag.peripherals.buttons[3].value:
        changeSettings()

def changeLights():
    # Light
    global SHOW_LIGHTS
    magtag.set_text('Lights',0,False)
    magtag.set_text('CHANGE',1,False)
    magtag.set_text('',2,False)
    magtag.set_text('',3,False)
    if SHOW_LIGHTS == True:
        magtag.set_text('Lights are on.',5,True)
    else:
        magtag.set_text('Lights are off.',5,True)
    while magtag.peripherals.buttons[0].value and magtag.peripherals.buttons[3].value:
        time.sleep(0.1)
    if not magtag.peripherals.buttons[0].value:
        if SHOW_LIGHTS == True:
            SHOW_LIGHTS = False
            magtag.peripherals.neopixels.fill(0x000000)
        else:
            SHOW_LIGHTS = True
            magtag.peripherals.neopixels.fill(0xffffff)
        displayNextQuestion()
    if not magtag.peripherals.buttons[3].value:
        changeSettings()

#FirstQuestion
displayNextQuestion()

while True:
    if not magtag.peripherals.buttons[0].value:
        changeSettings()
    if not magtag.peripherals.buttons[3].value:
        if SHOW_EXTRA == True:
            SHOW_EXTRA = False
            magtag.set_text('', 5, True)
        else:
            SHOW_EXTRA = True
            magtag.set_text(quizQuestions[WHICH_QUESTION]['parts'], 5, True)
    if not magtag.peripherals.buttons[2].value:
        if CORRECT_ANSWER == 2:
            NUMBER_CORRECT = NUMBER_CORRECT + 1
            magtag.set_background("owl.bmp")
            magtag.set_text('CORRECT!', 0, False)
            magtag.set_text('', 1, False)
            magtag.set_text('Current Streak: ' + str(NUMBER_CORRECT), 2, False)
            magtag.set_text('', 3, False)
            magtag.set_text('', 4, False)
            magtag.set_text('', 5, False)
            magtag.set_text(quizQuestions[WHICH_QUESTION]['question'], 6, False)
            magtag.set_text(quizQuestions[WHICH_QUESTION]['answer'], 7, True)
            if SHOW_LIGHTS == True:
                magtag.peripherals.neopixels.fill(0x002700)
            if PLAY_SOUNDS == True:
                song = ((262, 2),(262, 2),(349,6))
                for notepair in song:
                    magtag.peripherals.play_tone(notepair[0], notepair[1] * 0.2)
            if SHOW_LIGHTS == True:
                magtag.peripherals.neopixels.fill(0xffffff)
            else:
                magtag.peripherals.neopixels.fill(0x000000)
        else:
            magtag.set_background("owl.bmp")
            magtag.set_text('WRONG!', 0, False)
            magtag.set_text('', 1, False)
            magtag.set_text('', 2, False)
            magtag.set_text('', 3, False)
            magtag.set_text('', 4, False)
            magtag.set_text('', 5, False)
            magtag.set_text(quizQuestions[WHICH_QUESTION]['question'], 6, False)
            magtag.set_text(quizQuestions[WHICH_QUESTION]['answer'], 7, True)
            if SHOW_LIGHTS == True:
                magtag.peripherals.neopixels.fill(0x7f0000)
            if PLAY_SOUNDS == True:
                song = ((392, 2),(330, 2),(262,6))
                for notepair in song:
                    magtag.peripherals.play_tone(notepair[0], notepair[1] * 0.2)
            if SHOW_LIGHTS == True:
                magtag.peripherals.neopixels.fill(0xffffff)
            else:
                magtag.peripherals.neopixels.fill(0x000000)
            NUMBER_CORRECT = 0
        time.sleep(0.5)
        displayNextQuestion()
    if not magtag.peripherals.buttons[1].value:
        if CORRECT_ANSWER == 1:
            NUMBER_CORRECT = NUMBER_CORRECT + 1
            magtag.set_background("owl.bmp")
            magtag.set_text('CORRECT!', 0, False)
            magtag.set_text('', 1, False)
            magtag.set_text('Current Streak: ' + str(NUMBER_CORRECT), 2, False)
            magtag.set_text('', 3, False)
            magtag.set_text('', 4, False)
            magtag.set_text('', 5, False)
            magtag.set_text(quizQuestions[WHICH_QUESTION]['question'], 6, False)
            magtag.set_text(quizQuestions[WHICH_QUESTION]['answer'], 7, True)
            if SHOW_LIGHTS == True:
                magtag.peripherals.neopixels.fill(0x002700)
            if PLAY_SOUNDS == True:
                song = ((262, 2),(262, 2),(349,6))
                for notepair in song:
                    magtag.peripherals.play_tone(notepair[0], notepair[1] * 0.2)
            if SHOW_LIGHTS == True:
                magtag.peripherals.neopixels.fill(0xffffff)
            else:
                magtag.peripherals.neopixels.fill(0x000000)
        else:
            magtag.set_background("owl.bmp")
            magtag.set_text('WRONG!', 0, False)
            magtag.set_text('', 1, False)
            magtag.set_text('', 2, False)
            magtag.set_text('', 3, False)
            magtag.set_text('', 4, False)
            magtag.set_text('', 5, False)
            magtag.set_text(quizQuestions[WHICH_QUESTION]['question'], 6, False)
            magtag.set_text(quizQuestions[WHICH_QUESTION]['answer'], 7, True)
            if SHOW_LIGHTS == True:
                magtag.peripherals.neopixels.fill(0x7f0000)
            if PLAY_SOUNDS == True:
                song = ((392, 2),(330, 2),(262,6))
                for notepair in song:
                    magtag.peripherals.play_tone(notepair[0], notepair[1] * 0.2)
            if SHOW_LIGHTS == True:
                magtag.peripherals.neopixels.fill(0xffffff)
            else:
                magtag.peripherals.neopixels.fill(0x000000)
            NUMBER_CORRECT = 0
        time.sleep(0.5)
        displayNextQuestion()
    time.sleep(0.1)