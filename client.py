import pygame
from pygame import mixer
from network import Network

pygame.font.init()

width = 1400
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
time = None
done = False
flag = False
username = ''


class Button:
    def __init__(self, text, x, y, color,clickable = True):
        self.text = text
        self.x = x
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
        self.clickable = clickable

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        if self.clickable:
            x1 = pos[0]
            y1 = pos[1]
            if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
                return True
            else:
                return False


def redrawWindow(win, game, p):
    mixer.init()
    mixer.music.load("JPEG/pishti.mp3")
    global done, time
    win.fill((7, 99, 36))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", True, (255, 255, 255))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2), )
    else:
        for i in range(len(btns)):
            btns[i].width = 173
            if btns[i].height != 0:
                btns[i].height = 264
            btns[i].draw(win)

        p0name, p1name = game.getUserNames()
        font = pygame.font.SysFont("comicsans", 70)

        if p == 0:
            win.blit(pygame.font.SysFont("comicsans", 50).render(p0name, 1, (255, 255, 255)), (30, 430))
            win.blit(pygame.font.SysFont("comicsans", 50).render("Vs.", 1, (255, 255, 255)), (30, 380))
            win.blit(pygame.font.SysFont("comicsans", 50).render(p1name, 1, (255, 255, 255)), (30, 330))
        else:
            win.blit(pygame.font.SysFont("comicsans", 50).render(p0name, 1, (255, 255, 255)), (30, 330))
            win.blit(pygame.font.SysFont("comicsans", 50).render("Vs.", 1, (255, 255, 255)), (30, 380))
            win.blit(pygame.font.SysFont("comicsans", 50).render(p1name, 1, (255, 255, 255)), (30, 430))

        if game.p1Turn and p == 0:
            text1 = font.render("Your Turn", 1, (255, 255, 255))
        elif game.p2Turn:
            text1 = font.render("Opponent's Turn", 1, (255, 255, 255))

        if game.p2Turn and p == 1:
            text2 = font.render("Your Turn", 1, (255, 255, 255))
        elif game.p1Turn:
            text2 = font.render("Opponent's Turn", 1, (255, 255, 255))

        p1rematch, p2rematch = game.getrematchwanters()

        if p == 0:
            if p1rematch:
                win.blit(pygame.font.SysFont("comicsans", 40).render("Rematch request sent", 1, (255, 255, 255)),
                         (830, 680))
            elif p2rematch:
                win.blit(pygame.font.SysFont("comicsans", 40).render(p1name + " wants to rematch", 1, (255, 255, 255)),
                         (830, 680))
        elif p == 1:
            if p2rematch:
                win.blit(pygame.font.SysFont("comicsans", 40).render("Rematch request sent", 1, (255, 255, 255)),
                         (830, 680))
            elif p1rematch:
                win.blit(pygame.font.SysFont("comicsans", 40).render(p0name + " wants to rematch", 1, (255, 255, 255)),
                         (830, 680))

        if (len(game.leftCards) + len(game.p1cards) + len(game.p2cards)) == 0 and p == 0:

            win.blit(pygame.font.SysFont("comicsans", 80).render(str(game.calculator1()), 1, (255, 255, 255)),
                     (450, 700))
            win.blit(pygame.font.SysFont("comicsans", 80).render(str(game.calculator2()), 1, (255, 255, 255)),
                     (450, 100))

            if game.calculator2() < game.calculator1():
                win.blit(pygame.font.SysFont("comicsans", 80).render("YOU WIN", 1, (255, 255, 255), (128, 128, 128)),
                         (350, 400))
            elif game.calculator1() == game.calculator2():
                win.blit(pygame.font.SysFont("comicsans", 80).render("TIE", 1, (255, 255, 255), (128, 128, 128)),
                         (430, 400))
            else:
                win.blit(pygame.font.SysFont("comicsans", 80).render("YOU LOSE", 1, (255, 255, 255), (255, 0, 0)),
                         (350, 400))

            btns[-1].text = 'rematch'
            btns[-1].clickable = True

        elif (len(game.leftCards) + len(game.p1cards) + len(game.p2cards)) == 0 and p == 1:

            win.blit(pygame.font.SysFont("comicsans", 80).render(str(game.calculator1()), True, (255, 255, 255)),
                     (450, 100))
            win.blit(pygame.font.SysFont("comicsans", 80).render(str(game.calculator2()), True, (255, 255, 255)),
                     (450, 700))

            if game.calculator2() > game.calculator1():
                win.blit(pygame.font.SysFont("comicsans", 80).render("YOU WIN", 1, (255, 255, 255), (128, 128, 128)),
                         (350, 400))
            elif game.calculator2() == game.calculator1():
                win.blit(pygame.font.SysFont("comicsans", 80).render("TIE", 1, (255, 255, 255), (128, 128, 128)),
                         (430, 400))
            else:
                win.blit(pygame.font.SysFont("comicsans", 80).render("YOU LOSE", 1, (255, 255, 255), (255, 0, 0)),
                         (350, 400))

            btns[-1].clickable = True
            btns[-1].text = 'rematch'

        elif p == 1:
            win.blit(text2, (900, 680))
            btns[-1].clickable = False
            btns[-1].text = ''
        else:
            win.blit(text1, (900, 680))
            btns[-1].clickable = False
            btns[-1].text = ''

        if len(game.middleCards) > 0:
            done = False
            time = None
            card = pygame.image.load(r'JPEG/' + game.middleCards[-1] + '.png')
            if len(game.middleCards) > 1 and (len(game.leftCards) + len(game.p1cards) + len(game.p2cards)) != 0:
                card1 = pygame.image.load(r'JPEG/' + game.middleCards[-2] + '.png')
                if len(game.leftCards) == 40 and (len(game.p1cards) + len(game.p2cards) == 8):  # ilk turda kapalı olayı
                    card2 = pygame.image.load(r'JPEG/' + 'Red_back' + '.png')
                    win.blit(card2, (1050, 80))
                    win.blit(card, (1000, 30))
                elif len(game.middleCards) % 2 == 1:
                    win.blit(card1, (1050, 80))
                    win.blit(card, (1000, 30))

                else:
                    win.blit(card1, (1000, 30))
                    win.blit(card, (1050, 80))
            elif (len(game.leftCards) + len(game.p1cards) + len(game.p2cards)) != 0:
                win.blit(card, (1000, 30))
            else:
                pygame.display.update()

        else:  # piştilendiğimizde

            if time is None and done is False:  # sadece 1 kere giriyor
                time = pygame.time.get_ticks()
                done = True

            elif time is not None and done is True:
                tm = pygame.time.get_ticks() - time
                if tm < 1000:
                    if tm >= 620:
                        mixer.init()
                        mixer.music.load("JPEG/pishti.mp3")
                        mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.Clock().tick(10)
                        time = None

                    card4 = pygame.image.load(r'JPEG/' + game.pishticard + '.png')
                    win.blit(card4, (1000, 30))
                win.blit(pygame.image.load('JPEG/pishti.png'), (400, 320))



        if p == 0 and len(game.p1cards) + len(game.p2cards) != 0:
            card1 = pygame.image.load(r'JPEG/' + game.p1cards1[0] + '.png') if game.p1cards1[0] != 'x' else 'empty'
            card2 = pygame.image.load(r'JPEG/' + game.p1cards1[1] + '.png') if game.p1cards1[1] != 'x' else 'empty'
            card3 = pygame.image.load(r'JPEG/' + game.p1cards1[2] + '.png') if game.p1cards1[2] != 'x' else 'empty'
            card4 = pygame.image.load(r'JPEG/' + game.p1cards1[3] + '.png') if game.p1cards1[3] != 'x' else 'empty'
            cardsp1 = [card1, card2, card3, card4]

            for i in range(len(cardsp1)):
                if type(cardsp1[i]) != str:
                    win.blit(cardsp1[i], (200 * i + 30, 500))

            for i in range(len(game.p2cards)):
                win.blit(pygame.image.load(r'JPEG/Red_back.png'), (200 * i + 30, 30))

        elif p == 1 and len(game.p1cards) + len(game.p2cards) != 0:
            card1 = pygame.image.load(r'JPEG/' + game.p2cards1[0] + '.png') if game.p2cards1[0] != 'x' else 'empty'
            card2 = pygame.image.load(r'JPEG/' + game.p2cards1[1] + '.png') if game.p2cards1[1] != 'x' else 'empty'
            card3 = pygame.image.load(r'JPEG/' + game.p2cards1[2] + '.png') if game.p2cards1[2] != 'x' else 'empty'
            card4 = pygame.image.load(r'JPEG/' + game.p2cards1[3] + '.png') if game.p2cards1[3] != 'x' else 'empty'
            cardsp2 = [card1, card2, card3, card4]

            for i in range(len(cardsp2)):
                if type(cardsp2[i]) != str:
                    win.blit(cardsp2[i], (200 * i + 30, 500))

            for i in range(len(game.p1cards)):
                win.blit(pygame.image.load(r'JPEG/Red_back.png'), (200 * i + 30, 30))

    pygame.display.update()


btns = [Button('0', 30, 500, (7, 99, 36)), Button("0", 230, 500, (7, 99, 36)),
        Button("0", 430, 500, (7, 99, 36)), Button("0", 630, 500, (7, 99, 36)), Button("", 830, 500, (7, 99, 36),False)]


def main(usrname):
    global flag
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        n.send('username,' + usrname)

        if btns[0].text == '0' and len(
                game.p1cards) >= 4:  # dealfirst kartları dağıtıldığı halde butonlara text atanmadıysa
            for i in range(4):
                if player == 0:
                    btns[i].text = game.p1cards[i]

                elif player == 1:
                    btns[i].text = game.p2cards[i]

        if game.p1cards == [] and game.p2cards == [] and btns[1].height == 0:  # her tur bittiğinde
            if len(game.leftCards) > 0:
                n.send('deal')

        elif game.p1cards == [] and game.p2cards == []:  # ilk turda dağıtmak için
            n.send('dealfirst')

        if game.dealt and btns[0].height == 0 and btns[
            1].height == 0:  # her tur sonu kartlar dağıtıldığı halde butonlara text atanmadıysa
            for i in range(4):
                if player == 0:
                    btns[i].height = 100
                    btns[i].text = game.p1cards[i]

                elif player == 1:
                    btns[i].height = 100
                    btns[i].text = game.p2cards[i]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                for i in range(len(btns)):
                    if btns[i].click(pos) and game.connected():
                        if player == 0:

                            if btns[i].text == 'rematch':
                                n.send(btns[i].text)

                            elif game.p1Turn:
                                n.send(btns[i].text)
                                if len(btns[i].text) == 2:
                                    btns[i].text = ''
                                    btns[i].height = 0


                        else:
                            if btns[i].text == 'rematch':
                                n.send(btns[i].text)
                            elif game.p2Turn:
                                n.send(btns[i].text)
                                if len(btns[i].text) == 2:
                                    btns[i].text = ''
                                    btns[i].height = 0

        redrawWindow(win, game, player)


def menu_screen():
    global username
    run = True
    clock = pygame.time.Clock()
    textbox = pygame.Rect(540, 330, 140, 50)
    color = pygame.Color((255, 255, 255))
    btn = Button('Go', 570, 500, (0, 0, 0))

    while run:
        clock.tick(60)

        font = pygame.font.SysFont("comicsans", 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key != pygame.K_BACKSPACE:
                    if event.key != pygame.K_RETURN:
                        if event.key != pygame.K_COMMA:
                            username += event.unicode
                    else:
                        run = False
                else:
                    username = username[:-1]
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn.click(pos):
                    run = False


        win.fill((7, 99, 36))
        pygame.draw.rect(win, color, textbox, 2)

        text = font.render(username, True, (255, 255, 255))
        textsurface = font.render(username, True, (255, 255, 255))

        win.blit(textsurface, (textbox.x + 5, textbox.y + 5))
        win.blit(pygame.font.SysFont("comicsans", 40).render("Enter username: ", True, (255, 255, 255)), (540, 300))

        textbox.w = max(textsurface.get_width() + 10, 220)
        btn.draw(win)



        pygame.display.update()

    main(username)


while True:
    menu_screen()

