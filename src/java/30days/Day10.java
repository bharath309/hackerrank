import java.util.Scanner;

class Solution {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        int numTests = input.nextInt();
        for (int i = 0; i < numTests; i++) {
            int decimal = input.nextInt();
            System.out.println(Integer.toBinaryString(decimal));
        }
    }
}
