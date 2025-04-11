
class Multiply {
    public int num;

    Multiply(int num) {
        this.num = num;
    }

    public void multiplyByNum() {
        for (int i = 1; i <= 10; i++) {
            int result = i * this.num;
            System.out.println(i +  "x" + this.num + "="  + result);
    }
    }
}

public class FindMultiples {
    public static void main(String[] args) {
        Multiply obj = new Multiply(7);
        obj.multiplyByNum();
        
    }
}