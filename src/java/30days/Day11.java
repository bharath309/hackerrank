import java.util.Scanner;

class Solution {

    public static void main(String[] args) {

        Scanner input = new Scanner(System.in);

        int[][] array = new int[6][6];
        for (int row = 0; row < array.length; row++) {
            for(int col = 0; col < array[row].length; col++) {
                array[row][col] = input.nextInt();
            }
        }
        int answer = findLargestHourglass(array);
        System.out.println(answer);
    }

    public static int findLargestHourglass(int[][] array) {
        int largestHourglass = Integer.MIN_VALUE;
        for (int row = 0; row < array.length - 2;  row++) {
            for (int col = 0; col < array[row].length - 2; col++) {
               int hourglassValue = array[row][col] + array[row][col + 1] + array[row][col + 2]
                   + array[row + 1][col + 1]
                   + array[row + 2][col] + array[row + 2][col + 1] + array[row + 2][col + 2];
               largestHourglass = Math.max(largestHourglass, hourglassValue);
            }
        }
        return largestHourglass;

    }
}
