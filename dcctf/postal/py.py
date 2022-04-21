with open("in.IMB")as f:
    lines = []
    for line in f:
        lines.append(line)
    
    for line in lines:
        line = line.split(":", 1)
        for ch in line[1]:
            if ch == "0":
                print("\033[0;37;40m\033[0;30;40m"+ch+"\033[0;37;48m", end="")
            elif ch == "1":
                print("\033[0;37;47m"+ch+"\033[0;37;48m", end="")
            else:
                print(ch, end="")