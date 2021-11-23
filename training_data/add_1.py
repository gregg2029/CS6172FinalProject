# Goal: Add 1 to each element in a list

# Beginner
# Good characteristic: element instantiation
# Classification: readable
def add_one(arr):
  new_arr = []
  for elem in arr:
    new_elem = elem + 1
    new_arr.append(new_elem)
  return new_arr

# Doesn't have element instantiation
# Classification: semi-readable
def add_one(arr):
  new_arr = []
  for elem in arr:
    new_arr.append(elem + 1)
  return new_arr

# Classification: semi-unreadable
def add_one(arr):
  return [elem + 1 for elem in arr]

# Classification: unreadable
def mystery_func(boop):
  return map(lambda x: x + 1, boop)
