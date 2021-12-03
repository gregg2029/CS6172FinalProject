//Program: 
findIn(int[] yourArray, int itemToFind) { 
  for (int i=0; i < yourArray.length; i++) { 
    if( yourArray[i] == itemToFind ){ 
      int index = i; 
      return true; 
    } 
  } 
  return false; 
}
//Cost: 31.329101912519988
//===================================================
//Program: 
isInArray(int[] nums, int item) { 
  for(int count=0;count<nums.length;count++) { 
    if(nums[count] == item) { 
      return true; 
    } 
  } 
  return false; 
}
//Cost: 37.19122055002444
//===================================================
//Program: 
find(int[] a, int b) { 
  if (a == null) return false; 
  for (int j = 0; j < a.length; j++) if (a[j] == b) { 
    return true; 
  } 
  return false; 
}
//Cost: 26.99513321167069
//===================================================
//Program: 
myfunc ( int [] array, int itemToFind) { 
  for ( int i = 0 ; i < array.length; i++) { 
    if (array[i] == itemToFind) { 
      return true ; 
    } 
  } 
  return false ; 
}
//Cost: 36.31498847785252
//===================================================


//Synthesized Program:
find(int[] a, int b) { 
  if (a == null) return false; 
  for (int j = 0; j < a.length; j++) if (a[j] == b) { 
    return true; 
  } 
  return false; 
}
//Program cost: 26.99513321167069