import os, codecs

def main():
    submit_answers_list = ["y", "yes", "д", "да", ""]
    csv_files_to_process = []
    if input("Convert all csv files in current directory [y/n/Enter]?: ").lower() in submit_answers_list:
        csv_files_to_process = [file for file in os.listdir() if file.endswith("csv") and
                                not file.endswith("_semicolon.csv")]
    else:
        input_str = input("Enter file's names (file1, file1, etc): ")
        csv_files_to_process = [file.strip() for file in input_str.split(",") if file.endswith("csv")]
    if not csv_files_to_process:
        print("Correct file names not found")
        return
    print("Next files will be process:\n\t", "\n\t".join(csv_files_to_process), sep="")
    if input("Submit [y/n/Enter]: ") not in submit_answers_list:
        print("exit")
        return

    counters = {"'": False, "\"": False}
    for file_name in csv_files_to_process:
        if os.path.exists(file_name) is False:
            print(f"File \"{file_name}\" not found!")
            continue
        print(f"Convert file \"{file_name}\"...", end="", flush=True)
        new_file_name = "".join(file_name.split(".")[:-1])+"_semicolon.csv"
        is_success = True
        try:
            with codecs.open(file_name, "r", "utf_8_sig") as origin_file:
                with codecs.open(new_file_name, "w", "utf_8_sig") as new_file:
                    while True:
                        try:
                            file_line = origin_file.readline()
                        except UnicodeDecodeError as ex:
                            print("Fail\n\tUnicodeDecodeError =>", ex)
                        except Exception as ex:
                            print("Fail\n\tCan't read line =>", ex)
                            is_success = False
                            break
                        file_line = file_line.replace(",,", ",")
                        file_line = file_line.replace(",Неделя", "Время,Неделя")
                        file_line_list = list(file_line)
                        if file_line_list == []:
                            break
                        for symbol_index in range(len(file_line_list)):
                            symbol = file_line_list[symbol_index]
                            if symbol in counters.keys():
                                counters[symbol] = not counters[symbol]
                            elif symbol == "," and True not in counters.values():
                                file_line_list[symbol_index] = ";"
                        new_file.write("".join(file_line_list))
        except Exception as ex:
            print("Fail\n\tException raised =>", ex)
            is_success = False
        if is_success:
            print("Done")
        else:
            try:
                os.remove(new_file_name)
            except Exception:
                pass
                



if __name__ == "__main__":
    main()
