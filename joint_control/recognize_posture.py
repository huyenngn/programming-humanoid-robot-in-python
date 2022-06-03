'''In this exercise you need to use the learned classifier to recognize current posture of robot

* Tasks:
    1. load learned classifier in `PostureRecognitionAgent.__init__`
    2. recognize current posture in `PostureRecognitionAgent.recognize_posture`

* Hints:
    Let the robot execute different keyframes, and recognize these postures.

'''
import numpy as np

from angle_interpolation import AngleInterpolationAgent
from keyframes import leftBackToStand
import pickle
from os import listdir


class PostureRecognitionAgent(AngleInterpolationAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(PostureRecognitionAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.posture = 'unknown'
        self.posture_classifier = 'robot_pose.pkl'  # LOAD YOUR CLASSIFIER

    def think(self, perception):
        self.posture = self.recognize_posture(perception)
        return super(PostureRecognitionAgent, self).think(perception)

    def recognize_posture(self, perception):
        posture = 'unknown'
        # YOUR CODE HERE
        ROBOT_POSE_DATA_DIR = 'robot_pose_data'
        classes = listdir(ROBOT_POSE_DATA_DIR)
        joints = ['LHipRoll', 'LHipPitch', 'LElbowRoll', 'RHipRoll', 'RHipPitch',
                  'RElbowRoll', 'LShoulderPitch', 'RShoulderPitch']

        clf = pickle.load(open(self.posture_classifier, 'rb'))
        data = []
        for i in joints:
            data.append(perception.joint[i])
        for j in perception.imu:
            data.append(j)

        all_data = [data]
        #all_data = np.asarray(all_data)

        predicted = clf.predict(all_data)
        posture = np.array(classes)[predicted]
        return posture


if __name__ == '__main__':
    agent = PostureRecognitionAgent()
    agent.keyframes = leftBackToStand()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
