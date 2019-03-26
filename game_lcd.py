#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi
import time
import Adafruit_CharLCD as LCD
import pygame
import math
from random import randint 
import thread
# Raspberry Pi pin setup
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

import curses
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(0,10,"Hit 'q' to quit")
stdscr.refresh()

key = ''
timer = 0
done = False
    


player_x = 8
top_row = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]
bottom_row = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]
def updatescreen():
    global player_x,top_row,bottom_row,done,timer
    top_row = bottom_row
    if top_row[player_x] != " " :
       done = True
       print "Game Over "+str(timer)
       print "You're Time Was:"+str(timer)
       lcd.clear()
       lcd.message(" GAME OVER!! ")
       return
    bottom_row = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]
    for i in range(1,15):
	tree = randint(0,10)
	if tree > math.ceil(10-(timer*0.20)): bottom_row[i] = "^"
    lcd.clear()
    lcd.message("|")
    for i in range(0,player_x-1):
        lcd.message(top_row[i])
    lcd.message("*")
    for i in range(player_x,14):
        lcd.message(top_row[i])
    lcd.message("|\n|")
    for i in range(0,14):
	lcd.message(bottom_row[i])
    lcd.message("|")
        
updatescreen()

def refresh_screen():
    global done,timer
    while not done:
        time.sleep(0.5)
	timer += 0.5
        updatescreen()

thread.start_new_thread(refresh_screen,())

while key != ord('q'):
    key = stdscr.getch()
    stdscr.addch(20,25,key)
    stdscr.refresh()
    if key == curses.KEY_LEFT: 
        player_x -= 1
        if player_x == 0 : 
              player_x = 1
    elif key == curses.KEY_RIGHT: 
        player_x += 1
	if player_x == 15: 
              player_x = 14 

    
curses.endwin()
	
