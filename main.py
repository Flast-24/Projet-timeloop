import arcade

SCREEN_W, SCREEN_H = 800, 600
GRAVITY = 1.0
JUMP_SPEED = 20
MOVE_SPEED = 5

class MonJeu(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_W, SCREEN_H, "Jeu Temporel")
        
        # On prépare les variables
        self.player = None
        self.player_list = None  # <--- NOUVEAU : La liste pour le joueur
        self.walls = None
        self.physics = None
        self.history = [] 

    def setup(self):
        # 1. Créer les listes
        self.player_list = arcade.SpriteList()
        self.walls = arcade.SpriteList()

        # 2. Créer le joueur
        self.player = arcade.SpriteSolidColor(50, 50, arcade.color.BLUE)
        self.player.center_x = 100
        self.player.center_y = 100
        
        # 3. Ajouter le joueur à sa liste (OBLIGATOIRE maintenant)
        self.player_list.append(self.player)
        
        # 4. Créer le sol
        floor = arcade.SpriteSolidColor(800, 50, arcade.color.DARK_GREEN)
        floor.center_x = 400
        floor.center_y = 25
        self.walls.append(floor)

        # 5. Créer la plateforme haute
        plat = arcade.SpriteSolidColor(200, 30, arcade.color.DARK_GREEN)
        plat.center_x = 600
        plat.center_y = 250
        self.walls.append(plat)

        # Physique (Le joueur vs Les murs)
        self.physics = arcade.PhysicsEnginePlatformer(self.player, self.walls, GRAVITY)

    def on_draw(self):
        self.clear()
        
        # On dessine les LISTES, pas les objets seuls
        self.walls.draw()
        self.player_list.draw() # <--- CORRECTION ICI
        
        # Texte d'aide
        arcade.draw_text(f"Historique: {len(self.history)/60:.1f} sec", 10, 580, arcade.color.WHITE)
        if len(self.history) >= 300:
            arcade.draw_text("PRET POUR RETOUR (Appuie sur R)", 10, 550, arcade.color.RED)

    def on_update(self, delta_time):
        self.physics.update()
        # Enregistre la position
        self.history.append(self.player.position)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP and self.physics.can_jump():
            self.player.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVE_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVE_SPEED
            
        # FEATURE : Retour en arrière
        elif key == arcade.key.R and len(self.history) > 300:
            # Créer le clone (l'ancien toi)
            clone = arcade.SpriteSolidColor(50, 50, arcade.color.RED)
            clone.position = self.player.position
            self.walls.append(clone) # Le clone devient un mur
            
            # Téléporter le joueur 5 sec en arrière
            self.player.position = self.history[-300]
            self.history = [] 
            
            # Recharger la physique pour qu'elle prenne en compte le clone
            self.physics = arcade.PhysicsEnginePlatformer(self.player, self.walls, GRAVITY)

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player.change_x = 0

if __name__ == "__main__":
    window = MonJeu()
    window.setup()
    arcade.run()