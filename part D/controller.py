from suspicious_points_tfl import Suspicious_points_tfl
from SFM import SFM


class Controller:
    def __init__(self, pkl, images):
        self.pkl = pkl
        self.images = images
        self.suspicious_points_tfl = Suspicious_points_tfl()
        self.sfm = SFM(pkl)

    def get_images_for_detection(self, red_points, green_points):
        pass

    def run(self):
        for i in range(len(self.images)):
            self.suspicious_points_tfl.set_image(self.images[i])
            red_points, green_points = self.suspicious_points_tfl.run()
            images_for_detection = self.get_images_for_detection(red_points, green_points)
            #tfl_points=neron_net.run()
           