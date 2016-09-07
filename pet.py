#! /usr/bin/env python
from Tkinter import *
import json, time

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
		def mainMenu():
			def func():
				self.leaveLoadMenu(buttons)
				self.enterMainMenu()
			return func()	
		petDataStream = open("petpy.json", 'r')
		try:
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
			for i in petData.keys():
				buttons.append(pypet.addButton(petData[i]["name"], None))
				petMenuCommands.append(pickPet(petData[i]))
			for k in range(len(buttons)):
				print k
				buttons[k].config(command = addLeaveLoad(petMenuCommands[k]))
		except ValueError:
			self.displayText("No pets currently.")
		mainMenuButton = pypet.addButton("Main Menu", mainMenu)
		buttons.append(mainMenuButton)
	
	def leaveLoadMenu(self, buttons):
		print "destroy " + str(len(buttons)) + " buttons"
		for i in range(0, len(buttons)):
			buttons[i].destroy()
		
	def loadPet(self, stats):
		self.pet = Pet(stats['name'], stats['age'], stats['weight'], stats['picture'])
		print str(self.pet.name)
		self.pet.age = stats['age']
		self.pet.hungry = stats['hungry']
		self.pet.alive = stats['alive']
		self.pet.foodLevel = stats['foodLevel']
		
	def savePet (self):
		petDataStream = open('petpy.json', 'r')
		try: 
			petData = json.load(petDataStream)
			petDataStream.close()
		except ValueError:
			petData = {}
		petDataStream = open('petpy.json', 'w')
		if hasattr(petData, self.pet.name):
			del petData[self.pet.name]
		petData[self.pet.name] = vars(self.pet)
		json.dump(petData, petDataStream) 
		petDataStream.close()
		
	def newPet(self):
		self.leaveMainMenu();
		fileDataStream = open('petpytemplates.json', 'r')
		templates = json.load(fileDataStream)
		fileDataStream.close()
		buttons = []
		def makeCommand(newPet):
			def command():
				self.pet = Pet(newPet['name'], newPet['age'], newPet['weight'], newPet['picture'])
				print self.pet.picture
				self.displayText('New ' + newPet['type'] + ' created.')
			return command
		for i in templates.keys():
			buttons.append(pypet.addButton(templates[i]['type'], makeCommand(templates[i])))
		def playCommand(buttonlist, petbutton):
			def playfunc():
				for i in range(len(buttonlist)):
					buttonlist[i].destroy()
				self.mainMenuButton.destroy()
				petbutton.destroy()
				self.enterPetMode()
			return playfunc
		def leaveMenu(buttonlist, petModeB):
			def leaving():
				for i in range(len(buttonlist)):
					buttonlist[i].destroy()
				petModeB.destroy()
				self.leaveNewPet()
			return leaving
		self.mainMenuButton = pypet.addButton("Main Menu", None) 
		petModeButton = pypet.addButton('Play with Pet', None)
		self.mainMenuButton.config(command =leaveMenu(buttons, petModeButton))
		petModeButton.config(command = playCommand(buttons, petModeButton))
		
	def leaveNewPet(self):
		self.mainMenuButton.destroy()
		self.enterMainMenu()
	
	def enterRenameScreen(self):
		self.feedButton.destroy()
		self.greetButton.destroy()
		self.nameButton.destroy()
		self.mainMenuButton.destroy()
		self.renameScreen()
	
	def renameScreen(self):
		nameField = Entry(self.root, bd = 2)
		instructions = Label(self.root, text="Enter the name of your pet:")
		instructions.pack()
		nameField.pack()
		okButton = self.addButton("ok", None)
		def setAndLeave():
			self.pet.name = nameField.get()
			nameField.destroy()
			instructions.destroy()
			okButton.destroy()
			self.enterPetMode()
		okButton.config(command = setAndLeave)
		
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
		self.nameButton = pypet.addButton('Change Name', self.enterRenameScreen)
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
		self.nameButton.destroy()
		self.savePet()
		self.enterMainMenu()
		
pypet = PyPet()
pypet.enterMainMenu()

pypet.root.mainloop()
pypet.root.destroy()