import pygame
from core import config
from core.game import Game, run_game
from tampilan.main_ui import show_main_menu
from tampilan.ui_hasil import show_hasil
from tampilan.ui_mulai import show_mulai
from tampilan.ui_setting import show_setting

def mainkan(screen, pilihan):
    while True:
        maze_file = config.MAZE_FILES[pilihan["maze"]]
        game = Game(maze_file, pilihan["algorithm"])
        
        aksi = run_game(screen, game)
        
        if aksi != "finished":
            return aksi
            
        aksi = show_hasil(screen, game.winner, game.get_stats(), pilihan)
        if aksi != "replay":
            return aksi

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    while True:
        menu = show_main_menu(screen)
        if menu == "quit":
            break
            
        if menu == "setting":
            if show_setting(screen) == "quit":
                break
            
        elif menu == "mulai":
            pilihan = show_mulai(screen)
            if pilihan == "quit":
                break
            if pilihan != "back":
                if mainkan(screen, pilihan) == "quit":
                    break
                
    pygame.quit()

if __name__ == "__main__":
    main()