class A{
public static boolean find(int[] a, int n, int item) { for (int i = 0; i < a.length; i++) { if (a[i] == item) { return true; } } return false; }

public static void main(String[] args){
  int[] a = {1, 2, 3, 4};
  System.out.println(find(a, 4, 4));
}
}