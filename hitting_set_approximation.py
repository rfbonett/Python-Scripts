import sys
from collections import Counter

def get_span(inputs) :
    """ Finds the integer that spans the greatest number of lists, and returns
        that integer and all of the lists it belongs to """
    indices = [0]*len(inputs)
    current_span = []
    current_int = None

    while (indices.count(None) < len(indices)) :
        # Build a list of the values of inputs at the current indices
        values = []
        for i, j in enumerate(indices) :
            if j is not None :
                values.append(inputs[i][j])
        data = Counter(values)

        # Compute the mode; if the mode is greater than the previously found
        # span, replace the old span with the indices matching the mode
        mode = data.most_common(1)[0]
        if current_span is None or len(current_span) < mode[1] :
            current_int = mode[0]
            current_span = []
            for i, j in enumerate(indices) :
                if inputs[i][j] == mode[0] :
                    current_span.append(i)

        # Compute the minimum element, and increment each index having this value
        min_int = min(data.elements())
        for i, j in enumerate(indices) :
            if j is None :
                continue
            if inputs[i][j] == min_int :
                indices[i] += 1
            if indices[i] >= len(inputs[i]) :
                indices[i] = None

    return current_int, current_span


def find_hitting_set(inputs) :
    """ Returns an approximation for the smallest hitting set of inputs """
    return_set = []
    while len(inputs) > 0 :
        current_int = None
        current_span = None
        try :
            current_int, current_span = get_span(inputs)
        except Exception as e :
            print("Error getting span, " + e)
            sys.exit(1)

        # If the current_span has one index, no element spans more than one list,
        # so we add the first index of each list to the return set and return
        if len(current_span) == 1 :
            return_set += [ls[0] for ls in inputs]
            break
        else :
            # Add the spanning integer to the return set and remove the lists from
            # the inputs list whose indices are now accounted for
            return_set.append(current_int)
            for index in current_span[::-1] :
                inputs.pop(index)
    return return_set

if __name__ == '__main__' :
    # Read the input text file into a list of lists of integers
    fp = open(sys.argv[1])
    inputs = []
    for line in fp.readlines() :
        ls = [int(i) for i in line.split()]
        inputs.append(ls)
    fp.close()
    print("Smallest Hitting Set: " + str(sorted(find_hitting_set(inputs))))
