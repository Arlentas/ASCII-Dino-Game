''' This is a random game I made whilst bored. It will only work on windows machines due to clearing the terminal. If on linux, change the clearConsole define statement accordingly. '''
import random
import os
import time
import keyboard

class Game:

    def __init__(self, wins, jumps, score, losses):
        self.size = 0
        self.move = 0
        self.wins = wins
        self.jumps = jumps
        self.score = score
        self.losses = losses

    def clearConsole(self):
        command = 'clear'
        if os.name in ('nt', 'dos'):
            command = 'cls'
        os.system(command)

    def choose_size(self):
        try:
            self.size = input("Choose size (s, m, l): ")
            if self.size == 'quit':
                exit()
            if self.size not in ['s', 'm', 'l']:
                raise ValueError
            if self.size == 's':
                self.size = 750
            if self.size == 'm':
                self.size = 1500
            if self.size == 'l':
                self.size = 2500
        except ValueError:
            print('Please enter a valid self.size (s, m, l')
            self.choose_size()

    def create_map(self):
        air = []
        air1 = []
        air2 = []
        floor = []
        obstacles = []
        counter = 0
        self.choose_size()
        for i in range(self.size):
            air.append(' ')
            air1.append(' ')
            floor.append('=')
            cactus_roll = random.randint(1, 2)
            if counter == 30:
                counter = 0
            if counter == 0:
                if cactus_roll == 2:
                    obstacles.append('#')
                    counter += 1
                    height_roll = random.randint(2, 3)
                    if height_roll == 2:
                        air2.append('#')
                    else:
                        air2.append(' ')
                else:
                    obstacles.append(' ')
                    air2.append(' ')
                    counter += 1
            else:
                counter += 1
                air2.append(' ')
                obstacles.append(' ')
        for i in '|- - - - - - - -|':
            air2.append(i)
            air.append(i)
        for i in '|               |':
            obstacles.append(i)
            floor.append(i)
        for i in '|    Finish     |':
            air1.append(i)

        return [air, air1, air2, obstacles, floor]
    
    def print_line(self, stage):
        a = 0
        i = self.move
        line = ''
        lines = ''
 
        while a != 5:
            if len(stage[0]) - self.move <= 100:
                while i <= len(stage[1]) - 1:
                    line += stage[a][(i)]
                    i += 1
            else:
                while i <= (100 + self.move):
                    line += stage[a][i]
                    i += 1
            lines += line + '\n'
            line = ''
            a += 1
            i = self.move
        print(lines)

    def print_frame(self, stage):
        self.print_line(stage)
        time.sleep(0.016666666)
        self.clearConsole()

    def jump(self, stage):
        frame = 0
        jump = 3
        while frame <= 3:
            frame += 1
            if jump >= 0:
                self.move += 1
                jump -= 1
                dead = self.death_check(jump, stage)
                if not dead:
                    stage[jump][self.move] = 'x'
                    self.print_frame(stage)
                else:
                    break
            if not dead:
                self.move += 1
                self.death_check(jump, stage)
                self.print_frame(stage)
        if not dead:
            frame = 0
            while frame <= 3:
                frame += 1
                if jump <= 3:
                    self.move += 1
                    jump += 1
                    dead = self.death_check(jump, stage)
                    if not dead:
                        stage[jump][self.move] = 'x'
                        self.print_frame(stage)
                    else:
                        break
                if not dead:
                    self.move += 1
                    self.death_check(jump, stage)
                    self.print_frame(stage)
            return stage, dead

    def print_results(self):
        print('You jumped ' + str(self.jumps) + ' times!')
        time.sleep(1.5)
        print('You have won ' + str(self.wins) + ' times!')
        time.sleep(1.5)
        print('You have lost ' + str(self.losses) + ' times!')
        time.sleep(1.5)
        print('Your score is ' + str(self.score) + '!')
        time.sleep(1.5)

    def play_again(self):
        try:
            time.sleep(0.5)
            choice = input('Play again? (y/n): ')
            choice = choice.strip()
            if choice not in ['y', 'n']:
                raise ValueError
            if choice == 'y':
                print('Replaying, have fun!')
                time.sleep(0.5)
                return True
            else:
                print('Play again another time!')
                time.sleep(0.5)
                return False
        except ValueError:
            print('Please enter a valid input')
            time.sleep(0.5)
            self.play_again()

    def death_check(self, jump, stage):
        if stage[jump][self.move] == '#':
            self.clearConsole()
            print('You died!')
            self.losses += 1
            self.print_results()
            return True
        elif stage[3][self.move] == '#':
            self.score += 100
        return False

    def play(self):
        jump = 3
        stage = self.create_map() 
        while self.move < (len(stage[0]) - 7):
            self.move += 1
            dead = self.death_check(jump, stage)
            if dead:
                return self.wins, self.losses, self.jumps, self.score
            stage[3][self.move] = 'x'
            if keyboard.is_pressed(' '):
                self.jumps += 1
                stage, dead = self.jump(stage)
                if dead:
                    return self.wins, self.losses, self.jumps, self.score
            self.print_frame(stage)
        print('You Won!')
        self.wins += 1
        self.print_results()

        return self.wins, self.losses, self.jumps, self.score

wins = 0
losses = 0
jumps = 0
score = 0

while True:
    game = Game(wins, jumps, score, losses)
    wins, losses, jumps, score = game.play()

    retry = game.play_again()
    if retry == True:
        game = Game(wins, jumps, score, losses)
    else:
        exit()

