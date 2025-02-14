from tdblib import myfunctions
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
import time
import math
from fractions import Fraction

WIDTH = 960
HEIGHT = 540
inputKeys = []
num = 0
window = myfunctions.pygameSetup(WIDTH, HEIGHT)
pygame.display.set_caption("Trig")
unitCircleScreen = False
sinGraphsScreen = False
startMenuScreen = True
sin = True
cos = False
amp = 1
ampKeys = []

angle = Slider(window, WIDTH/2 - 50, 40, 100, 10, colour=(255, 255, 255), handleColour=(0,255,0), min=0, max=360, initial=0, step=1)
font = pygame.font.SysFont("timesnewroman", 30)
axisFont = pygame.font.SysFont("timesnewroman", 17)
titleFont = pygame.font.SysFont("timesnewroman", 50)

def getCoordinate(theta: float):
    x = math.cos(theta)
    y = math.sin(theta)
    if abs(x) < 0.000000000001:
        x = 0
    if abs(y) < 0.000000000001:
        y = 0
    return x, y

def sinWave(x, amp):
     y = -amp*math.sin((x - WIDTH/2) * (math.pi / 180))
     return y

def cosWave(x, amp):
     y = -amp*math.cos((x - WIDTH/2) * (math.pi / 180))
     return y

def getRootFrac(theta: float):
    x = Fraction(math.cos(theta * (math.pi / 180))).limit_denominator(10)
    y = Fraction(math.sin(theta * (math.pi / 180))).limit_denominator(10)
    if abs(x) < 0.000000000001:
        x = 0
    if abs(y) < 0.000000000001:
        y = 0
    if theta % 30 == 0 and theta != 0 and theta % 90 != 0:
        if theta > 90 and theta < 270:
            x = "-\u221A" + "3" + "/" + "2"
        else:
            x = "\u221A" + "3" + "/" + "2"
        if theta > 180:
            y = "-1/2"
        else:
            y = "1/2"
    if theta % 45 == 0 and theta != 0 and theta % 90 != 0:
        if theta > 90 and theta < 270:
            x = "-\u221A" + "2" + "/" + "2"
        else:
            x = "\u221A" + "2" + "/" + "2"
        if theta > 180:
            y = "-\u221A" + "2" + "/" + "2"
        else:
            y = "\u221A" + "2" + "/" + "2"
    if theta % 60 == 0 and theta != 0 and theta % 90 != 0:
        if theta > 90 and theta < 270:
            x = "-1/2"
        else:
            x = "1/2"
        if theta > 180:
            y = "-\u221A" + "3" + "/" + "2"
        else:
            y = "\u221A" + "3" + "/" + "2"
    return x, y

def unitCircle(unitCircleScreen):
    while unitCircleScreen:
        global inputKeys
        global num
        global angle
        angle.show()
            
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                unitCircleScreen = False
                quit()
            if event.type == pygame.KEYDOWN:
                        if event.key != pygame.K_RETURN and event.key != pygame.K_ESCAPE:
                            try:
                                inputKeys.append(int(pygame.key.name(event.key)))
                            except:
                                pass
                            print(inputKeys)
                        elif event.key == pygame.K_RETURN:
                            print(inputKeys)
                            for i in range(len(inputKeys)):
                                num = (num * 10) + inputKeys[i]
                            if num > 360:
                                num = 0
                            angle.setValue(int(num))
                            print(num)
                            inputKeys = []
                            num = 0
                            print(inputKeys)
                        if event.key == pygame.K_ESCAPE:
                            unitCircleScreen = False
                            startMenuScreen = True
                            startMenu(startMenuScreen)

        window.fill((0, 0, 0))

        pygame.draw.line(window, (255, 255, 255), (WIDTH/2 - 200, HEIGHT/2), (WIDTH/2 + 200, HEIGHT/2))
        pygame.draw.line(window, (255,255,255), (WIDTH/2, HEIGHT/2 - 200), (WIDTH/2, HEIGHT/2 + 200))
        
        #Angle Text
        angleMeasure = str(angle.getValue())
        angleRadian = float(angle.getValue()*(math.pi/180))
        angleText = font.render(angleMeasure + "\u00B0" + " / " + str(Fraction(angleRadian / math.pi).limit_denominator(10)) + "\u03C0", True, (255, 255, 255))
        angleRect = angleText.get_rect()
        angleRect.center = (WIDTH/2, 20)
        window.blit(angleText, angleRect)

        x, y = getCoordinate(angleRadian)

        #Coordinate Text
        xFrac, yFrac = getRootFrac(int(angleMeasure))
        coordinateText = font.render("(" + str(xFrac) + "," + str(yFrac) + ")", True, (255,255,255))
        coordinateRect = coordinateText.get_rect()
        coordinateRect.center = (WIDTH/2, 520)
        window.blit(coordinateText, coordinateRect)

        pygame.draw.line(window, (255, 0, 0), (WIDTH/2, HEIGHT/2), (x*200 + WIDTH/2, -y*200 + HEIGHT/2), 2)
        pygame.draw.circle(window, (255, 255, 255), (WIDTH/2, HEIGHT/2), 200, 2)
        
        pygame_widgets.update(events)
        pygame.display.update()
        time.sleep(0.0166)

def sinGraphs(sinGraphsScreen):
    while sinGraphsScreen:
        global angle
        global cos
        global sin
        global amp
        global ampKeys
        global num
        angle.hide()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sinGraphs = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if sin == True:
                        sin = False
                        cos = True
                        amp = 1
                    elif cos == True:
                        amp = 1
                        cos = False
                        sin = True
                        sinGraphsScreen = False
                        startMenuScreen = True
                        startMenu(startMenuScreen)
                if event.key != pygame.K_RETURN and event.key != pygame.K_ESCAPE:
                    try:
                        ampKeys.append(str(pygame.key.name(event.key)))
                        print(ampKeys)
                    except:
                        pass
                if event.key == pygame.K_RETURN:
                    tempamp = str(''.join(map(str, ampKeys)))
                    try:
                        amp = float(''.join(c for c in tempamp if (c.isdigit() or c ==".")))
                    except:
                        ampKeys = []
                    ampKeys = []
                    print(amp)

        window.fill((0,0,0))

        #Graph Lines
        pygame.draw.line(window, (255,255,255), (0, HEIGHT/2), (WIDTH, HEIGHT/2))
        pygame.draw.line(window, (255,255,255), (WIDTH/2, 0), (WIDTH/2, HEIGHT))
        for i in range(1,6):
            pygame.draw.line(window, (255,255,255), (WIDTH/2 - 20, ((HEIGHT/2) + i*67.5)), (WIDTH/2 + 20, ((HEIGHT/2) + i*67.5)))
            pygame.draw.line(window, (255,255,255), (WIDTH/2 - 20, ((HEIGHT/2) - i*67.5)), (WIDTH/2 + 20, ((HEIGHT/2) - i*67.5)))
            pygame.draw.line(window, (255,255,255), ((WIDTH/2) + 90*i, (HEIGHT/2) - 20), ((WIDTH/2) + 90*i, (HEIGHT/2) + 20))
            pygame.draw.line(window, (255,255,255), ((WIDTH/2) - 90*i, (HEIGHT/2) - 20), ((WIDTH/2) - 90*i, (HEIGHT/2) + 20))

        #Graph Key
        #y-axis
        for i in range(1,5):
            if i != 4 and i != 5:
                yAxisText = axisFont.render(str(Fraction(i/2).limit_denominator(2)), True, (255,255,255))
                yAxisTextRect = yAxisText.get_rect()
                yAxisTextRect.center = (WIDTH/2 - 40,HEIGHT/2 - i*67.5)
                window.blit(yAxisText, yAxisTextRect)
            if i == 4:
                yAxisText = axisFont.render(str(Fraction(i/2).limit_denominator(2)), True, (255,255,255))
                yAxisTextRect = yAxisText.get_rect()
                yAxisTextRect.center = (WIDTH/2 - 40,HEIGHT/2 - i*67.5 + 6)
                window.blit(yAxisText, yAxisTextRect)
            if i != 4 and i != 5:
                yAxisText = axisFont.render("-" + str(Fraction(i/2).limit_denominator(2)), True, (255,255,255))
                yAxisTextRect = yAxisText.get_rect()
                yAxisTextRect.center = (WIDTH/2 - 40,HEIGHT/2 + i*67.5)
                window.blit(yAxisText, yAxisTextRect)
            if i == 4:
                yAxisText = axisFont.render("-" + str(Fraction(i/2).limit_denominator(2)), True, (255,255,255))
                yAxisTextRect = yAxisText.get_rect()
                yAxisTextRect.center = (WIDTH/2 - 40,HEIGHT/2 + i*67.5 + 6)
                window.blit(yAxisText, yAxisTextRect)
        
        #x-axis
        for i in range(1,6):
            if i != 6:
                xAxisText = axisFont.render(str(Fraction(i/2).limit_denominator(2)) + "\u03C0", True, (255,255,255))
                xAxisTextRect = xAxisText.get_rect()
                xAxisTextRect.center = (WIDTH/2 + 90*i,HEIGHT/2 + 30)
                window.blit(xAxisText, xAxisTextRect)
                xAxisText = axisFont.render("-" + str(Fraction(i/2).limit_denominator(2)) + "\u03C0", True, (255,255,255))
                xAxisTextRect = xAxisText.get_rect()
                xAxisTextRect.center = (WIDTH/2 - 90*i,HEIGHT/2 + 30)
                window.blit(xAxisText, xAxisTextRect)
            
        #mouseover line
        mousex, mousey = pygame.mouse.get_pos()
        pygame.draw.line(window, (0,0,255), (mousex, 0), (mousex, HEIGHT))
        if sin:
            mouseoverText = axisFont.render("(" + str(Fraction((mousex / 180) - WIDTH/360).limit_denominator(10)) + "\u03C0" + ", " + str((((round(-sinWave(mousex, amp), 3))))) + ")", True, (255,0,0))
        if cos:
            mouseoverText = axisFont.render("(" + str(Fraction((mousex / 180) - WIDTH/360).limit_denominator(10)) + "\u03C0" + ", " + str((((round(-cosWave(mousex, amp), 3))))) + ")", True, (255,0,0))
        mouseoverRect = mouseoverText.get_rect()
        if mousex > 150:
            mouseoverRect.center = (mousex - 75, 50)
        else:
            mouseoverRect.center = (mousex + 75, 50)
        window.blit(mouseoverText, mouseoverRect)

        #Sinusoidal Waves
        if sin:
            for x in range (0, WIDTH):
                pygame.draw.line(window, (255,255,255), (x, (HEIGHT/2 + ((sinWave(x, amp))* HEIGHT/4))), (x, (HEIGHT/2 + ((sinWave(x+2, amp) * HEIGHT/4)))))
        if cos:
            for x in range (0, WIDTH):
                pygame.draw.line(window, (255,255,255), (x, (HEIGHT/2 + ((cosWave(x, amp))* HEIGHT/4))), (x, (HEIGHT/2 + ((cosWave(x+2, amp) * HEIGHT/4)))))            
                    
        pygame_widgets.update(events)
        pygame.display.update()
        time.sleep(0.0166)

def startMenu(startMenuScreen):

    global angle
    unitCircleScreen = False
    sinGraphsScreen = False
    startMenuScreen = True
    angle.hide()
    window.fill((0,0,0))

    while startMenuScreen:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                if event.key == pygame.K_u:
                    startMenuScreen = False
                    unitCircleScreen = True
                if event.key == pygame.K_s:
                    startMenuScreen = False
                    sinGraphsScreen = True
        
        title = titleFont.render("Trigonometry", True, (255,255,255))
        titleRect = title.get_rect()
        titleRect.center = (WIDTH/2, 100)
        window.blit(title, titleRect)
        unitText = font.render("Press 'u' for the Unit Circle", True, (255,255,255))
        unitRect = unitText.get_rect()
        unitRect.center = (WIDTH/2 - 250, 250)
        window.blit(unitText, unitRect)
        sinText = font.render("Press 's' for sin functions", True, (255,255,255))
        sinRect = sinText.get_rect()
        sinRect.center = (WIDTH/2 + 250, 250)
        window.blit(sinText, sinRect)
        pygame.display.update()

    
    if unitCircleScreen == True:
        unitCircle(unitCircleScreen)
    if sinGraphsScreen == True:
        sinGraphs(sinGraphsScreen)

startMenu(startMenuScreen=True)