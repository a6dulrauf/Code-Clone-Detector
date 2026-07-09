public class MathHelper {
    public int plus(int x, int y) { return x + y; }
    public int minus(int x, int y) { return x - y; }
    public int times(int x, int y) { return x * y; }
    public int over(int x, int y) {
        if (y == 0) { return 0; }
        return x / y;
    }
}
