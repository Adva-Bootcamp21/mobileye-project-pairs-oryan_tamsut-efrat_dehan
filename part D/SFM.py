import numpy as np
import pickle
from PIL import Image
import matplotlib.pyplot as plt
import SFM_function as SFM_f


class FrameContainer(object):
    def __init__(self, img_path):
        self.img = Image.open(img_path)
        self.traffic_light = []
        self.traffic_lights_3d_location = []
        self.EM = []
        self.corresponding_ind = []
        self.valid = []


class SFM:
    def __init__(self, pkl):
        with open(pkl, 'rb') as pklfile:
            data = pickle.load(pklfile, encoding='latin1')
        self.focal = data['flx']
        self.pp = data['principle_point']
        self.prev_container = None
        self.curr_container = None
        self.data = data

    def set_curr_prev(self, curr_path, prev_path, curr_tfl, prev_tfl):
        curr_id = curr_path.replace("dusseldorf_000049_0000", "").replace("_leftImg8bit", "")
        prev_id = prev_path.replace("dusseldorf_000049_0000", "").replace("_leftImg8bit", "")
        prev_container = FrameContainer(prev_path)
        curr_container = FrameContainer(curr_path)
        prev_container.traffic_light = np.array(prev_tfl)
        curr_container.traffic_light = np.array(curr_tfl)
        EM = np.eye(4)
        for i in range(prev_id, curr_id):
            EM = np.dot(self.data['egomotion_' + str(i) + '-' + str(i + 1)], EM)
        curr_container.EM = EM
        self.curr_container = curr_container
        self.prev_container = prev_container

    def run(self):
        norm_prev_pts, norm_curr_pts, R, norm_foe, tZ = SFM_f.prepare_3D_data(self.prev_container, self.curr_container,
                                                                              self.focal, self.pp)
        norm_rot_pts = SFM_f.rotate(norm_prev_pts, R)
        rot_pts = SFM_f.unnormalize(norm_rot_pts, self.focal, self.pp)
        foe = np.squeeze(SFM_f.unnormalize(np.array([norm_foe]), self.focal, self.pp))
        curr_sec = plt.plot()
        curr_sec.imshow(self.curr_container.img)
        curr_p = self.curr_container.traffic_light
        curr_sec.plot(curr_p[:, 0], curr_p[:, 1], 'b+')

        for i in range(len(curr_p)):
            curr_sec.plot([curr_p[i, 0], foe[0]], [curr_p[i, 1], foe[1]], 'b')
            if self.curr_container.valid[i]:
                curr_sec.text(curr_p[i, 0], curr_p[i, 1],
                              r'{0:.1f}'.format(self.curr_container.traffic_lights_3d_location[i, 2]), color='r')
        curr_sec.plot(foe[0], foe[1], 'r+')
        curr_sec.plot(rot_pts[:, 0], rot_pts[:, 1], 'g+')
        plt.show()
