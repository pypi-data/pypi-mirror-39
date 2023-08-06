from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np

class FaceParser:
    def __init__(self, shape):
        self.shape = shape
        self.shape_np = self.shape_to_np(self.shape)

    def shape_to_np(self, shape, dtype="int"):
        coords = np.zeros((68, 2), dtype="int")
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
        return coords

    def get_eye_ar(self, eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        C = dist.euclidean(eye[0], eye[3])

        ear = (A+B) / (2.0 * C)

        return ear

    def parse_eyes(self):
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        leftEye = self.shape_np[lStart:lEnd]
        rightEye = self.shape_np[rStart:rEnd]
        self.eyes = [leftEye, rightEye]

        leftEAR = self.get_eye_ar(leftEye)
        rightEAR = self.get_eye_ar(rightEye)

        self.ears = [leftEAR, rightEAR]
        return (leftEAR + rightEAR) / 2.0

    def get_mouth_ar(self, mouth):
        A = dist.euclidean(mouth[3], mouth[9])
        B = dist.euclidean(mouth[2], mouth[10])
        C = dist.euclidean(mouth[4], mouth[8])

        L = (A+B+C) / 3
        D = dist.euclidean(mouth[0], mouth[6])
        mar = L/D
        return mar

    def parse_mouth(self):
        (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
        mouth = self.shape_np[mStart:mEnd]

        ar = self.get_mouth_ar(mouth)
        self.mouthAR = ar
        return ar
