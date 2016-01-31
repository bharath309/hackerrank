import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;
import java.util.function.IntFunction;

public class Solution {

    public static class NamedPrimeChecker {
        public final String name;
        public final IntFunction<Boolean> primeChecker;
        public NamedPrimeChecker(String name, IntFunction<Boolean> primeChecker) {
            this.name = name;
            this.primeChecker = primeChecker;
        }

        public void benchmarkNumber(int n) {
            System.out.println("Running " + name);
            long start = System.nanoTime();
            boolean answer = primeChecker.apply(n);
            long end = System.nanoTime();
            long nanoSeconds = end - start;
            System.out.println("  " + n + " is " + (answer ? "" : "not ") + "prime.");
            System.out.printf("%,10d nano seconds%n%n", nanoSeconds);
        }

        public boolean isPrime(int n) {
            return primeChecker.apply(n);
        }
    }


    public static final NamedPrimeChecker linear =
        new NamedPrimeChecker("linear checker", (n -> {
                    if (n < 2) return false;
                    for (int divisor = 2; divisor < n; divisor++)
                        if (n % divisor == 0) return false;
                    return true;
                }));

    public static final NamedPrimeChecker sqrt =
        new NamedPrimeChecker("sqrt checker", (n -> {
                    if (n < 2) return false;
                    for (int divisor = 2; (divisor * divisor) <= n; divisor++)
                        if (n % divisor == 0) return false;
                    return true;
                }));

    public static final NamedPrimeChecker sqrtWheel =
        new NamedPrimeChecker("sqrtWheel checker", (n -> {
                    if (n < 2) return false;
                    if (n == 2) return true;
                    if (n % 2 == 0) return false;
                    for (int divisor = 3; (divisor * divisor) <= n; divisor += 2)
                        if (n % divisor == 0) return false;
                    return true;
                }));


    public static final NamedPrimeChecker sqrtWheel6 =
        new NamedPrimeChecker("sqrtWheel checker", (n -> {
                    if (n < 2) return false;
                    if (n == 2) return true;
                    if (n % 2 == 0 || n % 3 == 0) return false;

                    int sqrt = (int) Math.sqrt(n) + 1;
                    for (int divisor = 6; divisor <= sqrt; divisor += 6) {
                        if (n % (divisor - 1) == 0 ||
                            n % (divisor + 1) == 0) {
                            return false;
                        }
                    }
                    return true;
                }));
    public static void testRun() {


        List<NamedPrimeChecker> namedPrimeCheckers = new ArrayList<>();
        // namedPrimeCheckers.add(linear);
        namedPrimeCheckers.add(sqrt);
        namedPrimeCheckers.add(sqrtWheel);
        namedPrimeCheckers.add(sqrtWheel6);


        System.out.println("Warming up the JIT...");
        linear.isPrime(40_000);
        sqrt.isPrime(20_000 * 20_000);
        sqrtWheel.isPrime(60_000 * 60_000);
        System.out.println("Warm up complete.\n");

        int prime = 2047416197;
        namedPrimeCheckers.stream().forEach(checker -> checker.benchmarkNumber(prime));
    }

    public static void main(String[] args) {

        // testRun();
        Scanner input = new Scanner(System.in);
        int numTests = input.nextInt();
        for (int i = 0; i < numTests; i++) {
            int n = input.nextInt();
            if  (sqrtWheel6.isPrime(n)) {
                System.out.println("Prime");
            } else {
                System.out.println("Not prime");
            }
        }
    }

}
