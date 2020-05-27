def show_go_screen():
    screen.blit(background_image, (0, 0))
    text_surface = font.render("Press space bar to play again", True, white)
    screen.blit(text_surface, (400, 350))
    pygame.display.flip()
    global done
    again = False
    while not again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                again = True
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    again = True
        clock.tick(20)
