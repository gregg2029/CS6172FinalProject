trainingSet = [
  # find object in array
  ["def contains(item, arr):\n    return item in arr", "Readable"],
  ["def find_object(target_obj, arr):\n    for item in arr:\n        if item == target_obj:\n            return True\n\n    return False", "Acceptable"],
  ["def elem_in_list(element, check_list):\n  len_list = len(check_list)\n  for ind in range(len_list):\n    if check_list[ind] == element:\n      return True\n  \n  return False", "Difficult"],
  ["def obj_in_array(target_obj, arr):\n    return next(filter(lambda arr_item: arr_item == target_obj, arr), None) != None", "Unreadable"],
  # add 1 to every number in array
  ["def add_one(arr):\n  new_arr = []\n  for elem in arr:\n    new_elem = elem + 1\n    new_arr.append(new_elem)\n  return new_arr", "Readable"],
  ["def add_one(arr):\n  new_arr = []\n  for elem in arr:\n    new_arr.append(elem + 1)\n  return new_arr", "Acceptable"],
  ["def add_one(arr):\n  return [elem + 1 for elem in arr]",
    "Acceptable"],
  ["def add_one(arr):\n  return map(lambda x: x + 1, arr)",
    "Difficult"],
]
