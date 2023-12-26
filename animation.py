import sprite_sheet


def addAnimation(
            animation_steps,
            spriteSheet: sprite_sheet.SpriteSheet,
            imageWidth,
            imageHeight,
            imageScale,
            imageToRight
):
    animation_list = []
    steps = 0
    black = (0, 0, 0)
    for animation in animation_steps:
        temp_img_list = []
        temp_img_list.clear()
        for x in range(len(animation)):
            temp_img_list.append(spriteSheet.getImage(
                animation_steps[steps][x], imageWidth, imageHeight, imageScale, black, imageToRight
            ))
        animation_list.append(temp_img_list)
        steps += 1
    return animation_list
