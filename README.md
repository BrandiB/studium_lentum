# studium lentum
Adafruit MagTag Vocabulary Quiz Program.

"The Adafruit MagTag combines the new ESP32-S2 wireless module and a 2.9" grayscale E-Ink display to make a low-power IoT display that can show data on its screen even when power is removed!"  Came as part of Adabox017.

I programmed mine to be a flashcard quiz program.  Constant exposure to vocabulary is a good thing, so this way the user can answer a question or two when getting a snack out of the refrigerator. 

Graphics taken from an abandoned project of mine from a few years back (Athena Noctua).  Words taken from Wheelock's Latin, 6th Edition, vocabulary lists.

The user is presented with a word and two choices (A and B).  When the choice is made, the screen updates to inform the user whether the answer was correct or not before displaying the next word.  Additional grammatical information can be toggled on or off with the "Extra" button.  The "Setup" button allows the user to toggle on/off the NeoPixel lights and sound, which provide sensory flair when the answer is graded.  They can also select the level the questions should be drawn from (lessons 1 through 40, in groups of 5).

I modified the 18-pt font file that came on the MagTag: the lowercase "t" was not in line with the other letters, and it bothered me, so I edited the BDF file to bring it in line with the other letters.  

I originally had planned to make this a Japanese flashcard program, but quickly realized that the BDF file necessary for displaying Kanji and Kana would exceed the MagTag's storage space. So I may adapt this code in the future for a different board with that goal in mind.

A full write-up of this project will be forthcoming at http://encyclopaedia-fortuita.com
