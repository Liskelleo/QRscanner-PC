# Intro
This is my first contact with machine vision, based on opencv-python to write a small program.

# QRscanner-PC
A python script to support QR code recognition on a PC

# Required packages and environment configuration
see `requires.txt`

# Issues
By changing the param `self.creationflags` in `~/Lib/site-packages/selenium/webdriver/commom/service.py` in line 47 from `0` to `134217728`.
The cmd display prompt box is hidden, but it leads to a headache problem:
When pressing the 'esc' key after scanning the code to enter, the web page will be blocked for a period of time (about 10s).

# Contact
e-mail address: liskello_o@Outlook.com 
