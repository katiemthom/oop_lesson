class Rock(object): 
	def __init__(self, name): 
		self.name = name 

rock = Rock("katie")

if rock.__class__ is Rock:
	print "This works!"