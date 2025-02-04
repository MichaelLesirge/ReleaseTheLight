import pygame
import threading
import typing
import queue
            
BACKGROUND = "black"
MAIN = "white"

class LoadingScreen:
    def __init__(self, surface: pygame.Surface, func: typing.Callable) -> None:
        self.surface = surface
        self.progress = 0

        self.func = func
        
        self.queue = queue.Queue()

        self.font_size = 28
        self.font = pygame.font.Font(pygame.font.match_font('sans-serif'), self.font_size)
        
        self.going = True
        self.quit = False

    def run(self) -> None:
        loading_thread = threading.Thread(name=self.func.__name__, target=self.func, args=(self.queue,))
        loading_thread.start()

        self.start_time = pygame.time.get_ticks()

        self.going = True
        self.quit = False

        while loading_thread.is_alive() and self.going and not self.quit:
            self.events()
            self.display()
            self.update()

        if self.quit:
            self.queue.put(100)
            pygame.quit()

        loading_thread.join()

    def events(self) -> None:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.quit = True

    def display(self) -> None:
        self.surface.fill(BACKGROUND)

        width = self.surface.get_width()
        height = self.surface.get_height()

        bar_height = 30
        bar_width = width - width/ 4

        x = width / 2 - bar_width/2
        y = self.surface.get_height() / 2

        percentage = self.progress / 100

        fill = percentage*bar_width
        outline_rect = pygame.Rect(x - 10, y - 10, bar_width + 20, bar_height + 20)
        fill_rect = pygame.Rect(x, y, fill, bar_height)

        pygame.draw.rect(self.surface, MAIN, fill_rect)
        pygame.draw.rect(self.surface, MAIN, outline_rect, 2)

        trailing_periods = int((pygame.time.get_ticks() - self.start_time) / 1000) % 4

        text = self.font.render("Loading" + "." * trailing_periods, True, MAIN)
        text_rect = text.get_rect(center=(width/2, height/2 - self.font_size/2 - bar_height - 50))
        self.surface.blit(text, text_rect)

        pygame.display.flip()

    def update(self) -> None:
        if not self.queue.empty():
            self.progress = min(max(self.queue.get(), 0), 100)
        
        if self.progress == 100:
            self.going = False
            return