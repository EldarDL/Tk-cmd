import threading
import tkinter
from tkinter import Tk, Text, Button, Label
import subprocess
import sys
import time

continue_command = True


def button_click(input_command):
    global continue_command
    cmd.delete(1.0, 'end')
    pc_name = entry.get(1.0, "end-1c")
    available_commands = {'ping': f'ping {pc_name}',
                          'sysinfo': f'systeminfo /s {pc_name} | findstr /c:"System Model" /c:"Available Physical Memory" /c:"Total Physical Memory"',
                          'query user': f'query user /server {pc_name}',
                          'ping -t': f'ping {pc_name} -t',
                          }
    current_command = available_commands[input_command]
    disable_buttons()
    t_end = time.time() + 15

    def command_init():
        global continue_command
        process = subprocess.Popen(current_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   bufsize=1,
                                   universal_newlines=True, shell=True)
        while True and time.time() < t_end and continue_command:
            realtime_output = process.stdout.readline()
            if realtime_output == '' and process.poll() is not None:
                break
            if realtime_output:
                cmd.insert(tkinter.END, realtime_output)
                cmd.see(tkinter.END)
                cmd.update_idletasks()
                sys.stdout.flush()
        enable_buttons()
        continue_command = True

    threading.Thread(target=command_init).start()


def enable_buttons():
    for button in buttons:
        button.config(state='normal')


def disable_buttons():
    for button in buttons:
        button.config(state='disabled')


def cancel_command():
    global continue_command
    continue_command = False


# UI SETUP
window = Tk()
window.resizable(False, False)
window.config(padx=50, pady=50)
window.geometry("850x400")
window.title('Dashy by Eltoro')

cmd = Text(window, height=12, width=60)
cmd.config(font=("Lato", 12))
cmd.grid(column=1, row=1, padx=(95, 10), pady=10, columnspan=2, rowspan=4)

entry = Text(window, height=1, width=35)
entry.config(font=("Lato", 12))
entry.grid(column=2, row=0, padx=(25, 0))
entry.focus()
# entry.bind('<Return>', func=button_click)


ping_button = Button(text='Ping', command=lambda: button_click('ping'))
ping_button.grid(column=0, row=0, pady=10)
ping_button.config(font=("Arial", 15))
ping_button.configure(height=1, width=12)

ping_t_button = Button(text='Ping -t (15sec)', command=lambda: button_click('ping -t'))
ping_t_button.grid(column=0, row=1, pady=10)
ping_t_button.config(font=("Arial", 15))
ping_t_button.configure(height=1, width=12)

sysinfo_button = Button(text='System Info', command=lambda: button_click('sysinfo'))
sysinfo_button.config(font=("Arial", 15))
sysinfo_button.configure(height=1, width=12)
sysinfo_button.grid(column=0, row=2, pady=10)

query_user_button = Button(text='Query User', command=lambda: button_click('query user'))
query_user_button.config(font=("Arial", 15))
query_user_button.configure(height=1, width=12)
query_user_button.grid(column=0, row=3, pady=10)

cancel_button = Button(text='Cancel', command=cancel_command)
cancel_button.config(font=("Arial", 15))
cancel_button.configure(height=1, width=12)
cancel_button.grid(column=0, row=4, pady=10)

computer_label = Label(text='Computer/User Name:')
computer_label.config(font=("Lato", 12))
computer_label.grid(column=1, row=0, padx=(85, 10))

buttons = [ping_button, sysinfo_button, query_user_button, ping_t_button]

window.mainloop()