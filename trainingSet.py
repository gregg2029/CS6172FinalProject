trainingSet = [
  # find object in array
  ["def contains(item, arr):\n    return item in arr", "Readable"],
  ["def find_object(target_obj, arr):\n    for item in arr:\n        if item == target_obj:\n            return True\n\n    return False", "Acceptable"],
  ["def elem_in_list(element, check_list):\n  len_list = len(check_list)\n  for ind in range(len_list):\n    if check_list[ind] == element:\n      return True\n  \n  return False", "Difficult"],
  ["def obj_in_array(target_obj, arr):\n    return next(filter(lambda arr_item: arr_item == target_obj, arr), None) != None", "Unreadable"],
  ["inArray ( int [ ] array, int element ) { for ( int i = 0 ; i < array. length ; i++ ) { if ( array [ i ] == element ) return true ; } return false ; }", "Readable"],
  ["has ( int [] arr, int element ) { boolean exists = false ; for ( int j = 0 ; j < arr. length ; ++ j ) { if ( arr [ j ] == element ) { exists = true ; } } return exists ; }", "Readable"],
  ["isIn(int[] array, int value) { for (int index = 0; index < array.length; index++) { if (array[index] == value) { return true; } } return false; }", "Readable"],
  # java
  ["intArrayContains(int[] my_array, int an_element){ for (int element = 0; element < my_array.length; element++) { if (my_array[element] == an_element) return true; } return false; }", "Acceptable"],
  ["contains ( int [] a , int item ) { for ( int i = 0 ; i < a . length ; i ++) { if ( a [ i ]== item ) return true ; } return false ; }", "Acceptable"],
  ["findInArray(int[] array, int item) { boolean result = false; for (int i=0; i<array.length; i++) { if (item == array[i]) result = true; } if (result == true) return true; else return false; }", "Unreadable"],
  ["contains( int [] arr, int i) { for ( int c = 0 ; c<arr.length; c++) if (arr[c] == i) return true ; return false ; }", "Difficult"],
  ["isInside(int[] i, int item) { for (int i2 = 0; i2 <= i.length - 1; i2++) { if (i[i2] == item) { return true; } } return false; }", "Unreadable"],
  ["is(int[] a, int value) { for(int i=0;i< a.length;i++) { if(a[i]== value) { return true; } } return false; }", "Unreadable"],
  # add 1 to every number in array
  ["def add_one(arr):\n  new_arr = []\n  for elem in arr:\n    new_elem = elem + 1\n    new_arr.append(new_elem)\n  return new_arr", "Readable"],
  ["def add_one(arr):\n  new_arr = []\n  for elem in arr:\n    new_arr.append(elem + 1)\n  return new_arr", "Acceptable"],
  ["def add_one(arr):\n  return [elem + 1 for elem in arr]",
    "Acceptable"],
  ["def add_one(arr):\n  return map(lambda x: x + 1, arr)",
    "Difficult"],
  # fibonacci
  ["fibonacci(int n) { if (n < 2) return n; return fibonacci(n - 1) + fibonacci(n - 2); }", "Readable"],
  ["fibonacci(int n) { if(n < 2) { return n; } else { return fibonacci(n - 2) + fibonacci(n - 1); } }", "Readable"],
  ["fib ( int n ){ return n == 0 ? 0 : n == 1 ? 1 : fib ( n - 1 ) + fib ( n - 2 ); }", "Unreadable"],
  ["fibonacci(int nth) { if(nth == 0) { return 0; } else if(nth == 1) { return 1; } else { return fibonacci(nth-1)+fibonacci(nth-2); } }", "Acceptable"],
  ["fibNth ( int n ) { if ( n == 0 ) { return 0 ; } else if ( n == 1 ) { return 1 ; } else { return fibNth ( n - 1 ) + fibNth ( n - 2 ); } }", "Acceptable"]
]

onlyFunctions = list(map(lambda trainingData: trainingData[0], trainingSet))
