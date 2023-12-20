import pygame
import player_status

SCREEN_WIDTH = 950
SCREEN_HEIGHT = 600

SCREEN_BG = (100, 100, 100)
BLACK = (0, 0, 0)
animation_list_right = []
animation_list_left = []
animation_steps = [
    [[0, 0], [0, 1], [0, 2], [0, 3]],  # Stopped - Action=0
    [[1, 0], [1, 1], [1, 2], [1, 3]],   # Run - Action=1
    [[0, 4], [0, 5], [0, 6], [0, 7]],  # Stopped with sword - Action=2
    [[1, 4], [1, 5], [1, 6], [1, 7]],  # Run with sword - Action=3
]
last_update = pygame.time.get_ticks()
animation_cooldown = 250

run = True


def init_display():
    pygame.init()
    pygame.display.set_caption('Ninja Boladao')
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)


def add_animations():
    import sprite_sheet

    steps = 0

    # Carrega imagens do ninja
    sprite_sheet_image = pygame.image.load('ninja.png').convert_alpha()
    sprite_sheet = sprite_sheet.SpriteSheet(sprite_sheet_image)

    # Adciona as animações para a direita na lista
    for animation in animation_steps:
        temp_img_list = []
        temp_img_list.clear()
        for x in range(len(animation)):
            temp_img_list.append(sprite_sheet.getImage(animation_steps[steps][x], 24, 17, 5, BLACK, True))
        animation_list_right.append(temp_img_list)
        steps += 1

    steps = 0
    # Adciona as animações para a esquerda na lista
    for animation in animation_steps:
        temp_img_list = []
        temp_img_list.clear()
        for x in range(len(animation)):
            temp_img_list.append(sprite_sheet.getImage(animation_steps[steps][x], 24, 17, 5, BLACK, False))
        animation_list_left.append(temp_img_list)
        steps += 1


screen = init_display()
add_animations()
ninjaStatus = player_status.PlayerStatus(2.00, 1.00, 10.00, 5.00)

while run:
    screen.fill(SCREEN_BG)

    current_time = pygame.time.get_ticks()

    if current_time - last_update >= animation_cooldown:
        ninjaStatus.frame += 1
        last_update = current_time
        if ninjaStatus.frame >= len(animation_list_right[ninjaStatus.action]):
            ninjaStatus.frame = 0

    if ninjaStatus.right:
        screen.blit(animation_list_right[ninjaStatus.action][ninjaStatus.frame], ninjaStatus.player_position)
    elif ninjaStatus.left:
        screen.blit(animation_list_left[ninjaStatus.action][ninjaStatus.frame], ninjaStatus.player_position)
    elif ninjaStatus.old_direction:
        screen.blit(animation_list_left[ninjaStatus.action][ninjaStatus.frame], ninjaStatus.player_position)
    else:
        screen.blit(animation_list_right[ninjaStatus.action][ninjaStatus.frame], ninjaStatus.player_position)

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ninjaStatus.right = True
            if event.key == pygame.K_LEFT:
                ninjaStatus.left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ninjaStatus.right = False
                ninjaStatus.old_direction = False
            if event.key == pygame.K_LEFT:
                ninjaStatus.left = False
                ninjaStatus.old_direction = True

                # Speed Control
    ninjaStatus.speedControl()

    # Action Control
    ninjaStatus.actionControl()

    # Position Control
    ninjaStatus.positionControl()

    pygame.display.update()


pygame.quit()
