import java.io.*;
import java.util.*;
// Node
class Node {
    int data;
    Node next;
    Node(int d){
        data=d;
        next=null;
    }
}

class Solution {

    public static  Node insert(Node head, int data) {
        if (head == null) {
            return new Node(data);
        } else {
            Node node = head;
            while (node.next != null) {
                node = node.next
            }
            node.next = new Node(data);
            return head;
        }
    }

    public static  Node insert(Node head,int data) {
        //Complete this method
    }
}
