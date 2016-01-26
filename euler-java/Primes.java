import java.util.function.LongFunction;
import java.util.List;

public final class Primes {

    private Primes() {} // non-instaniable

    public static boolean isPrime (long n) {
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
    }

    public static List<Long> primeFactors(long n) {
    }

    // http://mathworld.wolfram.com/PrimeCountingFunction.html
    public static int numPrimesUpperBound(int max) {
        if(n >= 60184) {
            return (int)(n / (Math.log(n) - 1.1));
        } else if (n > 1) {
            return (int) (1.25506 * max / Math.log(n));
        } else {
            return 0;
        }
    }


    public static long[] sievePrimesUpTo(long n) {
        BitSet isPrime = new BitSet(n + 1);
        isPrime.set(2, isPrime.size());

        long limit = (long) Math.sqrt(n) + 1;
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

        long[] primes = new long[numPrimes];
        int primeIndex = 0;
        for (int i = 2; i < isPrime.size(); i++) {
            if (isPrime.get(i)){
                primes[primeIndex] = i;
                primeIndex++;
            }
        }

        return primes;
    }

}
