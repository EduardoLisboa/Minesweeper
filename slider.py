import pygame
from Constants.constants import Constants


class Slider:
    def __init__(self, x: int, y: int, width: int, min_value: int, max_value: int, initial_value: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = 20
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.dragging = False

        self.handle_radius = 15
        value_ratio = (self.value - self.min_value) / (self.max_value - self.min_value)
        self.handle_x = self.x + int(value_ratio * self.width)
    
    def draw(self, window: pygame.Surface):
        pygame.draw.line(
            window,
            Constants.WHITE,
            (self.x, self.y),
            (self.x + self.width, self.y),
            4
        )

        pygame.draw.circle(
            window,
            Constants.LIGHT_YELLOW if self.dragging else Constants.WHITE,
            (self.handle_x, self.y),
            self.handle_radius
        )

        pygame.draw.circle(
            window,
            Constants.BLACK,
            (self.handle_x, self.y),
            self.handle_radius,
            2
        )
    
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            distance = ((mouse_x - self.handle_x) ** 2 + (mouse_y - self.y) ** 2) ** 0.5
            if distance <= self.handle_radius:
                self.dragging = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = event.pos[0]
            self.handle_x = max(self.x, min(self.x + self.width, mouse_x))
            
            value_ratio = (self.handle_x - self.x) / self.width
            self.value = int(self.min_value + value_ratio * (self.max_value - self.min_value))
    
    def get_value(self) -> int:
        return self.value
