class coffee_maker:

	steps = ["water","milk","sugar","powder","temp","mix"]

	work = {
		"dispensor":["water","milk","sugar","powder"],
		"shaker":["temp","mix"]
	}

	recipie = {
		"simple":{
			"water":0,
			"milk":200,
			"sugar":100,
			"powder":100,
			"mix":400,
			"temp":30
		},
		"black":{
			"water":400,
			"milk":0,
			"sugar":0,
			"powder":100,
			"mix":400,
			"temp":30
		}
	}

	def __init__(self,name):
		self.water = coffee_maker.recipie[name]["water"]
		self.milk = coffee_maker.recipie[name]["milk"]
		self.sugar = coffee_maker.recipie[name]["sugar"]
		self.powder = coffee_maker.recipie[name]["powder"]
		self.mix = coffee_maker.recipie[name]["mix"]
		self.temp = coffee_maker.recipie[name]["temp"]

	def ret_steps(self,step):
		if step == "water":
			return self.water
		elif step == "milk":
			return self.milk
		elif step == "sugar":
			return self.sugar
		elif step == "powder":
			return self.powder
		elif step == "mix":
			return self.mix
		elif step == "temp":
			return self.temp
		
	
	