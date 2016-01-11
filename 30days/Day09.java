import java.util.Scanner;

class Solution {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        int a = input.nextInt();
        int b = input.nextInt();
        int answer = gcd(a, b);
        System.out.println(answer);
    }

    public static int gcd(int a, int b) {
        if (a == b) {
            return a;
        } else {
            if (a < b) {
                return gcd(a, b - a);
            } else {
                return gcd(a - b, b);
            }
        }

    }
}
