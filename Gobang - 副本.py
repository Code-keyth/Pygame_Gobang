
import pygame
import sys,time,random,numpy

IMG_PATH='img/'     # 静态资源路径

GREEN=(0,255,0)     # 绿色
class main:
    # 初始化类 加载必要参数
    def __init__(self):
        self.size = [966,966]       # 棋盘大小
        self.unit= 51.2             # 落子间距
        self.state = 1              # 游戏是否正在进行
        self.qipan_states = []      # 记录棋盘所有的点
        self.coordinate  = [0,0]    # 记录当前落子的位置
        self.value = 0              # 记录当前是黑子,还是白子（使用鼠标左右键的事件值来绑定，左键为 1[白子] 右键为3[黑子] 双击为游戏重新开始）
        
        # 加载棋盘和黑白棋子图片
        self.white = pygame.image.load(IMG_PATH+'white.png')
        self.black = pygame.image.load(IMG_PATH+'black.png')
        self.screen = pygame.display.set_mode(self.size)
        self.image=pygame.image.load(IMG_PATH + 'qipan.jpg' )
        
        self.points = []    # 记录最后的连线坐标
    
    # 初始化项目
    def start(self):
        pygame.display.init()
            
        self.qipan_states=numpy.array([[0]*19]*19)  # 填充 0 代表这个点是空的 1代表白子 3代表黑子
        self.screen.blit(self.image,[0,0])
        self.state=1
        self.points = []
    
    # 循环绑定事件
    def getEent(self):
        # 获取用户操作事件列表
        for event in pygame.event.get():
                # 检测是否退出程序
                if event.type == pygame.QUIT:
                    sys.exit()
                
                # 是否使用鼠标事件
                if event.type == pygame.MOUSEBUTTONDOWN :
                    #如果游戏
                    if self.state == 1:
                        # 获取当前鼠标点击的位置，计算落点
                        e_pos=event.pos
                        self.coordinate[0] = int(e_pos[0]/self.unit)
                        self.coordinate[1] = int(e_pos[1]/self.unit)
                        
                        # 检测这个点是否已经有棋子了
                        if self.qipan_states[self.coordinate[1]][self.coordinate[0]] == 0:
                            # 如果是白子，并且上一次是黑子落地(形成黑白交互下棋的过程)
                            if event.button == 1 and self.value != 1:
                                self.value = event.button   # 更新当前落子的状态
                                self.qipan_states[self.coordinate[1]][self.coordinate[0]]=1 # 在棋盘上记录这个点的值
                                self.screen.blit(self.white,[self.coordinate[0]*self.unit,self.coordinate[1]*self.unit])    # 在棋盘上加载这个点的图片
                                self.state=self.check() # 检测落子后对棋盘的影响(即落这个子,是否在四个方向上形成白色5子连珠)
                                
                            # 同上
                            if event.button == 3 and self.value != 3:
                                self.value = event.button
                                self.qipan_states[self.coordinate[1]][self.coordinate[0]]=3
                                self.screen.blit(self.black,[self.coordinate[0]*self.unit,self.coordinate[1]*self.unit])
                                self.state=self.check()
                        # 游戏结束,
                        if self.state == 0:
                            pygame.draw.lines(self.screen, GREEN, 0, self.points, 5)    # 绘制连线图
                            tips_title = 'White Victory!' if (self.value ==1) else'Black Victory!'
                            self.draw_text(tips_title,(370,100))    # 加载胜利提示语
 
                    # 检测双击事件，重新开始游戏
                    if event.button == 2:
                        self.start()

                pygame.display.flip()
    # 显示文字
    def draw_text(self, content,postion):
        pygame.font.init()
        font = pygame.font.SysFont('kaiti', 40)
        text = font.render(content, True, GREEN)
        self.screen.blit(text, postion)
    # 检测棋子的状态
    def check(self):
        # 在X轴上
        X_axis=self.qipan_states[self.coordinate[1]]    # 获取一行
        if self.straight_line(X_axis,self.coordinate[0]) == 0:  
            return 0
        # 在Y轴上
        Y_axis=self.qipan_states[:,self.coordinate[0]]  # 获取一列
        if self.straight_line(Y_axis,self.coordinate[1]) == 0:
            return 0
        # 正斜线
        if self.Diagonal() == 0:
            return 0
        # 反斜线
        if self.Backslash() == 0:
            return 0
        return 1

    # 在正斜线上检查是否五子相连
    def Diagonal(self):
        continuity=0
        self.points=[]
        # 检查落子处右下方向5个点是否与当前落子同颜色(包含落子)
        for i in range(0,5):
            if self.coordinate[0]+i>18 or self.coordinate[1]+i>18:
                break
            elif self.qipan_states[self.coordinate[1]+i][self.coordinate[0]+i] == self.value:
                self.points.append(((self.coordinate[0]+i)*self.unit+22,(self.coordinate[1]+i)*self.unit+22))
                continuity+=1
            else:
                break;
        # 检查落子处左上方向4个点是否与当前落子同颜色(不包含落子)
        for i in range(-1,-5,-1):
            if self.coordinate[0]+i<0 or self.coordinate[1]+i<0:
                break;
            elif self.qipan_states[self.coordinate[1]+i][self.coordinate[0]+i] == self.value:
                self.points.append(((self.coordinate[0]+i)*self.unit+22,(self.coordinate[1]+i)*self.unit+22))
                continuity+=1
            else:
                break
        return 0 if(continuity == 5) else 1
    
    # 在反斜线上检查是否五子相连
    def Backslash(self):
        continuity=0
        # 检查落子处右上方向5个点是否与当前落子同颜色(包含落子)
        for i in range(0,5):
            if self.coordinate[0]+i>18 or self.coordinate[1]-i<0:
                break;
            elif self.qipan_states[self.coordinate[1]-i][self.coordinate[0]+i] == self.value:
                self.points.append(((self.coordinate[0]+i)*self.unit+22,(self.coordinate[1]-i)*self.unit+22))
                continuity+=1
            else:
                break;
        # 检查落子处左下方向4个点是否与当前落子同颜色(不包含落子)
        for i in range(-1,-5,-1):
            if self.coordinate[1]-i>18 or self.coordinate[0]+i<0:
                break;
            elif self.qipan_states[self.coordinate[1]-i][self.coordinate[0]+i] == self.value:
                self.points.append(((self.coordinate[0]+i)*self.unit+22,(self.coordinate[1]-i)*self.unit+22))
                continuity+=1
            else:
                break;
        return 0 if(continuity == 5) else 1
    # 在垂直和水平方向上检查是否五子相连
    def straight_line(self,axis,current):
        continuity=0
        self.points=[]
        
        # 检查右侧（或下侧）5子是否五子相连(包含落子)
        for x in range(current,current+5):
            if x>18:
                break;
            elif axis[x] == self.value:
                self.points.append([x*self.unit+22,self.coordinate[1]*self.unit+22])
                continuity+=1
            else:
                break;
         # 检查左侧（或上侧）4子是否五子相连(不包含落子)
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