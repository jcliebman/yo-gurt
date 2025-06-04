import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class MinesweeperSwing {
    private final int ROWS = 9;
    private final int COLS = 9;

    public MinesweeperSwing() {
        JFrame frame = new JFrame("Minesweeper");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new GridLayout(ROWS, COLS));

        for (int row = 0; row < ROWS; row++) {
            for (int col = 0; col < COLS; col++) {
                JButton button = new JButton();
                int r = row, c = col;
                button.addActionListener(e -> handleCellClick(r, c, button));
                frame.add(button);
            }
        }

        frame.setSize(400, 400);
        frame.setVisible(true);
    }

    private void handleCellClick(int row, int col, JButton button) {
        // TODO: reveal cell, check for mine, etc.
        button.setText("Clicked!");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(MinesweeperSwing::new);
    }
}

