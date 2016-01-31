import java.util.ArrayList;
import java.util.List;
import java.util.BitSet;
import java.util.Scanner;

public class Solution {


    public static int[] sievePrimesUpTo(int n) {
        BitSet isPrime = new BitSet(n + 1);
        isPrime.set(2, isPrime.size());

        int limit = (int) Math.sqrt(n) + 1;
        for (int i = 2; i <= limit; i++) {
            if (isPrime.get(i)) {
                for (int j = i * i; j <= n; j += i) {
                    isPrime.clear(j);
                }
            }
        }

        int numPrimes = 0;
        for (int i = 2; i < isPrime.size(); i++) {
            if (isPrime.get(i)){
                numPrimes++;
            }
        }

        int[] primes = new int[numPrimes];
        int primeIndex = 0;
        for (int i = 2; i < isPrime.size(); i++) {
            if (isPrime.get(i)){
                primes[primeIndex] = i;
                primeIndex++;
            }
        }

        return primes;
    }

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        // Get input
        int numTests = input.nextInt();
        long largestN = -1;
        long[][] numAndLargestFactors = new long[numTests][2];
        for (int i = 0; i < numTests; i++) {
            long n = input.nextLong();
            numAndLargestFactors[i][0] = n;
            // Dummy value for largest factor
            numAndLargestFactors[i][1] = -1;
            largestN = Math.max(n, largestN);
        }

        // pick largest value
        // sieve up to sqrt(n)
        int largestNSqrt = (int) Math.sqrt(largestN) + 1;
        int[] primes = sievePrimesUpTo(largestNSqrt);

        // loop over sieve
        // check if each number is divisible, store largest in 2 element array
        for (int prime : primes) {
            for (int i = 0; i < numAndLargestFactors.length; i++) {
                long n = numAndLargestFactors[i][0];
                if (n % prime == 0) {
                    numAndLargestFactors[i][1] = prime;
                }
            }
        }

        for (long[] numAndFactor : numAndLargestFactors) {
            long n =  numAndFactor[0];
            long largestFactor = numAndFactor[1];
            largestFactor = largestFactor == -1 ? n : largestFactor;
            System.out.println(largestFactor);
        }
    }
}
