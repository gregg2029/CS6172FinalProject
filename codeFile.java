import java.io.*;

class A{

public static FileWriter createFile() {
  try {
    FileWriter myWriter = new FileWriter("codeTestOutput.txt");
    return myWriter;
  } 
  catch (IOException e) {
    System.out.println("An error occurred.");
    e.printStackTrace();
  }
  return null;
}

public static void writeFile(FileWriter writer, String text){
  try{
    writer.write(text + "\n");
    return;
  } catch (IOException e) {
      System.out.println("An error occurred.");
      e.printStackTrace();
  }
  return;
}

public static void closeFile(FileWriter writer){
  try{
    writer.close();
    return;
  } catch (IOException e) {
      System.out.println("An error occurred.");
      e.printStackTrace();
  }
  return;
}
    
public static boolean selectItem ( int [ ] nums , int item ) { for ( int i = 0 ; i < nums. length ; i ++ ) { if ( nums [ i ] == item ) { return true ; } } return false ; }

public static void main(String[] args){
FileWriter writer = createFile();
writeFile(writer, String.valueOf(selectItem(new int[] {1, 2, 3, 4}, 3)));
writeFile(writer, String.valueOf(selectItem(new int[] {1, 2, 3, 4}, 7)));
writeFile(writer, String.valueOf(selectItem(new int[] {1, 2, 3, 4}, 4)));
writeFile(writer, String.valueOf(selectItem(new int[] {1, 2, 3, 4, 4, 4}, 4)));
writeFile(writer, String.valueOf(selectItem(new int[] {1, 2, 3, 4, 4, 4}, 6)));
closeFile(writer);
}
}