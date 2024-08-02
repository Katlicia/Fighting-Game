import pygame

class Player:
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0: Idle, 1: Run, 2: Jump, 3: Attack_1, 4: Attack_2, 5:Hit, 6:Death #
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 80, 180)
        self.vel_y = 0
        self.jump = False
        self.running = False
        self.attacking = False
        self.hit = False
        self.dead = False
        self.attack_sound = sound
        self.attack_type = 0
        self.attack_cd = 0
        self.hp = 100
        
    def load_images(self, sprite_sheet, animation_steps):
        # Extract images from sheet.
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_image = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_image, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # Get key presses.
        key = pygame.key.get_pressed()
        # Can only perform actions when not attacking.
        if self.attacking == False and self.dead == False and round_over == False:
            # Check player 1 controls.
            if self.player == 1:
                # Movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                # Jump
                if key[pygame.K_w] and self.jump is False:
                    self.vel_y = -30
                    self.jump = True
                # Attack
                if key[pygame.K_c] or key[pygame.K_v]:
                    self.attack(target)
                    # Determine attack type.
                    if key[pygame.K_c]:
                        self.attack_type = 1
                    if key[pygame.K_v]:
                        self.attack_type = 2

                       # Check player 1 controls.
            if self.player == 2:
                # Movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                # Jump
                if key[pygame.K_UP] and self.jump is False:
                    self.vel_y = -30
                    self.jump = True
                # Attack
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    # Determine attack type.
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2


        # Apply gravity.
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Player stays on screen.
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            dy = screen_height - 110 - self.rect.bottom
            self.jump = False

        # Players face each other.
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # Apply attack cooldown.
        if self.attack_cd > 0:
            self.attack_cd -= 1

        # Update player position.
        self.rect.x += dx
        self.rect.y += dy

    # Handle animation updates.
    def update(self):
        # Check what action the player is performing.
        if self.hp <= 0:
            self.hp = 0
            self.dead = True
            self.update_action(6) # 6: Death
        elif self.hit == True:
            self.update_action(5) # 5: Hit
        elif self.attacking == True: 
            if self.attack_type == 2:
                self.update_action(4) # 4: Attack_2
            elif self.attack_type == 1:
                self.update_action(3) # 3: Attack_1 
        elif self.jump == True:
            self.update_action(2) # 2: Jump
        elif self.running == True:
            self.update_action(1) # 1: Run
        else:
            self.update_action(0) # 0: Idle

        animation_cd = 50
        # Update image.
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update.
        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # Check if animation has finished.
        if self.frame_index >= len(self.animation_list[self.action]):
            # If the player is dead then end the animation.
            if self.dead == True:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # Check if an attack was executed.
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cd = 20
                # Check if damage was taken.
                if self.action == 5:
                    self.hit = False
                    # If the player was in the middle of an attack, then the attack is stopped.
                    self.attacking = False
                    self.attack_cd = 20

    def attack(self, target):
        # Checking attack cooldown.
        if self.attack_cd == 0:
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.hp -= 10
                target.hit = True

    def update_action(self, new_action):
        # Check if the new animation is different from the previous one.
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))