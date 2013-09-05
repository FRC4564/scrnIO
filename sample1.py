# Sample use of scrnio library


import sys, time, math
import scrnio    #copy to /usr/lib/python2.7


try:
    # Initialize the screen
    s = scrnio.screen()
    if s.WIDTH < 80 or s.HEIGHT<25:
    	raise ValueError("Expand console to at least 25 rows by 80 columns")
    # Once color is set, screen dispaly commands and form controls will default to this color
    s.setcolor(s.YELLOW,s.BLACK,s.BOLD)
    # Clear the screen
    s.clear()

    s.setcolor(s.BLUE,s.YELLOW)   
    s.textat(1,1,'SCRNIO Library Sample')

    #Setup a form with input controls
    fin = scrnio.form(s)
    s.setcolor(s.CYAN,s.BLUE,s.BOLD)
    fin.addHBar("Steering",3,3,40,1200,2400,value=2000,delta = 10,type='POINT')
    fin.addHBar("Angular velocity",7,3,length=35,min=0,max=0.3,value=.05,delta=.01)
    # These controls will allow dynamic adjustment of the color of the 'Seconds' output control
    fin.addHBar("FG",3,50,length=8,min=0,max=7,value=7,delta=1)
    fin.addHBar("BG",7,50,length=8,min=0,max=7,value=0,delta=1)

    s.setcolor(s.CYAN,s.RED,s.BOLD)
    fin.addCheckbox("ckbEnable",3,65,"Enable Robot")
    fin.addButton("btnExit",8,65,"Exit",width=10)
    
    # Set the Steering control as being selected (active for input)
    fin.select("Steering")
    fin.show()

    # Setup a second form for output controls
    fout = scrnio.form(s)
    s.setcolor(s.WHITE,s.MAGENTA,s.BOLD)
    fout.addHBar("Seconds",19,11,length=60,min=0,max=59,value=0)
    fout.addHBar("Sine",22,11,length=60,min=-180,max=180,value=0,type='POINT')
    fout.show()

    # Set a box to show keystrokes in    
    s.setcolor(s.WHITE,s.MAGENTA,s.BOLD)
    s.box(13,5,5,75,fill=True,title='Keystrokes',footer='All common keys decoded')
    text = ''
    
    # Turn off the cursor and show the screen for the first time
    s.cursor(False)
    s.refresh()
    
    # Prep for main loop
    keys = ''
    object = ''

    fps = 20
    delay = 1.0 / fps 
    t = time.time() + delay
    
    secs = 0
    rotation = 0

    s.setcolor(s.GREEN,s.BLACK,s.UNDERLINE + s.BOLD)
    
    done = False
    while not done:
        # show seconds in an hbar
        secs += delay
        if secs >= 60:
            secs=0
        fout.controls('Seconds').value = int(secs*10)/10.0
        fg = fin.controls('FG').value
        bg = fin.controls('BG').value
        fout.controls('Seconds').palette(fg,bg,s.BOLD)
        
        # show sine in an hbar
        rotation = rotation + fin.controls('Angular velocity').value
        angle = int(math.sin(rotation)*180)
        fout.controls('Sine').value=angle
        if abs(angle)>160:
            fout.controls('Sine').palette(s.RED,s.RED,s.BOLD)
        elif abs(angle)>90:
            fout.controls('Sine').palette(s.YELLOW,s.BLACK,s.BOLD)
        else:
            fout.controls('Sine').palette(s.GREEN,s.BLACK,s.BOLD)

        # process key input
        key=s.inkey()
        if key != "":           
            text = text + key
            text = text[-70:]
            s.textat(15,7,text)
            # allow input form to process key as well
            result = fin.process(key)
            if result != '':
                done = True
                
        # update the output form
        fout.show()
        s.refresh()

        # throttle loop based on FPS delay
        while time.time() < t:
            s.wait(10)
        t = t + delay

    # Close out the Froms and Screen    
    s.close()
    print result,key
except:    
    s.close()
    raise
