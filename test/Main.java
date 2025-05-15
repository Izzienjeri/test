// Define the Playable interface
interface Playable {
    void play();
}

// Implement the Game class that implements Playable
class Game implements Playable {
    @Override
    public void play() {
        System.out.println("Playing the game");
    }
}

// Main method to create an instance of Game and call play
public class Main {
    public static void main(String[] args) {
        Game game = new Game();
        game.play();
    }
}
