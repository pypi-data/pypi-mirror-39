import plotille

#c = Canvas()

'''
def draw_plot(data_to_draw):
	#c = Canvas()
	for x in data_to_draw:
		index = data_to_draw.index(x)
		c.set( float(x['Position']), index)
	#print(c.frame())
print(c.frame())
'''

def draw_plot(X,Y):
	print(plotille.plot(X, Y, height=30, width=60, x_min=0))
