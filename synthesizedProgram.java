//Program: 
indexOf(int[] list, int value) { if (list.length == 0) { return true; } for (int i = 0; i < list.length; i++) { if (list[i] == value) { return true; } } return false; }
//Cost: 30.131359851683122
//===================================================
//Program: 
contains ( int [] array, int searchKey ){ for ( int i = 0 ; i < array. length ; i++){ if ( array [ i ] == searchKey ){ return true ; } } return false ; }
//Cost: 41.444543096397574
//===================================================
//Program: 
contains(int[] s, int v) { for (int i : s) { if (i == v) { return true; } } return false; }
//Cost: 40.77999428967506
//===================================================
//Program: 
selectItem ( int [ ] nums , int item ) { for ( int i = 0 ; i < nums. length ; i ++ ) { if ( nums [ i ] == item ) { return true ; } } return false ; }
//Cost: 39.16876489446908
//===================================================


//Synthesized Program:
indexOf(int[] list, int value) { if (list.length == 0) { return true; } for (int i = 0; i < list.length; i++) { if (list[i] == value) { return true; } } return false; }
//Program cost: 30.131359851683122