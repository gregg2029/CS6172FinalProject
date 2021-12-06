from data.features import numSemicolan, lengthOfCode


programAndCodexScore = [
  ("fib ( int n ) { if ( n < 2 ) return n ; else return fib ( n - 1 ) + fib ( n - 2 ); }", 20.27048733),
  ("valueN(int n ) { return n <= 2 ? 1 : valueN(n - 1) + valueN(n - 2); }", 21.29059429),
  ("fibonacci ( int i ) { if ( i == 0 ) { return 0 ; } else if ( i == 1 ) { return 1 ; } else { return fibonacci ( i - 1 ) + fibonacci ( i - 2 ); } }", 23.88914638),
  ("getFibValue(int i) { if (i <= 1) { return i; } else { return getFibValue(i-2) + getFibValue(i-1); } }", 23.59122504),
  ("intArrayContains(int[] my_array, int an_element){ for (int element = 0; element < my_array.length; element++) { if (my_array[element] == an_element) return true; } return false; }", 17.34740979),
  ("contains ( int [] a , int item ) { for ( int i = 0 ; i < a . length ; i ++) { if ( a [ i ]== item ) return true ; } return false ; }", 14.99085568),
  ("findInArray(int[] array, int item) { boolean result = false; for (int i=0; i<array.length; i++) { if (item == array[i]) result = true; } if (result == true) return true; else return false; }", 73.77842802),
  ("contains( int [] arr, int i) { for ( int c = 0 ; c<arr.length; c++) if (arr[c] == i) return true ; return false ; }", 14.87003334),
  ("isInside(int[] i, int item) { for (int i2 = 0; i2 <= i.length - 1; i2++) { if (i[i2] == item) { return true; } } return false; }", 75.62459555),
  ("is(int[] a, int value) { for(int i=0;i< a.length;i++) { if(a[i]== value) { return true; } } return false; }", 57.1073693964659),
  ("fibonacci(int n) { if (n < 2) return n; return fibonacci(n - 1) + fibonacci(n - 2); }", 12.1080911314456),
  ("fibonacci(int n) { if(n < 2) { return n; } else { return fibonacci(n - 2) + fibonacci(n - 1); } }", 13.58276936),
  ("fib ( int n ){ return n == 0 ? 0 : n == 1 ? 1 : fib ( n - 1 ) + fib ( n - 2 ); }", 60.86983561),
  ("fibonacci(int nth) { if(nth == 0) { return 0; } else if(nth == 1) { return 1; } else { return fibonacci(nth-1)+fibonacci(nth-2); } }", 15.0022914),
  ("fibNth ( int n ) { if ( n == 0 ) { return 0 ; } else if ( n == 1 ) { return 1 ; } else { return fibNth ( n - 1 ) + fibNth ( n - 2 ); } }", 18.75259921),
  ("inArray ( int [ ] array, int element ) { for ( int i = 0 ; i < array. length ; i++ ) { if ( array [ i ] == element ) return true ; } return false ; }", 14.02464538),
  ("has ( int [] arr, int element ) { boolean exists = false ; for ( int j = 0 ; j < arr. length ; ++ j ) { if ( arr [ j ] == element ) { exists = true ; } } return exists ; }", 46.49664676),
  ("isIn(int[] array, int value) { for (int index = 0; index < array.length; index++) { if (array[index] == value) { return true; } } return false; }", 22.54680451),
]

def featureBasedCost(program):
  numChar = len(program)
  numberOfSemicolan = numSemicolan(program)
  functionalLength = lengthOfCode(program)

  feature = numChar
  weight = 1/(functionalLength*numberOfSemicolan)
  return feature * weight

for program, score in programAndCodexScore:
  print("program:")
  print(program)
  print("old score: ", score)
  print("new score: ", featureBasedCost(program))
