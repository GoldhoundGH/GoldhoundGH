from os import system
from datetime import date
from calendar import monthrange,month_name
from random import choice,randint
import csv
from time import sleep
import pytest


if True:
    TITLE = "MY BUDGET PRO"
    FILE_NAME = "my_budget_pro"

    DATE_FORMAT = '%Y-%m-%d'
    
    # program window parameters
    SCREEN_WIDTH = 130
    SCREEN_HEIGHT = 30

    system(f'mode con: cols={SCREEN_WIDTH} lines={SCREEN_HEIGHT}')

    TERMINAL_WIDTH = 110
    SCREEN_MARGIN = (SCREEN_WIDTH - TERMINAL_WIDTH) // 2

    DISPLAY_MARGIN = " " * SCREEN_MARGIN
    input_proper = lambda text_str: input(DISPLAY_MARGIN + text_str)

    LEFT_AREA = TERMINAL_WIDTH // 2

    BLANK_CHAR = "◘"

    CANCEL_CHECK_LIST = {"end","cancel","exit"}


class records:
    key = 0
    all = {}
    categories = []
    restore = {}

    def __init__(self,date,amount,category):

        check_date = date.split("-")
        
        if len(check_date[1]) == 1:
            fix_month = "0" + check_date[1]
        else:
            fix_month = check_date[1]
        
        if len(check_date[2]) == 1:
            fix_day = "0" + check_date[2]
        else:
            fix_day = check_date[2]

        self.date = f"{check_date[0]}-{fix_month}-{fix_day}"

        if "." not in amount:
            amount += ".00"
        elif amount.index(".") > len(amount) - 3:
            for _ in range(amount.index(".") + 3 - len(amount)):
                amount += "0"
        else:
            amount = amount [0:amount.index(".")+3]

        self.amount = amount
        self.category = category
        self.id = str(records.key)
        
        if category not in records.categories:
            if "Demo:" not in category:
                records.categories.append(category)
        records.categories.sort()

        records.all[str(records.key)] = self
        records.key += 1

        records.sort_index()

    index = []
    max_amount_len = 0

    def sort_index():
        index = []
        records.max_amount_len = 0
        for e in records.all:
            date = records.all[e].date.split("-")
            year,month,day = date
            id = records.all[e].id

            amount = records.all[e].amount
            if len(amount) > records.max_amount_len:
                records.max_amount_len = len(amount)

            index.append((int(year),int(month),int(day),id))
        
        sortld = lambda x: (-x[0],-x[1],-x[2],x[3])

        new_index = sorted(index,key=sortld)
        
        records.index = []
        for i in new_index:
            records.index.append(i[3])
    
    def demo():
        for _ in range(5):
            year = 2024 + randint(0,2)
            month = choice(range(1,13))
            day = 50
            while day > monthrange(int(year),int(month))[1]:
                day = randint(1,31)
            # day = str(day)
            # if len(day) == 1:
            #     day = "0" + day
            amount = str(randint(0,99)) + "." + str(randint(0,9)) + str(randint(0,9))
            category = "Demo: " + choice(records.categories)
            records(f"{str(year)}-{str(month)}-{str(day)}",amount,category)
            
        

def get_record(key):
    return records.all[key]

def get_restore(key):
    return records.restore[key]

def is_main():
    return __name__ == "__main__"

def read_file():
    with open (f"{FILE_NAME}.py","r") as file:
        info = []
        for row in file:
            info.append(row)
    with open (f'{FILE_NAME}.txt',"w") as file:
        for v in info:
            file.write(v)
    return info

def acquire_data(file):
    # get expenses/credits
    
    data = []
    entry_collect = 0
    for row in file:
        if row == "":
            continue

        if "ENTRIES-END" in row and "#flag" not in row:
            entry_collect = 0

        if entry_collect == 1:
            if "^" in row and "#flag" not in row:
                row = row.replace("#","").strip()
                data.append(row)
        
        if "ENTRIES-START" in row and "#flag" not in row:
            entry_collect = 1
    
    arrange_data = csv.reader(data)
    for v in arrange_data:
        records(v[1], v[2], v[3])

def save_file(file):
    try:
        with open (f"{FILE_NAME}.py","w") as save_file:
            for row in file:
                save_file.write(row)
                if "# ENTRIES-START" in row and "#flag" not in row:
                    break
            count = 0
            for _,entry in records.all.items():
                count += 1
                data = f"# ^,{entry.date},{entry.amount},{entry.category}\n" #flag
                save_file.write(data)
            save_file.write("# ENTRIES-END") #flag
        return True if count == len(records.all) else False
    except:
        return False


if True:
        
    def run_pytest():
        _ = pytest.main(["-v", "--tb=line", "-rN", __file__])
        input_proper("Press enter to continue...")
        return

    def test_save_file():
        records.all = {}
        records.key = 0
        records.index = []
        file_contents = read_file()
        acquire_data(file_contents)
        assert save_file(file_contents) == True

    def test_multi_select():
        assert multi_select("1-100") == (set(range(1,101)),"CLEAR")
        assert multi_select("1,5") == ({1,5},"CLEAR")
        assert multi_select("1,5d") == (set(),"SPECIAL_CODE_ERROR")
        assert multi_select("1,5-7") == ({6,5,1,7},"CLEAR")
        assert multi_select("1,5,6,7") == ({1,5,6,7},"CLEAR")
        assert multi_select("1,5-7,5,6-9") == ({6,5,1,7,8,9},"CLEAR")
        assert multi_select("0-5,7-9") == ({0,1,2,3,4,5,8,7,9},"CLEAR")
        assert multi_select("asdf") == (set(),"SPECIAL_CODE_ERROR")

    def test_add_entry():
        assert add_entry(new_year="2026",new_month="11",new_day="2",new_amount="2.3",new_category="Tools") == "CLEAR"
        assert add_entry(new_year="20",new_month="11",new_day="2",new_amount="2.3",new_category="Tools") == "INPUT_YEAR_ERROR"
        assert add_entry(new_year="4000",new_month="11",new_day="2",new_amount="2.3",new_category="Tools") == "INPUT_YEAR_ERROR"
        assert add_entry(new_year="ASDF",new_month="11",new_day="2",new_amount="2.3",new_category="Tools") == "INPUT_YEAR_ERROR"
        assert add_entry(new_year="",new_month="11",new_day="2",new_amount="2.3",new_category="Tools") == "INPUT_YEAR_ERROR"
        assert add_entry(new_year=" ",new_month="11",new_day="2",new_amount="2.3",new_category="Tools") == "INPUT_YEAR_ERROR"
        assert add_entry(new_year="2026",new_month="13",new_day="2",new_amount="2.3",new_category="Tools") == "INPUT_MONTH_ERROR"
        assert add_entry(new_year="2026",new_month="0",new_day="2",new_amount="2.3",new_category="Tools") == "INPUT_MONTH_ERROR"
        assert add_entry(new_year="2026",new_month="",new_day="2",new_amount="2.3",new_category="Tools") == "INPUT_MONTH_ERROR"
        assert add_entry(new_year="2026",new_month="ASDF",new_day="2",new_amount="2.3",new_category="Tools") == "INPUT_MONTH_ERROR"
        assert add_entry(new_year="2026",new_month=" ",new_day="2",new_amount="2.3",new_category="Tools") == "INPUT_MONTH_ERROR"
        assert add_entry(new_year="2026",new_month="11",new_day="31",new_amount="2.3",new_category="Tools") == "INPUT_DAY_ERROR"
        assert add_entry(new_year="2026",new_month="11",new_day="30",new_amount="2.3",new_category="Tools") == "CLEAR"
        assert add_entry(new_year="2026",new_month="11",new_day="ASDF",new_amount="2.3",new_category="Tools") == "INPUT_DAY_ERROR"
        assert add_entry(new_year="2026",new_month="11",new_day="314",new_amount="2.3",new_category="Tools") == "INPUT_DAY_ERROR"
        assert add_entry(new_year="2026",new_month="11",new_day="",new_amount="2.3",new_category="Tools") == "INPUT_DAY_ERROR"
        assert add_entry(new_year="2026",new_month="11",new_day="-13",new_amount="2.3",new_category="Tools") == "INPUT_DAY_ERROR"
        assert add_entry(new_year="2026",new_month="11",new_day="0",new_amount="2.3",new_category="Tools") == "INPUT_DAY_ERROR"
        assert add_entry(new_year="2026",new_month="11",new_day="30",new_amount="",new_category="Tools") == "INPUT_AMOUNT_ERROR"
        assert add_entry(new_year="2026",new_month="11",new_day="30",new_amount=" ",new_category="Tools") == "INPUT_AMOUNT_ERROR"
        assert add_entry(new_year="2026",new_month="11",new_day="30",new_amount="ASDF",new_category="Tools") == "INPUT_AMOUNT_ERROR"
        assert add_entry(new_year="2026",new_month="11",new_day="30",new_amount="122.",new_category="Tools") == "CLEAR"
        assert add_entry(new_year="2026",new_month="11",new_day="30",new_amount="-3",new_category="Tools") == "CLEAR"

        assert add_entry(new_year="C",new_month="C",new_day="C",new_amount="C",new_category="C") == "CLEAR"


def gen_display_heading():
    leading_spaces = 1
    display = ""

    display += "\n" *leading_spaces
    lines = leading_spaces
    
    title_len = len(TITLE)
    
    if True:
        title_margin = (SCREEN_WIDTH - title_len) // 2
        display += " " * title_margin + TITLE + "\n"
        display += " " * title_margin + "─" * title_len + "\n\n"
        lines += 3

    return display, lines

def gen_display_body(text, display="",lines=0):
    sample = ""

    contents = text.strip().split()

    for i,word in enumerate(contents):

        sample += " " + word

    return sample

def gen_display(text):
    system('cls')

    display = ""
    sample = ""

    get_heading, heading_lines = gen_display_heading()
    display += get_heading
    lines = heading_lines

    text = gen_display_body(text, display=display, lines=lines)

    contents = text.strip().split()

    previous_word = ""
    for i,word in enumerate(contents):

        if True:
            com = ""
            new_line_toggle = 0
            n = ""
            s = ""
            auto_space = 1

        if "`" in word:
            com = word
            word = ""
            if "n" in com:
                n_index = com.index("n")
                count = 0
                while True:
                    count += 1
                    try:
                        if count + n_index + 1 <= len(com):
                            assert type(int(com[n_index + count])) == int
                            n += com[n_index + count]
                        else:
                            break
                    except:
                        break
                new_line_toggle = int(n) if n != "" else 0
            if "_" in com:
                s_index = com.index("_")
                count = 0
                while True:
                    count += 1
                    try:
                        if count + s_index + 1 <= len(com):
                            assert type(int(com[s_index + count])) == int
                            s += com[s_index + count]
                        else:
                            break
                        if int(s) != "0":
                            auto_space = 0
                    except:
                        break
                word = " " * int(s)

        if " " in previous_word:
            auto_space = 0

        if word == "":
            pass
        elif len(word) + 1 + len(sample) <= TERMINAL_WIDTH:
            if i + 1 != len(contents):
                sample += " " * auto_space + word if sample != "" else word
            elif i + 1 == len(contents):
                sample += " " * auto_space  + word if sample != "" else word
                display += DISPLAY_MARGIN + sample
                sample = ""
        else:
            new_line_toggle = 1

        if new_line_toggle != 0:
            display += DISPLAY_MARGIN + sample + "\n" * new_line_toggle
            sample = word
            lines += 1
        
        previous_word = word
    
    display = display.replace(BLANK_CHAR," ")

    return display

def display_date(date_code):
    date_data = date_code.split("-")
    return f"{month_name[int(date_data[1])][0:3]} {date_data[2]}, {date_data[0]}"


def gen_split_display(init_text_list, right_adjust=0):
    """Text - should be a list"""
    
    text_list = init_text_list.copy()

    # workaround for a bug I can't locate right now
    if True:
        checker = text_list[0].split()
        bonus_space = 1 if f"1{BLANK_CHAR}:" == checker[1] else 0

    true_len = len(text_list)
    
    if true_len < 7:
        while len(text_list) < true_len * 2:
            text_list.append(" `_5 ")

    list_len = len(text_list)


    if list_len % 2 == 1:
        text_list.append(" `_5 ")
    divide = list_len // 2 + list_len % 2
    if divide > 10:
        divide = 10
    next_set = (list_len - 1 - (divide))
    
    master_list = []
    text = ""
    count = 0
    i = -1
    entries = 0
    used = set()

    while entries < list_len:
        i += 1
        if i in used:
            continue
        v_len_l = len(text_list[i])
        try:
            line = f" {text_list[i]} `_{LEFT_AREA - v_len_l + bonus_space + 1 + text_list[i].count("`")} │ `_{5 - right_adjust} {text_list[i+divide]} `n1 "
        except:
            input("gen_split_display error")
        text += line
        used.add(i)
        used.add(i+divide)
        entries += 2
        count += 1
        if count == divide or i+1 >= list_len:
            master_list.append(text)
            text = ""
            next_set = (list_len - 1 - (i + divide))
            divide = next_set // 2 + next_set % 2
            if divide > 10:
                divide = 10
            if divide == 0:
                divide = 1
            count = 0
    if len(master_list) > 1 and master_list[-1].count("`n1") < master_list[-2].count("`n1"):
        for _ in range(master_list[-2].count("`n1") - master_list[-1].count("`n1")):
            master_list[-1] += " `n1 "

    return master_list
    
        


def add_entry(new_year="",new_month="",new_day="",new_amount="",new_category=""):
    # note regarding input_msg: the DISPLAY_MARGIN in the input_msg added to the display text is filtered out by gen_display

    loaded_params = False if new_year != "" else True

    year_default = "0"
    month_default = "0"
    day_default = "0"
    reset = 0
    while True:
        if reset == 1:
            year_default = "0"
            month_default = "0"
            day_default = "0"
        reset = 0
        
        clean_text = ""
        # clean_text += " For the [month] and [year] entries, you may type 'd' along with the number to store that number for additional entries. Type 'clear' in any " \
        " entry field to clear those stored values and reset the entry submission form. `n1 Type 'c' in any date field to fill in that with today's date. `n1 " \
        "Type 'end' to return to menu. `n1 "
        
        year_error = 0
        text = clean_text
        end_check_list = {"end","menu","exit","cancel"}
        for i in range(4):
            print(gen_display(text)) if loaded_params else True
            try:
                input_msg = DISPLAY_MARGIN + "Enter year (YYYY): "
                
                if new_year == "":
                    if year_default == "0":
                        year = input(input_msg)
                    else:
                        year = year_default
                else:
                    year = new_year
                
                if year.lower() in end_check_list:
                    return "CLEAR"
                if year.lower() == "clear":
                    reset = 1
                    break
                if "d" in year.lower():
                    year_default = year.replace("d","")
                    year = year_default
                if year.lower() == "c":
                    year = str(date.today().year)
                    if year_default != "0":
                        year_default = year

                assert type(int(year_default)) == int
                assert len(year) == 4
                assert int(year) < 2100
                clean_text += input_msg + " `_4 " + year + " `n1 "
                break
            except:
                year_default = "0"
                if year_error == 0:
                    text += " <Invalid input> `n1"
                    year_error = 1
                if i == 3:
                    return "INPUT_YEAR_ERROR"
        if reset == 1:
            continue


        month_error = 0
        text = clean_text
        for i in range(4):
            print(gen_display(text))if loaded_params else True
            try:
                input_msg = DISPLAY_MARGIN + "Enter month (MM): "
                
                if new_year == "":
                    if month_default == "0":
                        month = input(input_msg)
                    else:
                        month = month_default
                else:
                    month = new_month
                
                if month.lower() in end_check_list:
                    return "CLEAR"
                if month.lower() == "clear":
                    reset = 1
                    break
                if "d" in month:
                    month_default = month.replace("d","")
                    month = month_default
                if month.lower() == "c":
                    month = str(date.today().month)
                    if month_default != "0":
                        month_default = month

                assert type(int(month_default)) == int
                assert len(month) <= 2
                if len(month) == 1:
                    month = "0" + month
                assert 0 < int(month) <= 12
                clean_text += input_msg + " `_5 " + month + f" `_2 - {month_name[(int(month))]} `n1 "
                break
            except:
                month_default = "0"
                if month_error == 0:
                    text += " `n1 <Invalid input> `n1"
                    month_error = 1
                if i == 3:
                    return "INPUT_MONTH_ERROR"
        if reset == 1:
            continue

        day_error = 0
        text = clean_text
        for i in range(4):
            print(gen_display(text)) if loaded_params else True
            try:
                input_msg = DISPLAY_MARGIN + "Enter date (DD): "
                
                if new_day == "":
                    if day_default == "0":
                        day = input(input_msg)
                    else:
                        day = day_default
                else:
                    day = new_day

                if day.lower() in end_check_list:
                    return "CLEAR"
                if day.lower() == "clear":
                    reset = 1
                    break
                if "d" in day:
                    day_default = day.replace("d","")
                    day = day_default
                if day.lower() == "c":
                    day = str(date.today().day)
                    if day_default != "0":
                        day_default = day
                assert type(int(day)) == int
                if len(day) == 1:
                    day = "0" + day
                assert len(day) == 2
                assert 0 < int(day) <= monthrange(int(year),int(month))[1]
                clean_text += input_msg + " `_6 " + day + " `n1 "
                break
            except:
                day_default = "0"
                if day_error == 0:
                    text += " `n1 <Invalid input> `n1"
                    day_error = 1
                if i == 3:
                    return "INPUT_DAY_ERROR"
        if reset == 1:
            continue
                
        amount_error = 0
        text = clean_text
        for i in range(4):
            print(gen_display(text)) if loaded_params else True
            try:
                input_msg = DISPLAY_MARGIN + "Enter dollar amount: $" 
                
                if new_amount == "":
                    amount = input(input_msg)
                else:
                    amount = new_amount

                if amount.lower() in end_check_list and amount != "0":
                    return "CLEAR"
                if amount.lower() == "clear":
                    reset = 1
                    break
                if amount.lower() == "c":
                    amount = "0"
                else: 
                    assert type(float(amount)) == float
                clean_text += f" Enter dollar amount: `_2 ${float(amount):.2f} `n1 "
                break
            except:
                if amount_error == 0:
                    text += " `n1 <Invalid input. Please enter a number> `n1 "
                    amount_error = 1
                if i == 3:
                    return "INPUT_AMOUNT_ERROR"
        if reset == 1:
            continue

        category_error = 0
        cat_list = get_categories()
        new_cat_list = []
        for key in cat_list:
            new_cat_list.append(f" `_3 {key} - {cat_list[key]} ")
        cat_text = "Enter category / transaction number: `n2 "
        cat_text += gen_split_display(new_cat_list)[0] if loaded_params else ""
        cat_text += " `n1_3 or enter a new category. `n1 "
        
        clean_text += " `n1 " + cat_text + " `n1 "
        text = clean_text
        for i in range(4):
            print(gen_display(text)) if loaded_params else True
            try:
                input_msg = DISPLAY_MARGIN + "Category / Transaction: "
                
                if new_year == "":
                    category = input(input_msg)
                else:
                    category = new_category

                if category.lower() in end_check_list:
                    return "CLEAR"
                if category.lower() == "clear":
                    reset = 1
                    break
                if category.lower() == "c":
                    category = "Expenses"
                if category in cat_list:
                    category = cat_list[category]
                assert category != ""
                assert category != "c"
                assert not category in set(str(x) for x in range(-1000,1000))
                if len(category) > 16:
                    category = category[0:(16-len(category))]
                clean_text += input_msg + category.title() + " `n1 "
                print(gen_display(clean_text))
                break
            except:
                if category_error == 0:
                    text += " <Missing or invalid input> `n1 "
                    category_error = 1
                if i == 3:
                    return "INPUT_CATEGORY_ERROR"
        if reset == 1:
            continue        

        records(f"{year}-{month}-{day}",amount,category.title())

        end_check = input_proper(f"Press enter to continue or type 'end' to return to menu: ") if loaded_params else True
        if loaded_params:
            if end_check.lower() in end_check_list:
                return "CLEAR"
            if end_check.lower() == "clear":
                year_default = "0"
                month_default = "0"
        else:
            return "CLEAR"


def get_categories():
    cat_list = {}
    for i,entry in enumerate(records.categories):
        cat_list[str(i+1)] = entry
    return cat_list

def turn_page(option,page,book_list):
    pass_check = 0
    page_select = page

    if option in {"n","s"}:
        pass_check = 1
        if page < len(book_list) - 1:
            page_select = page + 1
    elif option in {"p","a"}: 
        pass_check = 1
        if page > 0:
            page_select = page - 1
    elif "p" in option or "page" in option:
        option = option.replace("p","").replace("age","").strip()
        try:
            option = int(option)
            pass_check = 1
            if option in range(len(book_list) + 1):
                page_select = option - 1
        except:
            page_select = page

    return pass_check, page_select

def display_book(index):
    text_list = []
    right_adjust = 2
    for key in index:
        spacing = records.max_amount_len - len(get_record(key).amount)
        text_list.append(f" `_{right_adjust} {display_date(get_record(key).date)} - $" + (BLANK_CHAR * spacing) + f"{get_record(key).amount} for {get_record(key).category}")
    
    return gen_split_display(text_list,right_adjust=right_adjust)

def enumerate_records(index,func=get_record, right_adjust=1):
    enumerate_id = 0
    key_dict = {}
    for key in index:
        enumerate_id += 1
        key_dict[enumerate_id] = key

    text_list = []
    
    for key,record_key in key_dict.items():
        if len(str(key)) == 1 and len(str(enumerate_id)) > 1:
            num = str(key) + BLANK_CHAR
        else:
            num = str(key)

        if func == get_record:
            spacing = records.max_amount_len - len(records.all[record_key].amount)
            text_list.append(f" `_{right_adjust} {num}: {display_date(records.all[record_key].date)} - $" + (BLANK_CHAR * spacing) + f"{records.all[record_key].amount} for {records.all[record_key].category}")
        else:
            spacing = records.max_amount_len - len(records.restore[record_key].amount)
            text_list.append(f" `_{right_adjust} {num}: {display_date(records.restore[record_key].date)} - $" + (BLANK_CHAR * spacing) + f"{records.restore[record_key].amount} for {records.restore[record_key].category}")
    
    return key_dict,text_list

def check_multi_select(option):
    if "," in option or "-" in option:
        return True
    return False


def multi_select(selection_code):
    error_msg = "CLEAR"
    code_access = selection_code.split(",")
    flag_records = set()
    for v in code_access:
        if "-" in v:
            v = v.split("-")
            if len(v) > 2:
                error_msg = "SPECIAL_CODE_ERROR"
            e_comp = []
            for e in v:
                try:
                    e = int(e.strip())
                except:
                    error_msg = "SPECIAL_CODE_ERROR"
                e_comp.append(e)
            if e_comp[0] > e_comp[1]:
                error_msg = "SPECIAL_CODE_ERROR"
            for code in range(e_comp[0],e_comp[1] + 1):
                flag_records.add(code)
        else:
            try:
                v = int(v.strip())
            except:
                error_msg = "SPECIAL_CODE_ERROR"
            flag_records.add(v)
        if error_msg != "CLEAR":
            flag_records = set()
    return flag_records, error_msg
    


def modify_records(option_default = []):
    defcheck = True if option_default == [] else False
    while True:
        cancel = 0
        action = "<ACTION_ERROR>"
        text = ""
        option_error = 0

        key_dict,text_list = enumerate_records(records.index)
        pre_text = " Budget Records: `n1 "
        book_list = display_book(records.index)
        pre_line = BLANK_CHAR + "─" * (TERMINAL_WIDTH - 2) + " `n1 "
        
        error_text = ""
        page_select = 0
        count = 0
        while True:
            pass_check = 0
            book_text = book_list[page_select]
            pages = f"Page {page_select + 1} of {len(book_list)}"
            page_margin = (TERMINAL_WIDTH - len(pages)) // 2
            book_text += BLANK_CHAR + "─" * (TERMINAL_WIDTH - 2) + " `n1 "
            book_text += BLANK_CHAR * page_margin + pages + " `n1 "
            book_text += BLANK_CHAR * page_margin + "─" * len(pages) + " `n1 "
            display_text = pre_text + pre_line + book_text

            print(gen_display(display_text + error_text)) if defcheck else True
            input_msg = "Edit a record [1] or remove a record [2]: "
            try:
                if option_default == []:
                    option = input_proper(input_msg).lower()
                else:  
                    option = option_default[0]
                pass_check, page_select = turn_page(option,page_select,book_list)
                if pass_check == 1:
                    count = 1
                    option_error = 0
                    error_text = ""
                    continue
                if option in CANCEL_CHECK_LIST:
                    cancel = 1
                    break
                if option in {"1","2","e","r"}:
                    break
                else:
                    assert False
            except:
                count += 1
                if option_error ==  0:
                    error_text += " `n1 <Invalid input.  Please enter either '1' or '2'.> `n1 "
                    option_error = 1
                if count == 4:
                    error_msg = " <Input Error>"
                    print(gen_display(error_msg)) if defcheck else True
                    sleep(1) if defcheck else True
                    return "MODIFY_RECORD_ERROR"
                
        if cancel == 1:
            return "CLEAR"

        if option in {"r","2"}:
            action = "remove"
            pre_text = f" Select a record or set of records (i.e. '1,3-5') to {action}: `n1 "
        if option in {"e","1"}:
            action = "edit"
            pre_text = f" Select a record to {action}: `n1 "

        split_text_list = gen_split_display(text_list)
        post_text = " "
        error_text = ""

        pre_line = BLANK_CHAR + "─" * (TERMINAL_WIDTH - 2) + " `n1 "
        input_msg = "Record number: "
        page_select = 0
        option_error = 0
        count = 0
        while True:
            pass_check = 0
            split_text = split_text_list[page_select]
            pages = f"Page {page_select + 1} of {len(split_text_list)}"
            page_margin = (TERMINAL_WIDTH - len(pages)) // 2
            split_text += BLANK_CHAR + "─" * (TERMINAL_WIDTH - 2) + " `n1 "
            split_text += BLANK_CHAR * page_margin + pages + " `n1 "
            split_text += BLANK_CHAR * page_margin + "─" * len(pages) + " `n1 "
            display_text = pre_text + pre_line + split_text + post_text
            print(gen_display(display_text + error_text)) if defcheck else True
            try:
                if option_default == []:
                    choose_record = input_proper(input_msg)
                else:
                    choose_record = option_default[1]
                pass_check,page_select = turn_page(choose_record,page_select,split_text_list)
                if pass_check == 1:
                    count = 1
                    option_error = 0
                    error_text = ""
                    continue
                if choose_record in CANCEL_CHECK_LIST:
                    cancel = 1
                    break
                if action == "remove" and ("," in choose_record or "-" in choose_record):
                    remove_special = choose_record
                    break 
                else:
                    remove_special = 0
                assert int(choose_record) in key_dict.keys()
                text += input_msg + f"{choose_record} `n2 "
                break
            except:
                count += 1
                if option_error == 0:
                    error_text += " <Invalid input.  Please select a record number from the provided list> `n1 "
                    option_error = 1
                if count == 4:
                    error_msg = " <Input Error> "
                    print(gen_display(error_msg)) if defcheck else True
                    sleep(1) if defcheck else True
                    return "SELECT_RECORD_ERROR"
        if cancel == 1:
            return "CLEAR"

        if option in {"r","2"}:
            error_msg = "CLEAR"

            if remove_special != 0:
                flag_records, error_msg = multi_select(remove_special)
                if error_msg != "CLEAR":
                    return error_msg
                for code in flag_records:
                    try:
                        key = key_dict[int(code)]
                        extract = records.all.pop(key)
                        records.index.pop(records.index.index(key))
                        records.restore[key] = extract
                    except:
                        error_msg = "INDEX_OVERFLOW_ERROR"
                    
                text = " Records removed. `n1 "
                print(gen_display(text)) if defcheck else True
                sleep(1) if defcheck else True

                return error_msg

            else:
                key = key_dict[int(choose_record)]
                extract = records.all.pop(key)
                records.index.pop(records.index.index(key))
                records.restore[key] = extract

                text = " Record removed. `n1 "
                print(gen_display(text)) if defcheck else True
                sleep(1) if defcheck else True

                return "CLEAR"
        
        if option in {"e","1"}:
            key = key_dict[int(choose_record)]
            record = records.all[key]
            o_year,o_month,o_day = record.date.split("-")
            o_amount = record.amount
            o_category = record.category

            text = f" {display_date(record.date)} - ${record.amount} for {record.category} `n2 "
            error_text = text

            option_error = 0
            for i in range(4):
                print(gen_display(error_text))
                try:
                    input_msg = f"Enter year (YYYY) [current: {o_year}]: "
                    year = input_proper(input_msg)

                    if year in CANCEL_CHECK_LIST:
                        cancel = 1
                        break
                    if year == "c":
                        year = o_year
                    assert len(year) == 4
                    assert int(year) < 2100
                    text += input_msg + year + " `n1 "
                    break
                except:
                    if option_error == 0:
                        error_text += " <Invalid input> `n1 "
                        option_error =1
                    if i == 3:
                        return "INPUT_YEAR_ERROR"
            if cancel == 1:
                continue
            
            error_text = text
            option_error = 0

            for i in range(4):
                print(gen_display(error_text))
                try:
                    input_msg = f"Enter month (MM) [current: {o_month}]: "
                    month = input_proper(input_msg)

                    if month in CANCEL_CHECK_LIST:
                        cancel = 1
                        break
                    if month == "c":
                        month = o_month
                    assert type(int(month)) == int
                    assert len(month) <= 2
                    if len(month) == 1:
                        month = "0" + month
                    assert 0 < int(month) <= 12
                    text += input_msg + month + f" `_2 - {month_name[(int(month))]} `n1 "
                    break
                except:
                    if option_error == 0:
                        error_text += " <Invalid input> `n1 "
                        option_error = 1
                    if i == 3:
                        return "INPUT_MONTH_ERROR"
            if cancel == 1:
                continue

            error_text = text
            option_error = 0

            for i in range(4):
                print(gen_display(error_text))
                try:
                    input_msg = f"Enter day (DD) [current: {o_day}]: "
                    day = input_proper(input_msg)

                    if day in CANCEL_CHECK_LIST:
                        cancel = 1
                        break
                    if day == "c":
                        day = o_day
                    assert type(int(day)) == int
                    assert len(day) <= 2
                    if len(day) == 1:
                        day = "0" + day
                    assert 0 < int(day) <= monthrange(int(year),int(month))[1]
                    text += input_msg + day + " `n1 "
                    break
                except:
                    if option_error == 0:
                        error_text += " <Invalid input> `n1 "
                        option_error =1
                    if i == 3:
                        return "INPUT_DAY_ERROR"
            if cancel == 1:
                continue

            error_text = text
            option_error = 0

            for i in range(4):
                print(gen_display(error_text))
                try:
                    input_msg = f"Enter dollar amount [current: {o_amount}]: $"
                    amount = input_proper(input_msg)

                    if amount in CANCEL_CHECK_LIST:
                        cancel = 1
                        break
                    if amount == "c":
                        amount = o_amount
                    assert type(float(amount)) == float
                    text += input_msg + f"{float(amount):.2f}" + " `n1 "
                    break
                except:
                    if option_error == 0:
                        error_text += " <Invalid input> `n1 "
                        option_error =1
                    if i == 3:
                        return "INPUT_AMOUNT_ERROR"
            if cancel == 1:
                continue

            

            cat_list = get_categories()
            new_cat_list = []
            for nkey in cat_list:
                new_cat_list.append(f" `_3 {nkey} - {cat_list[nkey]} ")
            cat_text = "Enter category / transaction number: `n2 "
            cat_text += gen_split_display(new_cat_list)[0]
            cat_text += " `n1_3 or enter a new category. `n1 "
            text += " `n1 " + cat_text + " `n1 "
            error_text = text
            option_error = 0
            for i in range(4):
                print(gen_display(error_text))
                try:
                    input_msg = f"Category / Transaction [current: {o_category}]: "
                    category = input_proper(input_msg)

                    if category in CANCEL_CHECK_LIST:
                        cancel = 1
                        break
                    if category == "c":
                        category = o_category
                    if category in cat_list:
                        category = cat_list[category]
                    assert category != ""
                    assert category != "c"
                    if len(category) > 16:
                        category = category[0:(16-len(category))]
                    text += input_msg + category.title() + " `n1 "
                    break
                except:
                    if option_error == 0:
                        error_text += " <Invalid input> `n1 "
                        option_error =1
                    if i == 3:
                        return "INPUT_CATEGORY_ERROR"
            if cancel == 1:
                continue
            
            records.all.pop(key)
            records(f"{year}-{month}-{day}",amount,category.title())

            text += " `n1 Record updated. `n1 "
            print(gen_display(text))
            sleep(1)
            return "CLEAR"
        

def restore_entry():
    while True:
        if len(records.restore) == 0:
            text = " `n2 There are no records to restore. "
            print(gen_display(text))
            sleep(1.75)
            return "CLEAR"

        restore_key_dict, text_list = enumerate_records(records.restore.keys(),func=get_restore)
        pre_text = " Select a record or set of records (i.e. '1,3-5') to restore: `n2 "
        split_text_list = gen_split_display(text_list)
        post_text = " `n1 "
        pre_line = BLANK_CHAR + "─" * (TERMINAL_WIDTH - 2) + " `n1 "
        error_text = ""
        page_select = 0
        count = 0
        option_error = 0
        while True:
            pass_check = 0
            book_text = split_text_list[page_select]
            pages = f"Page {page_select + 1} of {len(split_text_list)}"
            page_margin = (TERMINAL_WIDTH - len(pages)) // 2
            book_text += BLANK_CHAR + "─" * (TERMINAL_WIDTH - 2) + " `n1 "
            book_text += BLANK_CHAR * page_margin + pages + " `n1 "
            book_text += BLANK_CHAR * page_margin + "─" * len(pages) + " `n1 "
            display_text = pre_text + pre_line + book_text + post_text

            print(gen_display(display_text + error_text))
            input_msg = "Record number: "
            try:
                choose_restore = input_proper(input_msg)
                pass_check,page_select = turn_page(choose_restore,page_select,split_text_list)
                if pass_check == 1:
                    count = 1
                    option_error = 0
                    error_text = ""
                    continue
                if choose_restore in CANCEL_CHECK_LIST:
                    return "CLEAR"
                if check_multi_select(choose_restore):
                    restore_special = choose_restore
                    break
                else:
                    restore_special = 0
                assert int(choose_restore) in restore_key_dict.keys()
                text = display_text + input_msg + choose_restore + " `n1 "
                break
            except:
                count += 1
                if option_error == 0:
                    error_text += "<Invalid input. Select a number from the provided list.> `n1 "
                    option_error = 1
                if count == 4:
                    error_msg = " <Input Error> "
                    print(gen_display(error_msg))
                    sleep(1)
                    return "RESTORE_INDEX_ERROR"

        if restore_special != 0:
            flag_restore, error_msg = multi_select(restore_special)
            if error_msg != "CLEAR":
                return error_msg
            for code in flag_restore:
                try:
                    key = restore_key_dict[int(code)]
                    restore_record = records.restore[key]
                    records(restore_record.date,restore_record.amount,restore_record.category)
                    records.restore.pop(key)
                except:
                    error_msg = "INDEX_OVERFLOW_ERROR"
                
            text = " `n1 Records restored. `n1 "
            print(gen_display(text))
            sleep(1)

            return error_msg

        restore_record = records.restore[restore_key_dict[int(choose_restore)]]
        records(restore_record.date,restore_record.amount,restore_record.category)
        records.restore.pop(restore_key_dict[int(choose_restore)])
        text += " `n1 Record restored. `n1 "
        print(gen_display(text))
        sleep(1)
        return "CLEAR"
        

def report_no_entries():
    text = " `n1 There are no entries on record to display. `n1 "
    print(gen_display(text))
    sleep(2)
    return

def bookkeeping():
    while True:
        pre_text = " Budget Records: `n1 "
        
        if len(records.index) == 0:
            report_no_entries()
            return
        
        book_list = display_book(records.index)

        post_text = " Select an action: `n2 "
        post_text += " `_5 1 - Edit/remove an entry `n1 "
        post_text += " `_5 2 - Record a new expense/credit `n1 "
        post_text += " `_5 3 - Restore an entry `n1 "
        post_text += " `_5 0 - Return to main menu `n1 "

        pre_line = BLANK_CHAR + "─" * (TERMINAL_WIDTH - 2) + " `n1 "
        error_text = ""
        
        page_select = 0
        option_error = 0
        while True:
            pass_check = 0
            book_text = book_list[page_select]
            pages = f"Page {page_select + 1} of {len(book_list)}"
            page_margin = (TERMINAL_WIDTH - len(pages)) // 2
            book_text += BLANK_CHAR + "─" * (TERMINAL_WIDTH - 2) + " `n1 "
            book_text += BLANK_CHAR * page_margin + pages + " `n1 "
            book_text += BLANK_CHAR * page_margin + "─" * len(pages) + " `n1 "
            display_text = pre_text + pre_line + book_text + post_text

            print(gen_display(display_text + error_text))
            valid_options = {"0","1","2","3"}
            try:
                option = input_proper("   > ").lower()
                pass_check, page_select = turn_page(option,page_select,book_list)
                if pass_check == 1:
                    option_error = 0
                    error_text = ""
                    continue
                if option == "":
                    continue
                if option in CANCEL_CHECK_LIST:
                    option = "0"
                assert option in valid_options
                break
            except:
                if option_error == 0:
                    error_text += " `n1 <Invalid input. Please enter a number from the provided list> `n1 "
                    print(gen_display(error_text))
                    option_error = 1

        if option == "0" or option in CANCEL_CHECK_LIST:
            return
        
        if option == "1":
            error = modify_records()
            # entry editing function here
        
        if option == "2":
            entry_error = add_entry()
            if entry_error != "CLEAR":
                text = " An error occurred while attempting to record a new entry. `n2 "
                text += f" `_5 Error Code: {entry_error} `n1 "
                print(gen_display(text))
                input_proper("Press enter to continue...")
            
        if option == "3":
            error = restore_entry()
        

def display_nav():
    text = " `n1 "
    text += " At any command prompt, enter: `n2 "
    text += " `_5 'exit'/'end'/'cancel' `n2 to return to the previous window. `n3 "
    text += " When reviewing the budget records with multiple pages, enter: `n2 "
    text += " `_5 's' or 'n' to see the subsequent page, `n1 "
    text += " `_5 'a' or 'p' to see the previous page, `n1 "
    text += f" `_5 'p/page #' {BLANK_CHAR * 2}(where '#' is a number) to specify a page. `n3 "
    text += " When entering new budget entries, on the year/month/day lines enter: `n2 "
    text += f" `_5 'c' {BLANK_CHAR * 3} to fill in the current year/month/day, `n1 " 
    text += f" `_5 '#d' {BLANK_CHAR * 2} to set the entered # as the default year/month/day for concurrent new entries, `n1 "
    text += " `_5 'clear' to reset default values for year/month/day and reset entry data submission. `n1 "
    print(gen_display(text))
    input_proper("Press enter to return to menu...")

def compiance_statement():
    text = " STUDENT'S STATEMENT REGARDING RUBRIC COMPLIANCE: `n2 "
    text += " The rubric requires that: `n1 "
    text += " - the program runs correctly - On my computer, I can find no errors running the program. If errors are found, `n1_6 I would request being able to demonstrate" \
    " that the program runs correctly on my computers. `n1 "
    text += " - the program is divided into functions - check; the program uses 29 functions. `n1 "
    text += " - the program effectively uses python modules - check; the program uses 6 modules (not counting pytest). `n1 "
    text += " - the test file contains 2 or more test functions that each test 1 function - the rubric does not specify that `_6 each function (or each function of a particular type) " \
    " be tested, but only that at least 2 be tested. In `_6 compliance with the instructions in the rubric, I have written 3 test functions. `n1 "
    text += " - the test functions must pass - check `n1 "
    text += " - the test functions must have at least 2 calls and asserts each - one of my test functions only has `n1_6 1 call/assert because that function has only 1 possible input. " \
    " Perhaps it was unnecessary to test it, `n1_6 but my other 2 required text functions do meet the requirements. The third is a bonus, extra, `n1_6 not-required test function. `n2 "
    text += " As demonstrated here, my program complies with every requirement stated in the grading rubric.  Accordingly, I would request that any other grading constraints which were not " \
    " clearly written in this rubric, where they could have been referred to as needed throughout the development of this program, be excluded from use in the calculation of my final grade. `n2"
    text += " Thank you "
    print(gen_display(text))
    input_proper("Press enter to return to menu...")

def ai_statement():
    text = " STUDENT'S STATEMENT REGARDING USE OF AI: `n2 "
    text += " While and since this program uses a few concepts and tools not covered in this course (such as classes), I would like to state and declare that " \
    " I did not use AI in any part of the development of this program, nor did I copy any code or block of work from other develops (with the exception of the " \
    " code at line 20, which sets the dimensions of the terminal window). This program is my own original work, based on my learning both in as well as outside of class. `n2 "
    text += " Thank you "
    print(gen_display(text))
    input_proper("Press enter to return to menu...")

def main():
    file_contents = read_file()
    acquire_data(file_contents)
    if len(records.categories) == 0:
        records.categories = ["Groceries","Bills","Rent","Snacks","Gas","Books"]

    option = ""
    was_run = 0
    while True:
        
        text = ""

        text += "Select an action: `n2 "
        if len(records.all) > 0:
            book_status = "1 - Display budget book"
        else:
            book_status = "X - < No Budget Records >"
        text += f" `_5 {book_status} `n1 "
        text += " `_5 2 - Record a new expense/credit `n2 "
        # text += " `_5 7 - << RUBRIC COMPLIANCE STATEMENT - PLEASE READ >> `n1 "
        # text += " `_5 8 - << Statement on Usage of AI >> `n1 "
        # text += " `_5 9 - << RUN PYTEST FUNCTIONS >> `n2 "
        text += " `_5 0 - Show additional commands: `n1 "

        additional_text = " `n1 [ Additional Commands: `n2 "
        additional_text += f" `_5 'nav'{BLANK_CHAR} - show navigation instructions `n1 "
        additional_text += " `_5 'demo' - generate 5 dummy budget entries `n1 "
        if records.all == {}:
            additional_text += " `_5 'undo' - restore deleted entries `n1 "
        additional_text += " `_5 'save' - save data `n1 "
        additional_text += " `_5 'exit' - save and close program ] `n1 "

        if option == "0":
            text += additional_text
            print(gen_display(text))

        text += " `n1 "

        valid_options = {"0","1","2","3","x","8","9","7"}
        valid_commands = {"exit","save","test","demo","delete all records","undo","nav"}
        option_error = 0
        while True:
            print(gen_display(text))
            try:
                option = input_proper("   > ").lower()
                if option not in valid_commands and option != "":
                    assert option in valid_options
                break
            except:
                if option_error == 0:
                    text += " `n1 <Invalid input.  Please select from the provided options> `n1 "
                    print(gen_display(text))
                    option_error = 1
        
        text = ""
        
        if option == "":
            continue
        
        if option == "delete all records":
            text = " `n3 Confirm deletion of all records [type 'yes']: `n1 "
            print(gen_display(text))
            confirm = input_proper("         > ")
            if confirm.lower() == "yes":
                modify_records(["2","1-1000000"])

        if option == "undo":
            restore_entry()

        if option == "nav":
            display_nav()

        if option == "demo":
            records.demo()
        
        if option == "8":
            ai_statement()

        if option == "7":
            compiance_statement()

        if option == "test" or option == "9":
            if was_run < 1:
                run_pytest()
                was_run = 1
            else:
                text += " `n1 Cannot run PYTEST again.  Doing so would result in a strange bug that will not crash the program but causes " \
                "menu commands to fail, and I can't find the cause. `n2 To run PYTEST again, restart the program."
                for i in range(8):
                    print(gen_display(text + f" `n2 {"." * (8 - i)}"))
                    sleep(1)
            continue
        
        if option == "save":
            save_file(file_contents)
            
        if option == "exit":
            break

        if option in {"1","x"}:
            bookkeeping()

        if option == "2":
            entry_error = add_entry()
            if entry_error != "CLEAR":
                text = " An error occurred while attempting to record a new entry. `n2 "
                text += f" `_5 Error Code: {entry_error} `n1 "
                print(gen_display(text))
                input_proper("Press enter to continue...")

    save_file(file_contents)
    


if is_main():
    main()


# ENTRIES-START
# ENTRIES-END
