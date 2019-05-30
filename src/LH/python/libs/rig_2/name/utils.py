

def name_based_on_range(count,
                        name,
                        suffixSeperator="_",
                        suffix="",
                        side_name=False,
                        reverse_side=False,
                        do_return_side=False):
    return_names = []
    return_sides = []
    midpoint = count/2
    is_even=False
    if count % 2 == 0:
        # midpoint = None
        is_even = True
    if side_name:
        name = name.capitalize()
    specialized_name = name
    for idx in range(count):
        current = idx
        side = "L"
        if side_name:
            specialized_name = "inner" + name
        formatName = "{0}_{1}{2:02}{3}{4}"
        if do_return_side:
            formatName = "{0}{1:02}{2}{3}"
        if idx == midpoint and not is_even:
            side = "C"
            current = ""
            if side_name:
                specialized_name = "middle" + name
            formatName = "{0}_{1}{2}{3}{4}"
            if do_return_side:
                formatName = "{0}{1}{2}{3}"
        if idx > midpoint or idx == midpoint and is_even:
            side = "R"
            if side_name:
                specialized_name = "outer" + name
            current = count -1 - idx
        if side_name:
            side = side_name
        if do_return_side:
            return_names.append(formatName.format(specialized_name, current, suffixSeperator, suffix))
        else:
            return_names.append(formatName.format(side, specialized_name, current, suffixSeperator, suffix))
        return_sides.append(side)
    if reverse_side:
        return_names.reverse()
        return_sides.reverse()
    if do_return_side:
        return return_sides, return_names
    return return_names