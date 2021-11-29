chat_path = input("Enter chat_history path (defaults chat_history.txt, leave blank): ")
output_path = input("Enter output path (defaults output.txt, leave blank): ")

if chat_path == "":
    chat_path = "chat_history.txt"
if output_path == "":
    output_path = "output.txt"

snapchat_username = input("Enter snapchat username: ")
chat_file = open(chat_path, encoding="utf8")
type = False
string = False
line_iter = 0
extra_line = False
line_counter = 0
final_string = ""
total_messages = 0

open(output_path, 'a').close()
open(output_path, "w").close() # Clear output file


for x in chat_file:
    line_counter += 1
    if snapchat_username in x and not type:
        total_messages += 1
        type = True
    elif type:
        line_iter += 1
        if "TEXT" in x:
            string = True
        elif line_iter == 5 or extra_line or line_iter >= 6:
            if not "</td>" in x and not line_iter >= 6:
                extra_line = True
            
            if "<td style" in x:
                final_string += x.split(r'<td style="padding-top:0" colspan="3">')[1]

            if not extra_line:
                output_file = open(output_path, "a", encoding="utf8")
                # print(f"{final_string}\n")
                final_string = final_string.replace("</td>", "").strip('\n')
                output_file.write(f"{final_string}\n")
                output_file.close()
                type = False
                line_iter = 0
                string = False
                final_string = ""
            elif extra_line and line_iter == 6:
                if not x.split("</td>")[0] == "":
                    final_string += x.replace("</td>", "").strip('\n')
                extra_line = False

print(f"Done. {total_messages} total messages.")
