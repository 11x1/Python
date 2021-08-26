import requests
import tkinter as gui
import time
from datetime import datetime
import tkinter.colorchooser
import struct

# for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
# Discord webhook url:
url = "webhook_url"

bg = "gray15"
fg = "white"

main_window = gui.Tk()
main_window.title("Webhook controls")
main_window.geometry("600x315")
main_window.configure(bg=bg)

checkbox_embed_bool = gui.IntVar()
tts_embed_bool = gui.IntVar()
# color_embed = 14335

def send_msg():
    isEmbed = checkbox_embed_bool.get()
    isTts = tts_embed_bool.get()
    msg_text = msg_text_entry.get()
    time_now = datetime.now()
    current_time = time_now.strftime("%H:%M:%S")

    type_ = ""
    avatar_url = ""
    username = "webhook-name"

    for num in range(len(msg_text)):
        msg_text_entry.delete(0)

    #color_embed = tkinter.colorchooser.askcolor()
    #color_ = struct.pack('BBB',color_embed.encode('hex'))

    if isTts == 1:
        tts_bool = True
    elif isTts == 0:
        tts_bool = False

    if isEmbed == 1:
        title_text = embed_text_label.get()
        footer_text = embed_footer_entry.get()
        #print(color_embed)

        if footer_text == "":
            icon_url = ""
        else: 
            icon_url = ""
            
        msg_data = {
            "username": username,
            "avatar_url": avatar_url,
            "tts": tts_bool,
            "embeds": [
                {
                    "title": title_text,
                    "description": msg_text,
                    # "color": color_,
                    "footer": {
                        "text": footer_text,
                        "icon_url": icon_url,
                    }
                }
            ]
        }
        type_ = "(embed): "

    elif isEmbed == 0:
        msg_data = { 
            "username": username,
            "content": msg_text,
            "tts": tts_bool,
            "avatar_url": avatar_url,
        }
        type_ = "(msg): "

    main_window_text_history.insert(gui.END, "[" + current_time + "] " + type_ + msg_text + "\n")

    result = requests.post(url, json=msg_data)
  
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

def update_gui():
    isEmbed = checkbox_embed_bool.get()
    if isEmbed == 0:
        embed_text_label_text.place_forget()
        embed_text_label.place_forget()
        embed_footer_text.place_forget()
        embed_footer_entry.place_forget()
    elif isEmbed == 1:
        embed_text_label_text.place(x = 5, y= 50)
        embed_text_label.place(x=75,y=50)
        embed_footer_text.place(x=5, y=80)
        embed_footer_entry.place(x=85, y=80)
   
def quit_():
    main_window.destroy()

# add elements to gui
msg_text_label = gui.Label(main_window, text="Message: ", bg=bg, fg=fg)
msg_text_entry = gui.Entry(main_window)
msg_text_button = gui.Button(main_window, text="Send message!", command=send_msg, bg=bg,fg=fg)
msg_text_checkbox_embed = gui.Checkbutton(main_window, text="Embed mode", variable=checkbox_embed_bool, command=update_gui, bg=bg, fg=fg)
msg_text_button_exit = gui.Button(main_window, text="Quit", command=quit_, bg = "red", fg=fg)
msg_text_tts_embed = gui.Checkbutton(main_window, text="TTS", variable=tts_embed_bool, bg=bg, fg=fg)


# enable multidd
# msg_mdd_settings = gui.Menubutton(main_window, text="Choose wisely", indicatoron=True, borderwidth=1, relief="raised")
# msg_choices_embed = gui.Menu(msg_mdd_settings, tearoff=False)
# msg_mdd_settings.configure(menu=msg_choices_embed)

# choices = {}
# for choice in ("Title", "Footer"):
#    choices[choice] = gui.IntVar(value=0)
#    msg_choices_embed.add_checkbutton(label=choice, variable=choices[choice], onvalue=1, offvalue=0, command=printValues)

# embed text
embed_text_label_text = gui.Label(main_window, text="Embed title:", bg=bg, fg=fg)
embed_text_label = gui.Entry(main_window)

embed_footer_text = gui.Label(main_window, text="Embed footer:", bg=bg, fg=fg)
embed_footer_entry = gui.Entry(main_window)

# place elements in gui
msg_text_label.place(x = 5, y= 5)
msg_text_entry.place(x = 70, y = 5)
msg_text_button.place(x = 170, y = 3)
msg_text_checkbox_embed.place(x = 5, y = 25)
msg_text_tts_embed.place(x = 100, y = 25)
msg_text_button_exit.place(x = 220, y= 279)

#msg_text_label.pack()
#msg_text_entry.pack()
#msg_text_button.pack()
#msg_text_button_exit.pack()

# Message history window
# create textbox for sent message history
main_window_text_history = gui.Text()

main_window_text_history.place(x = 260, y =5, height = 300, width = 300)

# Run gui, to check for updates in menu
main_window.mainloop()
