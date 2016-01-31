import java.util.Scanner;

public class Solution {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        int numTests = input.nextInt();
        for (int i = 0; i < numTests; i++) {
            long limit = input.nextLong();
            long answer = sumEvenFibonacciNumbers(limit);
            System.out.println(answer);
        }
    }

    public static long sumEvenFibonacciNumbers(long limit) {
        long sum = 0;
        long a = 1;
        long b = 1;

        while (a < limit) {
            if (a % 2 == 0) {
                sum += a;
            }

            long tmp = b;
            b = a + b;
            a = tmp;
        }
        return sum;
    }

}
