import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

class Student{
    protected String firstName;
    protected String lastName;
    int phone;
    Student(String fname,String lname,int p){
        firstName=fname;
        lastName=lname;
        phone=p;
    }
    public void display(){// display the details of the student
        System.out.println("First Name: "+firstName+"\nLast Name: "+lastName+"\nPhone: "+phone);
    }

}

// Separate File Grade.java

class Grade extends Student {

    private final int score;

    public Grade(String firstName, String lastName, int phoneNumber, int score) {
        super(firstName, lastName, phoneNumber);
        this.score = score;
    }

    public char calculate() {
        if (score < 40) {
            return 'D';
        } else if (score < 60) {
            return 'B';
        } else if (score < 75) {
            return 'A';
        } else if (score < 90) {
            return 'E';
        } else {
            return 'O';
        }
    }
}
