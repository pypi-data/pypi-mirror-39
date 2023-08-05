def list_conjunction(sequence, word):
    if len(sequence) == 0:
        text = ""
    elif len(sequence) == 1:
        text = str(sequence)
    elif len(sequence) == 2:
        text = "{!s} {} {!s}".format(sequence[0], word, sequence[1])
    else:
        all_but_last = ", ".join(map(str, sequence[:-1]))
        last = sequence[-1]
        text = "{}, {} {!s}".format(all_but_last, word, last)
    return text
