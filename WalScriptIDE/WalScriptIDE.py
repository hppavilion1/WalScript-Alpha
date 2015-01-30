#Credit to Brian Oakley here: http://stackoverflow.com/questions/3732605/add-advanced-features-to-a-tkinter-text-widget
import Tkinter as tk
from Tkinter import Menu, BOTH, END, LEFT
import tkFont, tkFileDialog, tkMessageBox

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        ## Toolbar
        self.toolbar = tk.Frame()

        text_frame = tk.Frame(borderwidth=1, relief='sunken')
        self.text = tk.Text(wrap='none', bg='black', fg='white',
                            borderwidth=0, highlightthickness=0, insertbackground='#B6B6B4')
        self.vsb = tk.Scrollbar(orient='vertical', borderwidth=1,
                                command=self.text.yview)
        #self.text.insert('1.0', '\n')
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(in_=text_frame,side='right', fill='y', expand=False)
        self.text.pack(in_=text_frame, side='left', fill='both', expand=True)
        self.toolbar.pack(side='top', fill='x')
        text_frame.pack(side='bottom', fill='both', expand=True)

        # clone the text widget font and use it as a basis for some
        #tags
        self.text.tag_configure('command', foreground='orange')
        self.text.tag_configure('varoverflow', foreground='red', underline=True)
        self.text.tag_configure('unrecognizedCommand', background='red')

        #Keybindings
        self.text.bind('<Key>', self.highlightCommands) #highlighting
        self.text.bind('}', self.highlightCommands2) #more highlighting
            #Menu functions
        self.bind('<Control-c>', self.copy_command) 
        self.bind('<Control-x>', self.cut_command)
        self.bind('<Control-v>', self.paste_command)
        self.bind('<Control-g>', self.glue_command)

        # initialize the spell checking dictionary. YMMV.
        self._commands=open('commands.txt').read().split('\n')
        self._argTypes=open('argTypes.txt').read().split('\n')

        self.defaultfile = None
        self.title('Untitled .walrus file')
        #initialize menu
        menu = Menu(self)
        self.config(menu=menu)

        #file menu
        fileMenu = Menu(menu, tearoff=1)
        menu.add_cascade(label='File', menu=fileMenu)
        fileMenu.add_command(label='New', command=self.dummy('new'),state=tk.DISABLED)
        fileMenu.add_command(label='Open...', command=self.open_command)
        fileMenu.add_command(label='Save', command=self.save_command)
        fileMenu.add_command(label='Save As', command=self.saveas_command)
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=self.exit_command)

        #edit menu
        editMenu = Menu(menu, tearoff=1)
        menu.add_cascade(label='Edit',menu=editMenu)
        editMenu.add_command(label='Undo', command=self.dummy('undo'),state=tk.DISABLED)
        editMenu.add_command(label='Redo', command=self.dummy('redo'),state=tk.DISABLED)
        editMenu.add_separator()
        editMenu.add_command(label='Cut',command=self.cut_command)
        editMenu.add_command(label='Copy',command=self.copy_command)
        editMenu.add_command(label='Paste',command=self.paste_command)
        editMenu.add_command(label='Glue',command=self.glue_command)

        #help menu
        helpMenu = Menu(menu,tearoff=1)
        menu.add_cascade(label='Help', menu=helpMenu)
        helpMenu.add_command(label='About...', command=self.about_command)

        #right-click menu
        RCMenu = Menu(self, tearoff=0)
        RCMenu.add_command(label='test',command=self.dummy('test'))
        self.text.bind('<Button-3>', self.popup)

    def open_command(self):
        file = tkFileDialog.askopenfile(parent=self,mode='rb',title='Select a file',defaultextension='walrus',filetypes=[('Walrus Files', '.walrus'),('All Files','.*')],initialfile='*.walrus')
        if file != None:
            self.defaultfile = file
            contents = file.read()
            self.text.insert('1.0',contents)
            file.close()
            self.highlightAllSyntax
            self.title(str(file)[15:-27])

    def save_command(self):
        file = self.defaultfile
        if file != None:
            with open(file) as f:
                # slice off the last character from get, as an extra return is added
                data = self.text.get('1.0', END+'-1c')
                f.write(data)
                f.close()
        else:
            self.saveas_command()

    def saveas_command(self):
        file = tkFileDialog.asksaveasfile(mode='w',defaultextension='walrus',filetypes=[('Walrus Files', '.walrus'),('All Files','.*')],initialfile='*.walrus')
        if file != None:
            self.defaultfile = file
            # slice off the last character from get, as an extra return is added
            data = self.text.get('1.0', END+'-1c')
            file.write(data)
            file.close()
            self.title(str(file)[15:-26])
     
    def exit_command(self):
        if tkMessageBox.askokcancel('Quit', 'Do you really want to quit?'):
            self.destroy()
 
    def about_command(self):
        label = tkMessageBox.showinfo('About', 'WalScript IDE')
            
    def copy_command(self, event=False):
        self.text.clipboard_clear()
        try:
            t = self.text.get('sel.first', 'sel.last')
        except tk.TclError:
            pass
            t = ''
        self.text.clipboard_append(t)

    def cut_command(self,event=False):
        self.copy_command()
        self.text.delete('sel.first', 'sel.last')
        
    def glue_command(self,event=False):
        try:
            t = self.text.get('sel.first', 'sel.last')
        except tk.TclError:
            pass
            t = ''
        self.text.clipboard_append(t)

    def paste_command(self,event=False):
        try:
            t = self.text.selection_get(selection='CLIPBOARD')
        except tk.TclError:
            pass

    def popup(self, event=False):
        self.RCMenu.post(event.x_root, event.y_root)

    def dummy(self, test=''):
        print test+' button functional'

    def highlightCommands(self, event):
        index = self.text.search('}', 'insert', backwards=True)
        if index == '':
            index ='1.0'
        else:
            index = self.text.index('%s+2c' % index)
        command = self.text.get(index, 'insert')
        self.text.tag_remove('command', index, '%s+%dc' % (index, len(command)))
        self.text.tag_remove('unrecognizedCommand', index, '%s+%dc' % (index, len(command)))
        if command in self._commands:
            self.text.tag_add('command', index, '%s+%dc' % (index, len(command)))

    def highlightCommands2(self, event):
        index = self.text.search('}', 'insert', backwards=True, regexp=True)
        if index == '':
            index ='0.0'
        else:
            index = self.text.index('%s+1c' % index)
        command = self.text.get(index, 'insert')
        if not command in self._commands:
            self.text.tag_add('unrecognizedCommand', index, '%s+%dc' % (index, len(command)))

    def search(self, keyword, tag):
        pos = '1.0'
        while True:
            idx = self.text.search(keyword, pos, END)
            if not idx:
                break
            pos = '{}+{}c'.format(idx, len(keyword))
            self.text.tag_add(tag, idx, pos)

    def highlightAllSyntax(self):
        for x in self._commands:
            self.search(x, 'command')
        
if __name__ == '__main__':
    app=App()
    app.mainloop()
