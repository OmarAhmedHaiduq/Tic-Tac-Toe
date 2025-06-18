import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        while True:
            name = input("Enter your name (letters only): ")
            if name.isalpha():
                self.name = name
                break
            print("Invalid name. Please use letters only.")

    def choose_symbol(self, taken_symbol=None):
        while True:
            symbol = input(f"{self.name}, choose your symbol (a single letter): ")
            if symbol.isalpha() and len(symbol) == 1:
                symbol = symbol.upper()
                if taken_symbol and symbol == taken_symbol:
                    print("Symbol already taken by the other player. Choose another.")
                else:
                    self.symbol = symbol
                    break
            else:
                print("Invalid symbol. Please use a single letter.")

class Menu:
    def display_main_menu(self):
        print("Welcome to X-O Game!")
        print("1. Start Game")
        print("2. Quit Game")
        choice = input("Enter your choice (1 or 2): ")
        while choice not in ["1", "2"]:
            print("Invalid choice. Please enter 1 or 2.")
            choice = input("Enter your choice (1 or 2): ")
        return choice

    def display_endgame_menu(self):
        menu_text = """
Game Over!
1. Restart Game
2. Quit Game
Enter your choice (1 or 2): """
        choice = input(menu_text)
        while choice not in ["1", "2"]:
            print("Invalid choice. Please enter 1 or 2.")
            choice = input("Enter your choice (1 or 2): ")
        return choice

class Board:
    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]

    def display_board(self):
        for i in range(0, 9, 3):
            print(" | ".join(self.board[i:i+3]))
            if i < 6:
                print("-" * 9)

    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice-1] = symbol
            return True
        return False

    def is_valid_move(self, choice):
        return self.board[choice - 1].isdigit()

class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0

    def start_game(self):
        while True:
            choice = self.menu.display_main_menu()
            if choice == "1":
                self.setup_players()
                self.play_game()
            else:
                self.quit_game()
                break

    def setup_players(self):
        clear_screen()
        print("Player 1, enter your details:")
        self.players[0].choose_name()
        self.players[0].choose_symbol()
        clear_screen()
        print("Player 2, enter your details:")
        self.players[1].choose_name()
        self.players[1].choose_symbol(taken_symbol=self.players[0].symbol)
        clear_screen()

    def play_game(self):
        self.board = Board()
        self.current_player_index = 0
        while True:
            self.board.display_board()
            player = self.players[self.current_player_index]
            print(f"{player.name}'s turn ({player.symbol})")
            cell_choice = input("Choose a cell [1-9]: ")
            if not cell_choice.isdigit() or not (1 <= int(cell_choice) <= 9):
                print("Invalid choice. Please choose a number between 1 and 9.")
                continue
            cell_choice = int(cell_choice)
            if not self.board.update_board(cell_choice, player.symbol):
                print("Cell already taken. Choose another cell.")
                continue
            if self.check_win():
                self.board.display_board()
                print(f"{player.name} wins!")
                if self.menu.display_endgame_menu() == "1":
                    self.board = Board()
                    self.current_player_index = 0
                    continue
                else:
                    self.quit_game()
                    break
            if self.check_draw():
                self.board.display_board()
                print("It's a draw!")
                if self.menu.display_endgame_menu() == "1":
                    self.board = Board()
                    self.current_player_index = 0
                    continue
                else:
                    self.quit_game()
                    break
            self.current_player_index = (self.current_player_index + 1) % 2

    def check_win(self):
        b = self.board.board
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        for i, j, k in combos:
            if b[i] == b[j] == b[k] and not b[i].isdigit():
                return True
        return False

    def check_draw(self):
        return all(not cell.isdigit() for cell in self.board.board)

    def quit_game(self):
        print("Thank you for playing! Goodbye!")

if __name__ == "__main__":
    game = Game()
    game.start_game()