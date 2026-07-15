from os import system

if True:
    # program window parameters
    SCREEN_WIDTH = 130
    SCREEN_HEIGHT = 30

    system(f'mode con: cols={SCREEN_WIDTH} lines={SCREEN_HEIGHT}')

    TERMINAL_WIDTH = 100
    SCREEN_MARGIN = int((SCREEN_WIDTH - TERMINAL_WIDTH) / 2)

def is_main():
    if __name__ == "__main__":
        return True
    else:
        return False

def screen(text, width=80, center=0):

    system('cls')

    # print("\n\n\n\n\n")

    if width != TERMINAL_WIDTH:
        terminal_margin = int((TERMINAL_WIDTH - width) / 2)
    else: 
        terminal_margin = 0

    textcont = text.split()
    
    sample = ""
    display = ""
    new_lines = 0

    for i,word in enumerate(textcont):
        
        new_line_toggle = 0
        if "`" in word:
            if "@" in word:
                center = 1 - center % 2
            if "^" in word:
                new_line_toggle = word.count("^")
            if "_" in word:
                n = ""
                ci = word.index("_")
                count = 0
                while True:
                    count += 1
                    try:
                        if (ci + count + 1) <= len(word):
                            assert type(int(word[ci + count])) == int
                            n += word[ci + count]
                        else:
                            break
                    except:
                        break
                if n != "":
                    word = " " * int(n)
            else:
                word = ""
        if new_line_toggle == 0:
            if (len(word) + 1 + len(sample) + terminal_margin * 2) > TERMINAL_WIDTH:
                center_margin = int((width - len(sample)) / 2)
                display += "." * SCREEN_MARGIN + " " * terminal_margin + " " * (center_margin + (len(sample) % 2)) * center + sample + " " * center_margin + " " * center_margin * (1 - center % 2) + " " * terminal_margin + " " * (len(sample) % 2) * (1 - center % 2) + "." * SCREEN_MARGIN + "\n"
                sample = word
                new_lines += 1
            else:
                if sample == "":
                    sample = word
                else:
                    sample += f" {word}"

            if i == len(textcont)-1:
                center_margin = int((width - len(sample)) / 2)
                display += "." * SCREEN_MARGIN + " " * terminal_margin + " " * (center_margin + (len(sample) % 2)) * center + sample + " " * center_margin + " " * center_margin * (1 - center % 2) + " " * terminal_margin + " " * (len(sample) % 2) * (1 - center % 2)  + "." * SCREEN_MARGIN + "\n"
                new_lines += 1
        else:
            for _ in range(new_line_toggle):
                center_margin = int((width - len(sample)) / 2)
                display += "." * SCREEN_MARGIN + " " * terminal_margin + " " * (center_margin + (len(sample) % 2)) * center + sample + " " * center_margin + " " * center_margin * (1 - center % 2) + " " * terminal_margin + " " * (len(sample) % 2) * (1 - center % 2)  + "." * SCREEN_MARGIN + "\n"
                sample = ""
                new_lines += 1
        

    height_gap = round((SCREEN_HEIGHT - new_lines - new_lines % 2) / 2)
    print("\n" * (height_gap - round(SCREEN_HEIGHT * .1))) 
    
    print(display)
    if is_main():
        input()

if is_main():
    text = "This is a string of text that I will use as a sample `_5 with which to test my screen function." \
    " `@^ It needs to be long so that I can work and test `^ different features and changes to make sure everything works." \
    " `@^ This is an additional line to test an additional feature."

    # text = "Day 1 | 5:00 PM | Clear Sky ^ Jonaston Main Road"

    select = 80
    while select > 50:
        screen(text,select,0)
        system('cls')
        screen(text,select,1)
        select -= 2
        system('cls')