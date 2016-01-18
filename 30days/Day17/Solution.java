import java.io.*;
import java.util.*;

class Palindrome {

    private static final int INITIAL_SIZE = 1;

    private char[] stack = new char[INITIAL_SIZE];
    private int stackIndex = INITIAL_SIZE;


    private char[] queue = new char[INITIAL_SIZE];
    private int queueStartIndex = 0;
    private int queueEndIndex = 0;

    public void pushCharacter(char ch) {
        if (stackIndex == 0) {
            char[] newStack = new char[stack.length * 2];
            int offset = newStack.length - stack.length;
            System.arraycopy(stack, 0, newStack, offset, stack.length);
            stackIndex = offset;
            stack = newStack;
        }
        stackIndex--;
        stack[stackIndex] = ch;
    }

    public void enqueueCharacter(char ch) {
        if ((queueEndIndex + 1) % (queue.length + 1) == queueStartIndex) {
            char[] newQueue = new char[queue.length * 2];
            System.arraycopy(queue, queueStartIndex, newQueue, 0, queue.length - queueStartIndex);
            System.arraycopy(queue, 0, newQueue, queueStartIndex, queueEndIndex);
            queueStartIndex = 0;
            queueEndIndex = queue.length;
            queue = newQueue;
        }
        queue[queueEndIndex] = ch;
        queueEndIndex = (queueEndIndex + 1) % (queue.length + 1);
    }

    public char popCharacter() {
        if (stackIndex == stack.length) {
            throw new IndexOutOfBoundsException();
        }
        char ch = stack[stackIndex];
        stackIndex++;
        return ch;
    }

    public char dequeueCharacter() {
        if (queueStartIndex == queueEndIndex) {
            throw new IndexOutOfBoundsException();
        }
        char ch = queue[queueStartIndex];

        queueStartIndex = (queueStartIndex + 1) % queue.length;
        return ch;
    }
}

public class Solution {
    public static void main(String[] args) {
        Scanner sc=new Scanner(System.in);
        // read the string s.
        String s = sc.nextLine();

        // create the Palindrome class object p.
        Palindrome p = new Palindrome();
        char arr[]=s.toCharArray();//Converting string to a character array
        // push all the characters of string s to stack.
        for (char c : arr) {
            p.pushCharacter(c);
        }
        
        // enqueue all the characters of string s to queue.
        for (char c : arr) {
            p.enqueueCharacter(c);
        }
        
        boolean f = true;
        
        // pop the top character from stack.
        // dequeue the first character from queue.
        // compare both the characters.
        for (int i = 0; i < s.length(); i++) {
            if (p.popCharacter() != p.dequeueCharacter()) {
                f = false;                
                break;
            }
        }
        
        // finally print whether string s is palindrome or not.
        if (f) {
            System.out.println("The word, "+s+", is a palindrome.");
        } else {
            System.out.println("The word, "+s+", is not a palindrome.");
        }
    }
}
