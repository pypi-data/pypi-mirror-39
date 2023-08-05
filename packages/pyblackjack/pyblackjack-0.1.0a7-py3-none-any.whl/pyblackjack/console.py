def error(message):
    print("Error: {} Try again.".format(message))


def get_str(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        else:
            error("Input required.")


def get_action(prompt, options, lowchips):
    while True:
        s = get_str(prompt)[0].lower()
        if s in options:
            return s
        elif s in lowchips:
            error("Insufficient chips for that action.")
        else:
            error("Invalid action")


def get_yes_no(prompt):
    while True:
        s = get_str("{} [y/n]:".format(prompt)).lower()
        if s in {"y", "yes"}:
            return True
        elif s in {"n", "no"}:
            return False
        else:
            error("Invalid input.")


def get_int(prompt, min=None, max=None, alt=None):
    while True:
        s = get_str(prompt).lower()
        if s.lower() == alt.lower():
            return s.lower()
        try:
            z = int(s)
        except ValueError:
            error("Invalid integer.")
            continue
        if min is not None and z < min:
            error("Integer must be at least {}.".format(min))
            continue
        if max is not None and max < z:
            error("Integer must be at most {}.".format(max))
            continue
        return z
