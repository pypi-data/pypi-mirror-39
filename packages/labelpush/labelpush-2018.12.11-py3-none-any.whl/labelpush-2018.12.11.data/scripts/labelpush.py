#!python
# -*- mode: python -*-
#
# LabelPush - Simple lightweight label printing app
# Copyright (C) 2018 Matteljay-at-pm-dot-me
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Donate if you find this app useful, educational or you like to motivate more projects like this.
#
# XMR:  4B6YQvbL9jqY3r1cD3ZvrDgGrRpKvifuLVb5cQnYZtapWUNovde7K5rc1LVGw3HhmTiijX21zHKSqjQtwxesBEe6FhufRGS
# DASH: XnMLmmisNAyDMT3Sr1rhpfAPfkMjDyUiwJ
# NANO: xrb_3yztgrd4exg16r6dwxwc64fasdipi81aoe8yindsin7o31trqsgqanfi9fym
# ETH:  0x7C64707BD877f9cFBf0B304baf200cB1BB197354
# BTC:  14VZcizduTvUTesw4T9yAHZ7GjDDmXZmVs
#

# IMPORTS
# Kivy cross platform graphical user interface
from kivy import __version__ as KIVY_VERSION
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.properties import ConfigParser
# Python Imaging Library
from kivy.core.image import Image as CoreImage
from PIL import Image as pilImage
from PIL import ImageDraw, ImageFont, PILLOW_VERSION
# Threading
from kivy.clock import mainthread, Clock
from threading import Thread, Event
from time import sleep
import datetime
# Regular expressions
import re
# System
from io import BytesIO
from subprocess import Popen, PIPE
from pathlib import Path
import os
import sys
import shutil

name = 'labelpush'
version = '2018.12.11'
def_defaultcfg = {
    'lpname': 'default', # printer name
    'labw': 637, # labelwidth
    'labh': 295, # labelheight
    'font': 'DejaVuSans', # font selection
    'minfos': 32, # minimal font size
    'splitsep': 60, # split mode separation distance
    'multimod': 0, # multiple image modi
    'focorr': 0.20, # font height offset correction
}
def_font_pool = [ 'DejaVuSans', 'DejaVuSans-Bold', 'DejaVuSansMono', 'DejaVuSerif', 'DejaVuSerifCondensed' ]
def_jsondata = '''[
    { "type": "title", "title": "Printing" },
    { "type": "options", "title": "lp printername", "desc": "List of available printers from 'lpstat'",
    "section": "settings", "key": "lpname", "options": ["default"] },
    { "type": "title", "title": "Label size and style" },
    { "type": "numeric", "title": "Label width", "desc": "Horizontal resolution, paper size is set via CUPS! http://localhost:631",
    "section": "settings", "key": "labw" },
    { "type": "numeric", "title": "Label height", "desc": "Vertical resolution, current ratio set for 2+1/8 x 1 inch or 54x25 mm",
    "section": "settings", "key": "labh" },
    { "type": "options", "title": "Font selection", "desc": "Pick a font from 'fc-list :fontformat=TrueType'",
    "section": "settings", "key": "font", "options": ["DejaVuSans"] },
    { "type": "numeric", "title": "Minimal font size", "desc": "Start wrapping text when font is this size",
    "section": "settings", "key": "minfos" },
    { "type": "numeric", "title": "Split separation", "desc": "Separation between labels, example: wrap around cables: 1/10 label width",
    "section": "settings", "key": "splitsep" },
    { "type": "bool", "title": "More image cycle modi", "desc": "When clicking the image, you get 4 print choices instead of 2",
    "section": "settings", "key": "multimod" },
    { "type": "numeric", "title": "Font height correction", "desc": "For adjusting the vertical offset, use caps when in doubt",
    "section": "settings", "key": "focorr" },
    { "type": "title", "title": "Release version: ''' + version + ''' - Matteljay" }
    ]'''
Builder.load_string('''
<RootWidget>:
    canvas:
        Color:
            rgba: 0.9, 0.9, 0.9, 1
        Rectangle:
            pos: self.pos
            size: self.size
    statuslabel: id_statuslabel
    textbox: id_textbox
    btn_PRINT: id_btn_PRINT
    beeld: id_beeld
    padding: 30
    spacing: 30
    orientation: 'vertical'
    TextInput_multi_retsel:
        id: id_textbox
        text: ''
        font_size: 20
        focus: True
        on_text_validate: root.press_btn_PRINT()
    ImageButton:
        id: id_beeld
        on_press: root.btn_IMG(self)
        allow_stretch: True
        keep_ratio: True
        canvas.before:
            Color:
                rgba: 0.1, 0.1, 0.5, 1
            Rectangle:
                #:set bor 5
                pos: self.x-bor, self.y-bor
                size: self.width+bor*2, self.height+bor*2
    Label:
        id: id_statuslabel
        font_size: 16
        size_hint: 1, .1
        color_good: 0.1, 0.5, 0.1, 1
        color_bad: 0.5, 0.1, 0.1, 1
        text_size: self.width, None
        halign: 'center'
        text: ''
    Button:
        id: id_btn_PRINT
        on_press: root.press_btn_PRINT()
        text: 'PRINT'
        font_size: 20
        background_down: self.background_normal
''')

class GLO(): # global variables: status and config
    stop = Event()
    firstrun = True
    bad_status = ''
    bad_lockdown = False
    confpath = '' # will hold the system path to the user's config file
    font_pool = {} # used as a dict and will be populated with fontname/fontpath pairs
    immode = 0
    processed_immode = 0
    processed_text = ''
    dispatch_printaction = False
    defaultcfg = def_defaultcfg
    jsondata = def_jsondata

def fatal_lockdown(txt):
    if not GLO.bad_lockdown:
        GLO.bad_status = txt
    GLO.bad_lockdown = True

class ImageButton(ButtonBehavior, Image):
    pass

class TextInput_multi_retsel(TextInput):
    multiline = True
    unfocus_on_touch = False
    text_validate_unfocus = False
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[0] in (9, 10, 11, 12): # hor tab, line feed, vert tab, form feed
            keycode = (None, None)
        elif keycode[0] == 13:
            keycode = (None, None)
            self.dispatch('on_text_validate')
        return super(type(self), self).keyboard_on_key_down(window, keycode, text, modifiers)
    def insert_text(self, substring, from_undo=False):
        ret = substring
        if len(substring) == 1: # probably key press or single paste
            if substring in '\t\r\v\f\n':
                ret = ''
        else: # probably paste from clipboard
            ret = re.sub(r'[\t\r\v\f\n]', '', substring)
        return super(type(self), self).insert_text(ret, from_undo)

class RootWidget(BoxLayout):
    imbytes = ''
    def execute_print(self):
        self.textbox.select_all()
        lpname = ConfigParser.get_configparser('app').get('settings', 'lpname')
        if not lpname or lpname == 'default':
            p = Popen(['lp'], stdin=PIPE)
        else:
            p = Popen(['lp', '-d', lpname], stdin=PIPE)
        p.stdin.write(self.imbytes)
        p.stdin.close()
    def press_btn_PRINT(self):
        btn = self.btn_PRINT
        # spam control: alternative to Kivy's min_state_time button
        if btn.background_color[1] == 2: return
        btn.background_color[1] = 2
        def greenback(dt): btn.background_color[1] = 1
        Clock.schedule_once(greenback, 0.5)
        # spam control: check if finished drawing
        if GLO.processed_text != btn.text:
            GLO.dispatch_printaction = True
            return
        self.execute_print()
    def btn_IMG(self, btn):
        # spam control: wait for cycle to get drawn
        if GLO.processed_immode != GLO.immode:
            return
        # cycle image
        GLO.immode += 1
        config = ConfigParser.get_configparser('app')
        multimod = int(config.get('settings', 'multimod'))
        if GLO.immode >= 4:
            GLO.immode = 0
        if multimod == 0 and GLO.immode >= 2:
            GLO.immode = 0
    @mainthread
    def update_elements(self, im):
        self.beeld.texture = im.texture
        if GLO.bad_status:
            self.statuslabel.color = self.statuslabel.color_bad
            self.statuslabel.text = GLO.bad_status
            if GLO.bad_lockdown:
                self.btn_PRINT.disabled = True
                self.btn_PRINT.text = 'PLEASE RESTART'
            else:
                GLO.bad_status = ''
        else:
            self.statuslabel.color = self.statuslabel.color_good
            self.btn_PRINT.disabled = False
            if GLO.firstrun:
                self.statuslabel.text = 'First time run, welcome! Wrote config {} ---> press F1 to see the settings page'.format(GLO.confpath)
            else:
                self.statuslabel.text = 'Ready to print, click the image to cycle'
        # allow button to work instantly
        GLO.processed_immode = GLO.immode
        GLO.processed_text = self.textbox.text
        if GLO.dispatch_printaction:
            GLO.dispatch_printaction = False
            self.execute_print()
    def canvas_drawtext(self, canvas_img, maxw, maxh, txt):
        # read config settings
        # alternative: config = App.get_running_app().config
        config = ConfigParser.get_configparser('app')
        font = config.get('settings', 'font')
        if font in GLO.font_pool:
            font_path = GLO.font_pool[font] # get a nice absolute font path
        else:
            font_path = def_defaultcfg['font'] # fallback in case of broken config settings (shouldn't happen)
        minfos = max(4, int(config.get('settings', 'minfos')))
        splitsep = max(0, int(config.get('settings', 'splitsep')))
        focorr = max(0, float(config.get('settings', 'focorr')))
        # write actual text
        sepdist = int(splitsep / 2) # halve the distance
        if GLO.immode == 3:
            # facing: double, toward center
            func_makebox(canvas_img, (0, maxh, int(maxw/2-sepdist), 0), minfos, focorr, font_path, txt)
            overflow = func_makebox(canvas_img, (maxw, 0, int(maxw/2+sepdist), maxh), minfos, focorr, font_path, txt)
        elif GLO.immode == 2:
            # facing: double, plain
            func_makebox(canvas_img, (0, 0, int(maxw/2-sepdist), maxh), minfos, focorr, font_path, txt)
            overflow = func_makebox(canvas_img, (int(maxw/2+sepdist), 0, maxw, maxh), minfos, focorr, font_path, txt)
        elif GLO.immode == 1:
            # facing: double, away from center
            func_makebox(canvas_img, (int(maxw/2-sepdist), 0, 0, maxh), minfos, focorr, font_path, txt)
            overflow = func_makebox(canvas_img, (int(maxw/2+sepdist), maxh, maxw, 0), minfos, focorr, font_path, txt)
        else:
            # facing: single, plain
            overflow = func_makebox(canvas_img, (0, 0, maxw, maxh), minfos, focorr, font_path, txt)
        if overflow: # check text overflow
            GLO.bad_status = 'Warning: your text does not fit the label!'
    def clock_thread(self):
        while True:
            if GLO.stop.is_set(): # stop thread so that the program can quit
                return
            # get some basic settings
            config = ConfigParser.get_configparser('app')
            maxw = max(10, int(config.get('settings', 'labw')))
            maxh = max(10, int(config.get('settings', 'labh')))
            # create blank canvas
            canvas_img = pilImage.new('RGB', (maxw, maxh), color=(255, 255, 255))
            # draw text on the canvas
            if GLO.font_pool:
                self.canvas_drawtext(canvas_img, maxw, maxh, self.textbox.text)
            # clean up spaces from text input
            #self.textbox.text = re.sub(r'\s\s+', ' ', self.textbox.text.lstrip())
            # save png to disk
            #canvas_img.save('image_main.png')
            # live memory texture
            data = BytesIO()
            canvas_img.save(data, format='jpeg')
            data.seek(0) # yes, this is also important!
            self.imbytes = data.read()
            im = CoreImage(BytesIO(self.imbytes), ext='jpeg')
            self.update_elements(im) # instead of self.beeld.texture = im.texture, cannot update root widget from thread
            sleep(1)
    #def on_touch_down(self, touch):
    #    super(RightClickTextInput,self).on_touch_down(touch)
    #    if touch.button == 'right':
    #def __init__(self, **kwargs):
    #    super(type(self), self).__init__(**kwargs)
    #    self.textbox.text = 'example'
    #    self.textbox.select_all()
    #    Thread(target=self.clock_thread).start()

class LabelPushApp(App):
    resource_rootpath = ''
    def populate_printers(self):
        # check if lp/cups is found
        if shutil.which('lp') is None or shutil.which('lpstat') is None:
            fatal_lockdown('lp or lpstat command not found! Please install and configure CUPS printing service')
            return
        print(':: required lp and lpstat commands were found')
        # find printers
        p = Popen(['lpstat', '-d', '-a'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, errors = p.communicate()
        # example output, on cups 2.2.8-3 no test seems available to pro-actively
        # check if a printer is powered on (even when using -p or -t options)
        lines = output.decode('utf-8').strip().split('\n')
        printers = []
        default_prn = None
        for i, line in enumerate(lines):
            words = line.split()
            if not words: continue
            if i == 0: # lpstat '-d' option
                if words[0] != 'no': # 'no system default destination'
                    default_prn = words[-1] # 'system default destination: ...'
                    printers.append('default')
            else:
                printers.append(words[0]) # '... accepting requests since (time)'
        if not printers:
            fatal_lockdown('No printer found. Make sure CUPS is running and configured (http://localhost:631)')
            return
        lpname = self.config.get('settings', 'lpname')
        if not lpname in printers:
            if not default_prn:
                print('WARNING: No default printer found, will select: ' + printers[0], file=sys.stderr)
                self.config.set('settings', 'lpname', printers[0])
                self.config.write()
            else:
                print('WARNING: Bad printer setting, switching to default', file=sys.stderr)
                self.config.set('settings', 'lpname', 'default')
                self.config.write()
        prcat = '", "'.join(printers)
        GLO.jsondata = GLO.jsondata.replace('["default"]', '["{}"]'.format(prcat), 1)
    def populate_fonts(self):
        # check if fontconfig exists
        if shutil.which('fc-list') is None:
            fatal_lockdown('fc-list command not found! Please install and configure \'fontconfig\'')
            return
        print(':: required fc-list command was found')
        # Old method for testing font:
        #try:
        #    ImageFont.truetype(GLO.font_path)
        #except OSError:
        #    fatal_lockdown('Truetype font not found, please install ttf-dejavu')
        # get font path list
        #fc-list --format='%{file}\n' :fontformat=TrueType
        p = Popen(['fc-list', '--format=%{file}\n', ':fontformat=TrueType'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, errors = p.communicate()
        fontpaths = output.decode('utf-8').strip().split('\n')
        if not fontpaths or not fontpaths[0]:
            fatal_lockdown('no truetype fonts found, please install ttf-dejavu')
            return
        for font in def_font_pool:
            searchfont = '/{}.ttf'.format(font)
            for fontpath in fontpaths:
                if fontpath.find(searchfont) >= 0:
                    GLO.font_pool[font] = fontpath
        if not GLO.font_pool:
            fatal_lockdown('no truetype fonts found which match the font_pool, please install ttf-dejavu')
            return
        focat = '", "'.join(GLO.font_pool)
        GLO.jsondata = GLO.jsondata.replace('["DejaVuSans"]', '["{}"]'.format(focat), 1)
        # verify config user setting
        font = self.config.get('settings', 'font')
        if not font in GLO.font_pool:
            # in case of weird config setting, use the first font that was found from the pool
            print('WARNING: Could not find font name: ' + font)
            self.config.set('settings', 'font', list(GLO.font_pool.keys())[0])
            self.config.write()
    def get_application_config(self):
        confpath = super(type(self), self).get_application_config('~/.config/%(appname)s.ini')
        GLO.confpath = confpath
        if os.access(confpath, os.R_OK):
            GLO.firstrun = False
        else:
            GLO.firstrun = True
        return confpath
    def on_config_change(self, config, section, key, value):
        if config is not self.config:
            return # ignore config change of kivy itself
        if key == 'multimod':
            GLO.immode = 0 # reset view cycle modus
    def build_config(self, config):
        # Possible alternative for Kivy's config.setdefaults('settings', { 'key': 'value' }) method, WITH config comments!
        #confpath = os.path.expanduser('~') + '/.config/labelpush.ini'
        #print(confpath)
        #if not os.access(confpath, os.R_OK):
        #    GLO.defaultcfg = 'some test\n\and more'
        #    fd = open(confpath, 'w')
        #    fd.write(GLO.defaultcfg)
        #    fd.close()
        #    GLO.firstrun = True
        #config.setdefaults('settings', {}) # read newly created config into memory
        config.setdefaults('settings', GLO.defaultcfg)
    def close_settings(self, *largs):
        ret = super(type(self), self).close_settings(*largs)
        GLO.firstrun = False # config window was opened, no more need for this
        self.root.textbox.focus = True
        self.root.textbox.select_all()
        return ret
    def build_settings(self, settings):
        # F1 keyboard press will trigger the config menu, App.open_settings(), App.close_settings() could be used in the code
        settings.add_json_panel('LabelPush', self.config, data=GLO.jsondata)
    def on_start(self):
        # basic checks, modify json settings string array, give more user friendly feedback
        self.populate_printers()
        self.populate_fonts()
        # Prepare textbox
        self.root.textbox.text = str(datetime.date.today())
        self.root.textbox.select_all()
        # Start thread
        Thread(target=self.root.clock_thread).start()
    def on_stop(self):
        GLO.stop.set() # stop thread so that the program can exit
    def build(self):
        app_path = Path(__file__).resolve()
        for tryroot in (str(app_path.parents[1]) + '/share', str(app_path.parents[0]) + '/data'):
            tryicon = tryroot + '/pixmaps/' + name + '.png'
            if os.access(tryicon, os.R_OK):
                self.icon = tryicon
                self.resource_rootpath = tryroot
                break
        else:
            print('WARNING: Could not find application resource files', file=sys.stderr)
        return RootWidget()

#
########### NON-GUI Below
#

def func_sniptruetext(par_text, par_font, par_wlimit):
    textoverflow = False
    linepart = trypart = ''
    for word in par_text.split():
        if linepart == '':
            trypart = word
        else:
            trypart = linepart + ' ' + word # try adding a piece in trypart
        width, height = par_font.getsize(trypart)
        if width >= par_wlimit: # if not possible
            width, height = par_font.getsize(linepart)
            if width >= par_wlimit:
                textoverflow = True
            if len(linepart) > 0:
                yield (linepart, width, textoverflow)
            trypart = word
        linepart = trypart
    # push away last bit
    width, height = par_font.getsize(linepart)
    if width >= par_wlimit:
        textoverflow = True
    yield (linepart, width, textoverflow)

def func_makebox(canvas_img, bx, minfontscale, fontmarginfactor, fontname, stringprint, DEBUG=False):
    # canvas box & definitions
    if DEBUG:
        draw = ImageDraw.Draw(canvas_img)
        draw.rectangle(((bx[0], bx[1]), (bx[2], bx[3])), outline=(0, 0, 100))
    font = ImageFont.truetype(fontname, minfontscale)
    fontnamemargin = minfontscale * fontmarginfactor
    # pre-calculations/translations
    xswap = (bx[0] > bx[2])
    yswap = (bx[1] > bx[3])
    if xswap and yswap: # upside down
        mbox = (bx[2], bx[3], bx[0], bx[1])
    elif xswap: # rotate right
        #mbox = (bx[2], bx[1], bx[0], bx[3]) # normalize box
        #diffx = bx[0] - bx[2]
        #diffy = bx[3] - bx[1]
        mbox = (bx[2], bx[1], bx[2] + bx[3] - bx[1], bx[1] + bx[0] - bx[2]) # tilt box
    elif yswap: # rotate left
        #mbox = (bx[0], bx[3], bx[2], bx[1]) # normalize box
        #diffx = bx[2] - bx[0]
        #diffy = bx[1] - bx[3]
        mbox = (bx[0], bx[3], bx[0] + bx[1] - bx[3], bx[3] + bx[2] - bx[0]) # tilt box
    else:
        mbox = (bx[0], bx[1], bx[2], bx[3])
    mboxw = mbox[2] - mbox[0]
    mboxh = mbox[3] - mbox[1]
    G_maxlines = mboxh / (minfontscale + fontnamemargin)
    # read array and collect information
    textoverflow = False
    foboxw = foboxh = 0 # font box width, height
    ar_text = []
    ar_width = []
    for i, snipret in enumerate(func_sniptruetext(stringprint, font, mboxw)):
        ar_text.append(snipret[0])
        ar_width.append(snipret[1])
        if snipret[2] == True:
            textoverflow = True
        if (minfontscale + fontnamemargin) * (i + 1) > mboxh:
            textoverflow = True
        foboxh = (minfontscale + fontnamemargin) * (i + 1)
        foboxw = max(foboxw, ar_width[i])
    # if no text snipping, calculate scaling
    newscale = minfontscale
    if len(ar_text) == 1 and len(ar_text[0]) > 0:
        while True:
            width, height = font.getsize(ar_text[0]) # find dimensions of first (only) element
            if width < mboxw and height < mboxh:
                newscale += 1
                font = ImageFont.truetype(fontname, newscale)
            else:
                newscale -= 1
                font = ImageFont.truetype(fontname, newscale)
                foboxw, foboxh = font.getsize(ar_text[0])
                ar_width[0] = foboxw
                fontnamemargin = newscale * fontmarginfactor
                break
    # prepare to rotate
    tmp_img = pilImage.new('RGB', (mboxw, mboxh), color=(255, 255, 255))
    tmp_draw = ImageDraw.Draw(tmp_img)
    if DEBUG:
        tmp_draw.rectangle(((0, 0), (mboxw-1, mboxh-1)), outline=(0, 100, 0))
    # draw text centered
    xcorr = 0
    ycorr = (mboxh - foboxh) / 2
    for i, line in enumerate(ar_text):
            xcorr = (mboxw - ar_width[i]) / 2
            tmp_draw.text((xcorr, ((minfontscale + fontnamemargin) * i) + ycorr - (fontnamemargin / 2)), line, (0, 0, 0), font=font)
    # draw red debug frame
    if DEBUG:
        xcorr = (mboxw - foboxw) / 2
        ycorr = (mboxh - foboxh) / 2
        tmp_draw.rectangle(((xcorr, ycorr), (foboxw + xcorr, foboxh + ycorr)), outline=(255,0,0))
    # rotate
    if xswap and yswap: # upside down
        rot_img = tmp_img.rotate(180, resample=0, expand=1)
    elif xswap: # rotate right
        rot_img = tmp_img.rotate(-90, resample=0, expand=1)
    elif yswap: # to-the-left
        rot_img = tmp_img.rotate(90, resample=0, expand=1)
    else:
        rot_img = tmp_img
    canvas_img.paste(rot_img, (mbox[0], mbox[1]))
    # overflow warning for user
    return textoverflow

def fatal_err(line):
    print('ERROR: ' + line, file=sys.stderr)
    sys.exit(1)

def pymod_versioncheck(module_name, module_version, required_version):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split('.')]
    if normalize(module_version) < normalize(required_version):
        fatal_err('{} requires version {} (current version is {})'.format(module_name, required_version, module_version))
        sys.exit(1)
    else:
        print(':: {} version is: {}'.format(module_name, module_version))

#
##### Main program entry point (after reading all the functions above!)
#

if __name__ == '__main__':
    # check requirements
    pymod_versioncheck('kivy', KIVY_VERSION, '1.10.1')
    pymod_versioncheck('pillow', PILLOW_VERSION, '5.3.0') # DO NOT USE the old python-pil, i tried and it sucks
    # Kivy handles command line arguments :-)
    #from argparse import ArgumentParser
    #parser = ArgumentParser(description='Simple lightweight label printing app')
    #parser.add_argument('-c', '--config', default=['~/.config/labelpush.ini'], dest='FILE', help='configuration file to use')
    #print(parser.parse_args())
    # GUI settings
    Config.set('input', 'mouse', 'mouse,disable_multitouch') # right mouse behave like left button
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '636')
    LabelPushApp().run()

# End of file





