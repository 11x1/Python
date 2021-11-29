chat_path = input("Enter chat_history path (defaults chat_history.txt, leave blank): ")
output_path = input("Enter output path (defaults output.txt, leave blank): ")
total_lines = 0

blacklisted = ["Sul on vastamata kõne", "helistas sulle.", "set your nickname", "Videovestlus on lõppenud.", "Nüüd saad üksteisele helistada ja vaadata sellist teavet"]

if chat_path == "":
    chat_path = "message_1.txt"
if output_path == "":
    output_path = "output.txt"

f = open(chat_path, encoding="utf8")

open(output_path, 'a').close()
open(output_path, "w").close() # Clear output file

line_counter = 0
final_output = ""
for x in f:
    line_counter += 1
    if r'<div class="_3-96 _2pio _2lek _2lel">' in x:
        final_output += x.replace('<div class="_3-96 _2pio _2lek _2lel">', "").replace("</div>\n", "") + ": ".replace("                            ", "")
        line_counter = 0
    
    if line_counter == 4:
        if not "<a" in x:
            if "<div>" in x:
                final_output += x.split("<div>")[1]
            if "</div>" in x:
                final_output = final_output[:-7]
            continue_after_blacklist = True
            for blacklisted_word in blacklisted:
                if blacklisted_word in x:
                    continue_after_blacklist = False
                    final_output = ""
            
            if continue_after_blacklist:
                final_output = final_output.replace("                            ", "")
                w = open(output_path, "a", encoding="utf8")
                w.write(final_output + "\n")
                w.close()
                final_output = ""
                total_lines += 1
                continue_after_blacklist = True
        else:
            final_output = ""

print(f"Done. {total_lines} total messages.")
