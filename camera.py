import cv2
import datetime
import os


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        self.frame_rate = self.video.get(cv2.CAP_PROP_FPS)
        self.frame_width = int(self.video.get(3))
        self.frame_height = int(self.video.get(4))
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d")
        file_dir = os.path.dirname(os.path.abspath(__file__))
        self.out = cv2.VideoWriter(file_dir + '/' + now + '.avi',
                                   cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),  # Could also use XVID
                                   12,
                                   (self.frame_width, self.frame_height))

    """
    When the class stops, we release and clear all memory instantiated by opencv
    """
    def __del__(self):
        self.video.release()
        self.out.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def record(self):
        ret, frame = self.video.read()
        if ret:
            self.out.write(frame)