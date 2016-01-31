

public class Sqrt {
    public static void main(String[] args) {

        int numLess = 0;
        int numEqual = 0;
        int numGreater = 0;
        for (int i = 4; i < Integer.MAX_VALUE; i++) {

            int sqrt = (int) Math.sqrt((double) i);
            int square = sqrt * sqrt;
            if (square < i) {
                numLess++;
            } else if (square > i)  {
                numGreater++;
            } else {
                numEqual++;
            }

            if (i % 100_000_000 == 0) {
                System.out.println("i:          " + i);
                System.out.println("numLess:    " + numLess);
                System.out.println("numEqual:   " + numEqual);
                System.out.println("numGreater: " + numGreater);
                System.out.println();
            }

        }

        System.out.println("numLess:    " + numLess);
        System.out.println("numEqual:   " + numEqual);
        System.out.println("numGreater: " + numGreater);
    }
}
