# Code to look for object in array

# readable code
def contains(item, arr):
    return item in arr

# semireadable
def find_object(target_obj, arr):
    for item in arr:
        if item == target_obj:
            return True

    return False

# semi-unreadable
def elem_in_list(element, check_list):
  len_list = len(check_list)
  for ind in range(len_list):
    if check_list[ind] == element:
      return True
  
  return False

# unreadable code
def obj_in_array(target_obj, arr):
    return next(filter(lambda arr_item: arr_item == target_obj, arr), None) != None


# Testing
test_arr = [4, 2, 25, 6, 8]
print("readable true: ", contains(2, test_arr))
print("readable false: ", contains(7, test_arr))

print("semi-readable true: ", find_object(2, test_arr))
print("semi-readable false: ", find_object(7, test_arr))

print("semi-unreadable true: ", elem_in_list(2, test_arr))
print("semi-unreadable false: ", elem_in_list(7, test_arr))

print("unreadable true: ", obj_in_array(2, test_arr))
print("unreadable false: ", obj_in_array(7, test_arr))
