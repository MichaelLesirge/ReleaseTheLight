import releaseTheLight
import loading
import pygame

pygame.init()

game = releaseTheLight.Game()

loading_screen = loading.LoadingScreen(game.window, game.setup)

loading_screen.run()
game.run()