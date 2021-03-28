from main import myfont, P1


class onscreendisplay():
    def draw(self, surface):
        textsurface = myfont.render("bombs: "+str(P1.bombs), False, (0, 0, 0))
        surface.blit(textsurface, (0, 0))