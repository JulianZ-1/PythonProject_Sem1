
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: n10415483
#    Student name: Jiyan Zhu 
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
# PATIENCE
#
# This assignment tests your skills at processing data stored in
# lists, creating reusable code and following instructions to display
# a complex visual image.  The incomplete Python program below is
# missing a crucial function, "deal_cards".  You are required to
# complete this function so that when the program is run it draws a
# game of Patience (also called Solitaire in the US), consisting of
# multiple stacks of cards in four suits.  See the instruction sheet
# accompanying this file for full details.
#
# Note that this assignment is in two parts, the second of which
# will be released only just before the final deadline.  This
# template file will be used for both parts and you will submit
# your final solution as a single Python 3 file, whether or not you
# complete both parts of the assignment.
#
#--------------------------------------------------------------------#  



#-----Preamble-------------------------------------------------------#
#
# This section imports necessary functions and defines constant
# values used for creating the drawing canvas.  You should not change
# any of the code in this section.
#

# Import the functions needed to complete this assignment.  You
# should not need to use any other modules for your solution.  In
# particular, your solution must NOT rely on any non-standard Python
# modules that need to be installed separately, because the markers
# will not have access to such modules.

from turtle import *
from math import *
from random import *

# Define constant values used in the main program that sets up
# the drawing canvas.  Do not change any of these values.

# Constants defining the size of the card table
table_width = 1100 # width of the card table in pixels
table_height = 800 # height (actually depth) of the card table in pixels
canvas_border = 30 # border between playing area and window's edge in pixels
half_width = table_width // 2 # maximum x coordinate on table in either direction
half_height = table_height // 2 # maximum y coordinate on table in either direction

# Work out how wide some text is (in pixels)
def calculate_text_width(string, text_font = None):
    penup()
    home()
    write(string, align = 'left', move = True, font = text_font)
    text_width = xcor()
    undo() # write
    undo() # goto
    undo() # penup
    return text_width

# Constants used for drawing the coordinate axes
axis_font = ('Consolas', 10, 'normal') # font for drawing the axes
font_height = 14 # interline separation for text
tic_sep = 50 # gradations for the x and y scales shown on the screen
tics_width = calculate_text_width("-mmm -", axis_font) # width of y axis labels

# Constants defining the stacks of cards
stack_base = half_height - 25 # starting y coordinate for the stacks
num_stacks = 6 # how many locations there are for the stacks
stack_width = table_width / (num_stacks + 1) # max width of stacks
stack_gap = (table_width - num_stacks * stack_width) // (num_stacks + 1) # inter-stack gap
max_cards = 10 # maximum number of cards per stack

# Define the starting locations of each stack
stack_locations = [["Stack " + str(loc + 1),
                    [int(-half_width + (loc + 1) * stack_gap + loc * stack_width + stack_width / 2),
                     stack_base]] 
                    for loc in range(num_stacks)]

# Same as Turtle's write command, but writes upside down
def write_upside_down(string, **named_params):
    named_params['angle'] = 180
    tk_canvas = getscreen().cv
    tk_canvas.create_text(xcor(), -ycor(), named_params, text = string)

#
#--------------------------------------------------------------------#



#-----Functions for Creating the Drawing Canvas----------------------#
#
# The functions in this section are called by the main program to
# create the drawing canvas for your image.  You should not change
# any of the code in this section.
#

# Set up the canvas and draw the background for the overall image.
# By default the coordinate axes displayed - call the function
# with False as the argument to prevent this.
def create_drawing_canvas(show_axes = True):

    # Set up the drawing canvas
    setup(table_width + tics_width + canvas_border * 2,
          table_height + font_height + canvas_border * 2)

    # Draw as fast as possible
    tracer(False)

    # Make the background felt green and the pen a lighter colour
    bgcolor('green')
    pencolor('light green')

    # Lift the pen while drawing the axes
    penup()

    # Optionally draw x coordinates along the bottom of the table
    if show_axes:
        for x_coord in range(-half_width + tic_sep, half_width, tic_sep):
            goto(x_coord, -half_height - font_height)
            write('| ' + str(x_coord), align = 'left', font = axis_font)

    # Optionally draw y coordinates to the left of the table
    if show_axes:
        max_tic = int(stack_base / tic_sep) * tic_sep
        for y_coord in range(-max_tic, max_tic + tic_sep, tic_sep):
            goto(-half_width, y_coord - font_height / 2)
            write(str(y_coord).rjust(4) + ' -', font = axis_font, align = 'right')

    # Optionally mark each of the starting points for the stacks
    if show_axes:
        for name, location in stack_locations:
            # Draw the central dot
            goto(location)
            color('light green')
            dot(7)
            # Draw the horizontal line
            pensize(2)
            goto(location[0] - (stack_width // 2), location[1])
            setheading(0)
            pendown()
            forward(stack_width)
            penup()
            goto(location[0] -  (stack_width // 2), location[1] + 4)
            # Write the coordinate
            write(name + ': ' + str(location), font = axis_font)

    #Draw a border around the entire table
    penup()
    pensize(3)
    goto(-half_width, half_height) # top left
    pendown()
    goto(half_width, half_height) # top
    goto(half_width, -half_height) # right
    goto(-half_width, -half_height) # bottom
    goto(-half_width, half_height) # left

    # Reset everything, ready for the student's solution
    pencolor('black')
    width(1)
    penup()
    home()
    tracer(True)


# End the program and release the drawing canvas.
# By default the cursor (turtle) is hidden when the program
# ends - call the function with False as the argument to
# prevent this.
def release_drawing_canvas(hide_cursor = True):
    tracer(True) # ensure any partial drawing in progress is displayed
    if hide_cursor:
        hideturtle()
    done()
    
#
#--------------------------------------------------------------------#



#-----Test Data for Use During Code Development----------------------#
#
# The "fixed" data sets in this section are provided to help you
# develop and test your code.  You can use them as the argument to
# the deal_cards function while perfecting your solution.  However,
# they will NOT be used to assess your program.  Your solution will
# be assessed using the random_game function appearing below.  Your
# program must work correctly for any data set that can be generated
# by the random_game function.
#

# Each of these fixed games draws just one card
fixed_game_0 = [['Stack 1', 'Suit A', 1, 0]]
fixed_game_1 = [['Stack 2', 'Suit B', 1, 0]]
fixed_game_2 = [['Stack 3', 'Suit C', 1, 0]]
fixed_game_3 = [['Stack 4', 'Suit D', 1, 0]]

# Each of these fixed games draws several copies of just one card
fixed_game_4 = [['Stack 2', 'Suit A', 4, 0]]
fixed_game_5 = [['Stack 3', 'Suit B', 3, 0]]
fixed_game_6 = [['Stack 4', 'Suit C', 2, 0]]
fixed_game_7 = [['Stack 5', 'Suit D', 5, 0]]

# This fixed game draws each of the four cards once
fixed_game_8 = [['Stack 1', 'Suit A', 1, 0],
                ['Stack 2', 'Suit B', 1, 0],
                ['Stack 3', 'Suit C', 1, 0],
                ['Stack 4', 'Suit D', 1, 0]]

# These fixed games each contain a non-zero "extra" value
fixed_game_9 = [['Stack 3', 'Suit D', 4, 4]]
fixed_game_10 = [['Stack 4', 'Suit C', 3, 2]]
fixed_game_11 = [['Stack 5', 'Suit B', 2, 1]]
fixed_game_12 = [['Stack 6', 'Suit A', 5, 5]]

# These fixed games describe some "typical" layouts with multiple
# cards and suits. You can create more such data sets yourself
# by calling function random_game in the shell window

fixed_game_13 = \
 [['Stack 6', 'Suit D', 9, 6],
  ['Stack 4', 'Suit B', 5, 0],
  ['Stack 5', 'Suit B', 1, 1],
  ['Stack 2', 'Suit C', 4, 0]]
 
fixed_game_14 = \
 [['Stack 1', 'Suit C', 1, 0],
  ['Stack 5', 'Suit D', 2, 1],
  ['Stack 3', 'Suit A', 2, 0],
  ['Stack 2', 'Suit A', 8, 5],
  ['Stack 6', 'Suit C', 10, 0]]

fixed_game_15 = \
 [['Stack 3', 'Suit D', 0, 0],
  ['Stack 6', 'Suit B', 2, 0],
  ['Stack 2', 'Suit D', 6, 0],
  ['Stack 1', 'Suit C', 1, 0],
  ['Stack 4', 'Suit B', 1, 1],
  ['Stack 5', 'Suit A', 3, 0]]

fixed_game_16 = \
 [['Stack 6', 'Suit C', 8, 0],
  ['Stack 2', 'Suit C', 4, 4],
  ['Stack 5', 'Suit A', 9, 3],
  ['Stack 4', 'Suit C', 0, 0],
  ['Stack 1', 'Suit A', 5, 0],
  ['Stack 3', 'Suit B', 5, 0]]

fixed_game_17 = \
 [['Stack 4', 'Suit A', 6, 0],
  ['Stack 6', 'Suit C', 1, 1],
  ['Stack 5', 'Suit C', 4, 0],
  ['Stack 1', 'Suit D', 10, 0],
  ['Stack 3', 'Suit B', 9, 0],
  ['Stack 2', 'Suit D', 2, 2]]
 
# The "full_game" dataset describes a random game
# containing the maximum number of cards
stacks = ['Stack ' + str(stack_num+1) for stack_num in range(num_stacks)]
shuffle(stacks)
suits = ['Suit ' + chr(ord('A')+suit_num) for suit_num in range(4)]
shuffle(suits)
full_game = [[stacks[stack], suits[stack % 4], max_cards, randint(0, max_cards)]
             for stack in range(num_stacks)]

#
#--------------------------------------------------------------------#



#-----Function for Assessing Your Solution---------------------------#
#
# The function in this section will be used to mark your solution.
# Do not change any of the code in this section.
#
# The following function creates a random data set specifying a game
# of Patience to be drawn.  Your program must work for any data set 
# returned by this function.  The results returned by calling this 
# function will be used as the argument to your deal_cards function 
# during marking. For convenience during code development and marking 
# this function also prints the game data to the shell window.
#
# Each of the data sets generated is a list specifying a set of
# card stacks to be drawn. Each specification consists of the
# following parts:
#
# a) Which stack is being described, from Stack 1 to num_stacks.
# b) The suit of cards in the stack, from 'A' to 'D'.
# c) The number of cards in the stack, from 0 to max_cards
# d) An "extra" value, from 0 to max_cards, whose purpose will be
#    revealed only in Part B of the assignment.  You should
#    ignore it while completing Part A.
#
# There will be up to num_stacks specifications, but sometimes fewer
# stacks will be described, so your code must work for any number
# of stack specifications.
#
def random_game(print_game = True):

    # Percent chance of the extra value being non-zero
    extra_probability = 20

    # Generate all the stack and suit names playable
    game_stacks = ['Stack ' + str(stack_num+1)
                   for stack_num in range(num_stacks)]
    game_suits = ['Suit ' + chr(ord('A')+suit_num)
                  for suit_num in range(4)]

    # Create a list of stack specifications
    game = []

    # Randomly order the stacksx`

    # Create the individual stack specifications 
    for stack in game_stacks:
        # Choose the suit and number of cards
        suit = choice(game_suits)
        num_cards = randint(0, max_cards)
        # Choose the extra value
        if num_cards > 0 and randint(1, 100) <= extra_probability: 
            option = randint(1,num_cards)
        else:
            option = 0
        # Add the stack to the game, but if the number of cards
        # is zero we will usually choose to omit it entirely
        if num_cards != 0 or randint(1, 4) == 4:
            game.append([stack, suit, num_cards, option])
        
    # Optionally print the result to the shell window
    if print_game:
        print('\nCards to draw ' +
              '(stack, suit, no. cards, option):\n\n',
              str(game).replace('],', '],\n '))
    
    # Return the result to the student's deal_cards function
    return game

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
#  Complete the assignment by replacing the dummy function below with
#  your own "deal_cards" function.
#

# Draw the card stacks as per the provided game specification


#Add coordinate to a string
stack_1 = [-449,375]
stack_2 = [-270, 375]
stack_3 = [-91,375]
stack_4 = [88,375]
stack_5 = [267,375]
stack_6 = [446,375]

#Function for the first suit "winnie"
#--------------------------------------------
def draw_winnie ():

    #Drawing the card

    pendown()

    pencolor('black')

    begin_fill()

    fillcolor('#FFFFBC')

    forward(65)

    for turns in range (9):
        right(10)
        forward(1)

    forward(180)

    for turns in range (9):
        right(10)
        forward(1)

    forward(130)

    for turns in range(9):
        right(10)
        forward(1)

    forward(180)

    for turns in range (9):
        right(10)
        forward(1)

    forward(65)

    end_fill()

    #--------------------------------------#
    #End of the card

    #Start of the head
    #--------------------------------------#

    #Go to the head location

    pensize(2)

    penup()

    right(90)

    forward(20)

    color('black')

    right(90)

    pendown()

    #Drawing half of the head (left)

    begin_fill()
    fillcolor('orange')

    for top_head in range (30):
        left(0.5)
        forward(1)

    #Drawing left ear

    right(90)

    circle(10,300)

    #left face
    right(170)

    for left_face in range (25):
        left(1)
        forward(1)

    right(45)
    circle(10,130)

    #bottom face

    left(17)
    forward(80)

    #right face
    circle(10,130)

    right(25)
    for right_face in range (25):
        left(1)
        forward(1)

    #right ear
    right(140)

    circle(10,250)

    forward(5)

    #drawing half of the head (left)


    right(90)

    for top_head in range (30):
        left(1.3)
        forward(1)

    end_fill()

    #Going to the location for the right draw eyebrow

    penup()

    left(180)

    forward(23)

    right(90)

    forward(15)

    pendown()

    right(130)

    #Drawing right eyebrow

    circle(15,65)

    #Going to the location of the left eyebrow

    right(40)


    penup()

    forward(20)

    pendown()

    #Drawing the left eyebrow

    circle(15,65)

    #Going to the location of the left eye

    penup()

    left(45)

    forward(10)

    left(90)

    forward(8)

    #Drawing the left eye

    dot(5)

    #Going to the location of the right eye

    penup()

    right(15)

    forward(33)

    #Drawing the right eye

    dot(5)

    #Going to the location to draw nose

    penup()

    left(180)

    forward(22)

    left(90)

    forward(4)

    #Drawing nose

    pendown()

    begin_fill()

    fillcolor('black')

    left(90)
    
    for nose in range (3):
        forward(13)
        right(120)


    forward(7)
    right(90)
    forward(5)
    dot(12)

    end_fill()

    #Going to the location to draw the mouth

    penup()

    right(90)

    forward(25)

    right(180)

    #Drawing the mouth

    pendown()


    left(45)

    forward(5)

    left(180)

    forward(10)

    left(180)

    forward(5)

    right(100)

    circle(30,110)

    left(90)

    forward(5)

    left(180)

    forward(10)

    left(180)

    forward(5)

    #-----------------------------------------------#

    #End of the head

    #Start of the cloth

    #-----------------------------------------------#

    #Going to the location of the cloth

    penup()

    left(40)

    forward(25)

    left(90)

    forward(19)

    #Drawing cloth (Left)

    pendown()

    begin_fill()
    fillcolor('red')

    right(92)

    forward(25)

    circle(25,80)

    forward(15)

    for left_cloth in range(15):
        left(7)
        forward(1)

    forward(10)

    for left_cloth in range (12):
        left(7)
        forward(1)

    left(10)

    forward(20)

    #Drawing the middle of the cloth

    right(180)

    forward(25)

    for middle_cloth in range (6):
        right(8)
        forward(4)

    left(125)

    forward(60)

    left(110)

    forward(10)

    #Drawing the rightside of the cloth

    for right_cloth in range(4):
        right(8)
        forward(4)

    forward(25)

    right(180)

    forward(19)

    for right_cloth in range (10):
        left(9)
        forward(2)



    circle(13,90)

    forward(20)

    for right_cloth in range (8):
            left(13)
            forward(4)

    left(2)

    forward(40)

    end_fill()

    #-----------------------------------#

    #End of the cloth

    #Start of the bottom body

    #----------------------------------#

    #Going to the location of the bottom body

    penup()

    left(90)

    forward(60)

    right(90)

    forward(30)

    right(270)

    #Drawing the bottom body

    pendown()

    begin_fill()

    fillcolor('orange')

    circle(27,170)

    end_fill()

    #----------------------------------

    #end of bottom body

    #Left and right hands

    #-------------------------------

    #Going to the location of right hand

    penup()

    forward(18)

    right(90)

    forward(3)

    right(90)

    #Drawing the right hand

    pendown()

    begin_fill()

    fillcolor('orange')


    circle(10,185)

    right(27)

    end_fill()

    #Going to the location or left hand

    penup()

    left(120)

    forward(100)

    right(90)

    forward(5)

    left(180)

    #Drawing the left hand

    begin_fill()

    fillcolor('orange')

    pendown()

    circle(10,175)

    end_fill()

    #---------------------------

    #End of drawing two hands

    #Start drawing two legs

    #-----------------------------

    #Going to the location of left leg

    penup()

    right(180)

    forward(30)

    left(90)

    forward(10)

    right(85)


    #Drawing the left leg

    pendown()

    begin_fill()

    forward(20)

    right(180)

    circle(10,270)

    forward(20)

    left(90)

    forward(25)

    end_fill()

    #Going to the location for right leg

    penup()


    right(90)

    forward(20)

    right(90)

    #Drawing right leg

    pendown()

    begin_fill()

    forward(28)

    left(90)

    forward(22)

    circle(10,270)

    left(180)

    forward(24)

    end_fill()

    #Going to the locaiton for the stack
    
    penup()

    forward(80)

    left(90)

    forward(22.8)

    right(93)

    forward(20)

    right(89)
#------------------------------
#End of the first suit function

#Start of the second suit function
#--------------------------------

def draw_piglet():
    #Drawing the card

    pendown()

    color('white', '#640764')

    pensize(3)

    begin_fill()

    forward(65)

    for turns in range (9):
        right(10)
        forward(1)

    forward(180)

    for turns in range (9):
        right(10)
        forward(1)

    forward(130)

    for turns in range(9):
        right(10)
        forward(1)

    forward(180)

    for turns in range (9):
        right(10)
        forward(1)

    forward(65)

    end_fill()

    #---------------------------------------------------------
    #End of drawing card

    #Start of the head 

    #---------------------------------------------------------


    #Going to the location to draw the head

    penup()

    right(90)

    forward(40)

    #Drawing the left part of the head

    pencolor('black')

    pendown()

    begin_fill()

    fillcolor('#FFB3FF')

    right(90)

    circle(25,90)

    forward(5)

    right(45)

    circle(20,136)

    #Drawing the bottom part of the head

    forward(30)


    #Drawing the right part of the head

    circle(20,136)

    right(45)

    forward(5)

    circle(25,90)

    forward(6)

    end_fill()

    #------------------------------------------------
    #End of drawing head

    #Start of drawing two ears
    #------------------------------------------------

    #Going to the location to draw the left ear

    penup()

    forward(7)

    right(50)

    #Drawing the left ear

    pendown()

    begin_fill()

    fillcolor('#EC6DEC')

    forward(4)

    right(20)

    circle(50,30)

    for left_ear in range (10):
        right(10)
        forward(1)

    left(100)

    for left_ear in range (10):
        left(10)
        forward(2)

    for left_ear in range (6):
        left(18)
        forward(7.5)

    end_fill()

    forward(5)

    left(45)

    forward(3)

    left(90)

    forward(7)

    for inside_left_ear in range(10):
        left(7)
        forward(2)

    right(190)

    forward(10)

    left(90)

    for inside_left_ear in range(2):
        right(7)
        forward(3)

    #Going to the location to draw the right ear

    penup()

    right(80)

    forward(35)

    right(90)

    forward(13)

    left(165)

    #Drawing the right ear

    pendown()

    begin_fill()

    forward(8)

    left(40)

    for right_ear in range(6):
        right(1)
        forward(3)

    left(60)

    forward(4)

    right(90)

    forward(5)

    right(90)

    forward(5)

    for right_ear in range(25):
        right(4)
        forward(2)

    end_fill()

    right(90)

    forward(11)

    right(90)

    forward(5)

    for inside_right_ear in range(7):
        left(7)
        forward(3)

    #----------------------------------------------
    #End of drawing ears

    #Start of drawing face
    #---------------------------------------------

    #Going to the location to draw eyebro

    penup()

    left(65)

    forward(34)

    left(90)

    forward(33)

    left(90)

    #Drawing eyebrow

    pendown()

    pencolor('#EC6DEC')

    left(8)

    for eye_brows_left in range(8):
        right(1)
        forward(1)

    #Going to the location to draw the left eyebrow

    penup()

    right(5)


    forward(15)

    #Drawing the righ eyebrow

    pendown()

    left(8)

    for eye_bows_left in range(8):
        right(1)
        forward(1)

    #Going to the location to draw the left eye

    penup()

    right(180)

    forward(30)

    left(90)

    forward(10)

    left(90)

    forward(3)

    #Drawing the left eye

    dot(8,'#980898')

    #Going to the location to draw the right eye

    forward(24)

    #Drawing the right eye

    dot(8,'#980898')

    #Going to the location to draw nose

    left(180)

    forward(10)

    left(90)

    forward(5)

    #Drawing the nose

    pendown()

    pencolor('#EC6DEC')

    left(30)

    begin_fill()

    fillcolor('#EC6DEC')

    for nose in range (3):
        forward(13)
        right(120)

    end_fill()

    right(30)
    forward(7)

    dot(13,'#EC6DEC')

    #Going to the location to draw the mouth

    penup()

    right(90)

    forward(17)

    left(45)

    #Drawing the mouth

    pencolor('black')

    pendown()

    forward(5)

    left(180)

    forward(2.5)

    right(110)

    circle(22,120)

    right(110)

    forward(2.5)

    left(180)

    forward(5)

    #----------------------------------
    #End of drawing face

    #start of the body
    #----------------------------------

    #Going to the location of the body

    penup()

    left(90)

    forward(47)

    left(55)

    #Drawing the body

    pendown()

    begin_fill()

    fillcolor('#CE3E3E')

    forward(40)

    circle(20,180)

    forward(40)

    end_fill()

    #Going to the locaiton to draw cloth

    penup()

    left(90)

    forward(40)

    left(90)


    #Drawing cloth

    for cloth in range(4):
        pendown()
        circle(20,180)
        penup()
        left(90)
        forward(40)
        left(90)
        forward(10)

    #------------------------------
    #End of drawing body

    #Start of drawing arms and hands
    #------------------------------

    #Going to the location to draw left arm

    left(180)

    forward(30)

    left(60)

    #Drawing the left arm

    pendown()

    begin_fill()

    fillcolor('#FFB3FF')

    forward(5)

    for left_arm in range(10):
        left(1)
        forward(3)

    circle(10,180)

    forward(42)

    end_fill()

    #Going the location to draw the right arm

    penup()

    left(21)

    forward(39)

    left(45)

    #Drawing the right arm

    pendown()

    begin_fill()

    forward(40)

    circle(8,180)

    for right_arim in range(10):
        left(2)
        forward(3)

    end_fill()

    #-------------------------------------
    #End of drawing arms

    #Start of drawing legs
    #-----------------------------------------

    #Going to the location of the left leg

    penup()

    right(66)

    forward(35)

    left(90)

    forward(40)

    #Drawing the left leg

    pendown()

    begin_fill()

    fillcolor('#FFB3FF')

    forward(20)

    right(180)

    circle(10,270)

    forward(20)

    left(90)

    forward(25)

    end_fill()

    #Going to the location to draw right leg

    penup()


    right(90)

    forward(10)

    right(90)

    #Drawing the right leg

    pendown()

    begin_fill()

    forward(23)

    left(90)

    forward(22)

    circle(10,270)

    left(180)

    forward(20)

    end_fill()

    #Going to the location for the next stack
    
    penup()

    forward(86)

    left(90)

    forward(21.7)

    right(90)

    forward(20)

    right(89)
#---------------------------------
#End of the second suit function

#Start if the third suit function
#---------------------------------
def draw_tigger():
    #Drawing the card
        pendown()

        color('white', 'cyan')

        pensize(3)

        begin_fill()

        forward(65)

        for turns in range (9):
                right(10)
                forward(1)

        forward(180)

        for turns in range (9):
                right(10)
                forward(1)

        forward(130)

        for turns in range(9):
                right(10)
                forward(1)

        forward(180)

        for turns in range (9):
                right(10)
                forward(1)

        forward(65)

        end_fill()

        #---------------------------------------------------------
        #End of drawing card

        #Start of the head
        #---------------------------------------------------------

        #Going to the location of the head

        pencolor('black')

        penup()

        right(90)

        forward(25)

        #Drawing the left part of the head

        pendown()

        begin_fill()

        fillcolor('#FF8C00')

        right(90)

        circle(25,90)

        forward(5)

        right(45)

        circle(20,136)

        #Drawing the bottom part of the head

        forward(30)

        #Drawing the right part of the head

        circle(20,136)

        right(45)

        forward(5)

        circle(25,90)

        forward(6)

        end_fill()

        #----------------------------------------------------
        #End of the head

        #Start of the ear
        #----------------------------------------------------

        #Going to the location to draw the left ear

        penup()

        left(90)

        forward(10)

        right(90)

        forward(22)

        #Drawing the left ear

        pendown()

        begin_fill()

        fillcolor('#FF8C00')

        forward(18)

        left(90)

        circle(14,86)

        end_fill()

        penup()

        forward(1)

        left(90)

        forward(8)

        left(78)

        pendown()

        pensize(1)

        forward(17)

        pensize(3)

        #Going to the locaiton to draw the right ear

        penup()

        right(176)

        forward(73)

        left(10)

        forward(4)

        #Drawing the righ ear

        pendown()

        begin_fill()

        fillcolor('#FF8C00')

        circle(14,86)

        left(90)

        forward(18)

        end_fill()

        penup()

        left(90)

        forward(6)

        left(90)

        forward(3)

        left(20)

        pendown()

        pensize(1)

        forward(17)

        pensize(3)

        #-------------------------------------------------
        #End of drawing the head

        #Start of the face
        #------------------------------------------------

        #going to the locaiton of the eyebrows

        penup()

        left(164)

        forward(30)

        left(90)

        forward(5)

        right(90)

        forward(35)

        left(270)

        #Drawing the eye brows and eye 

        pendown()   #start of the eye brows

        begin_fill()

        fillcolor('#FFE4B5')

        for eye_brows in range(15):
                right(6)
                forward(1)

        pencolor('#FFE4B5')

        forward(20)

        pencolor('black')

        for eye_brows in range(15):
                right(6)
                forward(1)

        pencolor('#FFE4B5')

        for bottom_eye_brows in range(20):
                right(9)
                forward(3)

        end_fill()     #End of drawing the eyebrows

        penup()

        left(180)

        forward(10)

        left(90)      #Start of drawing the eye

        pencolor('black')

        forward(7)

        dot(7)

        forward(23)

        dot(7)

        #Going to the location to drawt the mouth and nose

        left(180)

        forward(30)

        left(90)

        forward(15)



        #Drawing the nose and the mouth
        pendown()       #Drawing the mouth

        right(40)

        forward(5)

        left(180)

        forward(2.5)

        right(110)

        circle(25,120)

        right(110)

        forward(2.5)

        left(180)

        forward(5)

        penup()

        left(47)        #Going to the location to draw the nose

        forward(18)

        dot(10, '#F08080')      #Drawing the nose

        left(90)

        forward(5)

        pendown()

        pensize(2)

        forward(10)

        #---------------------------------------------------------
        #End of face

        #Start of the body
        #---------------------------------------------------------

        #Going to the location of the body

        penup()

        right(87)

        forward(20)

        left(90)

        forward(10)

        #Drawing the body

        pendown()

        begin_fill()

        fillcolor('#FF8C00')

        forward(30)

        circle(17,180)

        forward(30)

        end_fill()

        penup()

        left(90)

        forward(26)

        left(90)

        pendown()

        begin_fill()

        fillcolor('#FFE4B5')

        forward(25)

        circle(9,180)

        forward(25)

        end_fill()

        #Going to the locaiton to draw pattern

        penup()

        right(90)

        forward(9)

        left(90)

        #Drawing the pattern

        pendown()

        pensize(1)

        for pattern in range (3):
                begin_fill()
                fillcolor('black')
                left(120)
                forward(8)
                left(120)
                forward(8)
                left(120)
                forward(8)
                right(180)
                forward(10)
                right(180)
                end_fill()

        penup()     #Now going to the left side

        left(90)

        forward(35)

        left(90)

        pendown()    #Now drawing the left side pattern

        for pattern in range (3):
                begin_fill()
                fillcolor('black')
                left(120)
                forward(8)
                left(120)
                forward(8)
                left(120)
                forward(8)
                right(180)
                forward(10)
                right(180)
                end_fill()

        #--------------------------------------------------
        #End of drawing the body

        #Start of the hands
        #--------------------------------------------------

        #Going to the location to draw the left hand

        penup()

        pensize(3)

        forward(10)

        right(45)

        #Drawing the left arm and hand

        pendown()

        begin_fill()

        fillcolor('#FF8C00')

        forward(40)

        circle(7,180)

        forward(25)

        end_fill()

        pensize(1) 

        for pattern in range (3): #Drawing the pattern
                begin_fill()
                fillcolor('black')
                left(120)
                forward(8)
                left(120)
                forward(8)
                left(120)
                forward(8)
                right(180)
                forward(10)
                right(180)
                end_fill()

        penup()

        left(90)

        forward(15)

        right(90)

        forward(5)

        right(180)

        pendown()

        for pattern in range (4): #Drawing the pattern
                begin_fill()
                fillcolor('black')
                left(120)
                forward(8)
                left(120)
                forward(8)
                left(120)
                forward(8)
                right(180)
                forward(10)
                right(180)
                end_fill()



        #Going to the location to drawr the right arm and hand

        penup()

        left(135)

        forward(37)

        right(90)

        forward(20)

        left(45)

        #Drawing the hands

        pendown()

        pensize(3)

        begin_fill()

        fillcolor('#FF8C00')

        forward(25)

        circle(7,180)

        forward(40)

        end_fill()

        pensize(1)

        for pattern in range (4): #Drawing the pattern
                begin_fill()
                fillcolor('black')
                left(120)
                forward(8)
                left(120)
                forward(8)
                left(120)
                forward(8)
                right(180)
                forward(10)
                right(180)
                end_fill()

        penup()

        left(90)

        forward(15)

        right(90)

        forward(5)

        right(180)

        pendown()

        for pattern in range (3): #Drawing the pattern
                begin_fill()
                fillcolor('black')
                left(120)
                forward(8)
                left(120)
                forward(8)
                left(120)
                forward(8)
                right(180)
                forward(10)
                right(180)
                end_fill()

        #------------------------------------------------------------
        #End of drawing the body

        #Start of the legs
        #------------------------------------------------------------

        #Going to the location of left leg

        penup()

        forward(28)

        right(135)

        forward(45)

        left(90)

        #Drawing the left leg

        pendown()

        begin_fill()

        fillcolor('#FF8C00')

        pensize(3)

        forward(35)

        right(180)

        circle(10,270)

        forward(20)

        left(90)

        forward(42)

        end_fill()

        pensize(1)

        for pattern in range (4): #Drawing the pattern
                begin_fill()
                fillcolor('black')
                left(120)
                forward(8)
                left(120)
                forward(8)
                left(120)
                forward(8)
                right(180)
                forward(10)
                right(180)
                end_fill()

        #Going to the location to draw the right leg

        penup()

        forward(42)

        right(90)

        forward(5)

        right(90)

        #Drawing the right leg

        pendown()

        pensize(3)

        begin_fill()

        fillcolor('#FF8C00')

        forward(45)

        left(90)

        forward(22)

        circle(10,270)

        left(180)

        forward(37)

        end_fill()

        penup()

        left(90)

        forward(11)

        left(90)

        forward(42)

        for pattern in range (4): #Drawing the pattern
                begin_fill()
                fillcolor('black')
                left(120)
                forward(8)
                left(120)
                forward(8)
                left(120)
                forward(8)
                right(180)
                forward(10)
                right(180)
                end_fill()
        #Going to the locaiton for the next stack

        penup()

        left(270)

        forward(6.7)

        right(90)

        forward(84)

        right(90)
#---------------------------------
#End of the third suit

#Start of the last suit function
#---------------------------------

def draw_rabbit():
    #Drawing the card
        pendown()

        color('white', '#778899')

        pensize(3)

        begin_fill()

        forward(65)

        for turns in range (9):
                right(10)
                forward(1)

        forward(180)

        for turns in range (9):
                right(10)
                forward(1)

        forward(130)

        for turns in range(9):
                right(10)
                forward(1)

        forward(180)

        for turns in range (9):
                right(10)
                forward(1)

        forward(65)

        end_fill()

        #---------------------------------------------------------
        #End of drawing card

        #Start of the head
        #---------------------------------------------------------

        #Going to the location of the head

        pencolor('black')

        penup()

        right(90)

        forward(25)

        #Drawing the left part of the head

        pendown()

        begin_fill()

        fillcolor('#FFF8DC')

        right(90)

        circle(25,90)

        forward(5)

        right(45)

        circle(20,136)

        #Drawing the bottom part of the head

        forward(30)

        #Drawing the right part of the head

        circle(20,136)

        right(45)

        forward(5)

        circle(25,90)

        #Drawing the right part of the head

        forward(6)

        end_fill()

        #------------------------------------------
        #End of the head

        #Start of the ear
        #---------------------------------------------

        #Going to the location of the ear

        penup()

        left(90)

        forward(5)

        right(90)

        forward(20)

        right(20)

        #Drawing the ear

        pendown()

        begin_fill()

        fillcolor('#FFF8DC')

        for left_ear in range (6):
                left(15)
                forward(8)

        forward(10)

        left(140)

        forward(30)

        for left_ear in range(4):
                left(3)
                forward(3)

        end_fill()

        left(45)

        penup()

        forward(5)

        left(115)

        pensize(5)

        pendown()

        pencolor('#FFB6C1')

        forward(10)

        for left_ear in range(9):
                left(3)
                forward(1)

        forward(5)

        #Going to the location to draw the right ear

        penup()

        left(130)

        forward(67)

        left(90)

        forward(17)

        right(90)

        #Drawing the righ ear

        pensize(3)

        pencolor('black')

        begin_fill()

        fillcolor('#FFF8DC')

        pendown()

        left(10)

        forward(5)

        for right_ear in range (6):
                right(15)
                forward(8)

        forward(10)

        right(140)

        forward(30)

        for right_ear in range(4):
                right(3)
                forward(3)

        end_fill()

        penup()

        forward(7)

        right(145)

        pensize(5)

        pendown()

        pencolor('#FFB6C1')

        forward(10)

        for left_ear in range(9):
                right(3)
                forward(1)

        forward(5)

        #Going to the location to draw the eyebrows

        penup()

        right(130)

        forward(65)

        right(95)

        forward(12)

        #Drawing the eyebrows (both)

        pendown()

        pencolor('black')

        pensize(3)

        for eye_brows in range(15):
                right(6)
                forward(1)

        penup()

        forward(20)

        pendown()

        for eye_brows in range(15):
                right(6)
                forward(1)

        #Going to the location to draw the eye

        penup()

        forward(5)

        right(90)

        forward(10)

        #Drawing the eyes(both)

        dot(15,'white')

        dot(5,'black')

        forward(20)

        dot(15,'white')

        dot(5,'black')

        #Going to the locaiton to draw the noise

        penup()

        left(180)

        forward(10)

        right(90)

        forward(15)

        #Drwaing the nose

        dot(15,'#F08080')

        #Going to the locaiton to draw the mouth 

        penup()

        right(90)

        forward(20)

        left(90)

        #Drawing the mouth

        pendown()

        right(40)

        forward(5)

        left(180)

        forward(2.5)

        right(110)

        circle(25,120)

        right(110)

        forward(2.5)

        left(180)

        forward(5)

        #----------------------------------------------------------
        #End of the the head

        #Start of the body
        #---------------------------------------------------------

        #Going to the location to draw the body

        penup()

        left(45)

        forward(35)

        left(93)

        forward(30)

        #Drawing the body

        pendown()

        begin_fill()

        fillcolor('#FFF8DC')

        forward(30)

        circle(17,180)

        forward(30)

        end_fill()

        penup()

        left(90)

        forward(26)

        left(90)

        pendown()

        begin_fill()

        fillcolor('white')

        forward(25)

        circle(9,180)

        forward(25)

        end_fill()


        #----------------------------------------------
        #End of the body

        #Start of the hand
        #----------------------------------------------

        #Going to the location to draw the arm and hand

        penup()

        pensize(3)

        left(90)

        forward(27)

        left(90)

        forward(7)

        right(45)

        #Drawing the left hand and arm

        pendown()

        begin_fill()

        fillcolor('#FFF8DC')

        pensize(3)

        forward(40)

        circle(7,180)

        forward(25)

        end_fill()

        #Going to the location for right arm and hand

        penup()

        right(45)

        forward(38)

        right(45)

        #Drawing the right arm

        pendown()

        pensize(3)

        begin_fill()

        fillcolor('#FFF8DC')

        forward(25)

        circle(7,180)

        forward(40)

        end_fill()

        #--------------------------------------------
        #End of the hands

        #Start of the legs
        #--------------------------------------------

        #Going to the location to draw the left leg

        penup()

        left(45)

        forward(30)

        left(90)

        forward(37)

        #Drawing the left leg

        pendown()

        begin_fill()

        fillcolor('#FFF8DC')

        pensize(3)

        forward(20)

        right(90)

        forward(10)

        right(90)

        circle(10,270)

        forward(30)

        left(90)

        forward(27)

        end_fill()

        #Going to the location to draw the right leg

        penup()

        right(90)

        forward(5)

        right(90)

        #Drawing the right leg

        pendown()

        begin_fill()

        fillcolor('#FFF8DC')

        forward(27)

        left(90)

        forward(30)

        circle(10,270)

        right(90)

        forward(10)

        right(90)

        forward(20)

        end_fill()


        #Going to the location for the next stack
        
        penup()

        forward(80)

        left(90)

        forward(19)

        right(90)

        forward(5)

        right(90)
#------------------------------------
#End of all suit function

#Start of the joyker card
#-----------------------------------------
    
def joyker_card():
    #-----------------------------------------------
    #Drawing the card

    pendown()

    color('white','orange')

    pensize(2)

    begin_fill()
    
    forward(65)

    for turns in range (9):
        right(10)
        forward(1)

    forward(180)

    for turns in range (9):
        right(10)
        forward(1)

    forward(130)

    for turns in range(9):
        right(10)
        forward(1)

    forward(180)

    for turns in range (9):
        right(10)
        forward(1)

    forward(65)

    end_fill()

    #--------------------------------------------------
    #End of drawing card

    #Start of the body
    # ---------------------------------------------------

    #Going to the location to draw the head

    penup()

    right(90)

    forward(20)

    #Drawing the head

    pencolor('black')

    pendown()

    begin_fill()

    fillcolor('#A0522D')

    right(90)

    circle(25,90)

    forward(5)

    right(45)

    circle(20,136)

    #Drawing the bottom part of the head

    forward(30)

    #Drawing the right part of the head

    circle(20,136)

    right(45)

    forward(5)

    circle(25,90)

    #Drawing the right part of the head

    forward(6)

    end_fill()

    #---------------------------------------------
    #End of the head

    #Start of the ear
    #---------------------------------------------

    #going to the location of left ear

    penup()

    left(90)

    forward(5)

    right(90)

    forward(20)

    right(35)

    #Drawing the left ear

    pendown()

    begin_fill()
    
    fillcolor('pink')

    for left_ear in range (7):
        forward(3)
        right(4)

    circle(10,150)

    for left_ear in range(27):
        forward(2)
        left(2)
    
    end_fill()
    
    left(110)

    penup()

    forward(20)

    left(50)

    pendown()

    forward(5)

    for left_ear in range(10):
        right(3)
        forward(2)

    left(180)

    for left_ear in range(10):
        left(3)
        forward(2)
    
    forward(5)

    left(180)

    forward(10)

    for left_ear in range(7):
        left(5)
        forward(3)

    #Going to the location to draw right ear

    penup()

    right(183)

    forward(93)

    left(45)

    #Drawing the right ear

    begin_fill()
    
    fillcolor('pink')

    pendown()

    for right_ear in range(20):
        forward(2)
        left(4)

    forward(15)

    circle(10,150)

    forward(23)

    end_fill()

    left(45)

    penup()

    forward(15)

    left(90)

    pendown()

    for right_ear in range(15):
        left(4)
        forward(2)

    right(180)

    for right_ear in range(15):
        right(4)
        forward(2)

    right(180)

    for right_ear in range(8):
        right(7)
        forward(2)

    #Going to the location to draw the eye

    penup()

    right(180)

    forward(25)

    left(30)

    forward(10)

    #Drawing the eye

    dot(7)

    forward(23)

    dot(7)
    
    #Going to the location to draw the nose

    penup()

    right(180)

    forward(12)

    right(90)

    forward(12)

    #Drawing the nose

    dot(8)

    #Going to the location of the mouth

    right(90)

    forward(20)

    left(90)


    #Drawing the mouth

    pendown()

    right(40)

    forward(5)

    left(180)

    forward(2.5)

    right(110)

    circle(25,120)

    right(110)

    forward(2.5)

    left(180)

    forward(5)

    #----------------------------------------------------
    #End of the head

    #Start of the second head
    #---------------------------------------------------

    #Going to the location to draw the second head

    penup()

    left(48)

    forward(30)

    left(90)

    forward(70)

    #Drawing the head

    pencolor('black')

    pendown()

    begin_fill()

    fillcolor('#A0522D')

    right(90)

    circle(25,90)

    forward(5)

    right(45)

    circle(20,136)

    #Drawing the bottom part of the head

    forward(30)

    #Drawing the right part of the head

    circle(20,136)

    right(45)

    forward(5)

    circle(25,90)

    #Drawing the right part of the head

    forward(6)

    end_fill()

    #---------------------------------------------
    #End of the head

    #Start of the ear
    #---------------------------------------------

    #Going to the location of left ear

    penup()

    left(90)

    forward(5)

    right(90)

    forward(20)

    right(35)

    #Drawing the left ear

    pendown()

    begin_fill()
    
    fillcolor('pink')

    for left_ear in range (7):
        forward(3)
        right(4)

    circle(10,150)

    for left_ear in range(27):
        forward(2)
        left(2)
    
    end_fill()
    
    left(110)

    penup()

    forward(20)

    left(50)

    pendown()

    forward(5)

    for left_ear in range(10):
        right(3)
        forward(2)

    left(180)

    for left_ear in range(10):
        left(3)
        forward(2)
    
    forward(5)

    left(180)

    forward(10)

    for left_ear in range(7):
        left(5)
        forward(3)

    #Going to the location to draw right ear

    penup()

    right(183)

    forward(93)

    left(45)

    #Drawing the right ear

    begin_fill()
    
    fillcolor('pink')

    pendown()

    for right_ear in range(20):
        forward(2)
        left(4)

    forward(15)

    circle(10,150)

    forward(23)

    end_fill()

    left(45)

    penup()

    forward(15)

    left(90)

    pendown()

    for right_ear in range(15):
        left(4)
        forward(2)

    right(180)

    for right_ear in range(15):
        right(4)
        forward(2)

    right(180)

    for right_ear in range(8):
        right(7)
        forward(2)

    #Going to the location to draw the eye

    penup()

    right(180)

    forward(25)

    left(30)

    forward(10)

    #Drawing the eye

    dot(7)

    forward(23)

    dot(7)
    
    #Going to the location to draw the nose

    penup()

    right(180)

    forward(12)

    right(90)

    forward(12)

    #Drawing the nose

    dot(8)

    #Going to the location

    right(90)

    forward(20)

    left(90)


    #Drawing the mouth

    pendown()

    right(40)

    forward(5)

    left(180)

    forward(2.5)

    right(110)

    circle(25,120)

    right(110)

    forward(2.5)

    left(180)

    forward(5)

    #Going to the next stack

    penup()

    left(60)

    forward(8)

    right(91)

    forward(100)

    right(95)
#-------------------------------
#End of the joyker card, END OF ANY DRAWING COMMAND

#Start of the deal_Card function
#----------------------------------------

#Below are the function for the dealing all the cards
def deal_cards(stacklocation_suit_joyker):
    for deck_stack in stacklocation_suit_joyker:
        if deck_stack[0] == 'Stack 1':  #If the first thing on the list is Stack 1
            goto(stack_1)               #Go to the stack 1 postion
            for num_of_cards in range (deck_stack[2]):  
                #Decide what suit to draw
                    if deck_stack[1] == 'Suit A':
                        #Choose when to draw the joyker card
                        if deck_stack[3] == num_of_cards + 1:
                            joyker_card()
                        else:
                            draw_winnie() 
                    elif deck_stack[1] == 'Suit B':
                        if deck_stack[3] == num_of_cards + 1:
                            joyker_card()
                        else:
                            draw_piglet()
                    elif deck_stack[1] == 'Suit C':
                        if deck_stack[3] == num_of_cards + 1:
                            joyker_card()
                        else:
                            draw_tigger()
                    elif deck_stack[1] == 'Suit D':
                        if deck_stack[3] == num_of_cards + 1:
                            joyker_card()
                        else:
                            draw_rabbit()
                    

                            
        elif deck_stack[0] == 'Stack 2':
            goto(stack_2)
            for num_of_cards in range (deck_stack[2]):
                if deck_stack[1] == 'Suit A':
                        if deck_stack[3] == num_of_cards + 1:
                            joyker_card()
                        else:
                            draw_winnie() 
                elif deck_stack[1] == 'Suit B':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                            draw_piglet()
                elif deck_stack[1] == 'Suit C':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_tigger()
                elif deck_stack[1] == 'Suit D':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_rabbit()

        elif deck_stack[0] == 'Stack 3':
            goto(stack_3)
            for num_of_cards in range (deck_stack[2]):
                if deck_stack[1] == 'Suit A':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_winnie() 
                elif deck_stack[1] == 'Suit B':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_piglet()
                elif deck_stack[1] == 'Suit C':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_tigger()
                elif deck_stack[1] == 'Suit D':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_rabbit()

        elif deck_stack[0] == 'Stack 4':
            goto(stack_4)
            for num_of_cards in range (deck_stack[2]):
                if deck_stack[1] == 'Suit A':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_winnie() 
                elif deck_stack[1] == 'Suit B':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_piglet()
                elif deck_stack[1] == 'Suit C':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_tigger()
                elif deck_stack[1] == 'Suit D':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_rabbit()

        elif deck_stack[0] == 'Stack 5':
            goto(stack_5)
            for num_of_cards in range (deck_stack[2]):
                if deck_stack[1] == 'Suit A':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_winnie() 
                elif deck_stack[1] == 'Suit B':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                            draw_piglet()
                elif deck_stack[1] == 'Suit C':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_tigger()
                elif deck_stack[1] == 'Suit D':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_rabbit()
                        
        elif deck_stack[0] == 'Stack 6':
            goto(stack_6)
            for num_of_cards in range (deck_stack[2]):
                if deck_stack[1] == 'Suit A':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_winnie() 
                elif deck_stack[1] == 'Suit B':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_piglet()
                elif deck_stack[1] == 'Suit C':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_tigger()
                elif deck_stack[1] == 'Suit D':
                    if deck_stack[3] == num_of_cards + 1:
                        joyker_card()
                    else:
                        draw_rabbit()

    
                    


                
                
            
        
        

#
#--------------------------------------------------------------------#


#-----Main Program---------------------------------------------------#
#
# This main program sets up the background, ready for you to start
# drawing the card game.  Do not change any of this code except
# as indicated by the comments marked '*****'.
#

# Set up the drawing canvas
# ***** Change the default argument to False if you don't want to
# ***** display the coordinates and stack locations
create_drawing_canvas()



# Control the drawing speed
# ***** Modify the following argument if you want to adjust
# ***** the drawing speed
speed('fastest')

# Decide whether or not to show the drawing being done step-by-step
# ***** Set the following argument to False if you don't want to wait
# ***** while the cursor moves around the screen
tracer(False)

# Give the drawing canvas a title
# ***** Replace this title with a description of your cards' theme
title("WInnie The Pooh")

### Call the student's function to draw the game
### ***** While developing your program you scan call the deal_cards
### ***** function with one of the "fixed" data sets, but your
### ***** final solution must work with "random_game()" as the
### ***** argument to the deal_cards function.  Your program must
### ***** work for any data set that can be returned by the
### ***** random_game function.
#deal_cards(fixed_game_0) # <-- used for code development only, not marking
#deal_cards(full_game) # <-- used for code development only, not marking
deal_cards(random_game()) # <-- used for assessment

# Exit gracefully
# ***** Change the default argument to False if you want the
# ***** cursor (turtle) to remain visible at the end of the
# ***** program as a debugging aid
release_drawing_canvas()



#
#--------------------------------------------------------------------#
