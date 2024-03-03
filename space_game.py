import arcade
import random 


class Display(arcade.Window):
    def __init__(self, Width, Height, Title):
        
        super().__init__(Width, Height, Title)
        #arcade.set_background_color(arcade.color.AMAZON)
        self.score = 0 
        self.scaling = 0.2
        self.center_y = 560
        self.center_x = 40
        self.background = arcade.load_texture("back.png")
        self.boolean = 0 
        
        i = 1
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()
        self.laser_list_enemy = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        while(i<=5):
            
            self.enemy = arcade.Sprite("alien.png",self.scaling)
            self.enemy.center_x = self.center_x + 90 
            self.center_x = self.enemy.center_x
            self.enemy.center_y = self.center_y 
            self.enemy.change_x = 2 
            self.enemy_list.append(self.enemy)
            i = i+1 
        
        self.player_sprite = arcade.Sprite("pl.png",0.25)
        self.player_sprite.center_y = 50
        self.player_sprite.center_x = 290
        self.player_list.append(self.player_sprite)
        
        self.bam = {}
        arcade.schedule(self.outside,1)

        self.laser_sound = arcade.load_sound("EnchantedFestivalLoop.wav")
        # self.bullet_sound = arcade.load_sound("laser.wav")
        self.eplosion_sound = arcade.load_sound("eplosion01.wav")
        self.enemy_laser_sound = arcade.load_sound("enemy_laser.wav")
        
        arcade.play_sound(self.laser_sound)
        
    
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_texture_rectangle(300,300,600,600,self.background)
        arcade.draw_text("SCORE: "+ str(self.score),5,10,arcade.color.ALMOND,15,font_name = "War Priest")
        
         
        self.enemy_list.draw()
        self.player_list.draw() 
        self.laser_list.draw()
        self.bullet_list.draw()
        
        if self.score>=5 and len(self.player_list) >= 1:
            arcade.draw_text("YOU HAVE WON",25,300,arcade.color.ALMOND,60)

        if self.boolean == 1:
            arcade.draw_text("YOU HAVE LOST",25,300,arcade.color.ALMOND,60)
       
                
        for eplosion, timer in list(self.bam.items()):
            if timer > 0:
                eplosion.draw()
                self.bam[eplosion] = timer - 1
            elif timer == 0:
                del self.bam[eplosion]
         

    def on_key_press(self,key,modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.center_x = self.player_sprite.center_x - 15
            if self.player_sprite.center_x < 20:
                self.player_sprite.center_x = 20
        if key == arcade.key.RIGHT:
            self.player_sprite.center_x = self.player_sprite.center_x + 15
            if self.player_sprite.center_x > 580:
                self.player_sprite.center_x = 580
        if key == arcade.key.UP:
            laser_sprite = arcade.Sprite("laser2.png",0.9)
            laser_sprite.center_x = self.player_sprite.center_x
            laser_sprite.center_y = self.player_sprite.center_y + 40 
            self.laser_list.append(laser_sprite)  
            arcade.play_sound(self.bullet_sound)
    def update(self,delta_time):
        
        SCREEN_HEIGHT = 580
        SCREEN_width = 20 
        self.enemy_list.update()
        SPEED = 3 
        for enemy in self.enemy_list[::-1]:
            if enemy.center_x > SCREEN_HEIGHT:
                SCREEN_HEIGHT = SCREEN_HEIGHT - 100
                enemy.change_x = enemy.change_x * -1 
        for enemy in self.enemy_list:
            if enemy.center_x < SCREEN_width:
                SCREEN_width = SCREEN_width + 100 
                enemy.change_x = enemy.change_x * -1
        for enemy in self.enemy_list:
            if(enemy.center_y <=20):
                enemy.change_y = 0.7
            elif(enemy.center_y>=550):
                enemy.change_y = -0.7

        self.player_hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.enemy_list)

        if len(self.player_hit_list) > 0:
            self.boolean = 1 
            self.player_sprite.remove_from_sprite_lists() 


        for laser in self.laser_list:
            if laser.center_y < 700: 
                laser.center_y += SPEED     
            
            elif laser.center_y  >= 700:
                laser.kill()
                print(len(self.laser_list))
            hit_list = arcade.check_for_collision_with_list(laser, self.enemy_list)
           
            if len(hit_list) > 0:
                laser.remove_from_sprite_lists()
          
            for enemy in hit_list:
                eplosion = arcade.Sprite("bam.png")
                eplosion.center_x = enemy.center_x
                eplosion.center_y = enemy.center_y
                eplosion.scale = enemy.scale
                self.bam[eplosion] = 10

                enemy.remove_from_sprite_lists()
                arcade.play_sound(self.eplosion_sound)
                self.score += 1
           
        for bullet_sprite in self.bullet_list:
            if bullet_sprite.center_y <= -100: 
                bullet_sprite.kill()

        bullet_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.bullet_list)

        if len(bullet_hit_list) > 0:
            self.boolean = 1 
            bullet_sprite.remove_from_sprite_lists()
            self.player_sprite.remove_from_sprite_lists()
       
        self.bullet_list.update()
        self.laser_list.update()
        
    def outside(self,delta_time):
        if len(self.enemy_list) > 0:
            number = random.randint(0,len(self.enemy_list)-1)
            pick = self.enemy_list[number]
            bullet_sprite = arcade.Sprite("laser04.png")
            arcade.play_sound(self.enemy_laser_sound)
            bullet_sprite.center_x  = pick.center_x
            bullet_sprite.center_y = pick.center_y - 40 
            bullet_sprite.scale = 0.9
            bullet_sprite.change_y = -10 
            self.bullet_list.append(bullet_sprite)


def main():
    screen = Display(600,600,"SPACE SHOOTING GAME")
    
    arcade.run()


main()

    
