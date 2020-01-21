import cv2
import sys

# camera number
# /dev/video0 = 0
# if input vifeo dir, work to play video
CAM_ID = "C:/Users/EUNU/Desktop/현지학기제/주차별 UCC/최종본 저화질1.mp4"

# state of tracking function
# perceive face
TRACKING_STATE_CHECK = 0
# init tracking function
TRACKING_STATE_INIT = 1
# work tracking
TRACKING_STATE_ON = 2

# check openCV version
(major_ver, minore_ver, subminor_ver) = (cv2.__version__).split('.')

if __name__ == '__main__':
    # print version
    print((cv2.__version__).split('.'))

    # choice tracking function
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    # base KCF is more fester
    tracker_type = tracker_types[2]

    # openCV is deferent that function name by version
    # if int(minore_ver) < 3:
    #     # if openCV version is under 3.2
    #     tracker = cv2.Tracker_create(tracker_type)
    # else:
        # over 3.3
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()


# opne the camera
    video = cv2.VideoCapture(CAM_ID)

    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # create face recognition function
    face_cascade = cv2.CascadeClassifier("E:/python/video-face-blur/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
    # load haar for face recoginition
    # face_cascade.load('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

    # var for save tracking state
    TrackingState = 0
    # var for save tracking area
    TrackingROI = (0,0,0,0)

    # Start program
    while True:
        # read 1 frame from camera
        ok, frame = video.read()
        if not ok:
            break
        h, w, l = frame.shape
        nh = int(h/5)
        nw = int(w/5)
        frame = cv2.resize(frame, (nw, nh))
        # if success face tracking
        if TrackingState == TRACKING_STATE_CHECK:
            # Change to gray
            grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # equalize histogram
            grayframe = cv2.equalizeHist(grayframe)
            # face recognition
            faces = face_cascade.detectMultiScale(grayframe, 1.1, 5, 0, (30, 30))

            # Catch face
            if len(faces) > 0:
                # Get location, scale from catched face
                x,y,w,h = faces[0]
                TrackingROI = (x,y,w,h)
                # Create face rectangle to green
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3, 4, 0)
                # Change state of tracking information
                TrackingState = TRACKING_STATE_INIT
                print('det w : %d ' %w + 'h : %d' % h)
        # initalize tracking
        # when recognized face
        elif TrackingState == TRACKING_STATE_INIT:
            # Initalize tracking function
            # input location, scale
            ok = tracker.init(frame, TrackingROI)
            if ok:
                TrackingState = TRACKING_STATE_ON
                print("tracking init succeeded")
            else:
                TrackingState = TRACKING_STATE_CHECK
                print("tracking init failed")
        elif TrackingState == TRACKING_STATE_ON:
            # Tracking
            ok, TrackingROI = tracker.update(frame)
            if ok:
                p1 = (int(TrackingROI[0]), int(TrackingROI[1]))
                p2 = (int(TrackingROI[0] + TrackingROI[2]), int(TrackingROI[1] + TrackingROI[3]))
                # apply to screen as blue box
                cv2.rectangle(frame, p1, p2, (255,0,0), 2,1)
                print("Success x %d " %(int(TrackingROI[0])) + "y %d " %(int(TrackingROI[2])) +
                "w %d " %(int(TrackingROI[2])) + "h %d " %(int(TrackingROI[3])))
            else:
                print("Tracking failed")
                TrackingState = TRACKING_STATE_CHECK

        # express camera video to screen that blue box if tracked face
        cv2.imshow("Tracking", frame)

        # If you press ESC key then shut down
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
