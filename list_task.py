# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    if not lst:
        return lst
    result = [lst[0]]
    for x in lst:
        if x != result[-1]:
            result.append(x)
    return result

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    result = list()
    l1 = len(lst1)
    l2 =len(lst2)
    i = 0
    j = 0
    while i < l1 and j < l2:
        if lst1[i] > lst2[j]:
            result.append(lst2[j])
            j += 1
        else:
            result.append(lst1[i])
            i += 1
    result.extend(lst1[i:])
    result.extend(lst2[j:])
    return result


