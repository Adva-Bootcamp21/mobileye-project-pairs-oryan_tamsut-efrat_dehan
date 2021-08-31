from suspicious_points_tfl import Suspicious_points_tfl


class Controller:
    def __init__(self, pkl, images):
        self.pkl = pkl
        self.images = images
        self.suspicios_point_tfl = Suspicious_points_tfl()

    def get_images_for_detection(self, red_points, green_points):
        pass

    def get_tfl_for_calc_distance(self, red_points, green_points):
        pass

    def run(self):
        for i in range(len(self.images)):
            self.suspicios_point_tfl.set_image(self.images[i])
            red_points, green_points = self.suspicios_point_tfl.run()
