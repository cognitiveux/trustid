
#
# Face Recognition core module
#

from typing_extensions import Literal
from unittest import result
import cv2
import numpy as np
import torch
import torch.nn as nn
from torchvision import models
import torchvision.transforms.functional as TF
import matplotlib.pyplot as plt
import dlib

import enum
from sklearn.svm import LinearSVC


class PoseEstimationResultValueEnum(enum.Enum):
    """List of possible values for PoseEstimationResult result value parameter."""
    SUCCESS = "PE_SUCCESS"
    ERR_NOT_ENOUGH_POINTS = "PE_SHAPEPREDICTION_NOT_ENOUGH_POINTS"
    ERR_INVALID_DETECTION = "PE_INVALID_DETECTION_RECT"

class PoseClassificationResultValueEnum(enum.Enum):
    """List of possible values for PoseEstimationResult.classifyPose result value."""
    LEFT_FACING = "PC_LEFT_FACING"
    RIGHT_FACING = "PC_RIGHT_FACING"
    UPWARD_FACING = "PC_UPWARD_FACING"
    DOWNWARD_FACING = "PC_DOWNWARD_FACING"
    FORWARD_FACING = "PC_FORWARD_FACING"

class ImageQualityResultValueEnum(enum.Enum):
    """List of possible values for ImageQualityResult result value parameter."""
    VERY_LOW_ILUMINATION = 'IQ_LOW_ILUM',
    VERY_HIGH_ILUMINATION = 'IQ_HIGH_ILUM',
    GOOD_IMAGE = 'IQ_GOOD_IMAGE',

class FaceRecognitionResultValueEnum(enum.Enum):
    """List of possible values for RecognitionResult result value parameter."""
    NO_MATCH = 'RECG_NOMATCH',
    INVALID_MATCH = 'RECG_INVALID_MATCH',
    FOUND_MATCH = 'RECG_MATCH',

class FaceRecognitionDictKeyEnum(enum.Enum):
    """List of possible key values for RecognitionResult internal dict."""
    IDENTITY_KEY = 'IDENTITY_KEY',
    SCORE_KEY = 'SCORE_KEY',

class FaceDetectionResultValueEnum(enum.Enum):
    """List of possible values for DetectionResult result value parameter."""
    NO_RESULTS = 'DECT_NONE',
    ONE_RESULT = 'DECT_ONE',
    MULTIPLE_RESULTS = 'DECT_MULTI',

class BoundingBoxHeuristic(enum.Enum):
    """List of possible heuristics to select a bounding box through the DetectionResult.getBoundingBox."""
    LARGEST_AREA = 'LARGEST_AREA'

class RecognitionResult():
    """Wrapper for result values for the Recognition procedure."""

    def __init__(self, resultValue: FaceRecognitionResultValueEnum=FaceRecognitionResultValueEnum.NO_MATCH, identity: str= None, score: float=None, *args):
        self.resultValue = resultValue
        self.identity = identity
        self.score = score
        self._debug_info = args

    def getResult(self) -> FaceRecognitionResultValueEnum:
        """Get result value set by recognition procedure.

        Returns:
            One of the predefined RecognitionResult.ResultType.
        """
        return self.resultValue

    def getMatchedIdentity(self) -> str:
        """Get matched identity if a match was found.

        Returns:
            Identity of the user matched, None if no match was found.
        """
        if (self.resultValue == FaceRecognitionResultValueEnum.FOUND_MATCH):
            return self.identity
        else:
            return None

    def getMatchConfidence(self) -> float:
        """Get result value set by detection procedure.

        Returns:
            Float value from [0, 100] representing the confidence value of the match, None if no match was found.
        """
        if (self.resultValue == FaceRecognitionResultValueEnum.FOUND_MATCH):
            return self.score
        else:
            return None

class DetectionResult():
    """Wrapper for retun values for the detection procedure in in the rFaceID class."""

    def __init__(self, resultValue: FaceDetectionResultValueEnum=FaceDetectionResultValueEnum.NO_RESULTS, bounding_boxes: list=None, *args):
        self.resultValue = resultValue
        self.bounding_boxes = bounding_boxes
        self._debug_info = args

    def getResult(self) -> FaceDetectionResultValueEnum:
        """Get result value set by detection procedure.

        Returns:
            One of the predefined FaceDetectionResultValueEnum values.
        """
        return self.resultValue

    def getBoundingBox(self, heuristic: BoundingBoxHeuristic = BoundingBoxHeuristic.LARGEST_AREA) -> np.array:
        """Get a bounding box from the list of detections according to a predefined heuristic.

        Args:
            heuristic: Heuristic to use to select the bounding box.

        Returns:
            Bounding box coordinates (in cvRecv representation) according to the predefined heuristic or None if no faces were detected.
        """
        # just returns the first bounding box according to heuristic
        return self.getAllBoundingBoxes(heuristic)[0]

    def getAmountOfDetections(self) -> int:
        """Get the amount of detected faces in the provided image."""

        return (0 if self.bounding_boxes is None else len(self.bounding_boxes))

    def getAllBoundingBoxes(self, heuristic: BoundingBoxHeuristic = BoundingBoxHeuristic.LARGEST_AREA) -> list:
        """Get list of all detected bounding boxes, sorted according to a predefined heuristic.

        Args:
            heuristic: Heuristic to use to select the bounding box.

        Returns:
            List of bounding box coordinates (in cvRecv representation), sorted according to the predefined heuristic or None if no faces were detected.
        """
        if (self.getAmountOfDetections() > 0):
            if (heuristic == BoundingBoxHeuristic.LARGEST_AREA):
                # sort by largest area
                return sorted(self.bounding_boxes, key=lambda x:-(x[2]*x[3]))
            else:
                raise NotImplementedError()
        else:
            return None

class ImageQualityResult():
    """Wrapper for result values for the CheckImageQuality procedure."""

    def __init__(self, resultValue: ImageQualityResultValueEnum, *args):
        self.resultValue = resultValue
        self._debug_info = args

    def getResult(self) -> ImageQualityResultValueEnum:
        """Get result value set by image quality verification procedure.

        Returns:
            One of the predefined ImageQualityResult.ResultType.
        """
        return self.resultValue

class PoseEstimationResult():
    """Wrapper for result values for the PoseEstimation procedure."""

    def __init__(self, resultValue: PoseEstimationResultValueEnum, poseVector : np.array = None, estimatedDist : float = None, landmarkLocations: np.array = None, *args):
        self.resultValue = resultValue
        self.poseVector = poseVector
        self.estimatedDist = estimatedDist
        self.landmarkLocations = landmarkLocations
        self._debug_info = args

    def getResult(self) -> PoseEstimationResultValueEnum:
        """Get result value set by pose estimation procedure.

        Returns:
            Result value according to PoseEstimationResultValueEnum values.
        """
        return self.resultValue

    def getPoseVector(self) -> np.array:
        """Get the vector (6x1) which represents the pose of the user, containing the Euler Angles (Z-Y-X in radians) and the translation vector.
        The return vector has the following shape [Rz, Ry, Rx, tx, ty, tz].

        Returns:
            Pose vector if the procedure was sucessful, None otherwise.
        """
        return self.poseVector

    #def getAngles(self) -> np.array:


    def getEstimatedDistance(self) -> float:
        """Get the user's estimated distance in cm to the camera.

        Returns:
            Estimated distance to the camera in cm if the procedure was sucessful, None otherwise.
        """
        return self.estimatedDist

    def getLandmarkLocations(self) -> np.array:
        """Get matrix representing the facial landmark locations according to the chosen face model.

        Returns:
            Matrix representing the facial landmark locations if the procedure was sucessful, None otherwise.
        """
        return self.landmarkLocations


    def classifyPose(self) -> PoseClassificationResultValueEnum:
        """Classify current pose.

        Returns:
            One of PoseClassificationResultValueEnum valuse if the pose estimation was sucessful, None otherwise.
        """
        if (self.getResult() != PoseEstimationResultValueEnum.SUCCESS):
            return None

        #maximum values obtained via the pose algorithm
        #max_alpha_angle = 30
        max_beta_angle = 35
        max_gamma_angle = 20
        max_forward_threshold_beta = 0.6
        max_forward_threshold_gamma = 0.6

        lin_interp = lambda max_val, min_val, x: max(min(1, (x - min_val)/(max_val-min_val)), 0)

        # get pose angles
        alpha = np.rad2deg( self.poseVector[0] )
        beta = np.rad2deg( self.poseVector[1] )
        gamma = np.rad2deg( self.poseVector[2] ) - 180         # get the solution in the 1st quadrant

        beta_percentage = lin_interp(max_beta_angle, -max_beta_angle, beta)
        gamma_percentage = lin_interp(max_gamma_angle, -max_gamma_angle, gamma)

        beta_classification = PoseClassificationResultValueEnum.FORWARD_FACING
        gamma_classification = PoseClassificationResultValueEnum.FORWARD_FACING

        if (beta_percentage <=  (1 - max_forward_threshold_beta)/2):
            beta_classification = PoseClassificationResultValueEnum.RIGHT_FACING
        elif (beta_percentage >= (1 + max_forward_threshold_beta)/2):
            beta_classification = PoseClassificationResultValueEnum.LEFT_FACING

        if (gamma_percentage <= (1 - max_forward_threshold_gamma)/2):
            gamma_classification = PoseClassificationResultValueEnum.UPWARD_FACING
        elif (gamma_percentage >= (1 + max_forward_threshold_gamma)/2):
            gamma_classification = PoseClassificationResultValueEnum.DOWNWARD_FACING

        # currently not checking corners, beta classification takes priority over gamma classification
        if (beta_classification != PoseClassificationResultValueEnum.FORWARD_FACING):
            return beta_classification
        else:
            return gamma_classification

# draw landmarks (v x 2 matrix) with '+' marker (size)
def cvDrawLandMarks(image, landmarks, color=(0, 0, 255), size=3, thickness=1):

    # get number of landMarks
    n = landmarks.shape[0]

    # draw landmarks
    for i in range(0, n):

        # get (x,y) landmark coords (cast to int)
        x = landmarks[i,0].astype(int)
        y = landmarks[i,1].astype(int)

        # Draw '+' marker centered at each landmark
        cv2.line( image, (x-size, y), (x+size, y), color, thickness)
        cv2.line( image, (x, y-size), (x, y+size), color, thickness)

# draw Delaunay triangles
def showDelaunayTriangles(image, s, triangles, color=(0, 0, 255), thickness=1):

    # get the number of triangles
    ntriangles = triangles.shape[0]

    # for each triangle
    for t in range(0,ntriangles):

      # get indexs of points belonging to the same triangle
      idx = triangles[t,:]

      # get three points
      pt1 = ( s[idx[0],0].astype(int), s[idx[0],1].astype(int) )
      pt2 = ( s[idx[1],0].astype(int), s[idx[1],1].astype(int) )
      pt3 = ( s[idx[2],0].astype(int), s[idx[2],1].astype(int) )

      # draw triangle (from three lines)
      cv2.line(image, pt1, pt2, color, thickness, cv2.LINE_AA)
      cv2.line(image, pt1, pt3, color, thickness, cv2.LINE_AA)
      cv2.line(image, pt2, pt3, color, thickness, cv2.LINE_AA)

## Define CNN network
class Network(nn.Module):

    def __init__(self, nclass=10, pretrained=False):
        super().__init__()                  # call parent's constructor

        # load ResNet34 structure
        self.model = models.resnet34(pretrained=pretrained)

        # freeze all all batch normalization layers
        for name, param in self.model.named_parameters():
            param.requires_grad = False

        # replace last layer (fc) by a fully connected layer w/ nclass
        self.model.fc = nn.Linear(self.model.fc.in_features, nclass)

    # forward pass
    def forward(self, x):
        x = self.model(x)
        return x

# Core module
class rFaceID():
    """
    Core class for the TRUSTID image processing module.
    """

    def __init__(self):
        """
        Default constructor.
        """

        # init version number
        self.version = 0

        # CNN object
        self.net = []

        # init number of labels
        self.nlabels = 0

        # init label names (list of identities)
        self.nlabels = []


        # select CPU/GPU device
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        #print(self._device)

        # load dlib face detector
        self.detector = dlib.get_frontal_face_detector()


        ## 3D Head Pose data ##

        # shape align module
        self.shpAlign = None

        # delaunay triangulation of 2D base mesh
        self.triangles = None

        # sparse rigid 3D head model
        self.s3D = None

        # camera matrix (intrinsics)
        self.K = None

        self.svmClassifier = None
        self.faceEmbeddingNN = None



    def load(self, pretrained_model_filename):
        """
        Loads the class parameters from the pre-trained model state stored in the file system.

        Args:
            pretrained_model_filename: Path to the pretrained model state.
        """
        try:
            # load pretrained model
            state = torch.load( pretrained_model_filename, map_location="cpu")
        except:
            print('invalid model')
            exit(1)

        # load version number
        #self.version = state['version']

        # load number of labels
        self.nlabels = state['nlabels']

        # load lablenames (identities)
        self.labelnames = state['svm'].classes_ #state['labelnames']

        # init CNN network obj
        #self.net = Network( nclass=self.nlabels )

        # load network
        #self.net.load_state_dict( state['state_dict'] )

        # send network to device (CPU/GPU)
        #self.net.to( self.device )

        # enable CNN evaluation mode
        #self.net.eval()

        self.svmClassifier = state['svm']
        self.faceEmbeddingNN = dlib.face_recognition_model_v1('models/dlib_face_recognition_resnet_model_v1.dat')
        self.load_head_pose_model()


    def load_head_pose_model(self):
        """
        Loads 3D head pose model data (shape alignment model + delaunay triangles + 3D head model)
        """
        try:
            # load 2D shape align module
            self.shpAlign = dlib.shape_predictor( "models/ERT68.dat" )

            # load 2D delaunay triangulation
            self.triangles = np.load( "models/triangles.npy" )

            # load sparse 3D head rigid model
            self.s3D = np.load( "models/sparse_s3D.npy" )

            # pre-define focal distance
            f = 2500

            # init camera matrix
            self.K = np.array([ [f, 0, 0],[0, f, 0], [0 ,0 ,1] ], dtype=np.float64)
            #self.K = np.array([ [f, 0, 960],[0, f, 540], [0 ,0 ,1] ], dtype=np.float64)

        except:
            print('error loading head pose data')
            exit(1)



    def detection(self, image: np.array) -> DetectionResult:
        """Analyses the input image for human faces and returns the bounding boxes containing the detected faces.

        Args:
            image: OpenCV RGB image.

        Returns:
            DetectionResult(resultValue = FaceDetectionResultValueEnum.DETECTION_NO_RESULTS) if there's no detected face in the image.
            DetectionResult(resultValue = FaceDetectionResultValueEnum.DETECTION_ONE_RESULT, ret:cvRect) if there's one detected face in the image.
            DetectionResult(resultValue = FaceDetectionResultValueEnum.DETECTION_MULTIPLE_RESULTS) if there's multiple detected faces in the image.
        """
        # face detection
        detections = self.detector(image)

        # found at least one match
        if ( len(detections) > 0 ):
            detection_rects = []
            for d in detections:
                x = max(0, d.left())
                y = max(0, d.top())
                endx = min(d.right(), image.shape[1] )
                endy = min(d.bottom(), image.shape[0] )
                detection_rects.append(np.array([x, y, endx-x, endy-y]))

            return DetectionResult(resultValue = (FaceDetectionResultValueEnum.ONE_RESULT if len(detections) == 1
            else FaceDetectionResultValueEnum.MULTIPLE_RESULTS), bounding_boxes=detection_rects)

        # return no results
        return DetectionResult(resultValue=FaceDetectionResultValueEnum.NO_RESULTS)



    def checkImageQuality(self, image_rgb: np.array, rect: np.array) -> ImageQualityResult:
        """Determines if the detected face image is good enough for the training model.

        Args:
            image: OpenCV RGB image containing the detected face.
            rect: Bounding box coordinates (in cvRect representation) from the face detection algorithm.

        Returns:
            ImageQualityResult(resultValue = IMAGE_QUALITY.VERY_LOW_ILUMINATION) if the image's ilumination is too low.
            ImageQualityResult(resultValue = IMAGE_QUALITY.VERY_HIGH_ILUMINATION) if the image's ilumination is too high.
            ImageQualityResult(resultValue = IMAGE_QUALITY.GOOD_IMAGE) if the image quality is good for training and inference.
        """

        # parameters for checking image quality
        threshold=[0.5, 0.4] # [threshold_for_low_ilumination, threshold_for_high_ilumination]
        bounds=[0, 256] # [min_bound_to_consider, max_bound_to_consider]
        bin_step=4 # step for creating bins

        # crop image
        roi = image_rgb[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])].copy()

        # convert to gray level
        graylevel_img = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)

        # generate bin list
        bin_list = np.arange(start=(0 if bounds[0] is None else max(bounds[0], 0)),
                        stop=(255 if bounds[1] is None else min(bounds[1], 255)),
                        step=bin_step)

        # add 256 to the bin list to make sure that the last bin captures pure white pixels
        hist, _ = np.histogram(graylevel_img, bins=np.append(bin_list, 256))
        cum_dist = np.cumsum(hist)
        cum_dist = cum_dist/cum_dist[-1]

        # assume optimal histogram follows a normal distribution with the given mean and standard dev of LFW dataset images
        mean = 123.4355355363004
        std = 44.324144077811525
        optimal_dist = lambda x : (1/(std*np.sqrt(2*np.pi))*np.exp((-1/2)*((x-mean)/std)**2))
        optimal_disc_dist = np.cumsum(optimal_dist(bin_list))
        optimal_disc_dist /= optimal_disc_dist[-1]

        # check if the difference between the distributions surpasses the predefined threshold
        diff = cum_dist - optimal_disc_dist

        if (abs(np.max(diff)) > threshold[0]):
            result = ImageQualityResult(ImageQualityResultValueEnum.VERY_LOW_ILUMINATION,
            image_rgb, rect, threshold, bounds, roi, graylevel_img, bin_list, hist, cum_dist, optimal_disc_dist)
        elif (abs(np.min(diff)) > threshold[1]):
            result = ImageQualityResult(ImageQualityResultValueEnum.VERY_HIGH_ILUMINATION,
            image_rgb, rect, threshold, bounds, roi, graylevel_img, bin_list, hist, cum_dist, optimal_disc_dist)
        else:
            result = ImageQualityResult(ImageQualityResultValueEnum.GOOD_IMAGE,
            image_rgb, rect, threshold, bounds, roi, graylevel_img, bin_list, hist, cum_dist, optimal_disc_dist)

        return result



    def is_low_contrast_naive(self, image, rect, threshold=0.5):
        """ - naive/basic implementation of previous is_low_contrast(.) function
            - only allows to detect low-light situations
        Args:
            image: OpenCV RGB image containing the detected face.
            rect: Bounding box coordinates (in cvRect representation) from the face detection algorithm.
            [threshold]: 1/3 histogram area cutoff value
        Returns:
            True if the image has low contrast, false otherwise.
        """

        # crop image
        roi = image[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])].copy()

        # convert to gray level
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # compute the normalized histogram
        bin_list = np.arange(256)
        hist, _ = np.histogram(gray_roi, bins=256)

        # normalize histogram [0,1]
        hist = hist / (rect[2]*rect[3])

        # debug
        #plt.clf()
        #plt.plot(hist)
        #plt.pause(0.05)

        # add histogram values up to grey intensity 85 (1/3 histogram)
        partial_hist_sum = np.sum( hist[0:85] )
        #print("partial_hist_sum =", partial_hist_sum)

        # check if the histogram test area overcomes the cutoff threshold (percentage)
        if( partial_hist_sum > threshold ): return True
        else: return False

    # Apply CNN identity prediction
    #def recognition(self, image, rect, fr_threshold=0.9):
    def recognitionCNN(self, image, rect, fr_threshold=0.9):
        """Runs inference on the image containing the detected face in order to identify the user in the image.

        Args:
            image: OpenCV RGB image containing the detected face.
            rect: Bounding box coordinates from the face detection algorithm (cvRect format).
            threshold: Threshold for matching an identity.
        Returns:
            RecognitionResult(resultValue=FaceRecognitionResultValueEnum.NO_MATCH)
        """

        # run only w/ valid detections
        if (rect is not None):

            # get rectangle attributes
            x, y, w, h = rect

            # crop image
            imagecrop = image[y:y+h, x:x+w]

            # resize image
            rimage = cv2.resize(imagecrop, (224, 224), cv2.INTER_LINEAR)

            # -> convert to tensor (in mini-batch format)  [3x224x224]
            timage = TF.to_tensor(rimage)

            # normalize image = (image - mean) / std
            timage = TF.normalize(timage, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5) )

            # disable backward propagation calculation
            with torch.no_grad():

                # add extra dim (mini-batch format)
                img = torch.unsqueeze(timage, 0)
                #print(img.shape)

                # send to device
                img = img.to(self.device)

                #------------------------------
                # network forward pass
                #------------------------------
                prediction = self.net( img ).cpu().squeeze()

                # send predition back to CPU and apply softmax to get probabilities
                probabilities = nn.functional.softmax(prediction)

                # grab label and prediction score
                sortedProbabilities = prediction.argsort(descending=True)
                # decode identity name (string)
                scorePerIdentity = [{FaceRecognitionDictKeyEnum.IDENTITY_KEY: self.labelnames[idx.item()], FaceRecognitionDictKeyEnum.SCORE_KEY: probabilities[idx].item()} for idx in sortedProbabilities]

                identitiesWithGoodScore = np.sum([1 if identity[FaceRecognitionDictKeyEnum.SCORE_KEY] >= fr_threshold else 0 for identity in scorePerIdentity ])

                # checks if there's more than one identity with significant probability, if so then return invalid match
                if (identitiesWithGoodScore == 1):
                    return RecognitionResult(FaceRecognitionResultValueEnum.FOUND_MATCH, scorePerIdentity[0][FaceRecognitionDictKeyEnum.IDENTITY_KEY], scorePerIdentity[0][FaceRecognitionDictKeyEnum.SCORE_KEY], scorePerIdentity)
                elif (identitiesWithGoodScore > 1):
                    return RecognitionResult(FaceRecognitionResultValueEnum.INVALID_MATCH, None, None, scorePerIdentity)
                else:
                    return RecognitionResult(FaceRecognitionResultValueEnum.NO_MATCH, None, None, scorePerIdentity)

        else:
            return RecognitionResult(FaceRecognitionResultValueEnum.NO_MATCH, None, None, None)


    def recognition(self, image, rect, fr_threshold=0.9):
        # convert cvRect to dlib rectangle
        drect = dlib.rectangle( rect[0], rect[1], rect[2] + rect[0], rect[3] + rect[1])

        # run 2D face alignment (ERT w/ 68 landmarks)
        shape = self.shpAlign(image, drect)
        face_descriptor = np.asarray(self.faceEmbeddingNN.compute_face_descriptor(image, shape)).reshape(1, -1)
        confidenceScores = np.squeeze(self.svmClassifier.decision_function(face_descriptor))
        #confidenceScores = np.exp(confidenceScores)/np.sum(np.exp(confidenceScores))

        scorePerIdentity = sorted([{FaceRecognitionDictKeyEnum.IDENTITY_KEY: self.labelnames[idx], FaceRecognitionDictKeyEnum.SCORE_KEY: score} for idx, score in enumerate(confidenceScores)], key = lambda x: -x[FaceRecognitionDictKeyEnum.SCORE_KEY])
        identitiesWithGoodScore = np.sum([1 if identity[FaceRecognitionDictKeyEnum.SCORE_KEY] >= 0 else 0 for identity in scorePerIdentity ])

        # checks if there's more than one identity with significant probability, if so then return invalid match
        if (identitiesWithGoodScore == 1):
            return RecognitionResult(FaceRecognitionResultValueEnum.FOUND_MATCH, scorePerIdentity[0][FaceRecognitionDictKeyEnum.IDENTITY_KEY], scorePerIdentity[0][FaceRecognitionDictKeyEnum.SCORE_KEY], scorePerIdentity)
        elif (identitiesWithGoodScore > 1):
            return RecognitionResult(FaceRecognitionResultValueEnum.INVALID_MATCH, None, None, scorePerIdentity)
        else:
            return RecognitionResult(FaceRecognitionResultValueEnum.NO_MATCH, None, None, scorePerIdentity)


    # estimate 3D head pose
    def estimate_head_pose(self, image, rect):
        """ Estimate 3D head pose.
        Args:
            image: OpenCV RGB image containing a detected face.
            rect: Bounding box coordinates from the face detection algorithm (cvRect format).
        Returns:
            PoseEstimationResult
        """

        # check if head pose data is loaded (and loads if required)
        if( self.s3D is None ):
            # load 3D head pose model(s)
            self.load_head_pose_model()


        # init success flag (pose computation)
        returnFlag = PoseEstimationResultValueEnum.SUCCESS

        # init 3D pose vector: [alpha (Rz), beta (Ry), gamma (Rz), tx, ty, tz]
        pose = np.zeros((6,1), dtype=np.float64)

        # init scaled distance to the camera
        sdist = -1.0

        # init 2D shape (v x 2) matrix
        s = np.zeros( (68,2), dtype=np.float64)


        # if valid rectangle
        if (rect is not None):

            # convert cvRect to dlib rectangle
            drect = dlib.rectangle( rect[0], rect[1], rect[2] + rect[0], rect[3] + rect[1])

            # run 2D face alignment (ERT w/ 68 landmarks)
            shape = self.shpAlign(image, drect)

            # accept only valid shapes
            if( len( shape.parts() ) == 68 ):
                # copy landmarks to (v x 2) matrix (s)
                for i in range(0, 68):
                    s[i,0] = np.float64( shape.part(i).x )
                    s[i,1] = np.float64( shape.part(i).y )

                # display 2D mesh (debug)
                #showDelaunayTriangles(image, s, self.triangles, color=(0, 0, 255), thickness=1)
                #cvDrawLandMarks(image, s, (255,255,255), size=3, thickness=1)

                # update camera's principal point (deal w/ unknown image size)
                self.K[0,2] = image.shape[1]/2      # cx
                self.K[1,2] = image.shape[0]/2      # cy

                # ---------------------
                # estimate 3D Pose (Levenberg-Marquardt optimization)
                retVal, rvecs, tvecs = cv2.solvePnP(self.s3D, s, self.K, distCoeffs=None, useExtrinsicGuess = False, flags=cv2.SOLVEPNP_ITERATIVE)

                # successful recovery of 3D pose
                if (retVal):

                    # Get 3x3 Rotation matrix
                    R = cv2.Rodrigues( rvecs )[0]

                    # Compute the Euler Angles Z-Y-X (Inverse Kinematics)
                    alpha = np.arctan2( R[1,0], R[0,0] )
                    beta = np.arctan2( -R[2,0], np.sqrt( R[0,0]*R[0,0] + R[1,0]*R[1,0] ) )
                    gamma = np.arctan2( R[2,1], R[2,2] )

                    # Ensure gamma angle (Rx) discontinuity around -pi
                    if( gamma < 0 ):
                        gamma = gamma + 2 * np.pi

                    # compute scaled distance to the camera
                    sdist = np.sqrt(  tvecs[2,0]*tvecs[2,0] + tvecs[1,0]*tvecs[1,0] + tvecs[0,0]*tvecs[0,0] ) / self.K[0,0] * 100

                    # enable flag
                    success = True

                    #print("alpha ", alpha, "beta ", beta, "gamma", gamma)
                    #print("[deg]: alpha ", np.rad2deg( alpha ), "beta ", np.rad2deg( beta ), "gamma", np.rad2deg( gamma ) - 180, "dist", sdist )

                    # copy pose parameters
                    pose[0] = alpha
                    pose[1] = beta
                    pose[2] = gamma
                    pose[3:] = tvecs
                    #print(pose)
            else:
                returnFlag = PoseEstimationResultValueEnum.ERR_NOT_ENOUGH_POINTS
        else:
            returnFlag = PoseEstimationResultValueEnum.ERR_INVALID_DETECTION

        if (success):
            return PoseEstimationResult(returnFlag, pose, sdist, s)
        else:
            return PoseEstimationResult(returnFlag)

    # display 3D pose axis (projected axis)
    def show_head_pose(self, image, pose, show_axis=True, show_cube=False, thickness = 6):
        """ Display a 3D pose representation (oriented axis and/or cube)
        Args:
            image - OpenCV image to draw (BGR format)
            pose - estimated pose vector
            show_axis - (boolean) enable/disable 3D reference axis
                        (colors: x axis -> red, y axis -> green, z axis -> blue))
            show_cube - (boolean) enable/disable 3D cube around the head (color: violet)
            thickness - line thickness value
        """

        # define axis scale (length in mm expressed w.r.t. the head model)
        qscale = 1.25e2

        # get pose angles (alpha (a), beta (b), gamma (g))
        a, b, g = pose[:3]

        # compute 3D Rotation Matrices
        Rx = np.array([ [1, 0, 0], [0, np.cos(g), -np.sin(g)], [0, np.sin(g), np.cos(g)] ], dtype=np.float64)
        Ry = np.array([ [np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0 , np.cos(b)] ], dtype=np.float64)
        Rz = np.array([ [np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1] ], dtype=np.float64)

        # compute full rotation matrix
        R = Rz @ Ry @ Rx

        # get 3D translation
        t = pose[3:]


        # display pose oriented axis
        if( show_axis ):

            # define origin and 3D unit vectors
            ref3D = np.array([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]] , dtype=np.float64) * qscale

            # apply Perspective Projection: S = ( K * [R|t] * [ref3D; ones(1, 4)] )'
            S = np.transpose( self.K @ np.hstack((R,t)) @ np.vstack( (ref3D, np.ones((1, 4))) ) )

            # normalize by the 3rd coord
            spx = S[:,0] / S[:,2]
            spy = S[:,1] / S[:,2]

            # define thickness of axis lines
            #thickness = 6

            # get the 3D origin (0,0,0) projection in the image -> (ox,oy)
            ox = spx[0].astype(int)
            oy = spy[0].astype(int)

            # get the (1,0,0) projection in the image -> (ux,uy)
            ux = spx[1].astype(int)
            uy = spy[1].astype(int)
            #cv2.line( image, (ox, oy), (ux, uy), color=(0, 0, 255), thickness=thickness)
            cv2.arrowedLine( image, (ox, oy), (ux, uy), color=(0, 0, 255), thickness=thickness, tipLength=0.05)

            # get the (0,1,0) projection in the image -> (sx,sy)
            sx = spx[2].astype(int)
            sy = spy[2].astype(int)
            #cv2.line( image, (ox, oy), (sx, sy), color=(0, 255, 0), thickness=thickness)
            cv2.arrowedLine( image, (ox, oy), (sx, sy), color=(0, 255, 0), thickness=thickness, tipLength=0.05)

            # get the (0,0,1) projection in the image -> (vx,vy)
            vx = spx[3].astype(int)
            vy = spy[3].astype(int)
            #cv2.line( image, (ox, oy), (vx, vy), color=(255, 0, 0), thickness=thickness)
            cv2.arrowedLine( image, (ox, oy), (vx, vy), color=(255, 0, 0), thickness=thickness, tipLength=0.05)

        # display 3D cube
        if( show_cube ):

            # define cube (half) edge scale (mm)
            qscale = 75

            # define 3D cube vertexs (scaled)
            cubeRef = np.array([
                    [1, 1, 1],      # A #[0]
                    [-1, 1, 1],     # B #[1]
                    [-1, -1, 1],    # C #[2]
                    [1, -1, 1],     # D #[3]
                    [1, -1, -1],    # E #[4]
                    [1, 1, -1],     # F #[5]
                    [-1, 1, -1],    # G #[6]
                    [-1, -1, -1]    # H #[7]
            ], dtype=np.float64) * qscale

            # select coords of forward facing plane
            #cube = cubeRef[[0,1,2,3,0],:].T

            # select cube (index) vertexs for w/ line drawing (i.e. pairs of points)
            cube = cubeRef[[0,1,2,3,0,5,6,1,6,7,2,7,4,3,4,5],:].T

            # apply Perspective Projection: S = ( K * [R|t] * [cube; ones(1, 16)] )'
            S = np.transpose( self.K @ np.hstack((R,t)) @ np.vstack( (cube, np.ones((1, 16))) ) )

            # normalize by the 3rd coord
            spx = S[:,0] / S[:,2]
            spy = S[:,1] / S[:,2]

            # for each pair of cube vertexs
            for i in range(0,15,1):

                # select current point
                px = spx[i].astype(int)
                py = spy[i].astype(int)

                # select next point
                nx = spx[i+1].astype(int)
                ny = spy[i+1].astype(int)

                # draw cube edge line
                cv2.line( image, (px, py), (nx, ny), color=(255, 0, 128), thickness=thickness)
