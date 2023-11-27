import tkinter as tk
from tkinter import messagebox
import json

class LoginRegisterWindow:
    def __init__(self, parent, on_login_successful):
        self.parent = parent
        self.on_login_successful = on_login_successful

        self.window = tk.Toplevel(parent)
        self.window.title("Вход в игру")
        self.window.geometry("300x200")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.verify_password_var = tk.StringVar()

        tk.Label(self.window, text="Имя пользователя:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.window, textvariable=self.username_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.window, text="Пароль:").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.window, textvariable=self.password_var, show="*").grid(row=1, column=1, padx=10, pady=5)

        self.login_button = tk.Button(self.window, text="Вход", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.register_button = tk.Button(self.window, text="Регистрация", command=self.show_registration)
        self.register_button.grid(row=3, column=0, columnspan=2)

    def on_login_successful(self, username):
        self.window.destroy()
        self.on_login_successful(username)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if self.check_credentials(username, password):
            messagebox.showinfo("Успех", "Вход выполнен успешно!")
            self.on_login_successful(username)
        else:
            messagebox.showerror("Ошибка", "Неправильное имя пользователя или пароль")

    def check_credentials(self, username, password):
        try:
            with open("user_data.json", "r") as file:
                data = json.load(file)
                stored_username = data.get("username")
                stored_password = data.get("password")
                return username == stored_username and password == stored_password

        except FileNotFoundError:
            return False

    def show_registration(self):
        self.register_window = tk.Toplevel(self.parent)
        self.register_window.title("Регистрация")
        self.register_window.geometry("300x200")

        tk.Label(self.register_window, text="Имя пользователя:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.register_window, textvariable=self.username_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.register_window, text="Пароль:").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.register_window, textvariable=self.password_var, show="*").grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.register_window, text="Повторите пароль:").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.register_window, textvariable=self.verify_password_var, show="*").grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.register_window, text="Регистрация", command=self.register).grid(row=3, column=0, columnspan=2, pady=10)
    def register(self):
        username = self.username_var.get()
        password = self.password_var.get()
        verify_password = self.verify_password_var.get()

        if password == verify_password:
            messagebox.showinfo("Успех", "Регистрация выполнена успешно!")
            self.register_window.destroy()
            self.save_credentials(username, password)
        else:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
    def save_credentials(self, username, password):
        data = {"username": username, "password": password}
        with open("user_data.json", "w") as file:
            json.dump(data, file)
class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Крестики-Нолики")

        self.players = {"X": None, "O": None}
        self.current_player = "X"
        self.board = [" " for _ in range(9)]

        self.buttons = [tk.Button(self.window, text=" ", font=('normal', 20), width=6, height=3,
                                  command=lambda i=i: self.make_move(i)) for i in range(9)]
        self.restart_button = tk.Button(self.window, text="Перезапустить игру", command=self.reset_game)
        self.restart_button.grid(row=3, column=0, columnspan=3)

        self.game_window = None
        self.login_register_window = LoginRegisterWindow(self.window, self.on_login_successful)

        self.login_successful = False
    def on_login_successful(self, username):
        self.players["X"] = username
        self.players["O"] = "Bot"
        self.login_register_window.window.withdraw()
        for i, button in enumerate(self.buttons):
            row, col = divmod(i, 3)
            button.grid(row=row, column=col)
        self.window.deiconify()
        self.window.mainloop()
    def make_move(self, index):
        if self.board[index] == " " and " " in self.board:
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player, state=tk.DISABLED)
            if self.check_winner():
                messagebox.showinfo("Победа!", f"Игрок {self.players[self.current_player]} победил!")
                self.disable_buttons()
            elif " " not in self.board:
                messagebox.showinfo("Ничья!", "Ничья! Игра окончена.")
                self.disable_buttons()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O":
                    self.make_bot_move()

    def make_bot_move(self):
        best_move = self.get_best_move()
        self.make_move(best_move)

    def get_best_move(self):
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                if self.check_winner():
                    self.board[i] = " "
                    return i
                self.board[i] = " "
        return self.minimax(self.board, depth=0, maximizing_player=True)["index"]
    def minimax(self, board, depth, maximizing_player):
        if self.check_winner():
            return {"счёт": -1} if maximizing_player else {"счёт": 1}
        elif " " not in board:
            return {"счёт": 0}

        moves = []
        for i in range(9):
            if board[i] == " ":
                board[i] = "O" if maximizing_player else "X"
                score = self.minimax(board, depth + 1, not maximizing_player)["счёт"]
                board[i] = " "
                moves.append({"index": i, "счёт": score})

        return max(moves, key=lambda x: x["счёт"]) if maximizing_player else min(moves, key=lambda x: x["счёт"])
    def check_winner(self):
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i + 1] == self.board[i + 2] != " ":
                return True
        for i in range(3):
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != " ":
                return True
        if self.board[0] == self.board[4] == self.board[8] != " " or self.board[2] == self.board[4] == self.board[6] != " ":
            return True
        return False
    def disable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
    def reset_game(self):
        for i in range(9):
            self.board[i] = " "
            self.buttons[i].config(text=" ", state=tk.NORMAL)
        self.current_player = "X"
        if self.current_player == "O":
            self.make_bot_move()
    def run(self):
        self.window.withdraw()
        self.login_register_window.window.mainloop()

game = TicTacToe()
game.run()
