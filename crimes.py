class Crimes: 

	totCount = 0

	def __init__(self, category, count):
		self.category = category
		self.count = count

	def displayCount(self):
		print self.count

	def increaseCount(self):
		self.count+=1
		totCount+=1

	def displayCrime(self):
		print self.category + " " + self.count

	def getTotCount(self):
		print Crimes.totCount
