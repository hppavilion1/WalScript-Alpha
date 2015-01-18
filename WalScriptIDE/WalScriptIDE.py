#Credit to Brian Oakley here: http://stackoverflow.com/questions/3732605/add-advanced-features-to-a-tkinter-text-widget
import Tkinter as tk
from Tkinter import Menu
import tkFont, tkFileDialog

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        ## Toolbar
        self.toolbar = tk.Frame()

        ## Main part of the GUI
        # I'll use a frame to contain the widget and 
        # scrollbar; it looks a little nicer that way…
        text_frame = tk.Frame(borderwidth=1, relief='sunken')
        self.text = tk.Text(wrap='word', bg='black', fg='white', 
                            borderwidth=0, highlightthickness=0)
        self.vsb = tk.Scrollbar(orient='vertical', borderwidth=1,
                                command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(in_=text_frame,side='right', fill='y', expand=False)
        self.text.pack(in_=text_frame, side='left', fill='both', expand=True)
        self.toolbar.pack(side='top', fill='x')
        text_frame.pack(side='bottom', fill='both', expand=True)

        # clone the text widget font and use it as a basis for some
        # tags
        self.text.tag_configure('command', foreground='orange')
        self.text.tag_configure('varoverflow', foreground='red', underline=True)
        self.text.tag_configure('unrecognizedCommand', background='red')
        self.text.bind('<Key>', self.highlightSyntax)
        self.text.bind('}', self.highlightSyntax2)


        # initialize the spell checking dictionary. YMMV.
        self._commands=open('commands.txt').read().split('\n')

        def open_command():
            file = tkFileDialog.askopenfile(parent=self,mode='rb',title='Select a file')
            if file != None:
                contents = file.read()
                self.text.insert('1.0',contents)
                file.close()
                self.highlightSyntax
 
        def save_command(self):
            file = tkFileDialog.asksaveasfile(mode='w')
            if file != None:
                # slice off the last character from get, as an extra return is added
                data = self.text.get('1.0', END+'-1c')
                file.write(data)
                file.close()
         
        def exit_command():
            if tkMessageBox.askokcancel('Quit', 'Do you really want to quit?'):
                self.destroy()
 
        def about_command():
            label = tkMessageBox.showinfo('About', 'Just Another TextPad \n Copyright \n No rights left to reserve')

        def dummy():
            pass
        #initialize menu
        menu = Menu(self)
        self.config(menu=menu)
        fileMenu = Menu(menu)
        menu.add_cascade(label='File', menu=fileMenu)
        fileMenu.add_command(label='New', command=dummy)
        fileMenu.add_command(label='Open...', command=open_command)
        fileMenu.add_command(label='Save', command=save_command)
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=exit_command)
        editMenu = Menu(menu)
        editMenu.add_command(label='Undo', command=dummy())
        helpMenu = Menu(menu)
        menu.add_cascade(label='Help', menu=helpMenu)
        helpMenu.add_command(label='About...', command=about_command)
        
    def highlightSyntax(self, event):
        index = self.text.search(r'\s', 'insert', backwards=True, regexp=True)
        if index == '':
            index ='0.0'
        else:
            index = self.text.index('%s+1c' % index)
        command = self.text.get(index, 'insert')
        self.text.tag_remove('command', index, '%s+%dc' % (index, len(command)))
        self.text.tag_remove('unrecognizedCommand', index, '%s+%dc' % (index, len(command)))
        if command in self._commands:
            self.text.tag_add('command', index, '%s+%dc' % (index, len(command)))

    def highlightSyntax2(self, event):
        index = self.text.search(r'\s', 'insert', backwards=True, regexp=True)
        if index == '':
            index ='0.0'
        else:
            index = self.text.index('%s+1c' % index)
        command = self.text.get(index, 'insert')
        if not command in self._commands:
            self.text.tag_add('unrecognizedCommand', index, '%s+%dc' % (index, len(command)))

if __name__ == '__main__':
    app=App()
    app.mainloop()
