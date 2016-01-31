import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Scanner;

public class Solution {
    public static void main(String... args) {
        Scanner input = new Scanner(System.in);
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("d M y");
        LocalDate returnDate = LocalDate.parse(input.nextLine(), dtf);
        LocalDate dueDate = LocalDate.parse(input.nextLine(), dtf);
        int fine = calculateFine(returnDate, dueDate);
        System.out.println(fine);
    }

    public static int calculateFine(LocalDate returnDate, LocalDate dueDate) {
        final int MAX_FINE = 10_000;
        final int returnYear = returnDate.getYear();
        final int dueYear = dueDate.getYear();
        if (returnYear > dueYear) {
            return MAX_FINE;
        } else if (returnYear < dueYear) {
            return 0;
        }

        // Years are equal

        final int MONTH_FINE_MULTIPLE = 500;
        final int returnMonth = returnDate.getMonthValue();
        final int dueMonth = dueDate.getMonthValue();
        if (returnMonth > dueMonth) {
            return (returnMonth - dueMonth) * MONTH_FINE_MULTIPLE;
        } else if (returnMonth < dueMonth) {
            return 0;
        }

        // Months are equal

        final int DAY_FINE_MULTIPLE = 15;
        final int returnDay = returnDate.getDayOfMonth();
        final int dueDay = dueDate.getDayOfMonth();
        if (returnDay > dueDay) {
            return (returnDay - dueDay) * DAY_FINE_MULTIPLE;
        }

        return 0;
    }
}
