from features import *
import sys
sys.path.append("")
import openai
from readability import *

openai.api_key = config('OPENAI_TOKEN')

programs = [
  'fib ( int n ) { if ( n < 2 ) return n ; else return fib ( n - 1 ) + fib ( n - 2 ); }',
  'valueN(int n ) { return n <= 2 ? 1 : valueN(n - 1) + valueN(n - 2); }',
  'fibonacci ( int i ) { if ( i == 0 ) { return 0 ; } else if ( i == 1 ) { return 1 ; } else { return fibonacci ( i - 1 ) + fibonacci ( i - 2 ); } }',
  'getFibValue(int i) { if (i <= 1) { return i; } else { return getFibValue(i-2) + getFibValue(i-1); } }',
  "intArrayContains(int[] my_array, int an_element){ for (int element = 0; element < my_array.length; element++) { if (my_array[element] == an_element) return true; } return false; }",
  "contains ( int [] a , int item ) { for ( int i = 0 ; i < a . length ; i ++) { if ( a [ i ]== item ) return true ; } return false ; }",
  "findInArray(int[] array, int item) { boolean result = false; for (int i=0; i<array.length; i++) { if (item == array[i]) result = true; } if (result == true) return true; else return false; }",
  "contains( int [] arr, int i) { for ( int c = 0 ; c<arr.length; c++) if (arr[c] == i) return true ; return false ; }",
  "isInside(int[] i, int item) { for (int i2 = 0; i2 <= i.length - 1; i2++) { if (i[i2] == item) { return true; } } return false; }",
  "is(int[] a, int value) { for(int i=0;i< a.length;i++) { if(a[i]== value) { return true; } } return false; }",
  "def add_one(arr):\n  new_arr = []\n  for elem in arr:\n    new_elem = elem + 1\n    new_arr.append(new_elem)\n  return new_arr",
  "def add_one(arr):\n  new_arr = []\n  for elem in arr:\n    new_arr.append(elem + 1)\n  return new_arr",
  "def add_one(arr):\n  return [elem + 1 for elem in arr]",
  "def add_one(arr):\n  return map(lambda x: x + 1, arr)",
  "fibonacci(int n) { if (n < 2) return n; return fibonacci(n - 1) + fibonacci(n - 2); }",
  "fibonacci(int n) { if(n < 2) { return n; } else { return fibonacci(n - 2) + fibonacci(n - 1); } }",
  "fib ( int n ){ return n == 0 ? 0 : n == 1 ? 1 : fib ( n - 1 ) + fib ( n - 2 ); }",
  "fibonacci(int nth) { if(nth == 0) { return 0; } else if(nth == 1) { return 1; } else { return fibonacci(nth-1)+fibonacci(nth-2); } }",
  "fibNth ( int n ) { if ( n == 0 ) { return 0 ; } else if ( n == 1 ) { return 1 ; } else { return fibNth ( n - 1 ) + fibNth ( n - 2 ); } }"
]

for program in programs:
  print("\tCode: ", program)
  classification = classifier(program)
  code_cost = cost(classification)
  print("\tScore: ", code_cost)
  print("\tNumber of brackets: ", numBrackets(program))
  print("\tNumber of characters:  ", len(program))
  print("\tTime complexity: ", timeComplexity(program))
