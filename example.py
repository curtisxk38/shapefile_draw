from PIL import Image
import shapefile_draw

def my_modify(self, new_point):
	new_point[0] -= self.sh_list[0].shapes()[0].bbox[0]
	new_point[1] -= self.sh_list[0].shapes()[0].bbox[1]
	new_point[0] //= 8
	new_point[1] //= 8
	

im = Image.new('RGBA', (2786, 2770), (255, 255, 255, 0))
pic = shapefile_draw.ShapefileDrawer(im, modify_function=my_modify)
pic.load_shapefile("city_limit/municipal_boundary_area_06_25_2015", "black")
#pic.load_shapefile("road_area/road_area_06_30_2015", "black")
pic.load_shapefile("bicycle_lane/bicycle_lane_line_06_27_2015", "blue")

pic.draw()