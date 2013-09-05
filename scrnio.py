import curses

class screen:

    def __init__(self):
        #
        # Define Constants
        # attributes
        self.BOLD       = curses.A_BOLD
        self.UNDERLINE  = curses.A_UNDERLINE
        self.REVERSE    = curses.A_REVERSE
        self.BLINK      = curses.A_BLINK
        # colors
        self.BLACK      = curses.COLOR_BLACK
        self.RED        = curses.COLOR_RED
        self.GREEN      = curses.COLOR_GREEN
        self.YELLOW     = curses.COLOR_YELLOW
        self.BLUE       = curses.COLOR_BLUE
        self.MAGENTA    = curses.COLOR_MAGENTA
        self.CYAN       = curses.COLOR_CYAN
        self.WHITE      = curses.COLOR_WHITE
        #
        # Inititalize screen and keyboard 
        self.scr = curses.initscr()  # Initializes the 'curses' screen
        curses.noecho()              # Disables echoing of keystrokes
        curses.cbreak()              # Sets keyboard input mode to single character
        self.scr.nodelay(1)          # No wait for getch(). If no input available, returns curses.ERR
        self.scr.keypad(True)        # Capture non-ASCII keystrokes as cursor KEY values (ex: KEY_BACKSPACE)
        #
        # Establish color pairs - init all 64 possible combinations
        curses.start_color()         # Enable colors
        for fgcolor in range(0,8):
            for bgcolor in range(0,8):
                pairnum = fgcolor * 8 + bgcolor + 1
                curses.init_pair(pairnum,fgcolor,bgcolor)
        #
        # Window constants
        self.SETCOLOR = curses.color_pair(0)
        self.HEIGHT = self.scr.getmaxyx()[0] - self.scr.getbegyx()[0]   #Last row of terminal reserved
        self.WIDTH = self.scr.getmaxyx()[1] - self.scr.getbegyx()[1] - 1
        #
        # Special purpose Key values used by inkey() function
        self.KEYS = { 9:'TAB',
                     10:'ENTER',
                    258:'DOWN',
                    259:'UP',
                    260:'LEFT',
                    261:'RIGHT',
                    263:'BACKSPACE',
                    265:'NUMLOCK',
                    266:'KP/',
                    267:'KP*',
                    268:'KP-',
                    269:'F5',
                    270:'F6',
                    271:'F7',
                    272:'F8',
                    273:'F9',
                    274:'F10',
                    275:'F11',
                    276:'F12',
                    330:'DELETE',
                    331:'INSERT',
                    338:'PGDN',
                    339:'PGUP',
                    343:'KPENTER',
                    353:'BACKTAB'}

        
    # Properly close out of 'curses' window.
    # Failing to 'close' may require you to reset terminal. Enter 'reset' at shell prompt.
    def close(self):
        self.scr.nodelay(0)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def clear(self):
        self.scr.bkgd(' ',self.SETCOLOR)
        self.scr.clear()
        
    # Combine color pair and attributes into color palette value.
    # This will work with all Curses command that accept a color pair.
    def calcpalette(self,fgcolor,bgcolor,attributes=0):
        return fgcolor * 2048 + bgcolor * 256 + 256 + attributes

    # Set default color, used by all screen functions    
    def setcolor(self,fgcolor,bgcolor=0,attributes=0):
        # Set active color and atrributes.
        self.SETCOLOR = self.calcpalette(fgcolor,bgcolor,attributes)

    # Move cursor to
    def moveto(self,row,col):
        self.scr.move(row,col)
        
    # print text string at current cursor position 
    def text(self,text):
        self.scr.addstr(str(text),self.SETCOLOR)

    # print text string at specified position 
    def textat(self,row,col,text):
        self.scr.addstr(row,col,str(text),self.SETCOLOR)

    # Print horizontal line of characters starting at cursor and drawing right.
    # Cursor moved to end of line.
    def Hline(self,length,palette=0,ch=0):
        if ch == 0:
            ch = curses.ACS_HLINE
        if palette == 0:
            palatte = self.SETCOLOR
        self.scr.attrset(palette)
        self.scr.hline(ch,length)
        row,col = self.scr.getyx()
        col += length
        if col > self.WIDTH:
            self.scr.move(row,self.WIDTH)
        else:
            self.scr.move(row,col)
            
    # Print vertical line of characters starting at cursor and drawing down.
    # Cursor moved to bottow of line.
    def Vline(self,height,palette=0,ch=0):
        if ch == 0:
            ch = curses.ACS_VLINE
        if palette == 0:
            palatte = self.SETCOLOR
        self.scr.attrset(palette)
        self.scr.vline(ch,height)
        row,col = self.scr.getyx()
        row += height
        if row > self.HEIGHT:
            self.scr.move(self.HEIGHT,col)
        else:
            self.scr.move(row,col)
        
        
    def box(self,rowstart,colstart,height,width,fill=False,border=True,title='',footer='',palette=0):
        # 
        colend = colstart + width - 1
        rowend = rowstart + height - 1
        insidewidth = width - 2
        insideheight = height - 2
        if palette == 0:
            palette = self.SETCOLOR
        #
        if insidewidth >= 0 and insideheight >= 0:
            if fill:
                str = ' ' * width
                for row in range(0,height):
                    self.textat(rowstart+row,colstart+1,str)
            if border:    
                # top row
                self.scr.addch(rowstart,colstart,curses.ACS_ULCORNER,palette)
                self.Hline(insidewidth,palette,' ')
#                for ch in range(0,insidewidth):
#                    self.scr.addch(curses.ACS_HLINE,palette)
                self.scr.addch(curses.ACS_URCORNER,palette)
                # vertical lines - fill or no fill
                self.moveto(rowstart+1,colend)
                self.Vline(insideheight,palette)
                self.moveto(rowstart+1,colstart)
                self.Vline(insideheight,palette)
#                for rows in range(1,insideheight+1):
#                    self.scr.addch(rowstart + rows, colstart, curses.ACS_VLINE,palette)
#                    self.scr.addch(rowstart + rows, colend, curses.ACS_VLINE,palette)
                # bottom row
                self.scr.addch(curses.ACS_LLCORNER,palette)
                self.Hline(insidewidth,palette,' ')
#                for ch in range(0,insidewidth):
#                    self.scr.addch(curses.ACS_HLINE,palette)
                self.scr.addch(curses.ACS_LRCORNER,palette)           
            # title on top row
            if title != '':
                self.scr.addstr(rowstart,colstart + 1,title,palette)
            # footer on bottom row - right justified
            if footer != '':
                self.scr.addstr(rowend,colend - len(footer),footer,palette)
                
    def inkey(self):
        key = self.scr.getch()
        # If no key pressed, return null
        if key == curses.ERR:
            return ''
        # Printable ASCII character
        elif key >= 32 and key <= 126:
            return chr(key)
        # Control key sequence
        elif key >=1 and key <= 26:
            if key == 9:
                return 'TAB'
            if key == 10:
                return 'ENTER'
            return 'CTRL-' + chr(key + 64)
        # Escape sequence
        elif key == 27:
            # upto 5 total characters can be in sequence.
            # ESC can be by itself, with a sequence of 2 or more characters 
            key2 = self.scr.getch()
            if key2 == curses.ERR:
                return 'ESC'
            # sequence will have at least one more character
            key3 = self.scr.getch()
            if key3 == curses.ERR:
                return ''
            # Numeric keypad sequence - <ESC>O<?>
            if chr(key2) == 'O':
                if key3 == 108:
                    return 'KP+'
                if key3 == 110:
                    return 'KP.'
                if key3 >= 112 and key3 <= 121:
                    return 'KP' + str(key3 - 112)
                return ''
            # Shift or Ctrl Arrow sequences - <ESC>[<?>
            # Home and End key sequences - <ESC>[<?>~
            # Function F1-F4 key sequences - <ESC>[1<?>~
            if chr(key2) == '[':
                if key3 == 65:
                    return 'SHIFT-UP'
                if key3 == 66:
                    return 'SHIFT-DOWN'
                if key3 == 67:
                    return 'SHIFT-RIGHT'
                if key3 == 68:
                    return 'SHIFT-LEFT'
                # sequence must be 4 or perhaps 5 chars
                key4 = self.scr.getch()
                if key4 == curses.ERR:
                    return 'ERR CH 4'
                if key3 == 49 and chr(key4) == '~':
                    return 'HOME'
                if key3 == 52 and chr(key4) == '~':
                    return 'END'
                # perhaps it is a 5 char function key sequence
                if chr(key3) == '1':
                    key5 = self.scr.getch()
                    if key5 == curses.ERR:
                        return 'ERR CH 5'
                    if chr(key5) == '~':
                        return 'F'+chr(key4)
                    return '<ESC-UNKNOWN>'
        else:
            try:
                return self.KEYS[key]
            except:
                return ''
#               return '<'+str(key)+'>'  #uncomment line to test key untrapped values
            
    def wait(self,ms):
        curses.napms(ms)

    def cursor(self,flag):
        curses.curs_set(flag)  # Show (True) or Hide (False) cursor

    def refresh(self):
        if self.scr.is_wintouched():
            self.scr.refresh()



class form:
    def __init__(self,scrn):
        self.scrn = scrn
        self.CONTROLS = []
        self.NAMES = []
        self.selected = 0
        self.actionkeys = ('F10','ESC')
        self.moveprevkeys = ('LEFT','UP','BACKTAB')
        self.movenextkeys = ('RIGHT','DOWN','TAB','ENTER')

    def addButton(self,ctlname,row,col,text,width=0):
        self.NAMES.append(ctlname)
        self.CONTROLS.append(button(self,row,col,text,width))

    def addHBar(self,ctlname,row,col,length,min,max,value,delta=0,type='FILL'):
        self.NAMES.append(ctlname)
        self.CONTROLS.append(hbar(self,row,col,length,min,max,value,delta,type,name=ctlname))

    def addCheckbox(self,ctlname,row,col,text='',value=False,size=0):
        self.NAMES.append(ctlname)
        if text == '':
            text = ctlname
        self.CONTROLS.append(checkbox(self,row,col,text,value,size))
        
    def select(self,ctlname):
        self.CONTROLS[self.selected].select(False)
        self.selected = self.NAMES.index(ctlname)
        self.CONTROLS[self.selected].select(True)

    # return reference to named control
    def controls(self,ctlname):
        index = self.NAMES.index(ctlname)
        return self.CONTROLS[index]
        
    # Update controls and process keys
    def process(self,key):
        # ignore empty key
        if key == '':
            return ''
        # Allow selected control to process key
        result = self.CONTROLS[self.selected].process(key)
        # If ACTION was taken, then return with control name, so calling process can react
        if result == "ACTION":
            return self.NAMES[self.selected]
        # If ACCEPTED is returned, then key was processed, so do no more and return nothing
        if result == "ACCEPTED":
            return ''
        # Otherwise process the key to see if Movement, or Form exit chosen
        if key in self.movenextkeys:
            self.CONTROLS[self.selected].select(False)
            self.selected += 1
            if self.selected == len(self.CONTROLS):
                self.selected = 0
            self.CONTROLS[self.selected].select(True)
            return ''
        if key in self.moveprevkeys:
            self.CONTROLS[self.selected].select(False)
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.CONTROLS) - 1
            self.CONTROLS[self.selected].select(True)
            return ''
            
    def show(self):
        for obj in self.CONTROLS:
            obj.show()
        self.scrn.refresh()
        
           

class button:
    def __init__(self,form,row,col,text,width=0):
        self.form = form
        self.scrn = form.scrn
        self.row = row
        self.col = col
        self.text = text
        if width == 0:
            self.width = len(text)+4
        else:
            self.width = width
            if self.width < len(text)+4:
                self.width = len(text)+4
        self.colornormal = self.scrn.SETCOLOR 
        self.colorselected = self.scrn.SETCOLOR ^ self.scrn.REVERSE
        self.selected = False
        self.actionkeys = ('ENTER',' ')

    def show(self):
        savecolor = self.scrn.SETCOLOR

        # how many additional spaces need to fit self.width
        spaces = self.width - len(self.text) - 4

        self.scrn.SETCOLOR = self.colornormal
        self.scrn.textat(self.row,self.col,"< ")
        self.scrn.text(" " * int(spaces/2.0 + .5))
        
        if self.selected:
            self.scrn.SETCOLOR = self.colorselected
            self.scrn.text(self.text)
            self.scrn.SETCOLOR = self.colornormal
        else:
            self.scrn.text(self.text)

        self.scrn.text(" " * int(spaces/2))         
        self.scrn.text(" >")
        
        self.scrn.SETCOLOR = savecolor

    def select(self,flag):
        if flag != self.selected:
            self.selected = flag
            self.show()
        
    def process(self,key):
        if key in self.actionkeys:
            return 'ACTION'
        else:
            return ''


class hbar:
    def __init__(self,form,row,col,length,min,max,value,delta=0,type='FILL',name=''):
        self.form = form
        self.scrn = form.scrn
        self.row = row
        self.col = col
        self.length = length
        self.min = min
        self.max = max
        self.value = value
        self.range = max - min
        self.name = name
        if delta == 0:       # delta is the amount of change per keystroke
            self.delta = float(self.range) / self.length
        else:
            self.delta = delta
        self.type = type   # FILL=fill bar from L to R, POINT=point indicator along bar
        self.labelpos = 'BOTTOM'  # Show current value at TOP or BOTTOM center, LEFT or RIGHT ends, or INSIDE
        self.colornormal = self.scrn.SETCOLOR 
        self.colorselected = self.scrn.SETCOLOR ^ self.scrn.REVERSE
        self.selected = False
        self.actionkeys = ()
        self.decreasekeys = ('LEFT','KP-','-')
        self.increasekeys = ('RIGHT','KP+','+')

    def show(self):
        # Draw box
        pal = self.colornormal
        self.scrn.box(self.row,self.col,3,self.length+2,fill=False,title=self.name,palette=pal)
        # Draw bar - color based on selected flag
        if self.selected:
            pal = self.colorselected
        # Calculate postition of value along length of bar
        cells = int(round(float(self.value - self.min) / self.range * self.length))
        # Show bar
        self.scrn.moveto(self.row+1,self.col+1)
        if self.type == 'FILL':
            if cells == 0:   #special case when value=min, we want bar to appear in range
                cells = 1
                self.scrn.scr.addch(curses.ACS_LTEE,pal)
            else:
                self.scrn.Hline(cells,pal,curses.ACS_CKBOARD)
            self.scrn.Hline(int(self.length - cells),pal)
        else:
            # Type POINTER
            self.scrn.Hline(self.length,pal)
            if cells == self.length:   #special case when value=max, we want bar to appear in range
                cells -= 1
            self.scrn.moveto(self.row + 1,self.col + cells + 1)
            self.scrn.scr.addch(curses.ACS_PLUS,pal)
        # Center text value
        center = (self.col + self.length/2) - len(str(self.value))/2
        self.scrn.scr.addstr(self.row+2,center,' '+str(self.value)+' ', pal)

    def select(self,flag):
        if flag != self.selected:
            self.selected = flag
            self.show()
        
    def process(self,key):
        if key in self.actionkeys:
            return 'ACTION'
        if key in self.decreasekeys:
            self.value -= self.delta
            if self.value < self.min:
                self.value = self.min
            self.show()
            return 'ACCEPTED'
        if key in self.increasekeys:
            self.value += self.delta
            if self.value > self.max:
                self.value = self.max
            self.show()
            return 'ACCEPTED'
        else:
            return ''

    def palette(self,fgcolor,bgcolor,attributes=0):
        self.colornormal = self.scrn.calcpalette(fgcolor,bgcolor,attributes) 
        self.colorselected = self.colornormal ^ self.scrn.REVERSE



class checkbox:
    def __init__(self,form,row,col,text,value=False,size=0):
        self.form = form
        self.scrn = form.scrn
        self.row = row
        self.col = col
        self.text = text
        if size == 0:
            self.size = len(text)+5
        else:
            self.size = size
        self.value = value
        self.colornormal = self.scrn.SETCOLOR 
        self.colorselected = self.scrn.SETCOLOR ^ self.scrn.REVERSE
        self.selected = False
        self.actionkeys = ()
        self.changekeys = (' ','ENTER','KPENTER')

    def show(self):
        # Check box format [x] Text
        if self.selected:
            pal = self.colorselected
        else:
            pal = self.colornormal
        if self.value:
            t = '[x] '
        else:
            t = '[ ] '
        self.scrn.scr.addstr(self.row,self.col,t,self.colornormal)
        self.scrn.scr.addstr(self.text,pal)
    
    def select(self,flag):
        if flag != self.selected:
            self.selected = flag
            self.show()
        
    def process(self,key):
        if key in self.actionkeys:
            return 'ACTION'
        if key in self.changekeys:
            self.value = not self.value
            self.show()
            return 'ACCEPTED'
        else:
            return ''

    def palette(self,fgcolor,bgcolor,attributes=0):
        self.colornormal = self.scrn.calcpalette(fgcolor,bgcolor,attributes) 
        self.colorselected = self.colornormal ^ self.scrn.REVERSE
