import java.util.Scanner;

public class StringReverserManual {

    public static void main(String[] args) {
        // Create a Scanner object to take user input
        Scanner scanner = new Scanner(System.in);

        // Prompt the user to enter a string
        System.out.print("Enter a string to reverse: ");
        String originalString = scanner.nextLine(); // Read user input

        String reversedString = ""; // Initialize an empty string for the result

        // Iterate from the last character to the first
        for (int i = originalString.length() - 1; i >= 0; i--) {
            reversedString = reversedString + originalString.charAt(i);
        }

        // Output the results
        System.out.println("Original string: " + originalString);
        System.out.println("Reversed string: " + reversedString);
        
        // Close the scanner
        scanner.close();
    }
}
