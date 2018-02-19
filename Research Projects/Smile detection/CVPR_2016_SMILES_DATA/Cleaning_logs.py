file = open("Xception_result_txt.log", "r")
lines = file.readlines()
file.close;
cleaned_file = open("Xception_cleaned_results.log", "w")
for line in lines:
    if 'Epoch' in line:
        cleaned_file.write(line)

    if "+-+-" in line or\
                    "Start:" in line or\
                    "Finished" in line or\
                    "161/161 " in line :
        cleaned_file.write(line+"\n")

cleaned_file.close()
file = open("Xception_cleaned_results.log", "r")
lines = file.readlines()
cleaned_file.close;
cleaned_file_summary = open("Xception_cleaned_summary.log", "w")
for index, line in enumerate(lines):
    if "Epoch 100/100" in line or "Epoch 99/100" in line or "Epoch 98/100" in line or "Epoch 97/100" in line or "Epoch 96/100" in line:
        cleaned_file_summary.write(line)
        cleaned_file_summary.write(lines[index + 1] + "\n")

    if "+-+-" in line:
        cleaned_file_summary.write(line + "\n")

cleaned_file_summary.close()
