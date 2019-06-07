class BackEnd:
	def call(xes):
		print("\033[1;32;40m Back-end call received. \n")
		set = Views.ViewFactory.buildViewFromXES(xes)
