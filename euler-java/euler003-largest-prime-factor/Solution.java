import java.util.ArrayList;
import java.util.List;
import java.util.BitSet;
import java.util.Scanner;

public class Solution {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        int numTests = input.nextInt();
        for (int i = 0; i < numTests; i++) {
            long n = input.nextLong();
            System.out.println(generateSieve((int) n));
        }
    }

    public static List<Integer> getPrimeFactors(long n) {
        return null;
    }

    public static List<Integer> generateSieve(int limit) {
        if (limit < 2) {
            return new ArrayList<>();
        }

        BitSet isPrime = new BitSet(limit + 1);
        isPrime.set(2, isPrime.size());

        int stopping = (int) Math.sqrt(limit) + 1;
        for (int i = 2; i < stopping; i++) {
            if (!isPrime.get(i)) {
                continue;
            }

            for (int j = i * i; j <= limit; j += i) {
                isPrime.clear(j);
            }
        }

        List<Integer> primes = new ArrayList<>();

        for (int i = 2; i < isPrime.size(); i++) {
            if (isPrime.get(i)) {
                primes.add(i);
            }
        }
        return primes;
    }
}
