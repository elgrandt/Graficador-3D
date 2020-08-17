import pygame

def add_border(surface,color = (0,0,0),b1 = 1,b2 = 1,b3 = 1,b4 = 1):
    w,h = surface.get_size()
    # Arriba
    b1s = pygame.surface.Surface((w,b1))
    # Izquierda
    b2s = pygame.surface.Surface((b2,h))
    # Derecha
    b3s = pygame.surface.Surface((b3,h))
    # Abajo
    b4s = pygame.surface.Surface((w,b4))

    b1s.fill(color)
    b2s.fill(color)
    b3s.fill(color)
    b4s.fill(color)
    
    surface.blit(b1s,(0,0))
    surface.blit(b2s,(0,0))
    surface.blit(b3s,(w-b3,0))
    surface.blit(b4s,(0,h-b4))
    
    return surface