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


import FileFinder
import pygame
import Loaders.WaitForConnectionLoader
from beedriver import connection
import time
import FileFinder

class WaitScreen():
    """
    @var connected: status of USB connection to the BTF      
    """
    connected = False
    screen = None
    exit = False
    
    lblTop = None
    lblBottom = None
    bgImage = None
    
    loader = None
    
    nextPullTime = None
    
    """
    BEEConnect vars
    """
    beeCon = None
    beeCmd = None
    mode = None
    
    displayWidth = 480
    displayHeight = 320


    """*************************************************************************
                                Init Method 
    
    intis all compoments
    *************************************************************************"""
    def __init__(self, screen, dispWidth = 480, dispHeight = 320, shutdownCallback=None):
        """
        .
        """
        
        self.displayWidth = dispWidth
        self.displayHeight = dispHeight
        
        self.connected = False
        
        print("Printer Connection: {0}".format(self.connected))
        
        
        self.exit = False
        self.screen = screen
        self.currentScreen = 'WaitConnection'
        
        self.loader = Loaders.WaitForConnectionLoader.WaitForConnectionLoader(self.displayWidth, self.displayHeight)
        
        lblText = self.loader.GetLblsText()
        lblX = self.loader.GetLblsXPos()
        lblY = self.loader.GetLblsYPos()
        lblFont = self.loader.GetLblsFont()
        lblFontColor = self.loader.GetLblsFontColor()
        
        for i in range(0,len(lblText)):
            lbl = lblFont[i].render(lblText[i],1,lblFontColor[i])
            self.screen.blit(lbl,(lblX[i],lblY[i]))
        
        
        self.bgImage = pygame.image.load(self.loader.GetImagePath())
        imgX = self.loader.GetImageX()
        imgY = self.loader.GetImageY()

        # Draw Image
        self.screen.blit(self.bgImage,(imgX,imgY))

        # update screen
        pygame.display.update()
        
        self.nextPullTime = time.time() + 0.5
        
        tries = 10
        
        while (not self.connected) and (not self.exit) and (tries > 0):
            # Handle events
            self.handle_events()
            
            t = time.time()
            if t > self.nextPullTime:
                
                self.beeCon = connection.Conn(shutdownCallback)
                # Connect to first Printer
                self.beeCon.connectToFirstPrinter()
                printerDict = self.beeCon.connectedPrinter
                if(self.beeCon.isConnected() == True):
                    self.beeCmd = self.beeCon.getCommandIntf()

                    self.mode = self.beeCmd.getPrinterMode()

                    fwVersion = self.beeCmd.getFirmwareVersion()

                    #resp = self.beeCmd.startPrinter()
                
                    if('Firmware' in self.mode):

                        if '10.4.7' not in fwVersion and not self.beeCmd.isPrinting():
                            self.beeCmd.goToBootloader()
                            self.beeCon.close()
                            self.beeCon = None
                        else:
                            self.connected = self.beeCon.connected

                    elif('Bootloader' in self.mode):

                        printerVID = printerDict['VendorID']
                        printerPID = printerDict['ProductID']

                        fwName = ''
                        fwString = ''

                        if printerVID == '65535' and printerPID == '334':
                            #Old Bootloader Printer
                            fwString = 'BEEVC-BEETHEFIRST0-10.4.8'
                            fwName = '/Firmware/BEEVC-BEETHEFIRST0-Firmware-10.4.8.BIN'
                        elif printerVID == '10697':
                            #New Bootloader Printers
                            if printerPID == '1':
                                #BEETHEFIRST
                                fwString = 'BEEVC-BEETHEFIRST-10.4.8'
                                fwName = '/Firmware/BEEVC-BEETHEFIRST-Firmware-10.4.8.BIN'
                            elif printerPID == '2':
                                #BEETHEFIRST+
                                fwString = 'BEEVC-BEETHEFIRST_PLUS-10.4.8'
                                fwName = '/Firmware/BEEVC-BEETHEFIRST_PLUS-Firmware-10.4.8.BIN'
                            elif printerPID == '3':
                                #BEEME
                                fwString = 'BEEVC-BEEME-10.4.8'
                                fwName = '/Firmware/BEEVC-BEEME-Firmware-10.4.8.BIN'
                            elif printerPID == '4':
                                #BEEINSCHOOL
                                fwString = 'BEEVC-BEEINSCHOOL-10.4.8'
                                fwName = '/Firmware/BEEVC-BEEINSCHOOL-Firmware-10.4.8.BIN'
                            elif printerPID == '5':
                                #BEETHEFIRST_PLUS_A
                                fwString = 'BEEVC-BEETHEFIRST_PLUS_A-10.4.8'
                                fwName = '/Firmware/BEEVC-BEETHEFIRST_PLUS_A-Firmware-10.4.8.BIN'

                        if '10.4.8' not in fwVersion:
                            print('Falshing new Firmare')
                            ff = FileFinder.FileFinder()
                            fwPath = ff.GetAbsPath(fwName)
                            self.beeCmd.flashFirmware(fwPath,fwString)
                            while self.beeCmd.getTransferCompletionState() is not None:
                                time.sleep(0.5)
                            self.beeCon.close()
                            self.beeCon = None
                        else:
                            print("Changing to firmware")
                            self.beeCmd.goToFirmware()
                            #self.beeCon.close()
                            #time.sleep(1)

                            self.mode = self.beeCmd.getPrinterMode()
                            if 'Firmware' not in self.mode:
                                self.beeCon = None
                            else:
                                self.connected = self.beeCon.connected
                            #return True
                    else:
                        # USB Buffer need cleaning
                        print('Printer not responding... cleaning buffer\n')
                        self.beeCmd.cleanBuffer()

                        self.beeCon.close()
                        self.beeCon = None
                        # return None
                    
                self.nextPullTime = time.time() + 0.5
                #print("Wait for connection")
                tries -= 1
        
        if(tries <= 0):
            print('Printer not found')
            return False
        else:
            status = self.beeCmd.getStatus()
            if status is not None:
                if 'Shutdown' in status:
                    self.beeCmd.clearShutdownFlag()
            
            
        return
    

    """*************************************************************************
                                handle_events
    
    waits for a USB conenction to be stablished
    *************************************************************************"""
    def handle_events(self):
        """handle all events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
                
        return
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        self.bgImage = None
        self.lblTop = None
        self.lblBottom = None
        self.loader = None
        self.nextPullTime = None
        
        return

        




