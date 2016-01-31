

class Node {
    int data;
    Node next;
    Node(int d) {
        data = d;
        next = null;
    }

    class Solution {

        public static Node removeDuplicates(Node head) {
            Node anchor = head;
            while (anchor != null) {
                Node runner = anchor;
                while (runner.next != null && runner.next.data == anchor.data) {
                    runner = runner.next;
                }
                anchor.next = runner.next;
                anchor = runner.next;
            }
            return head;
        }


    }
}
