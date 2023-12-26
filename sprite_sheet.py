import  pygame


class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def getImage(self, frame, width, heigt, scale, colour, right):
        image = pygame.Surface((width, heigt)).convert_alpha()
        areaIni = [width, heigt]

        if frame[1] != 0:
            areaIni[1] += 15

        image.blit(self.sheet, (0, 0), (areaIni[0] * frame[0], areaIni[1] * frame[1], width, heigt))
        image = pygame.transform.scale(image, [width * scale, heigt * scale])
        if not right:
            image = pygame.transform.flip(image, True, False)
        image.set_colorkey(colour)

        return image
