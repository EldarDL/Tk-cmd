import threading
import tkinter
from tkinter import Tk, Text, Button, Label
import subprocess
import sys


# Ping Test
def button_click(input_command):
    cmd.delete(1.0, 'end')
    pc_name = entry.get(1.0, "end-1c")
    if input_command == 'ping':
        command = f"ping {pc_name}"
    elif input_command == 'sysinfo':
        command = f'systeminfo /s {pc_name} | findstr /c:"System Model" /c:"Available Physical Memory" /c:"Total Physical Memory"'

    elif input_command == 'query user':
        command = f'query user /server {pc_name}'

    def command_init():
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   bufsize=1,
                                   universal_newlines=True, shell=True)

        while True:
            realtime_output = process.stdout.readline()
            sysinfo_button.config(state='disable')
            ping_button.config(state='disable')
            query_user_button.config(state='disable')
            if realtime_output == '' and process.poll() is not None:
                break
            if realtime_output:
                cmd.insert(tkinter.END, realtime_output)
                cmd.update_idletasks()
                sys.stdout.flush()
        sysinfo_button.config(state='normal')
        ping_button.config(state='normal')
        query_user_button.config(state='normal')
    threading.Thread(target=command_init).start()


# UI SETUP
window = Tk()
window.resizable(False, False)
window.config(padx=50, pady=50)
window.geometry("850x400")
window.title('Dashy by Eltoro')

entry = Text(window, height=1, width=30)
entry.config(font=("Lato", 12))
entry.grid(column=2, row=0, padx=(30, 0))
entry.focus()

cmd = Text(window, height=10, width=55)
cmd.config(font=("Lato", 12))
cmd.grid(column=1, row=1, padx=(100, 10), pady=10, columnspan=2)

ping_button = Button(text='Ping', command=lambda: button_click('ping'))
ping_button.place(x=10, y=10)
ping_button.config(font=("Arial", 15))
ping_button.configure(height=1, width=12)
# ping_button.grid(column=0, row=0)

sysinfo_button = Button(text='System Info', command=lambda: button_click('sysinfo'))
sysinfo_button.config(font=("Lato", 15))
sysinfo_button.configure(height=1, width=12)
sysinfo_button.grid(column=0, row=1, padx=10)

query_user_button = Button(text='Query User', command=lambda: button_click('query user'))
query_user_button.config(font=("Lato", 15))
query_user_button.configure(height=1, width=12)
query_user_button.grid(column=0, row=2, padx=10)

computer_label = Label(text='Computer/User Name:')
computer_label.config(font=("Lato", 12))
computer_label.grid(column=1, row=0, padx=(85, 10))

window.mainloop()
