#!/usr/bin/env python3

"""
* Copyright (c) 2015 BEEVC - Electronic Systems This file is part of BEESOFT
* software: you can redistribute it and/or modify it under the terms of the GNU
* General Public License as published by the Free Software Foundation, either
* version 3 of the License, or (at your option) any later version. BEESOFT is
* distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
* without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
* PARTICULAR PURPOSE. See the GNU General Public License for more details. You
* should have received a copy of the GNU General Public License along with
* BEESOFT. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Marcos Gomes"
__license__ = "MIT"

from time import time

from Loaders import *
import FileFinder
import pygame

class FilamentChangeScreen():
    
    """
    BEEConnect vars
    """
    beeCon = None
    beeCmd = None
    
    ff = None
    exit = False
    interfaceState = 0
    
    lblTopText = None           #list for top label text
    lblTop = None               #Top label object
    lblTopFont = None           #Top label font
    lblTopFontColor = None      #top label color
    
    buttons = None              #list for interface buttons
    
    image = None                #image object for heating screen
    
    targetTemperature = 210
    nozzleTemperature = 0
    pullInterval = 5         #pull interval for simulation mode
    nextPullTime = None
    
    firstNextReady = False      #true when target temperature is established
    
    pickColorRect = None        #Rect for selected color
    colorCodes = None
    colorNameList = None
    colorCodeList = None
    colorList = None
    listPosition = 0
    selectedColoridx = 0
    
    selectedColorFont = None
    selectedColorFontColor = None
    
    selectedColorCode = None
    selectedColorName = None
    
    """
    Progress Bar vars
    """
    progressBar = None
    pBarRect = None
    pBarFill = None
    
    exitNeedsHoming = True
    exitCallBackResp = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader, con):
        
        print("Loading Filament Change Screen Components")
        
        if(con is None):
            self.beeCmd = None
            self.beeCon = None
        else:
            self.beeCon = con
            self.beeCmd = self.beeCon.getCommandIntf()
        
        self.firstNextReady = False
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        self.interfaceState = 0         #reset interface state
        
        """
        Load lists and settings from interfaceLoader
        """
        self.lblTopFont = self.interfaceLoader.GetlblFont(self.interfaceState)
        self.lblTopFontColor = self.interfaceLoader.GetlblFontColor(self.interfaceState)
        self.lblTopText = self.interfaceLoader.GetlblText(self.interfaceState)
        self.buttons = self.interfaceLoader.GetButtonsList(self.interfaceState)
        
        self.progressBar = self.interfaceLoader.GetProgessBar()
        self.image = pygame.image.load(self.interfaceLoader.GetImagePath())
        self.selectedColorFont = self.interfaceLoader.GetSelectedLblFont()
        self.selectedColorFontColor = self.interfaceLoader.GetSelectedLblFontColor()
        
        """
        Load Colors
        """
        self.colorCodes = ColorCodesLoader.ColorCodes()
        self.colorNameList = self.colorCodes.GetColorNameList()
        self.colorCodeList = self.colorCodes.GetColorCodeList()
        self.colorList = self.colorCodes.GetColorList()
        
        #Get Nozzle Temeprature
        self.nozzleTemperature = self.beeCmd.getNozzleTemperature()
        print("Current Nozzle Temperature: ", self.nozzleTemperature)
        
        #Heat Nozzle
        #self.beeCmd.setNozzleTemperature(self.targetTemperature)
        
        #Go to Heat Position
        self.ShowMovingScreen()
        self.beeCmd.startHeating(self.targetTemperature + 5)
        
        #Get current color code
        self.selectedColorCode = self.beeCmd.getFilamentString()
        print("Current Color Code: ", self.selectedColorCode)
        self.selectedColorName = self.colorCodes.GetColorName(self.selectedColorCode)
        print("Current Color Name: ", self.selectedColorName)
        
        self.nextPullTime = time() + self.pullInterval
        
        return
        

    """*************************************************************************
                                handle_events Method 
    
    Received the event vector and checks if it has any event from interface items
    *************************************************************************"""
    def handle_events(self,retVal):
        """handle all events."""
        for event in retVal:
            
            if event.type == pygame.MOUSEBUTTONDOWN:
            	self.GetSelectedIdx(event)
                
            for btn in self.buttons:
                if 'click' in btn.handleEvent(event):
                    btnName = btn._propGetName()
                    
                    if btnName == "Next":
                        if self.interfaceState == 0:
                            self.interfaceState = 1
                            self.ShowMovingScreen()
                            self.beeCmd.goToLoadUnloadPos()
                        elif self.interfaceState == 2:
                            self.interfaceState = 1
                            #Get selected list index
                            self.selectedColoridx = (2+self.listPosition) % len(self.colorList)
                            #Get selected color code
                            self.selectedColorCode = self.colorCodeList[self.selectedColoridx]
                            self.beeCmd.setFilamentString(self.selectedColorCode)
                            #Get selected color name
                            self.selectedColorName = self.colorCodes.GetColorName(self.selectedColorCode)
                            print("Selected Filament Code: ", self.selectedColorCode)
                    elif btnName == "OK":
                        if self.interfaceState == 1:
                            if(self.selectedColorName == "Unknown"):
                                self.interfaceState = 3
                            else:
                                self.ShowWaitScreen()
                                self.exitCallBackResp = "Restart"
                    elif btnName == "Pick Color":
                        self.interfaceState = self.interfaceState + 1
                    elif btnName == "Load":
                        print("Load Filament")
                        self.ShowLoadScreen()
                        self.beeCmd.load()
                    elif btnName == "Unload":
                        print("Unload Filament")
                        self.ShowUnloadScreen()
                        self.beeCmd.unload()
                        self.selectedColorName = "Unknown"
                    elif btnName == "Up":
                        self.listPosition = self.listPosition - 1
                    elif btnName == "Down":
                        self.listPosition = self.listPosition + 1
                        
                    """
                    Load new buttons and labels from interfaceLoader
                    """
                    self.lblTopFont = None
                    self.lblTopFontColor = None
                    self.buttons = None
                    self.lblTopFont = self.interfaceLoader.GetlblFont(self.interfaceState)
                    self.lblTopFontColor = self.interfaceLoader.GetlblFontColor(self.interfaceState)
                    self.buttons = self.interfaceLoader.GetButtonsList(self.interfaceState)
                    self.lblTopText = self.interfaceLoader.GetlblText(self.interfaceState)
            
            pygame.event.get()
            
        return
    

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        self.lblTop = self.lblTopFont.render(self.lblTopText, 1, self.lblTopFontColor)
        
        for btn in self.buttons:
            if self.interfaceState == 0:
                if btn._propGetName() == "Next":
                    btn.visible = self.firstNextReady
                else:
                    btn.visible = True
            else:
                btn.visible = True

        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):
        
        self.screen.blit(self.lblTop, (self.interfaceLoader.GetlblTopXPos(self.interfaceState),
                                            self.interfaceLoader.GetlblTopYPos(self.interfaceState)))
        
        for btn in self.buttons:
            btn.draw(self.screen)
        
        if self.interfaceState == 0:
            # Draw Image
            x = self.interfaceLoader.GetImageX()
            y = self.interfaceLoader.GetImageY()
            self.screen.blit(self.image,(x,y))
            
            # Draw Progress Bar
            self.progressBar.DrawRect(self.screen)
            self.screen.blit(self.progressBar.GetSurface(self.nozzleTemperature,self.targetTemperature),
                                self.progressBar.GetPos())
        elif self.interfaceState == 1:
            lblCurrentColorText = "Current Color: " + self.selectedColorName
            lbl = self.selectedColorFont.render(lblCurrentColorText, 1, self.selectedColorFontColor)
            self.screen.blit(lbl, (self.interfaceLoader.GetSelectedLblX(),self.interfaceLoader.GetSelectedLblY()))
            
        elif self.interfaceState == 2:
            
            x = self.interfaceLoader.GetPickerX()
            y = self.interfaceLoader.GetPickerY()
            width = self.interfaceLoader.GetPickerWidth()
            height = self.interfaceLoader.GetPickerHeight()
            pickerColor = self.interfaceLoader.GetPickerFontColor()
            fontSize = self.interfaceLoader.GetPickerFontSize()
            pickerFont = self.interfaceLoader.GetPickerFont()
            lblOffset = int((height-fontSize)/2)
            
            for i in range(0, 5):
                pos = i + self.listPosition
                
                idx = pos % len(self.colorList)   
                
                colorSurf = pygame.Surface((height*0.8,height*0.8))
                colorSurf.fill(self.colorList[idx])
                self.screen.blit(colorSurf, (x+(int(0.1*height)),y+((-2+i)*height)+(int(0.1*height))))
                
                colorLbl = None
                if i == 2:
                    colorLbl = pickerFont.render(self.colorNameList[idx], 1, pickerColor)
                else:
                    ff = FileFinder.FileFinder()
                    font = pygame.font.Font(ff.GetAbsPath("/Fonts/DejaVuSans-Light.ttf"),fontSize)
                    colorLbl = font.render(self.colorNameList[idx], 1, pickerColor)
                    
                self.screen.blit(colorLbl, (x + height +5,y+lblOffset+((-2+i)*height)))
                
                if i>0 and i<5:
                    pygame.draw.line(self.screen, pickerColor, (x, y+((-2+i)*height)),
                                (x+width, y+((-2+i)*height)), int(0.05*height))
            
            
            self.pickColorRect = pygame.draw.rect(self.screen, pickerColor, (x,y,width,height), 3)
            
        
        
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "Filament"
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        #CANCEL HEATING
        self.beeCmd.setNozzleTemperature(0)
        
        self.interfaceState = None
    
        self.lblTopText = None
        self.lblTop = None
        self.lblTopFont = None
        self.lblTopFontColor = None
    
        self.buttons = None
    
        self.image = None
    
        self.targetTemperature = None
        self.nozzleTemperature = None
        self.pullInterval = None
        self.nextPullTime = None
    
        self.firstNextReady = None
    
        self.pickColorRect = None
        self.colorCodes = None
        self.colorNameList = None
        self.colorCodeList = None
        self.colorList = None
        self.listPosition = None
        self.selectedColoridx = None
    
        self.selectedColorFont = None
        self.selectedColorFontColor = None
    
        self.progressBar = None
        self.pBarRect = None
        self.pBarFill = None
        
        return
    
    """*************************************************************************
                                ExitCallBack Method 
    
    Tells the main class to load the default interface
    *************************************************************************""" 
    def ExitCallBack(self):
        
        
        return self.exitCallBackResp
    
    """*************************************************************************
                                Pull Method 
    
    Pull variables
    *************************************************************************""" 
    def Pull(self):
        
        t = time()
        if t > self.nextPullTime:
            
            self.nozzleTemperature = self.beeCmd.getNozzleTemperature()
            
            if self.nozzleTemperature >= self.targetTemperature:
                self.nozzleTemperature = self.targetTemperature
                if(self.firstNextReady == False):
                    self.beeCmd.beep()
                
                self.firstNextReady = True
            
            self.nextPullTime = time() + self.pullInterval
        
        
        return
    
    """*************************************************************************
                                GetSelectedIdx Method 
    
    Identifies which color the user chose by clicking the list
    *************************************************************************""" 
    def GetSelectedIdx(self, event):
        
        if self.interfaceState ==2:
            pos = pygame.mouse.get_pos()
            posX = pos[0]
            posY = pos[1]
            
            width = self.interfaceLoader.GetPickerWidth()
            height = self.interfaceLoader.GetPickerHeight()
            pickerXMin = self.interfaceLoader.GetPickerX()
            pickerXMax = pickerXMin + width
            pickerYMin = self.interfaceLoader.GetPickerY() - (2 * height)
            pickerYMax = pickerYMin + (5 * height)
            
            if (posX>pickerXMin) and (posX<pickerXMax) and (posY>pickerYMin) and (posY<pickerYMax):
                relY = posY - pickerYMin
                idxChange = -2 + int(relY/height)
                self.listPosition = self.listPosition + idxChange
        
        return
    
    """*************************************************************************
                                ShowMovingScreen Method 
    
    Shows Wait Screen 
    *************************************************************************"""  
    def ShowMovingScreen(self):
        
        #Clear String
        self.screen.fill(pygame.Color(255,255,255))
        
        if(self.ff is None):
            self.ff = FileFinder.FileFinder()
        
        moovingImgPath = self.ff.GetAbsPath('/Images/moving.png')
        
        moovingImg = pygame.image.load(moovingImgPath)

        # Draw Image
        self.screen.blit(moovingImg,(0,0))
        
        # update screen
        pygame.display.update()
        
        pygame.event.get()
        
        return
    
    """*************************************************************************
                                ShowLoadScreen Method 
    
    Shows Load Screen 
    *************************************************************************"""  
    def ShowLoadScreen(self):
        
        #Clear String
        self.screen.fill(pygame.Color(255,255,255))
        
        if(self.ff is None):
            self.ff = FileFinder.FileFinder()
        
        moovingImgPath = self.ff.GetAbsPath('/Images/Load.png')
        
        moovingImg = pygame.image.load(moovingImgPath)

        # Draw Image
        self.screen.blit(moovingImg,(0,0))
        
        # update screen
        pygame.display.update()
        
        pygame.event.get()
        
        return
    
    """*************************************************************************
                                ShowUnloadScreen Method 
    
    Shows Unload Screen 
    *************************************************************************"""  
    def ShowUnloadScreen(self):
        
        #Clear String
        self.screen.fill(pygame.Color(255,255,255))
        
        if(self.ff is None):
            self.ff = FileFinder.FileFinder()
        
        moovingImgPath = self.ff.GetAbsPath('/Images/Unload.png')
        
        moovingImg = pygame.image.load(moovingImgPath)

        # Draw Image
        self.screen.blit(moovingImg,(0,0))
        
        # update screen
        pygame.display.update()
        
        pygame.event.get()
        
        return
    
    """*************************************************************************
                                ShowWaitScreen Method 
    
    Shows Loading Screen 
    *************************************************************************"""  
    def ShowWaitScreen(self):
        
        #Clear String
        self.screen.fill(pygame.Color(255,255,255))
        
        if(self.ff is None):
            self.ff = FileFinder.FileFinder()
        
        moovingImgPath = self.ff.GetAbsPath('/Images/please_wait.png')
        
        moovingImg = pygame.image.load(moovingImgPath)

        # Draw Image
        self.screen.blit(moovingImg,(0,0))
        
        # update screen
        pygame.display.update()
        
        pygame.event.get()
        
        return