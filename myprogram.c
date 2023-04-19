#include <ncurses.h>

int main() {
    initscr(); // Initialize ncurses
    printw("Hello, World!"); // Print "Hello, World!" to the screen
    refresh(); // Refresh the screen to show changes
    getch(); // Wait for user input
    endwin(); // End ncurses mode
    return 0;
}
