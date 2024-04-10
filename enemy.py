import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, animation_list, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = health
        self.last_attack = pygame.time.get_ticks()
        self.attack_cooldown = 1000 #miliseconds
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0 # 0 = walk, 1 = attack, 2 = death
        self.update_time = pygame.time.get_ticks()
        
        #select starting image
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 25, 40)
        self.rect.center = (x, y)
        
    def update(self, surface, target, bullet_group):
        
        if self.alive:
            # check bullet collision
            if pygame.sprite.spritecollide(self, bullet_group, True):
                # lower enemy helath
                self.health -= 25
            
            # enemy attack castle
            if self.rect.right > target.rect.left:
                self.update_action(1)
                
            # attack cooldown
            if self.action == 1:
                if pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:                
                    target.health -= 25
                    if target.health < 0:
                        target.health = 0
                    # print(target.health)
                    self.last_attack = pygame.time.get_ticks()
            
            # move enemy
            if self.action == 0: 
                self.rect.x += self.speed
            
            # enemy killed 
            if self.health <= 0:
                target.money += 100
                target.score += 100
                self.update_action(2)
                self.alive = False
            
        self.update_animation()
        
        # draw enemy
        # pygame.draw.rect(surface, (255, 255, 255), self.rect, 1) = for hitbox
        surface.blit(self.image, (self.rect.x - 10, self.rect.y - 15))
        
    def update_animation(self):
        ANIMATION_COOLDOWN = 50
        # update image according to action
        self.image = self.animation_list[self.action][self.frame_index]
        # check passed time
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            
        # reset animation
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else: 
                self.frame_index = 0
                
            
    def update_action(self, new_action):
        #check if action changed into new one
        if new_action != self.action:
            self.action = new_action
            
            #update animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()