from fileinput import FileInput

def max_sum_no_zeroes(array):
    first_nonzero_index = -1
    for i, num in enumerate(array):
        if num != 0:
            first_nonzero_index = i
            break

    if first_nonzero_index == -1:
        return 0

    best = array[first_nonzero_index]
    current = array[first_nonzero_index]
    for i in range(first_nonzero_index + 1, len(array)):
        if array[i] == 0:
            current = None
            continue

        if current is None:
            current = array[i]
        else:
            current = max(array[i], current + array[i])

        best = max(best, current)

    return max(best, 0)

def main():
    with FileInput("-") as input_file:
        array_size = int(input_file.readline())
        array = [int(x) for x in input_file.readline().split()]
        print(max_sum_no_zeroes(array))

main()


