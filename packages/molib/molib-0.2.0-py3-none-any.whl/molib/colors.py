def rescale_colors(color_list):
	# Rescale to values between 0 and 1 
	for i in range(len(color_list)):  
		r, g, b = color_list[i]  
		color_list[i] = (r / 255., g / 255., b / 255.)
	return color_list
	
def tableau10(index):
	# Tableau 10 Colors
	tableau10_list = [(31,119,180),(255,127,14),(44,160,44),(214,39,40),(148,103,189),(140,86,75),(227,119,194),(127,127,127),(188,189,34),(23,190,207)];
	tableau10_list = rescale_colors(tableau10_list)
	return tableau10_list[index]

def tableau20(index):
	# Tableau 20 Colors
	tableau20_list = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
	tableau20_list = rescale_colors(tableau20_list)
	return tableau20_list[index]
	
def tableau10blind(index):
	# Tableau Color Blind 10
	tableau10blind_list = [(0, 107, 164), (255, 128, 14), (171, 171, 171), (89, 89, 89),
             (95, 158, 209), (200, 82, 0), (137, 137, 137), (163, 200, 236),
             (255, 188, 121), (207, 207, 207)]
	tableau10blind_list = rescale_colors(tableau10blind_list)
	return tableau10blind_list[index]