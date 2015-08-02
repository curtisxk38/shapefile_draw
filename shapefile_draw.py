import shapefile
from PIL import ImageDraw

# Assumes all shapes in a shapefile are of the same shapeType

class ShapefileDrawer():
	def __init__(self, image, modify_function=None, output=None):
		self.image = image
		self.sh_list = []
		self.colors = []
			
		self.modify_function = modify_function
		self.output = output
		
		self.image = image
		self.image_drawer = ImageDraw.Draw(image)
		# incomplete dict
		self.drawing_dict = {
			3 : lambda line, color: self.image_drawer.line(line, fill=color, width=1),
			5 : lambda poly, color: self.image_drawer.polygon(poly, outline=color),
			15: lambda poly, color: self.image_drawer.polygon(poly, outline=color),
			}
		
	def load_shapefile(self, sh, color):
		self.sh_list.append(shapefile.Reader(sh))
		# color should be PIL color
		self.colors.append(color)
	
	def modify(self, sh):
		shape_list = sh.shapes()
		#print(len(sh))
		point_list = [i.points for i in shape_list]
		fixed_sh = []
		for i, shape in enumerate(point_list):
			#print(len(shape))
			fixed_sh.append([self.modify_point(j) for j in shape])
			#print("shape {}".format(i))
		return(fixed_sh)

	def modify_point(self, point):
		new_point = list(point)
		if self.modify_function is not None:
			self.modify_function(self, new_point)
		return new_point[0], new_point[1]
	
	def draw(self):
		for index, shapefile in enumerate(self.sh_list):
			shape_type = shapefile.shapes()[0].shapeType
			# look up the how to draw the shapefile in self.draw_dict based on the shapeType
			try:
				drawing_function = self.drawing_dict[shape_type]
			except KeyError as e:
				print("Shape type of value {} not described in self.drawing_dict".format(shape_type))
				raise
			# loop through shapefile modified for drawing and draw it
			for shape in self.modify(shapefile):
				drawing_function(shape, self.colors[index])
		if self.output is not None:
			self.image.save(self.output)
		else:
			self.image.save("output.png")