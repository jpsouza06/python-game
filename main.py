import pygame
import player_status
import animation
import sprite_sheet

SCREEN_WIDTH = 950
SCREEN_HEIGHT = 600

WHITE = pygame.Color(255, 255, 255)
SCREEN_BG = (100, 100, 100)

player_position = [475, 450]

animation_steps = [
    [[0, 0], [0, 1], [0, 2], [0, 3]],   # Stopped - Action=0
    [[1, 0], [1, 1], [1, 2], [1, 3]],   # Run - Action=1
    [[0, 4], [0, 5], [0, 6], [0, 7]],   # Stopped with sword - Action=2
    [[1, 4], [1, 5], [1, 6], [1, 7]],   # Run with sword - Action=3
    [[5, 1]],                           # Lowered - Action=4
    [[7, 0], [7, 1], [7, 2], [7, 3]],  # Walk lowered - Action=5
    [[2, 0]],                           # Jump - Action=6
    [[2, 4]]                            # Jump With Sword - Action=7
]
last_update = pygame.time.get_ticks()
animation_cooldown = 150

run = True

objects = [
    pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),
    pygame.Rect(0, SCREEN_HEIGHT - 100, 50, 50)
]

clock = pygame.time.Clock()


def init_display():
    pygame.init()
    pygame.display.set_caption('Ninja Boladao')
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)


screen = init_display()

# Load Image
sprite_sheet_image = pygame.image.load('ninja.png').convert_alpha()
sprite_sheet = sprite_sheet.SpriteSheet(sprite_sheet_image)

# Add animation right
animation_list_right = animation.addAnimation(
    animation_steps, sprite_sheet, 29, 17, 5, True)

# Add animation left
animation_list_left = animation.addAnimation(
    animation_steps, sprite_sheet, 29, 17, 5, False)

# Create ninja
ninjaStatus = player_status.PlayerStatus(
    2.50, 2.50, 7.00, 7.00, [475, 450], 0.4, 2)

ninja = screen.blit(animation_list_right[ninjaStatus.action][ninjaStatus.frame], ninjaStatus.player_position)

while run:
    screen.fill(SCREEN_BG)

    ninja_sensors = [
        pygame.Rect(ninjaStatus.player_position[0], ninjaStatus.player_position[1], 2, ninja.height),  # left,
        pygame.Rect(ninjaStatus.player_position[0], ninjaStatus.player_position[1], ninja.width, 2),  # top
        pygame.Rect(ninjaStatus.player_position[0] + ninja.width, ninjaStatus.player_position[1], 2, ninja.height),  # right
        pygame.Rect(ninjaStatus.player_position[0], ninjaStatus.player_position[1] + ninja.height, ninja.width, 2),  # down
    ]

    for sensor in ninja_sensors:
        pygame.draw.rect(screen, WHITE, sensor)

    for obj in objects:
        if ninja_sensors[0].colliderect(obj):
            ninjaStatus.collided_left = True

        elif ninja_sensors[1].colliderect(obj):
            ninjaStatus.collided_up = True

        elif ninja_sensors[2].colliderect(obj):
            ninjaStatus.collided_right = True

        elif ninja_sensors[3].colliderect(obj):
            ninjaStatus.collided_down = True
            ninjaStatus.ground = True

        pygame.draw.rect(screen, WHITE, obj)

    current_time = pygame.time.get_ticks()

    if current_time - last_update >= animation_cooldown:
        ninjaStatus.frame += 1
        last_update = current_time
        if ninjaStatus.frame >= len(animation_list_right[ninjaStatus.action]):
            ninjaStatus.frame = 0

    if ninjaStatus.right:
        ninja = screen.blit(animation_list_right[ninjaStatus.action][ninjaStatus.frame], ninjaStatus.player_position)
    elif ninjaStatus.left:
        ninja = screen.blit(animation_list_left[ninjaStatus.action][ninjaStatus.frame], ninjaStatus.player_position)
    elif ninjaStatus.old_direction:
        ninja = screen.blit(animation_list_left[ninjaStatus.action][ninjaStatus.frame], ninjaStatus.player_position)
    else:
        ninja = screen.blit(animation_list_right[ninjaStatus.action][ninjaStatus.frame], ninjaStatus.player_position)

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ninjaStatus.right = True
            if event.key == pygame.K_LEFT:
                ninjaStatus.left = True
            if event.key == pygame.K_DOWN:
                ninjaStatus.down = True
            if event.key == pygame.K_SPACE:
                if ninjaStatus.ground:
                    ninjaStatus.jump = True
                    ninjaStatus.jumping = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ninjaStatus.right = False
                ninjaStatus.old_direction = False
            if event.key == pygame.K_LEFT:
                ninjaStatus.left = False
                ninjaStatus.old_direction = True
            if event.key == pygame.K_DOWN:
                ninjaStatus.down = False

    # if not ninjaStatus.ground and ninjaStatus.speed_y < 0 and ninjaStatus.player_position[1] >= 520:
    #     ninjaStatus.ground = True
    #     ninjaStatus.speed_y = 0
    #     ninjaStatus.player_position[1] = 515

    # Speed Control
    ninjaStatus.speedXControl()
    ninjaStatus.speedYControl()

    # Action Control
    ninjaStatus.actionControl()

    # Position Control
    ninjaStatus.positionControl()

    pygame.display.update()

    clock.tick(60)

pygame.quit()
