import java.util.*;
import java.io.*;
class Node {
    Node left,right;
    int data;
    Node(int data) {
        this.data=data;
        left=right=null;
    }
}
class Solution {

    private static final List<List<Integer>> levels = new ArrayList<>();

    static void levelOrder(Node root) {
        fillLevels(root, 0);
        levels.stream().forEach(level -> {
                level.stream().forEach(data -> System.out.print(data + " "));
            });
    }

    private static void fillLevels(Node node, int level) {
        if (node == null) {
            return;
        }
        if (level >= levels.size()) {
            List<Integer> levelList = new ArrayList<>();
            levels.add(levelList);
        }
        levels.get(level).add(node.data);
        fillLevels(node.left, level + 1);
        fillLevels(node.right, level + 1);
    }

    static void levelOrder(Node root) {
        Queue<Node> unprocessed = new ArrayDeque<>();

        if (root == null) return;

        unprocessed.add(root);
        while (!unprocessed.isEmpty()) {
            Node toProcess = unprocessed.remove();
            System.out.print(toProcess.data + " ");

            if (toProcess.left != null) unprocessed.add(toProcess.left);
            if (toProcess.right != null) unprocessed.add(toProcess.right);
        }
    }


    public static Node insert(Node root,int data) {
        if(root==null) {
            return new Node(data);
        } else {
            Node cur;
            if(data<=root.data) {
                cur=insert(root.left,data);
                root.left=cur;
            } else {
                cur=insert(root.right,data);
                root.right=cur;
            }
            return root;
        }
    }
    public static void main(String args[]) {
        Scanner sc=new Scanner(System.in);
        int T=sc.nextInt();
        Node root=null;
        while(T-->0) {
            int data=sc.nextInt();
            root=insert(root,data);
        }
        levelOrder(root);
    }
}
