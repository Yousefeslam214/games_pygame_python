import pygame

successes, fails = pygame.init()
print(successes, fails)
startTime = 0
gameActive = False
move_right = [pygame.image.load("hero/R1.png"), pygame.image.load("hero/R2.png"), pygame.image.load("hero/R3.png"), pygame.image.load("hero/R4.png"), pygame.image.load("hero/R5.png"), pygame.image.load("hero/R6.png"), pygame.image.load("hero/R7.png"), pygame.image.load("hero/R8.png"), pygame.image.load("hero/R9.png")]
move_left = [pygame.image.load("hero/L1.png"), pygame.image.load("hero/L2.png"), pygame.image.load("hero/L3.png"), pygame.image.load("hero/L4.png"), pygame.image.load("hero/L5.png"), pygame.image.load("hero/L6.png"), pygame.image.load("hero/L7.png"), pygame.image.load("hero/L8.png"), pygame.image.load("hero/L9.png")]

move_rightE = [pygame.image.load("enemy/R1E.png"), pygame.image.load("enemy/R2E.png"), pygame.image.load("enemy/R3E.png"), pygame.image.load("enemy/R4E.png"), pygame.image.load("enemy/R5E.png"), pygame.image.load("enemy/R6E.png"), pygame.image.load("enemy/R7E.png"), pygame.image.load("enemy/R8E.png"), pygame.image.load("enemy/R9E.png"), pygame.image.load("enemy/R10E.png"), pygame.image.load("enemy/R11E.png")]
move_leftE = [pygame.image.load("enemy/L1E.png"), pygame.image.load("enemy/L2E.png"), pygame.image.load("enemy/L3E.png"), pygame.image.load("enemy/L4E.png"), pygame.image.load("enemy/L5E.png"), pygame.image.load("enemy/L6E.png"), pygame.image.load("enemy/L7E.png"), pygame.image.load("enemy/L8E.png"), pygame.image.load("enemy/L9E.png"), pygame.image.load("enemy/L10E.png"), pygame.image.load("enemy/L10E.png")]

bulletSound = pygame.mixer.Sound("sounds/bullet.wav")
hitSound = pygame.mixer.Sound("sounds/hit.wav")

bg = pygame.image.load("bg.jpg")
hero = pygame.image.load("hero/standing.png")
score = 0
screenWidth = 700
screenHeight = 500
clock = pygame.time.Clock()

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("yousef game")

BLACK = (0, 0, 0)  # RGB
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 100, 0)

class Player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.width = width
        self.height = height
        self.step = 5
        self.left = False
        self.right = False
        self.moves = 0
        self.speed = 10
        self.isJumping = True
        self.standing = True
        self.hitbox = (self.x + 20, self.y + 10, self.width - 40, self.height - 10)

    def draw(self, screen):
        if not self.standing:
            if self.left:
                screen.blit(move_left[self.moves // 2], (self.x, self.y))
                self.moves += 1
                if self.moves == 18:
                    self.moves = 0
            elif self.right:
                screen.blit(move_right[self.moves // 2], (self.x, self.y))
                self.moves += 1
                if self.moves == 18:
                    self.moves = 0
        else:
            if self.right:
                screen.blit(move_right[0], (self.x, self.y))
            else:
                screen.blit(move_left[0], (self.x, self.y))
        self.hitbox = (self.x + 20, self.y + 10, self.width - 40, self.height - 10)

    def hit(self):
        self.x = self.start_x
        self.y = self.start_y
        self.isJumping = True
        self.speed = 10
        self.moves = 0
        font = pygame.font.SysFont("comicsans", 30)
        if score < 10:
            text = font.render("Game Over",f'your score {score}', 1, RED)
            screen.blit(text, (200, 200))
            pygame.display.update()
            pygame.time.delay(2000)
            
            quit()
        


        i = 0
        while i < 150:
            i += 1
            pygame.time.delay(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()


class Bullet:
    def __init__(self, x, y, radius, color, direction, step):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.step = step * direction

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,(self.x, self.y) ,self.radius)

class Enemy:
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.start = x
        self.step = 5
        self.moves = 0
        self.hitbox = (self.x + 20, self.y, self.width - 30, self.height)
        self.health = 10
        self.visible = True

    def draw(self, screen):
        if self.visible:
            self.move()
            if self.step < 0:
                screen.blit(move_leftE[self.moves // 2], (self.x, self.y))
                self.moves += 1
                if self.moves == 11 * 2:
                    self.moves = 0
            else:
                screen.blit(move_rightE[self.moves // 2], (self.x, self.y))
                self.moves += 1
                if self.moves == 11 * 2:
                    self.moves = 0

            pygame.draw.rect(screen, RED, (self.hitbox[0], self.hitbox[1] - 15, 50, 10))
            pygame.draw.rect(screen, GREEN, (self.hitbox[0], self.hitbox[1] - 15, self.health * 5, 10))

    def move(self):
        if self.step > 0:
            if self.x + self.step > self.end:
                self.step *= -1
            else:
                self.x += self.step
        else:
            if self.x - self.step < self.start:
                self.step *= -1
            else:
                self.x += self.step

        self.hitbox = (self.x +20, self.y , self.width - 30, self.height)
        #pygame.draw.rect(screen, RED, self.hitbox, 2)
    def hit(self):
        hitSound.play()
        self.health -= 1
        if self.health == 0:
            self.visible = False
            self.hitbox = (0, 0, 0, 0)



class Enemy2:
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.start = x
        self.step = 8
        self.moves = 0
        self.hitbox = (self.x + 20, self.y, self.width - 30, self.height)
        self.bar = 16 
        self.visible = False

    def draw(self, screen):
        if self.visible:
            self.move()
            if self.step < 0:
                screen.blit(move_leftE[self.moves // 2], (self.x, self.y))
                self.moves += 1
                if self.moves == 11 * 2:
                    self.moves = 0
            else:
                screen.blit(move_rightE[self.moves // 2], (self.x, self.y))
                self.moves += 1
                if self.moves == 11 * 2:
                    self.moves = 0

            pygame.draw.rect(screen, RED, (self.hitbox[0], self.hitbox[1] - 15, 50, 10))
            pygame.draw.rect(screen, GREEN, (self.hitbox[0], self.hitbox[1] - 15, self.bar * 5, 10))

            # pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 15, 100, 1))
            # pygame.draw.rect(screen, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 15,  self.bar * 5, 10))
        if self.bar ==0:
            self.visible=False


    def move(self):
        if self.step > 0:
            if self.x + self.step > self.end:
                self.step *= -1
            else:
                self.x += self.step
        else:
            if self.x - self.step < self.start:
                self.step *= -1
            else:
                self.x += self.step

        self.hitbox = (self.x +20, self.y , self.width - 30, self.height)
        #pygame.draw.rect(screen, RED, self.hitbox, 2)
    def hit(self):
        hitSound.play()
        self.bar -= 1
        if self.bar == 0:
            self.visible = False
            self.hitbox = (0, 0, 0, 0)
        # else:
        #     if enemy2.hitbox[0] < bullet.x < enemy2.hitbox[0] + enemy2.hitbox[2]:
        #         if enemy2.hitbox[1] < bullet.y < enemy2.hitbox[1] + enemy2.hitbox[3]:
        #             bullets.remove(bullet)
        #             enemy2.hit()
        #             score += 1
        #             enemy2.bar -=1


man = Player(600, 400, 64, 64)
enemy  = Enemy(000, 400, 64, 64, 550)
enemy2 = Enemy2(000, 300, 64, 64, 650)
enemy2.visible = False
font = pygame.font.SysFont("comicsans", 35, True)
############################  text
textFont =pygame.font.Font('font/Pixeltype.ttf',50)
################## introScreen
avatarStand = pygame.image.load('hero/standing.png').convert_alpha()
avatarStandScaled = pygame.transform.rotozoom(avatarStand,0,2)
avatarStandRect = avatarStand.get_rect(center =(300,200))

gameMessage = textFont.render('Press Space to run',False,(0,0,255))
gameMessageRect =gameMessage.get_rect(center =(350,375))
def redrawGame():
    global moves

    text = font.render("Score = " + str(score), True, BLACK)
    text2 = font.render("healt 1 = " + str(enemy.health), True, BLACK)
    text3 = font.render("healt 2 = " + str(enemy2.bar), True, BLACK)


    screen.blit(bg, (0, 0))
    screen.blit(text, (500, 50))
    screen.blit(text2, (500, 100))
    screen.blit(text3, (500, 150))

    enemy.draw(screen)
    enemy2.draw(screen)
    
    man.draw(screen)

    # avatarName = textFont.render(f'00your score {score}',1, (0,0,255))
    # avatarNameRect = avatarName.get_rect(center = (350,130))
    for bullet in  bullets:
        bullet.draw(screen)

bullets = []
while True:
    
    clock.tick(30)

    x_mid = (man.hitbox[0] + man.hitbox[0] + man.hitbox[2]) // 2
    y_mid = (man.hitbox[1] + man.hitbox[1] + man.hitbox[3]) // 2
    if enemy.hitbox[0] < x_mid < enemy.hitbox[0] + enemy.hitbox[2]:
            if enemy.hitbox[1] < y_mid < enemy.hitbox[1] + enemy.hitbox[3]:
                score -= 5
                man.hit()
    if enemy2.hitbox[0] < x_mid < enemy2.hitbox[0] + enemy2.hitbox[2]:
        if enemy2.hitbox[1] < y_mid < enemy2.hitbox[1] + enemy2.hitbox[3]:
            score -= 5
            man.hit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            
        if gameActive:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if len(bullets) < 5:
                        bulletSound.play()
                        direction = 0
                        if man.right:
                            direction = 1
                        else:
                            direction = -1
                        bullets.append(
                            Bullet(round(man.x + man.width // 2), round(man.y + man.height // 2), 5, RED, direction, 10))
        else:
            if  event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    gameActive=True 
                    man.left =800
                    startTime = int(pygame.time.get_ticks() / 1000)
    keys = pygame.key.get_pressed()

    for bullet in bullets:
        if enemy.hitbox[0] < bullet.x < enemy.hitbox[0] + enemy.hitbox[2] :
            if enemy.hitbox[1] < bullet.y < enemy.hitbox[1] + enemy.hitbox[3] :
                bullets.remove(bullet)
                enemy.hit()
                score += 1
                
        if   enemy2.hitbox[0] < bullet.x < enemy2.hitbox[0] + enemy2.hitbox[2]:
            if enemy2.hitbox[1] < bullet.y < enemy2.hitbox[1] + enemy2.hitbox[3]:
                bullets.remove(bullet)
                enemy2.hit()
                score += 1
                enemy2.bar -=1




        if bullet.x < screenWidth and bullet.x > 0:
            bullet.x += bullet.step
        else:
            bullets.remove(bullet)




    if gameActive:
        if keys[pygame.K_LEFT] and man.x - man.step >= 0:
            man.x -= man.step
            man.left = True
            man.right = False
            man.standing = False
        elif keys[pygame.K_RIGHT] and man.x + man.width + man.step <= screenWidth:
            man.x += man.step
            man.right = True
            man.left = False
            man.standing = False
        else:
            man.standing = True
            man.moves = 0
        if not man.isJumping:
            if keys[pygame.K_SPACE]:
                man.isJumping = True
        else:
            if man.speed >= -10 :
                neg = 1
                if man.speed < 0:
                    neg = -1
                man.y -= (man.speed ** 2) * 0.25 * neg
                man.speed -= 1
            else:
                man.speed = 10
                man.isJumping = False
    redrawGame()
    
    if score ==10:
        gameActive=False
    if gameActive ==False:
            
            avatarName = textFont.render("ready",1, (0,0,255))
            avatarNameRect = avatarName.get_rect(center = (350,130))
            screen.fill((0,255,127))
            
            screen.blit(avatarStandScaled,avatarStandRect)
            screen.blit(avatarName,avatarNameRect)
            screen.blit(gameMessage,gameMessageRect)
    
    if gameActive ==False and score ==10:
            avatarName = textFont.render(f'your score {score}',1, (0,0,255))
            avatarNameRect = avatarName.get_rect(center = (350,130))
            screen.fill((0,255,127))
            screen.blit(avatarStandScaled,avatarStandRect)
            screen.blit(avatarName,avatarNameRect)
            gameMessage = textFont.render("you are win",1, (0,0,255))
            gameMessageRect =gameMessage.get_rect(center =(350,400))
            screen.blit(gameMessage,gameMessageRect)
            score=11
            enemy2.visible=True
            enemy.visible=True
            enemy.health = 10
            enemy2.bar=15
             
    if enemy.visible == False and enemy2.visible == False :
        score=30
    if score==30:
        enemy.visible == False 
        enemy2.visible == False
        avatarName = textFont.render(f'your score {score}',1, (0,0,255))
        avatarNameRect = avatarName.get_rect(center = (350,130))
        screen.fill((0,255,127))
        screen.blit(avatarStandScaled,avatarStandRect)
        screen.blit(avatarName,avatarNameRect)
        gameMessage = textFont.render("you are win and finish this game",1, (0,0,255))
        gameMessageRect =gameMessage.get_rect(center =(350,400))
        screen.blit(gameMessage,gameMessageRect)
        pygame.time.delay(100)
        
        
            
        # score=0
        # enemy2.visible=False
        # enemy.visible=True
        # enemy.health = 10
        # score=0
    
    pygame.display.update()
    
    