

def sentences_score(input_string, target_string) -> int:
    """
    This function calculates the score of the input string based on the target string.

    Args:
    input_string: The input string to be scored.
    target_string: The target string to be scored against.

    """

    input_string = ' '.join(input_string.lower().split())
    target_string = target_string.lower()
    score = 0
    for i in range(len(target_string)):
        if target_string[i] == input_string[i]:
            score += 2
        else:
            if input_string[i] == input_string[i-1]:
                target_string = target_string[:i] + " " + target_string[i:]
                score -= sub_score_for_missing_or_duplicate_char(i)
            elif input_string[i] == target_string[i+1]:
                input_string = input_string[:i] + " " + input_string[i:]
                score -= sub_score_for_missing_or_duplicate_char(i)
            else:
                if i > 4:
                    score -= 1
                else:
                    score -= i+1

    return score

def sub_score_for_missing_or_duplicate_char(index: int) -> int :
    """
    This function calculates the score that need to subtract for missing or duplicate characters.
    :param index:
    :return:  The score that need to subtract for missing or duplicate characters.
    """
    if index > 4:
        return 2
    else:
        return 10 - index*2
