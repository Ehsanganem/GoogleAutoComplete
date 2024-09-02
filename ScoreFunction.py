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

    # Compare characters up to the length of the shorter string
    min_length = min(len(input_string), len(target_string))

    for i in range(min_length):
        if target_string[i] == input_string[i]:
            score += 2
        else:
            if i > 0 and input_string[i] == input_string[i-1]:
                score -= sub_score_for_missing_or_duplicate_char(i)
            elif i < len(target_string) - 1 and input_string[i] == target_string[i+1]:
                score -= sub_score_for_missing_or_duplicate_char(i)
            else:
                if i > 4:
                    score -= 1
                else:
                    score -= i + 1

    # Penalize for any extra characters in the longer string
    if len(input_string) > min_length:
        score -= (len(input_string) - min_length)
    elif len(target_string) > min_length:
        score -= (len(target_string) - min_length)

    return score

def sub_score_for_missing_or_duplicate_char(index: int) -> int:
    """
    This function calculates the score that needs to subtract for missing or duplicate characters.
    :param index:
    :return: The score that needs to subtract for missing or duplicate characters.
    """
    if index > 4:
        return 2
    else:
        return 10 - index * 2
