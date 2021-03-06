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

import Loaders.ColorCodesLoader
import FileFinder
import pygame
import FileFinder

class PrintScreen():
    
    screen = None
    interfaceLoader = None
    printing = None
    exit = None
    aliveTimer = 0;
    
    lblFontColor = None
    lblXPos = None
    lblYPos = None
    lblText = None
    lblFont = None
    lbl = None
    
    timeLbl = None
    timeLblFontColor = None
    timeLblXPos = None
    timeLblYPos = None
    timeLblText = None
    timeLblFont = None
    
    colorLbl = None
    colorLblFontColor = None
    colorLblXPos = None
    colorLblYPos = None
    colorLblText = None
    colorLblFont = None
    
    buttons = None
    
    interfaceState = None
    
    image = None
    imageX = None
    imageY = None
    
    timeRemaining = None
    printPercent = 0
    
    nextPullTime = None
    pullInterval = 10
    
    """
    Progress Bar vars
    """
    progressBar = None
    pBarRect = None
    pBarFill = 0
    pBarMax = 0
    
    estimatedTime = 1000
    elapsedTime = 0
    numberLines = 0
    executedLines = 0
    
    targetTemperature = 220     
    nozzleTemperature = 0
    
    """
    Color Picker vars
    """
    pickColorRect = None  # Rect for selected color
    colorCodes = None
    colorNameList = None
    colorCodeList = None
    colorList = None
    listPosition = 0
    selectedColoridx = 0
    
    """
    BEEConnect vars
    """
    # conn = None
    beeCon = None
    beeCmd = None
    ff = None
    
    exitNeedsHoming = False
    exitCallBackResp = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader, con, interfaceState=0):
        """
        .
        """
        print("loading Print Screen with interface:", interfaceState)
        
        if(con is None):
            self.beeCmd = None
            self.beeCon = None
        else:
            self.beeCon = con
            self.beeCmd = self.beeCon.getCommandIntf()
        
        self.interfaceState = interfaceState  # set interface state
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        # TODO UPDATE TIME REMAINING
        self.timeRemaining = 0
        
        self.UpdateVars()
        
        self.nextPullTime = time()
        
        """
        Load Colors
        """
        self.colorCodes = Loaders.ColorCodesLoader.ColorCodes()
        self.colorNameList = self.colorCodes.GetColorNameList()
        self.colorCodeList = self.colorCodes.GetColorCodeList()
        self.colorList = self.colorCodes.GetColorList()
        
        
        
        return

    """*************************************************************************
                                handle_events Method 
    
    Received the event vector and checks if it has any event from interface items
    *************************************************************************"""
    def handle_events(self, retVal):
        
        """handle all events."""
        for event in retVal:
            buttonEvent = False

            for btn in self.buttons:
                if 'click' in btn.handleEvent(event):
                    btnName = btn._propGetName()
                    
                    if btnName == "Cancel":
                        if(self.interfaceState == 0):
                            self.ShowWaitScreen()
                            self.beeCmd.cancelPrint()
                            self.ShowMovingScreen()
                            printerReady = False
                            delay = time()
                            while(printerReady == False):
                                if(time() > delay + 1):
                                    st = self.beeCmd.getStatus()
                                    if(st == 'Ready'):
                                        printerReady = True
                                
                        buttonEvent = True
                        self.exitCallBackResp = "Restart"
                        break
                    elif btnName == "Finish":
                        self.exitCallBackResp = "Restart"
                        buttonEvent = True
                    elif btnName == "Resume":
                        self.interfaceState = 0
                        print("\n//TODO: SEND RESUME PRINT\n")
                    elif btnName == "Pause":
                        self.interfaceState = 1
                        print("\n//TODO: SEND PAUSE PRINT\n")
                    elif btnName == "ShutDown":
                        self.interfaceState = 2
                        print("\n//TODO: SEND SHUTDOWN\n")
                    elif btnName == "Close":
                        print("\n//TODO: SEND CLOSE COMMAND\n")
                        self.exitCallBackResp = "Restart"
                    elif btnName == "Change Filament":
                        self.interfaceState = 3
                        print("\n//TODO: VERIFY ReadyToLoad?\n")
                    elif btnName == "Load":
                        print("\n//TODO: LOAD FILAMENT \n")
                    elif btnName == "Unload":
                        print("\n//TODO: UNLOAD FILAMENT \n")
                    elif btnName == "Color":
                        self.interfaceState = 4
                    elif btnName == "Up":
                        self.listPosition = self.listPosition - 1
                    elif btnName == "Down":
                        self.listPosition = self.listPosition + 1
                    elif btnName == "Next":
                        self.selectedColoridx = (2 + self.listPosition) % len(self.colorList)
                        self.interfaceState = 3
                        print("\n//TODO: SEND COLOR CODE: ", self.colorCodeList[self.selectedColoridx], "\n")
                
                self.UpdateVars()
                
            if(event.type == pygame.MOUSEBUTTONUP and buttonEvent == False and self.interfaceState == 0):
                self.GetSelectedIdx(event)
        
        return

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        # Update Top label
        self.lbl = self.lblFont.render(self.lblText, 1, self.lblFontColor)
        
        # Update Time Label
        if self.interfaceState == 0:
            lblStr = self.timeLblText + str(self.timeRemaining)
            self.timeLbl = self.timeLblFont.render(lblStr, 1, self.timeLblFontColor)
            
        # Update Color Label
        elif self.interfaceState == 3:
            lblStr = self.colorLblText + self.colorNameList[self.selectedColoridx]
            self.colorLbl = self.colorLblFont.render(lblStr, 1, self.colorLblFontColor)
        
        elif self.interfaceState == 5:
            lblStr = self.timeRemaining
            self.timeLbl = self.timeLblFont.render(lblStr, 1, self.timeLblFontColor)
        
        for btn in self.buttons:
            if btn._propGetName() == "Update":
                btn.visible = self.updateReady
            else:
                btn.visible = True
        
        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):        
        # clear whole screen
        # self.screen.fill(self.BEEDisplay.GetbgColor())
        
        # Draw Top label
        self.screen.blit(self.lbl, (self.lblXPos, self.lblYPos))
        
        # Draw Time label
        if self.interfaceState == 0:
            self.screen.blit(self.timeLbl, (self.timeLblXPos, self.timeLblYPos))
            
            # Draw Progress Bar
            self.progressBar.DrawRect(self.screen)
            self.screen.blit(self.progressBar.GetSurface(self.executedLines, self.numberLines),
                                self.progressBar.GetPos())
        # Draw Time label
        elif self.interfaceState == 3:
            self.screen.blit(self.colorLbl, (self.colorLblXPos, self.colorLblYPos))
            
        elif self.interfaceState == 4:
            x = self.interfaceLoader.GetPickerX()
            y = self.interfaceLoader.GetPickerY()
            width = self.interfaceLoader.GetPickerWidth()
            height = self.interfaceLoader.GetPickerHeight()
            pickerColor = self.interfaceLoader.GetPickerFontColor()
            fontSize = self.interfaceLoader.GetPickerFontSize()
            pickerFont = self.interfaceLoader.GetPickerFont()
            lblOffset = int((height - fontSize) / 2)
            
            for i in range(0, 5):
                pos = i + self.listPosition
                
                idx = pos % len(self.colorList)   
                
                colorSurf = pygame.Surface((height * 0.8, height * 0.8))
                colorSurf.fill(self.colorList[idx])
                self.screen.blit(colorSurf, (x + (int(0.1 * height)), y + ((-2 + i) * height) + (int(0.1 * height))))
                
                colorLbl = None
                if i == 2:
                    colorLbl = pickerFont.render(self.colorNameList[idx], 1, pickerColor)
                else:
                    ff = FileFinder.FileFinder()
                    font = pygame.font.Font(ff.GetAbsPath("/Fonts/DejaVuSans-Light.ttf"), fontSize)
                    colorLbl = font.render(self.colorNameList[idx], 1, pickerColor)
                    
                self.screen.blit(colorLbl, (x + height + 5, y + lblOffset + ((-2 + i) * height)))
                
                if i > 0 and i < 5:
                    pygame.draw.line(self.screen, pickerColor, (x, y + ((-2 + i) * height)),
                                (x + width, y + ((-2 + i) * height)), int(0.05 * height))
            
            
            self.pickColorRect = pygame.draw.rect(self.screen, pickerColor, (x, y, width, height), 3)
        
        elif(self.interfaceState == 5):
            self.screen.blit(self.timeLbl, (self.timeLblXPos, self.timeLblYPos))
                                   
        # Draw Image
        if (self.interfaceState != 3) and (self.interfaceState != 4):
            self.screen.blit(self.image, (self.imageX, self.imageY))
        
        for btn in self.buttons:
            btn.draw(self.screen)
        
        
        
        # update screen
        # pygame.display.update()
        
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "Printing"
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        self.screen = None
        self.interfaceLoader = None
        self.printing = None
        self.lblFontColor = None
        self.lblXPos = None
        self.lblYPos = None
        self.lblText = None
        self.lblFont = None
        self.lbl = None
        self.timeLbl = None
        self.timeLblFontColor = None
        self.timeLblXPos = None
        self.timeLblYPos = None
        self.timeLblText = None
        self.timeLblFont = None
        self.colorLbl = None
        self.colorLblFontColor = None
        self.colorLblXPos = None
        self.colorLblYPos = None
        self.colorLblText = None
        self.colorLblFont = None
        self.buttons = None
        self.interfaceState = None
        self.image = None
        self.imageX = None
        self.imageY = None
        self.timeRemaining = None
        self.printPercent = None
        self.nextPullTime = None
        self.pullInterval = None
        self.progressBar = None
        self.pBarRect = None
        self.pBarFill = None
        self.pBarMax = None
        self.pickColorRect = None
        self.colorCodes = None
        self.colorNameList = None
        self.colorCodeList = None
        self.colorList = None
        self.listPosition = None
        self.selectedColoridx = None
    
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
    def Pull(self, arg=None):
        
        t = time()
        if t > self.nextPullTime:
            self.nextPullTime = time() + self.pullInterval
            
            if self.interfaceState == 0:
                
                try:
                    pStatus = self.beeCmd.getPrintVariables()
                    self.elapsedTime = pStatus['Elapsed Time']
                    self.estimatedTime = pStatus['Estimated Time']
                    self.numberLines = pStatus['Lines']
                    self.executedLines = pStatus['Executed Lines']
                except:
                    pass
                
                self.timeRemaining = ""
                minutesLeft = int(self.estimatedTime - self.elapsedTime) 
                if(minutesLeft == 0):
                    self.timeRemaining = 'Less Than a Minute'
                elif(minutesLeft > 0):
                    h = minutesLeft//60
                    if(h > 0):
                        self.timeRemaining += str(h) + 'h:'
                    
                    m = int(minutesLeft - (h*60))
                    self.timeRemaining += str(m) + 'm'
                elif(minutesLeft < 0):
                    self.timeRemaining = 'Unknown'
                else:
                    self.timeRemaining = 'Taking longer than expected'
                    
                if(self.executedLines >= self.numberLines):
                    h = self.elapsedTime//60
                    m = self.elapsedTime - (h * 60)
                    
                    printerStatus = self.beeCmd.getStatus()
                    
                    if(printerStatus != 'SD_Print'):
                        self.timeRemaining = 'Print Finished. Total time: ' + str(int(h)) + 'h' + str(int(m))
                        print(self.timeRemaining)
                        self.interfaceState = 5
                        self.UpdateVars()
                    else:
                        if(self.numberLines == 0):
                            self.timeRemaining = 'Printing Info is Not Available'
                        else:
                            self.timeRemaining = 'Error reading print variables'
                        self.executedLines = self.numberLines
         
        return
    
    """*************************************************************************
                                Update Vars Method 
    
    Update variables
    *************************************************************************""" 
    def UpdateVars(self):
        
        self.lblFontColor = self.interfaceLoader.GetLblsFontColor(self.interfaceState)
        self.lblXPos = self.interfaceLoader.GetLblsXPos(self.interfaceState)
        self.lblYPos = self.interfaceLoader.GetLblsYPos(self.interfaceState)
        self.lblText = self.interfaceLoader.GetLblsText(self.interfaceState)
        self.lblFont = self.interfaceLoader.GetLblsFont(self.interfaceState)
        
        self.timeLblFontColor = self.interfaceLoader.GetTimeLblFontColor(self.interfaceState)
        self.timeLblXPos = self.interfaceLoader.GetTimeLblXPos(self.interfaceState)
        self.timeLblYPos = self.interfaceLoader.GetTimeLblYPos(self.interfaceState)
        self.timeLblText = self.interfaceLoader.GetTimeLblText(self.interfaceState)
        self.timeLblFont = self.interfaceLoader.GetTimeLblFont(self.interfaceState)
        
        self.colorLblFontColor = self.interfaceLoader.GetColorLblFontColor(self.interfaceState)
        self.colorLblXPos = self.interfaceLoader.GetColorLblXPos(self.interfaceState)
        self.colorLblYPos = self.interfaceLoader.GetColorLblYPos(self.interfaceState)
        self.colorLblText = self.interfaceLoader.GetColorLblText(self.interfaceState)
        self.colorLblFont = self.interfaceLoader.GetColorLblFont(self.interfaceState)
        
        self.buttons = self.interfaceLoader.GetButtonsList(self.interfaceState)
        
        if (self.interfaceState == 3) or (self.interfaceState == 4):
            self.image = None
            self.imageX = None
            self.imageY = None
        else:    
            self.image = pygame.image.load(self.interfaceLoader.GetImagePath(self.interfaceState))
            self.imageX = self.interfaceLoader.GetImageX(self.interfaceState)
            self.imageY = self.interfaceLoader.GetImageY(self.interfaceState)
        
        self.progressBar = self.interfaceLoader.GetProgessBar(self.interfaceState)
        
        return
    
    """*************************************************************************
                                GetSelectedIdx Method 
    
    Identifies which color the user chose by clicking the list
    *************************************************************************""" 
    def GetSelectedIdx(self, event):
        
        if self.interfaceState == 4:
            pos = pygame.mouse.get_pos()
            posX = pos[0]
            posY = pos[1]
            
            width = self.interfaceLoader.GetPickerWidth()
            height = self.interfaceLoader.GetPickerHeight()
            pickerXMin = self.interfaceLoader.GetPickerX()
            pickerXMax = pickerXMin + width
            pickerYMin = self.interfaceLoader.GetPickerY() - (2 * height)
            pickerYMax = pickerYMin + (5 * height)
            
            if (posX > pickerXMin) and (posX < pickerXMax) and (posY > pickerYMin) and (posY < pickerYMax):
                relY = posY - pickerYMin
                idxChange = -2 + int(relY / height)
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
