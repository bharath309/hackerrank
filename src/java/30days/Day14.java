import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;


class Difference {
  	private int[] elements;
  	public int maximumDifference;

    public Difference(int[] elements) {
        this.elements = elements;
    }

    public void computeDifference() {
        int smallest = 1_000_000_000;
        int largest = 0;

        for (int i = 0; i < elements.length; i++) {
            smallest = Math.min(smallest, elements[i]);
            largest = Math.max(largest, elements[i]);
        }
        maximumDifference = largest - smallest;
    }

} // End of Difference Class

public class Solution {
  	public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int N = sc.nextInt();
        int[] a = new int[N];

        for (int i = 0; i < N; i++) {
            a[i] = sc.nextInt();
        }

      	Difference D = new Difference(a);

        D.computeDifference();

        System.out.print(D.maximumDifference);
    }
}
