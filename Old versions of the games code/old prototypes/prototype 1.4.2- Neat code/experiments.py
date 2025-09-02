def main(level): #note i added the level parameter that you have to pass in
    if level == "level1":
        p = Platformer('Adventure Time!', 'map1.tmx', 600, 600, 30)
    else:
        p = Platformer('Adventure Time!', 'map2.tmx', 600, 600, 30)
    p.main_loop()


def handleCollisionWith(self, name, other):
    if other.kind == 'door':
        level = 'level2'
        Class_name.main(level) #you have to call main() with reference to the class it is in
