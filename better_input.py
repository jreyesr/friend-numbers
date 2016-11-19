from typing import List


def simple_input(prompt: str) -> str:
    """
    Ask the user for input. Extremely thin wrapper around the common input() function
    :param prompt: Is printed to standard output before reading input
    :return: The user's input
    """
    return input(prompt)


def condition_input(prompt: str, return_type=str, condition=None, error_message=None):
    """
    Ask the user for input, checking if it meets a condition
    :param prompt: The question the user will be asked
    :param return_type: The type the user's input will be casted to
    :param condition: An optional check, done AFTER the type cast
    :param error_message: An optional error message to be shown when an input does not meet the condition
    :return: The user's input, casted to return_type and complying with condition
    """
    while True:
        try:
            answer = return_type(simple_input(prompt))
        except ValueError:
            print(error_message)
            continue
        if condition is not None:
            if condition(answer):
                return answer
        else:
            return answer
        if error_message is not None:
            print(error_message)


def choice_input(prompt: str, choices: List[str], enumeration='number', error_message=None):
    """
    Ask the user for input from a set of choices
    :param prompt: The question the user will be asked
    :param choices: A list of choices the user has to select from
    :param enumeration: Can be 'number' or 'char'. 'char' should only be used when len(choices)<27
    :param error_message: An optional error message to be shown when an input is not a valid choice
    :return: The index of the selected choice
    """
    from string import ascii_uppercase
    if enumeration == 'number':
        chars = [str(x + 1) for x in range(len(choices))]
    elif enumeration == 'char':
        assert len(choices) < 27, "Choices can't be represented by single chars"
        chars = ascii_uppercase[:len(choices)]
    else:
        raise ValueError("enumeration is not \'number\' or \'char\'")

    for c, text in zip(chars, choices):
        print("{}) {}".format(c, text))

    answer = condition_input(prompt, condition=lambda x: x.upper() in chars, error_message=error_message)
    return chars.index(answer.upper())
