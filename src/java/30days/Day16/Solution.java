import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;
import java.util.TreeSet;

public class Solution {

    public static void main(String[] args) {

        Scanner input = new Scanner(System.in);
        int numElements = input.nextInt();
        List<Integer> numbers = new ArrayList<>(numElements);
        for (int i = 0; i < numElements; i++) {
            numbers.add(input.nextInt());
        }
        getMinDifferences(numbers);
    }

    public static void getMinDifferences(List<Integer> numbers) {
        Collections.sort(numbers);
        int minDifference = Integer.MAX_VALUE;

        for (int i = 1; i < numbers.size(); i++) {
            int left = numbers.get(i - 1);
            int right = numbers.get(i);
            int difference = Math.abs(left - right);
            minDifference = Math.min(minDifference, difference);
        }

        for (int i = 1; i < numbers.size(); i++) {
            int left = numbers.get(i - 1);
            int right = numbers.get(i);
            int difference = Math.abs(left - right);
            if (difference == minDifference) {
                System.out.print(left + " " + right + " ");
            }
        }
    }

    public static class Pair {
        public final int left;
        public final int right;
        public Pair(int left, int right) {
            assert left != right
                : "Pair has same value for left and right of: " + left;
            this.left = Math.min(left, right);
            this.right = Math.max(left, right;)
        }
        @Override
        public boolean equals(Object o) {
            if (!(o instanceOf Pair)) {
                return false;
            }
            Pair p = (Pair) o;
            return this.left == p.left && this.right == p.right;
        }

        @Override
        public int hashCode() {
            // We want an unordered pair so:
            // Pair(1, 5).hashCode() == Pair(5, 1).hashCode()
            return 31 + left * 31 + right;
        }
    }

    public static List<Pair> getMinDifferencesOneLoop() {
        TreeSet<Integer> allNumbers = new TreeSet<>();

        Scanner input = new Scanner(System.in);
        int numElements = input.nextInt();
        for (int i = 0; i < numElements; i++) {
            int nextNumber = input.nextInt();
            allNumbers.add(nextNumber);
            
        }
    }
}
