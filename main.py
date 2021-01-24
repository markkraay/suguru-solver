from suguru import Suguru
import pygame

if __name__ == "__main__":
    x = int(input("Enter amount of columns: "))
    y = int(input("Enter amount of rows: "))
    
    suguru = Suguru(x, y)
    screen_size = suguru.GetDimensions()
    
    pygame.init()
    pygame.display.set_caption("Suguru Solver")

    screen = pygame.display.set_mode((screen_size[0], screen_size[1]))

    # Pygame GUI
    running = True
    while running:
        suguru.Render(screen)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    x, y = pygame.mouse.get_pos()
                    suguru.InsertNumber(event.key - 48, x, y)

                if event.key == pygame.K_s:
                    suguru.ReadInBoard()
                    suguru.Solve()

                if event.key == pygame.K_q:
                    x, y = pygame.mouse.get_pos()
                    suguru.HighlightBoard(x, y)

                if event.key == pygame.K_a:
                    suguru.IncrementKey()

            elif event.type == pygame.QUIT:
                running = False


