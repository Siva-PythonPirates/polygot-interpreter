import java.util.Arrays;
public class Main {
    public static void main(String[] args) {
        String input = "{}";
        if (args.length > 0) {
            input = args[0]; // e.g., {"a": [25, 50, 75, 100]}
        }
        
        String arrayStr = input.substring(input.indexOf('[') + 1, input.indexOf(']'));
        String[] items = arrayStr.split(",");
        int[] a = new int[items.length];
        for(int i = 0; i < items.length; i++) {
            a[i] = Integer.parseInt(items[i].trim());
        }

        System.out.println("Sorted array : " + Arrays.toString(a));
    }
}