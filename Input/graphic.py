
def BlitCenter       (Surface1,Surface2):
    Surface1.blit(Surface2,GetCenterPosition(Surface1,Surface2))
    return Surface1
def GetCenterPosition(Surface1,Surface2):
    return int(Surface1.get_size()[0]/2-Surface2.get_size()[0]/2),int(Surface1.get_size()[1]/2-Surface2.get_size()[1]/2)
def getCenter        (xA,yA,wA,wB,hA,hB):
    position_x = xA + wA / 2 - wB / 2
    position_y = yA + hA / 2 - hB / 2
    return position_x,position_y

def BlitTextCenter(Surface,Text,Font,Color):
    Rend = Font.render(Text,1,Color)
    Surf = BlitCenter(Surface,Rend)
    return Surf

class position                     :
    def __init__(self):
        self.X = 0
        self.Y = 0
    def setX    (self,X  ):
        self.X = X
    def setY    (self,Y  ):
        self.Y = Y
    def getX    (self    ):
        return self.X
    def getY    (self    ):
        return self.Y
    def sumX    (self,X  ):
        self.X += X
    def sumY    (self,Y  ):
        self.Y += Y
    def get_pos (self    ):
        return self.getX(),self.getY()
    def set_pos (self,X,Y):
        self.setX(X)
        self.setY(Y)
class dimension                    :
    def __init__(self):
        self.H = 0
        self.W = 0
    def setH    (self,H):
        self.H = H
        self.recalculate_surfaces()
    def setW    (self,W):
        self.W = W
        self.recalculate_surfaces()
    def getW(self):
        return self.W
    def getH(self):
        return self.H
    def GetDimensions(self):
        return [self.W, self.H]
    def setDimensions(self,dim):
        self.setW(dim[0])
        self.setH(dim[1])
        self.recalculate_surfaces()
class square   (position,dimension):
    def __init__(self):
        position.__init__(self)
        dimension.__init__(self)
    def focused  (self,MOUSE):
        X,Y     = MOUSE.get_position()
        if X > self.X and X < self.X + self.W:
            if Y > self.Y and Y < self.Y + self.H:
                return True
        return False
    def pressed  (self,MOUSE):
        return self.focused(MOUSE) and MOUSE.get_now_pressed()[0]
class graphic                      :
    def __init__(self):
        self.EVENTS    = None
        self.SCREEN    = None
        self.container = None
        self.STARTED   = True
    def setEventsReference    (self,EVENTS):
        self.EVENTS = EVENTS
        self.eventing(EVENTS)
    def setScreenReference    (self,SCREEN):
        self.SCREEN = SCREEN
        self.screening(SCREEN)
    def setUpRef              (self,UP    ):
        self.container = UP
    def cLogic                (self,EVENTS,MOUSE,KEYBOARD):
        pass
    def cGraphic              (self,SCREEN               ):
        pass
    def logic_update          (self       ):
        if self.STARTED:
            if self.EVENTS and self.SCREEN:
                self.cLogic(self.EVENTS,self.EVENTS.get_mouse(),self.EVENTS.get_keyboard())
    def graphic_update        (self       ):
        if self.STARTED:
            if self.SCREEN and self.EVENTS:
                self.cGraphic(self.SCREEN)
    def eventing              (self,EVENTS):
        pass
    def screening             (self,SCREEN):
        pass
    def autodelete            (self       ):
        self.container.deleteElement(self)
class container(graphic           ):
    def __init__        (self           ):
        graphic.__init__(self)
        self.elements = []
        self.selected = None
        self.real     = -1
        self.lreal    = -1
    def logic_update    (self           ):
        graphic.logic_update(self)

        if self.EVENTS.get_mouse().get_now_pressed()[0]:
            self.updateAct  ()
        self.updateFoc()

        for x in range(len(self.elements)):
            #print self.elements[x].EVENTS
            if x >= len(self.elements):
                break
            self.elements[x].logic_update()

    def graphic_update  (self           ):
        graphic.graphic_update(self)
        for x in range(len(self.elements)):
            self.elements[x].graphic_update()
    def takeToTop       (self,element   ):
        for x in range(len(self.elements)):
            if self.elements[x] == element:
                self.elements.append( element )
                del self.elements[x]
                return 0
    def addElement      (self,element   ):
        element.setScreenReference(self.SCREEN)
        element.setUpRef          (self)
        self.elements.append(element)
    def updateAct       (self           ):
        valor = -1

        for x in range(len(self.elements)):
            element = self.elements[x]
            if element.pressed(self.EVENTS.get_mouse()):
                valor = x
        if valor != -1:
            self.takeToTop( self.elements[valor] )
    def updateFoc       (self           ):
        valor = -1
        for x in range(len(self.elements)):
            if self.elements[x].focused(self.EVENTS.get_mouse()):
                valor = x
        self.real = valor
        if self.real != self.lreal:
            for x in range(len(self.elements)):
                if x == self.real or x == len(self.elements)-1:
                    self.elements[x].setEventsReference(self.EVENTS)
                else:
                    self.elements[x].setEventsReference(None)
            self.lreal = self.real
    def deleteElement   (self,element   ):
        for x in range(len(self.elements)):
            if self.elements[x] == element:
                del self.elements[x]
                if self.selected == x:
                    self.selected = None
                return