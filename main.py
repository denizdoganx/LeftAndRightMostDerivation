# These global variables hold general data for execution of program
FILE_LL = 'll.txt'
FILE_LR = 'lr.txt'
FILE_INPUT = 'input.txt'
ll_table = list()
lr_table = list()
input_table = list()
terminals_of_ll_table = list()
non_terminals_of_ll_table = list()
parsing_table_of_ll_in_dict_format = dict()
parsing_table_of_lr_in_dict_format = dict()
first_action_of_ll_table = None


# For flow of program, we wrote this stack class
class Stack:
    def __init__(self):
        self.stack_array = list()

    def push(self, element):
        self.stack_array.append(element)

    def pop(self):
        if not self.is_empty():
            return self.stack_array.pop()
        return None

    def peek(self):
        if not self.is_empty():
            element = self.pop()
            self.push(element)
            return element
        return None

    def is_empty(self) -> bool:
        return len(self.stack_array) == 0

    def size(self) -> int:
        return len(self.stack_array)

    # We wrote this method as an extra to a normal stack class,
    # The purpose of the method is to fill the given string to the stack in reverse.
    def fill_in_the_stack(self, element):
        length = len(element)
        temp_terminal_element = ""
        temp_list = list()
        for i in range(length):
            temp_terminal_element += element[i]
            if terminals_of_ll_table.__contains__(temp_terminal_element) or non_terminals_of_ll_table.__contains__(
                    temp_terminal_element) or temp_terminal_element.upper() == 'ϵ':
                temp_list.append(temp_terminal_element)
                temp_terminal_element = ""

        for temp_element in temp_list.__reversed__():
            self.push(temp_element)


# This method prepares the dictionaries we use when checking for matches.
def convert_to_parsing_table():
    global first_action_of_ll_table
    row_num = 0
    for row in ll_table:
        column_num = 0
        for cell in row:
            # Firstly, terminals and non-terminals in ll_table are captured
            if row_num == 0 and column_num != 0:
                terminals_of_ll_table.append(cell)
            if row_num != 0 and column_num == 0:
                non_terminals_of_ll_table.append(cell)
            column_num += 1
        row_num += 1

    row_num = 0
    for row in ll_table:
        column_num = 0
        for cell in row:
            if row_num != 0 and column_num != 0:
                # Matches found here in ll_table are placed in the dictionary using a hashing mechanism
                parsing_table_of_ll_in_dict_format[
                    str(str(non_terminals_of_ll_table[row_num - 1]) + str(" ") + str(
                        terminals_of_ll_table[column_num - 1]))
                ] = cell
                # Also in these loops the first action in ll_table is saved in a global variable
                if (cell != "" or cell is not None) and first_action_of_ll_table is None:
                    first_action_of_ll_table = cell
            column_num += 1
        row_num += 1

    row_num = 0
    terminals_and_non_terminals = list()
    states = list()

    for row in lr_table:
        column_num = 0
        for cell in row:
            if column_num != 0 and row_num == 1:
                # Firstly, terminals and non-terminals in lr_table are captured
                terminals_and_non_terminals.append(cell)
            if column_num == 0 and row_num > 1:
                # the states also found in lr_table are stored in a list
                states.append(str(cell).split("_")[1])
            column_num += 1
        row_num += 1
    row_num = 0

    for row in lr_table:
        column_num = 0
        for cell in row:
            if row_num > 1 and column_num > 0:
                # Finally, the states in lr_table and
                # their matching terminal or non-terminals are placed in a dictionary with a hashing mechanism.
                parsing_table_of_lr_in_dict_format[
                    states[row_num - 2] + " " + terminals_and_non_terminals[column_num - 1]] = cell
            column_num += 1
        row_num += 1


# FILE_LL, FILE_LR and FILE_INPUT are to be read inside of this method
def read_files() -> bool:
    # Here, as an extra, we do not include spaces and \n characters in the text file in our data structures.
    try:
        global FILE_LL, FILE_LR, FILE_INPUT, ll_table, lr_table, input_table
        with open(FILE_LL, encoding="utf-8") as file_object_of_left_most_derivation:
            for lineText in file_object_of_left_most_derivation.readlines():
                lineTextWithoutSpace = lineText.replace(" ", "")
                lineTextWithoutNewLineAndSpace = lineTextWithoutSpace.replace("\n", "")
                pieces = lineTextWithoutNewLineAndSpace.split(";")
                ll_table.append(pieces)

        with open(FILE_LR, encoding="utf-8") as file_object_of_right_most_derivation:
            for lineText in file_object_of_right_most_derivation.readlines():
                lineTextWithoutSpace = lineText.replace(" ", "")
                lineTextWithoutNewLineAndSpace = lineTextWithoutSpace.replace("\n", "")
                pieces = lineTextWithoutNewLineAndSpace.split(";")
                lr_table.append(pieces)

        with open(FILE_INPUT, encoding="utf-8") as file_object_of_input:
            for lineText in file_object_of_input.readlines():
                if lineText.startswith("table"):
                    pass
                else:
                    lineTextWithoutSpace = lineText.replace(" ", "")
                    lineTextWithoutNewLineAndSpace = lineTextWithoutSpace.replace("\n", "")
                    pieces = lineTextWithoutNewLineAndSpace.split(";")
                    input_table.append(pieces)
        return True
    except FileNotFoundError:
        return False


# This method writes the data in a stack to the screen in the desired direction.
def get_string_in_stack(stack, length, direction="u") -> str:
    temp_stack = Stack()
    ret_string = ""
    for i in range(length):
        if direction == "u":
            ret_string += stack.peek()
        temp_stack.push(stack.pop())

    for j in range(length):
        if direction != "u":
            ret_string += temp_stack.peek()
        stack.push(temp_stack.pop())

    return ret_string


# The information text about the input to be processed is formatted and returned in this method.
def get_information_text(table_name, input_string) -> str:
    return f"\nProcessing input string {input_string} for {table_name}(1) parsing table.\n"


def processing_given_string(input_row):
    space_num = 20
    step = 1
    no_letters = "NO"  # this variable is used to write the console
    input_letters = "INPUT"  # this variable is used to write the console
    action_letters = "ACTION"  # this variable is used to write the console
    table_name = str(input_row[0])  # Getting LL or LR letters from given input_row
    input_string = input_row[1]  # Getting input from given input_row
    print(get_information_text(table_name, input_string))  # printing an information to console about input_string
    if table_name.lower() == 'll':
        stack_letters = "STACK"  # this variable is used to write the console
        input_stack = Stack()  # creating an input_stack to hold input string
        input_stack.fill_in_the_stack(input_string)  # input_string is filled in the stack
        current_action = first_action_of_ll_table  # getting first action from a global variable
        control_stack = Stack()
        control_stack.push("$")
        # Titles are wrote to console
        print(
            f"\t{no_letters:{space_num}}{stack_letters:{space_num}}{input_letters:{space_num}}{action_letters:{space_num}}")
        # First step is wrote to console
        printing_step_for_ll(step, control_stack, input_stack, current_action, space_num)
        control_stack.fill_in_the_stack((str(current_action).split("->"))[1].replace(" ", ""))
        next_action = ""
        while True:
            step += 1
            isDeleted = False
            deletedElement = None
            # If the elements at the top of the stack match, we will delete them.
            if control_stack.peek() == input_stack.peek():
                deletedElement = input_stack.peek()
                isDeleted = True
                # but if the matching values are '$' sign, the language recognized the string
                if deletedElement == '$':
                    next_action = "ACCEPTED"
                    printing_step_for_ll(step, control_stack, input_stack, next_action, space_num)
                    break
            # if a string is deleted, next action is edited accordingly
            if isDeleted:
                next_action = "Match and remove " + deletedElement

            else:
                # the matching character is checked, if the check result is an empty string,
                # the language does not recognize that string
                hash_index = control_stack.peek() + " " + input_stack.peek()
                try:
                    if parsing_table_of_ll_in_dict_format[hash_index] != "":
                        next_action = parsing_table_of_ll_in_dict_format[hash_index]
                    else:
                        next_action = f"REJECTED ({control_stack.peek()} does not have an action/step for {input_stack.peek()})"
                        printing_step_for_ll(step, control_stack, input_stack, next_action, space_num)
                        break
                except KeyError:
                    print("An error occurred while matching input to stack")
            # Result of step is writing to console
            printing_step_for_ll(step, control_stack, input_stack, next_action, space_num)
            # Necessary deletions are made and the next action stack is thrown.
            if isDeleted:
                input_stack.pop()
                control_stack.pop()
            else:
                control_stack.pop()
                control_stack.fill_in_the_stack((str(next_action).split("->"))[1].replace(" ", ""))
                if str(control_stack.peek()).upper() == 'ϵ':
                    control_stack.pop()

    else:
        state_stack_letters = "STATE STACK"  # this variable is used to write the console
        read_letters = "READ"  # this variable is used to write the console
        state_stack = Stack()
        input_list = list()
        pointer = 0  # This variable holds index location of processing reading data
        state_stack.push(str(lr_table[2][0]).split("_")[1])  # First action is thrown to state_Stack
        # In lr_processing, we stored the inputs in a list instead of a stack.
        for c in input_string:
            input_list.append(c)
        # Titles are wrote to console
        print(
            f"\t{no_letters:{space_num}}{state_stack_letters:{space_num}}{read_letters:{space_num}}{input_letters:{space_num}}{action_letters:{space_num}}")
        while True:
            read = input_list[pointer]  # read data from input_list
            hash_index = state_stack.peek() + " " + read
            # It is checked if there is a connection between the read data and the state.
            if parsing_table_of_lr_in_dict_format[hash_index] != "":
                cell = str(parsing_table_of_lr_in_dict_format[hash_index])
                cell_lower = cell.lower()
                # If the entered cell is the accept cell, it means that the language recognizes that string.
                if cell_lower.startswith("accept"):
                    current_action = "ACCEPTED"
                    printing_step_for_lr(step, state_stack, read, input_list, current_action, space_num)
                    break
                # if it is a state cell, the pointer is incremented and that state is stacked
                elif cell_lower.startswith("state"):
                    next_state = cell_lower.split("_")[1]
                    current_action = f"Shift to state {next_state}"
                    printing_step_for_lr(step, state_stack, read, input_list, current_action, space_num)
                    state_stack.push(next_state)
                    pointer += 1
                # If the cell to go to is a rule, that means we will do a replacement on the input.
                else:
                    pieces = cell.split("->")
                    current_action = f"Reverse {cell}"
                    printing_step_for_lr(step, state_stack, read, input_list, current_action, space_num)
                    # how many characters match the state is deleted from the state stack
                    for i in range(len(pieces[1])):
                        state_stack.pop()
                    str_format_of_input_list = ""
                    # input_list is converted to a string
                    for c in input_list:
                        str_format_of_input_list += c
                    str_format_of_input_list = str_format_of_input_list.replace(pieces[1], pieces[0])
                    input_list.clear()
                    for c in str_format_of_input_list:
                        input_list.append(c)
                    # the current pointer is set as the position of the changed character
                    pointer = input_list.index(pieces[0])
            else:
                # In case of rejection, the variables are set and the screen is informed.
                current_action = f"REJECTED (State {state_stack.peek()} does not have an action/step for {read})"
                printing_step_for_lr(step, state_stack, read, input_list, current_action, space_num)
                break
            step += 1


# If the input is processed according to LL,
# The necessary information is written to the screen in this method at every step.
def printing_step_for_ll(step_no, control_stack, input_stack, action, space_num):
    control_stack_str = get_string_in_stack(control_stack, control_stack.size(), 'd')
    input_stack_str = get_string_in_stack(input_stack, input_stack.size())
    print(
        f"\t{step_no:<{space_num}}{control_stack_str:<{space_num}}{input_stack_str:<{space_num}}{action:<{space_num}}")


# If the input is processed according to LR,
# The necessary information is written to the screen in this method at every step.
def printing_step_for_lr(step_no, state_stack, read, input_, action, space_num):
    # First of all, the data to be written to the screen is formatted to look pretty.
    input_str = ""
    state_stack_str = ""
    for i in get_string_in_stack(state_stack, state_stack.size(), 'd'):
        state_stack_str += i + " "
    for i in input_:
        input_str += i
    print(
        f"\t{step_no:<{space_num}}{state_stack_str:<{space_num}}{read:<{space_num}}{input_str:<{space_num}}{action:<{space_num}}")


# This method gives the inputs from the input file sequentially to the method that will process it
def process_inputs_one_by_one():
    for input_row in input_table:
        processing_given_string(input_row)


# Methods are called in the correct order
def main():
    if read_files():
        convert_to_parsing_table()
        process_inputs_one_by_one()
    else:
        print("Files not found in the system.")


# first method to be called
if __name__ == "__main__":
    main()
