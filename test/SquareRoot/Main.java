
import java.util.Scanner;

class SquareRoot {
    public static Double squareRoot(Double num) {
        if (num < 0 ){
            System.out.println("Cannot square root a negative number");
        }
        return Math.sqrt(num);
    }
}

public class Main {
    public static void main(String[] args) {
       Scanner scanner = new Scanner(System.in);
       System.out.println("Please Enter a number: ");
       Double num = scanner.nextDouble();
       Double answer = SquareRoot.squareRoot(num);
       System.out.println("The square root of " + num + " is " + answer);
       scanner.close(); 
    }
}