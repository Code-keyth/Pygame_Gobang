import pygame
import sys,time,random,numpy
IMG_PATH='img/'
GREEN=(0,255,0)
class main:
    def __init__(self):
        self.size=[966,966]
        self.img_path=IMG_PATH+'qipan.jpg'
        self.unit=51.2
        self.state=0
        self.qipan_states=[]
        self.coordinate=[0,0]
        self.value=0
        self.white = pygame.image.load(IMG_PATH+'white.png')
        self.black = pygame.image.load(IMG_PATH+'black.png')
        self.victory = pygame.image.load(IMG_PATH+'victory.jpg')
        self.screen = pygame.display.set_mode(self.size)
        self.image=pygame.image.load(self.img_path)
        self.points = []

    def start(self):
        pygame.display.init()
        self.qipan_states=numpy.array([[0]*19]*19)
        self.screen.blit(self.image,[0,0])
        self.state=1
        self.points = []

    def getEent(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if self.state == 1:
                        e_pos=event.pos
                        self.coordinate[0] = int(e_pos[0]/self.unit)
                        self.coordinate[1] = int(e_pos[1]/self.unit)
                        if self.qipan_states[self.coordinate[1]][self.coordinate[0]] == 0:
                            if event.button == 1 and self.value != 1:
                                self.value = event.button
                                self.qipan_states[self.coordinate[1]][self.coordinate[0]]=1
                                self.screen.blit(self.white,[self.coordinate[0]*self.unit,self.coordinate[1]*self.unit])
                                self.state=self.check()
                                
                            if event.button == 3 and self.value != 3:
                                self.value = event.button
                                self.qipan_states[self.coordinate[1]][self.coordinate[0]]=3
                                self.screen.blit(self.black,[self.coordinate[0]*self.unit,self.coordinate[1]*self.unit])
                                self.state=self.check()
                            
                        if self.state == 0:
                            pygame.draw.lines(self.screen, GREEN, 0, self.points, 5)
                            tips_title = 'White Victory!' if (self.value ==1) else'Black Victory!'
                            self.draw_text(tips_title,(370,100))
                    else:
                        if event.button == 2:
                            self.start()

                pygame.display.flip()
    def draw_text(self, content,postion):
        pygame.font.init()
        font = pygame.font.SysFont('kaiti', 40)
        text = font.render(content, True, GREEN)
        self.screen.blit(text, postion)
        
    def check(self):
        #X axis
        X_axis=self.qipan_states[self.coordinate[1]]
        if self.straight_line(X_axis,self.coordinate[0]) == 0:
            return 0
        #Y axis
        Y_axis=self.qipan_states[:,self.coordinate[0]]
        if self.straight_line(Y_axis,self.coordinate[1]) == 0:
            return 0
            
        #Diagonal line
        if self.Diagonal() == 0:
            return 0
        #Backslash
        if self.Backslash() == 0:
            return 0
        
        return 1

    def Diagonal(self):
        continuity=0
        self.points=[]
        for i in range(0,5):
            if self.coordinate[0]+i>18 or self.coordinate[1]+i>18:
                break
            elif self.qipan_states[self.coordinate[1]+i][self.coordinate[0]+i] == self.value:
                self.points.append(((self.coordinate[0]+i)*self.unit+22,(self.coordinate[1]+i)*self.unit+22))
                continuity+=1
            else:
                break;
        for i in range(-1,-5,-1):
            if self.coordinate[0]+i<0 or self.coordinate[1]+i<0:
                break;
            elif self.qipan_states[self.coordinate[1]+i][self.coordinate[0]+i] == self.value:
                self.points.append(((self.coordinate[0]+i)*self.unit+22,(self.coordinate[1]+i)*self.unit+22))
                continuity+=1
            else:
                break
        return 0 if(continuity == 5) else 1
            
    def Backslash(self):
        continuity=0
        for i in range(0,5):
            if self.coordinate[0]+i>18 or self.coordinate[1]-i<0:
                break;
            elif self.qipan_states[self.coordinate[1]-i][self.coordinate[0]+i] == self.value:
                self.points.append(((self.coordinate[0]+i)*self.unit+22,(self.coordinate[1]-i)*self.unit+22))
                continuity+=1
            else:
                break;
        for i in range(-1,-5,-1):
            if self.coordinate[1]-i>18 or self.coordinate[0]+i<0:
                break;
            elif self.qipan_states[self.coordinate[1]-i][self.coordinate[0]+i] == self.value:
                self.points.append(((self.coordinate[0]+i)*self.unit+22,(self.coordinate[1]-i)*self.unit+22))
                continuity+=1
            else:
                break;
        return 0 if(continuity == 5) else 1
        
    def straight_line(self,axis,current):
        continuity=0
        self.points=[]
        for x in range(current,current+5):
            if x>18:
                break;
            elif axis[x] == self.value:
                self.points.append([x*self.unit+22,self.coordinate[1]*self.unit+22])
                continuity+=1
            else:
                break;
        for x in range(current-1,current-5,-1):
            
            if x<0:
                break;
            elif axis[x] == self.value:
                self.points.insert(0,[x*self.unit+10,self.coordinate[1]*self.unit+22])
                continuity+=1
            else:
                break;
            
        return 0 if(continuity == 5) else 1

if __name__ == '__main__':

    Game = main()
    Game.start()
    while True:
        Game.getEent()