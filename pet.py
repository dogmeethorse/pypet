#! usr/bin/env python
from Tkinter import *
import json

print "Welcome to Pet Thing!"

class Pet:
	def __init__(self, name, age, weight, picture):
		self.name = name
		self.age = age
		self.weight = weight
		self.picture = picture
		self.hungry = False
		self.foodLevel = 50
		self.message = None
		self.picBox = None
		self.alive = True
		
	def greet(self):
		greet =  "Hello I am " + self.name
		if self.alive is False:
			greet = self.name + " stares back at you with cold dead eyes." 
		pypet.displayText(greet)
		return greet
			
	def feed(self):
		if self.alive is False:
			self.message = "You desecrate the corpse."	
		elif self.hungry is True:
			self.weight += 2
			self.foodLevel +=2
			self.message = "yummy"	
			self.hungry = False
		else: 
			self.message = "BARF"
			self.weight += 1
			self.foodLevel +=1
		pypet.displayText(self.message)
		return self.message
		
class PyPet:
	def __init__(self):
		self.pet = None
		self.root = Tk()
		self.root.title('PY-PET!')
		self.nextUpdate = None
		self.picture = StringVar()
		self.pictureFrame = Label(master=self.root, textvariable=self.picture)
		self.pictureFrame.pack()
		self.frame = Frame(master = self.root, width = 100, height = 100)
		self.textWidget = Text(master = self.frame, width =30, height = 4)
		self.frame.pack(side=TOP, fill=BOTH)
		self.scrollbar = Scrollbar(self.frame)
		self.textWidget.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.textWidget.yview)
		self.scrollbar.pack(side=RIGHT, fill=Y)
		self.textWidget.pack(fill=BOTH)

	def displayPet(self):
		self.picture.set(self.pet.picture)
		
	def displayText(self, text):
		self.textWidget.tag_configure('center', justify='center')
		self.textWidget.insert(END, text, 'center')
		self.textWidget.insert(END, '\n')
		self.textWidget.see(END)
		
	def addButton(self, name, command):
		button = Button(self.root)
		button["text"] = name
		button["command"] = command
		button.pack()
		return button
		
	def loadMenu(self):
		self.leaveMainMenu()
		buttons = []
		petMenuCommands = [] 
		petDataStream = open("petpy.json", 'r')
		petData = json.load(petDataStream)
		def pickPet(petter):
			def petterfunc(): 
				self.loadPet(petter)
				self.enterPetMode()
			return petterfunc
		def addLeaveLoad(func):
			def leaveFunc():
				func()
				self.leaveLoadMenu(buttons)
			return leaveFunc	
		def mainMenu():
			def func():
				self.leaveLoadMenu(buttons)
				self.enterMainMenu()	
		for i in petData.keys():
			buttons.append(pypet.addButton(petData[i]["name"], None))
			petMenuCommands.append(pickPet(petData[i]))
		for k in range(len(buttons)):
			print k
			buttons[k].config(command = addLeaveLoad(petMenuCommands[k]))
		mainMenuButton = pypet.addButton("Main Menu", mainMenu)
		buttons.append(mainMenuButton)
	
	def leaveLoadMenu(self, buttons):
		print "destroy " + str(len(buttons)) + " buttons"
		for i in range(0, len(buttons)):
			buttons[i].destroy()
		
	def loadPet(self, stats):
		self.pet = Pet(stats['name'], stats['age'], stats['weight'], stats['picture'])
		print str(self.pet.name)
	
	def savePet (self):
		petDataStream = open('petpy.json', 'r+')
		petData = json.load(petDataStream)
		petDataStream.seek(0,0)
		del petData[self.pet.name]
		petData[self.pet.name] = vars(self.pet)
		json.dump(petData, petDataStream) 
		petDataStream.close()
		
	def newPet(self):
		self.leaveMainMenu();
		self.mainMenuButton = pypet.addButton("Main Menu", self.leaveNewPet)
		
	def leaveNewPet(self):
		self.mainMenuButton.destroy()
		self.enterMainMenu()
		
	def enterMainMenu(self):
		self.loadPetButton = self.addButton("Load Pet", self.loadMenu)
		self.newPetButton = self.addButton("New Pet", self.newPet)
	
	def leaveMainMenu(self):
		self.loadPetButton.destroy()
		self.newPetButton.destroy()
		
	def enterPetMode(self):
		print self.pet
		self.displayPet()
		self.feedButton = pypet.addButton("FEED", self.pet.feed)
		self.greetButton = pypet.addButton("Greet", self.pet.greet)
		self.mainMenuButton = pypet.addButton("Main Menu", self.leavePetMode)
		self.petMode()
	
	def petMode(self):
		self.pet.foodLevel -= 1
		if self.pet.foodLevel > 60:
			self.pet.hungry = False
		elif self.pet.foodLevel < 40:
			self.pet.hungry = True 
		if self.pet.foodLevel < 0:
			print "starved"
			self.pet.alive = False
			self.displayText("Oh no! " + self.pet.name + " starved to death!")
			self.root.after_cancel(self.nextUpdate)
		elif self.pet.foodLevel > 100:
			self.pet.alive = False
			self.displayText("You overfed " + self.pet.name + " and his \n stomach ruptured!")
			self.root.after_cancel(self.nextUpdate)
		else:
			self.nextUpdate = self.root.after(1000, self.petMode)
		print self.pet.foodLevel
		
	def leavePetMode(self):
		if self.nextUpdate:
			self.root.after_cancel(self.nextUpdate)
		self.feedButton.destroy()
		self.greetButton.destroy()
		self.mainMenuButton.destroy()
		self.savePet()
		self.enterMainMenu()
		
pypet = PyPet()
pypet.enterMainMenu()

pypet.root.mainloop()
pypet.root.destroy()