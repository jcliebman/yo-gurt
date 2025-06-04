import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.Objects;
import java.util.Random;


public class MinesweeperSwing {
    private final byte ROWS = 16;
    private final byte COLS = 16;
    private final byte MINES = 40;
    private final boolean[][] BOARD = new boolean[16][16];

    private ImageIcon hiddenIcon;
    private ImageIcon mineIcon;
    private ImageIcon flagIcon;
    private ImageIcon blastIcon;
    private ImageIcon cell1Icon;
    private ImageIcon cell2Icon;
    private ImageIcon cell3Icon;
    private ImageIcon cell4Icon;
    private ImageIcon cell5Icon;
    private ImageIcon cell6Icon;
    private ImageIcon cell7Icon;
    private ImageIcon cell8Icon;
    private ImageIcon celldownIcon;
    private ImageIcon falsemine;
    private final JButton[][] gameButtons = new JButton[ROWS][COLS];
    private final boolean[][] revealedCells = new boolean[ROWS][COLS];
    private final boolean[][] flaggedCells = new boolean[ROWS][COLS];
    private boolean gameIsOver = false;
    private ImageIcon smileyDefaultIcon;
    private ImageIcon smileyWinIcon;
    private ImageIcon smileyLoseIcon;
    private ImageIcon smileyOohIcon;

    private JButton resetButton;
    private final int SMILEY_SIZE = 60;


    public MinesweeperSwing() {
        // Compute an approximate cell size:
        int frameSize = 600;
        int cellW = frameSize / COLS;
        int cellH = frameSize / ROWS;

        // Load & scale textures once:
        smileyDefaultIcon = loadAndScale("/smileface.png", SMILEY_SIZE, SMILEY_SIZE);
        smileyWinIcon     = loadAndScale("/winface.png", SMILEY_SIZE, SMILEY_SIZE);
        smileyLoseIcon    = loadAndScale("/lostface.png", SMILEY_SIZE, SMILEY_SIZE);
        smileyOohIcon  = loadAndScale("/clickface.png", SMILEY_SIZE, SMILEY_SIZE);
        hiddenIcon = loadAndScale("/tile.png", cellW, cellH);
        mineIcon   = loadAndScale("/mine.png", cellW, cellH);
        flagIcon   = loadAndScale("/flag.png", cellW, cellH);
        blastIcon    = loadAndScale("/blast.png",    cellW, cellH);
        cell1Icon    = loadAndScale("/cell1.png",    cellW, cellH);
        cell2Icon    = loadAndScale("/cell2.png",    cellW, cellH);
        cell3Icon    = loadAndScale("/cell3.png",    cellW, cellH);
        cell4Icon    = loadAndScale("/cell4.png",    cellW, cellH);
        cell5Icon    = loadAndScale("/cell5.png",    cellW, cellH);
        cell6Icon    = loadAndScale("/cell6.png",    cellW, cellH);
        cell7Icon    = loadAndScale("/cell7.png",    cellW, cellH);
        cell8Icon    = loadAndScale("/cell8.png",    cellW, cellH);
        celldownIcon = loadAndScale("/celldown.png", cellW, cellH);
        falsemine = loadAndScale("/falsemine.png", cellW, cellH);

        JFrame frame = new JFrame("Minesweeper");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());

        java.net.URL iconURL = getClass().getResource("icon.png");
        if (iconURL != null) {
            frame.setIconImage(new ImageIcon(iconURL).getImage());
        } else {
            System.err.println("Application icon not found!");
        }
        // --- Top Panel for Reset Button ---
        JPanel topPanel = new JPanel(new FlowLayout(FlowLayout.CENTER)); // To center the button
        resetButton = new JButton();
        resetButton.setIcon(smileyDefaultIcon);
        resetButton.setPreferredSize(new Dimension(SMILEY_SIZE + 10, SMILEY_SIZE + 10));
        resetButton.setMargin(new Insets(0,0,0,0));
        resetButton.setBorder(BorderFactory.createEtchedBorder());

        resetButton.addActionListener(e -> resetGame());
        topPanel.add(resetButton);
        frame.add(topPanel, BorderLayout.NORTH);

        // --- Grid Panel for Game Buttons ---
        JPanel gridPanel = new JPanel(new GridLayout(ROWS, COLS));


        // Create buttons & assign the “hidden” texture:
        for (int row = 0; row < ROWS; row++) {
            for (int col = 0; col < COLS; col++) {
                JButton button = new JButton();
                // Icon will be set by resetGame initially
                button.setMargin(new Insets(0, 0, 0, 0));
                gameButtons[row][col] = button;

                final int r = row;
                final int c = col;

                button.addMouseListener(new MouseAdapter() {
                    @Override
                    public void mousePressed(MouseEvent e) {
                        if (!gameIsOver && gameButtons[r][c].isEnabled()) {

                            if (SwingUtilities.isLeftMouseButton(e) && resetButton != null && smileyOohIcon != null) {
                                 resetButton.setIcon(smileyOohIcon);
                            }

                            // Process the click
                            if (SwingUtilities.isLeftMouseButton(e)) {
                                handleCellClick(r, c);
                            } else if (SwingUtilities.isRightMouseButton(e)) {
                                handleRightClick(r, c);
                            }
                            if (!gameIsOver && resetButton != null && smileyOohIcon != null && resetButton.getIcon() == smileyOohIcon) {
                                 resetButton.setIcon(smileyDefaultIcon);
                            }
                        }
                    }

                });
                gridPanel.add(button);
            }
        }
        frame.add(gridPanel, BorderLayout.CENTER); // Add gridPanel to the frame

        // Initial game setup
        resetGame();

        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setResizable(false);
        frame.setVisible(true);
    }
    private void resetGame() {
        gameIsOver = false; // Reset game state

        // Clear game board and state arrays
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                BOARD[r][c] = false;
                revealedCells[r][c] = false;
                flaggedCells[r][c] = false;
            }
        }

        // Generate a new minefield
        generateField();

        // Reset all game buttons to their initial state
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (gameButtons[r][c] != null) {
                    gameButtons[r][c].setIcon(hiddenIcon);
                    gameButtons[r][c].setDisabledIcon(null);
                    gameButtons[r][c].setEnabled(true);
                }
            }
        }

        // Reset smiley face button to default icon
        if (resetButton != null) {
            resetButton.setIcon(smileyDefaultIcon);
        }

        System.out.println("Game Reset!");
    }

    // Helper to load a resource from / (JAR’s root) and scale it:
    private ImageIcon loadAndScale(String resourcePath, int targetW, int targetH) {
        java.net.URL imageUrl = getClass().getResource(resourcePath);
        ImageIcon raw = new ImageIcon(Objects.requireNonNull(imageUrl, "Failed to find resource: " + resourcePath));
        Image img = raw.getImage();
        if (raw.getIconWidth() == -1) { // ImageIcon uses -1 if image couldn't be loaded from URL
            System.err.println("WARNING: ImageIcon reported an error loading image data for: " + resourcePath + " (URL was: " + imageUrl + ")");
        }
        Image scaled = img.getScaledInstance(targetW, targetH, Image.SCALE_SMOOTH);
        return new ImageIcon(scaled);
    }

    private void handleCellClick(int row, int col) {
        if (revealedCells[row][col] || flaggedCells[row][col]) {
            return;
        }

        if (BOARD[row][col]) {
            gameButtons[row][col].setIcon(blastIcon); // Set the icon for the clicked mine *before* calling gameOver
            gameOver(); // Handle game over sequence
        } else {
            revealCell(row, col); // Start reveal process for a non-mine cell
            if (!gameIsOver) {
                checkWinCondition();
            }
        }
    }

    private void revealCell(int row, int col) {
        // Boundary check
        if (row < 0 || row >= ROWS || col < 0 || col >= COLS) {
            return;
        }
        // If already revealed or it's a mine (mines aren't revealed by flood fill)
        if (revealedCells[row][col] || BOARD[row][col] || flaggedCells[row][col]) {
            return;
        }

        revealedCells[row][col] = true;
        JButton button = gameButtons[row][col];

        int adjacentMines = countAdjacentMines(row, col);
        ImageIcon revealedIcon = null; // To store the icon we want to display

        switch (adjacentMines) {
            case 0:
                revealedIcon = celldownIcon;
                button.setIcon(revealedIcon);
                // Set the disabled icon to be the same as the revealed icon
                button.setDisabledIcon(revealedIcon);
                button.setEnabled(false); // Now disable it

                // Flood fill: recursively reveal neighbors
                for (int dRow = -1; dRow <= 1; dRow++) {
                    for (int dCol = -1; dCol <= 1; dCol++) {
                        if (dRow == 0 && dCol == 0) continue; // Skip self
                        revealCell(row + dRow, col + dCol);
                    }
                }
                break; // Important: break after case 0 processing
            case 1: revealedIcon = cell1Icon; break;
            case 2: revealedIcon = cell2Icon; break;
            case 3: revealedIcon = cell3Icon; break;
            case 4: revealedIcon = cell4Icon; break;
            case 5: revealedIcon = cell5Icon; break;
            case 6: revealedIcon = cell6Icon; break;
            case 7: revealedIcon = cell7Icon; break;
            case 8: revealedIcon = cell8Icon; break;
        }

        // For cases 1-8, set the icon and disabled icon
        if (adjacentMines > 0) {
            button.setIcon(revealedIcon);
            button.setDisabledIcon(revealedIcon); // Make disabled state use the full-color icon
            button.setEnabled(false);
        }
    }
    private void handleRightClick(int row, int col) {
        // Can't flag/unflag an already revealed cell
        if (gameIsOver || revealedCells[row][col]) {
            return;
        }

        JButton button = gameButtons[row][col];
        if (flaggedCells[row][col]) {
            // Cell is currently flagged, so unflag it
            flaggedCells[row][col] = false;
            button.setIcon(hiddenIcon);
        } else {
            // Cell is not flagged, so flag it
            flaggedCells[row][col] = true;
            button.setIcon(flagIcon);

        }
    }
    private void gameOver() {
        if (gameIsOver) { // Prevent multiple calls
            return;
        }
        gameIsOver = true; // Set game state to over
        System.out.println("Game Over!");
        if (resetButton != null) {
            resetButton.setIcon(smileyLoseIcon);
        }

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                JButton button = gameButtons[r][c];
                ImageIcon currentButtonIcon = (ImageIcon) button.getIcon();

                if (BOARD[r][c]) { // It's a MINE
                    if (currentButtonIcon == blastIcon) {
                        button.setDisabledIcon(blastIcon);
                    } else if (flaggedCells[r][c]) { // Correctly flagged mine
                        button.setIcon(mineIcon); // Standard is to show it as a mine
                        button.setDisabledIcon(mineIcon);
                    } else { // Unflagged mine
                        button.setIcon(mineIcon);
                        button.setDisabledIcon(mineIcon);
                    }
                } else { // NOT a mine
                    if (flaggedCells[r][c]) {
                        button.setIcon(falsemine);
                        button.setDisabledIcon(falsemine);
                    } else if (!revealedCells[r][c]) { // Hidden safe cell
                        button.setDisabledIcon(hiddenIcon);
                    } else { // Revealed safe cell
                        button.setDisabledIcon(currentButtonIcon);
                    }
                }
                button.setEnabled(false);
            }
        }
    }
    private int countAdjacentMines(int row, int col) {
        int counter = 0;

        for (int deltaX = -1; deltaX <= 1; deltaX++) {
            for (int deltaY = -1; deltaY <= 1; deltaY++) {
                int offsetX = row + deltaX;
                int offsetY = col + deltaY;

                // Bounds check:
                if (offsetX < 0 || offsetX >= ROWS || offsetY < 0 || offsetY >= COLS) {
                    continue;
                }

                // Skip the center cell itself:
                if (deltaX == 0 && deltaY == 0) {
                    continue;
                }

                // Now it’s safe to read BOARD[offsetX][offsetY]:
                if (BOARD[offsetX][offsetY]) {
                    counter++;
                }
            }
        }
        return counter;
    }

    private void generateField() {
        Random randomNumber = new Random();
        int[][] minesCoordinates = new int[40][2];
        int minesplaced = 0;
        // Initialize mines
        while (minesplaced < MINES) {
            boolean isAlreadyPlaced = false;
            int newRow = randomNumber.nextInt(16);
            int newCol = randomNumber.nextInt(16);
            for (int[] minesCoordinate : minesCoordinates) {
                if (minesCoordinate[0] == newRow && minesCoordinate[1] == newCol) {
                    isAlreadyPlaced = true;
                    break;
                }
            }
            if (!isAlreadyPlaced) {
                minesCoordinates[minesplaced][0] = newRow;
                minesCoordinates[minesplaced][1] = newCol;
                BOARD[newRow][newCol] = true;
                minesplaced++;
            }
        }
        // Initialize other squares
        for (int row = 0; row < ROWS; row++) {
            for (int column = 0; column < COLS; column++) {
                if (!BOARD[row][column]) {
                    BOARD[row][column] = false;
                }
            }
        }
    }
    private void checkWinCondition() {
        if (gameIsOver) { // Don't check if game already ended
            return;
        }

        int totalSafeCells = (ROWS * COLS) - MINES;
        int revealedSafeCellsCount = 0;

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                // If a cell is marked as revealed, logic ensures it's a safe cell
                if (revealedCells[r][c]) {
                    revealedSafeCellsCount++;
                }
            }
        }

        if (revealedSafeCellsCount == totalSafeCells) {
            gameWon();
        }
    }
    private void gameWon() {
        if (gameIsOver) { // Prevent multiple calls
            return;
        }
        gameIsOver = true; // Set game state to over
        System.out.println("Congratulations! You Win!");
        if (resetButton != null) {
            resetButton.setIcon(smileyWinIcon);
        }

        // Auto-flag remaining mines and disable all buttons
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                JButton button = gameButtons[r][c];
                if (BOARD[r][c]) { // If it's a mine
                    if (!flaggedCells[r][c]) { // And it wasn't already flagged by the player
                        button.setIcon(flagIcon); // Auto-flag it
                    }
                    button.setDisabledIcon(flagIcon);
                } else {
                    button.setDisabledIcon((ImageIcon) button.getIcon());
                }
                button.setEnabled(false); // Disable all buttons
            }
        }

        // Display win message
        JFrame topFrame = null;
        if (gameButtons[0][0] != null && gameButtons[0][0].getTopLevelAncestor() instanceof JFrame) {
            topFrame = (JFrame) gameButtons[0][0].getTopLevelAncestor();
        }
        if (topFrame != null) {
            JOptionPane.showMessageDialog(topFrame, "Congratulations! You've cleared all the mines!", "You Win!", JOptionPane.INFORMATION_MESSAGE);
        } else {
            // Fallback if frame cannot be found, though rare in typical Swing apps
            System.out.println("Displaying JOptionPane fallback because topFrame was null.");
            JOptionPane.showMessageDialog(null, "Congratulations! You've cleared all the mines!", "You Win!", JOptionPane.INFORMATION_MESSAGE);
        }
    }
}

