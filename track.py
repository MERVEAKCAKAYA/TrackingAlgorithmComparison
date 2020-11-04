from __future__ import print_function
import cv2

global tracker
global multiTracker
tracker_type="CSRT"

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
if tracker_type == 'CSRT':
    tracker = cv2.TrackerCSRT_create()
if tracker_type=='MOSSE':
    tracker = cv2.TrackerMOSSE_create()

num=175
save_video=True

faceCascade = cv2.CascadeClassifier("facecascades/haarcascade_frontalface_alt.xml")
faceprofileCascade = cv2.CascadeClassifier("facecascades/haarcascade_profileface.xml")


def createMultitracker(bboxes, frame):
    multiTracker = cv2.MultiTracker_create()

    for bbox in bboxes:
        multiTracker.add(tracker, frame, bbox)
    return multiTracker


def select():
    bboxes.clear()
    while True:
        success, frame_s = cap.read()

        gray = cv2.cvtColor(frame_s, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        facesP = faceprofileCascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            bboxes.append((x, y, w, h))
            colors.append((255, 255, 255))
            break
        for (x, y, w, h) in facesP:
            bboxes.append((x, y, w, h))
            colors.append((255, 255, 255))

        if len(bboxes) > 0:
            break
        else:
            cv2.rectangle(frame_s, (int(xc - num), int(yc - num)), (int(xc + num), int(yc + num)), ((255, 255, 255)), 1,
                          1)
            cv2.imshow('MultiTracker', frame_s)
            if cv2.waitKey(1) & 0xFF == 11111:
                pass
    return bboxes

def select2(frame):
    bboxes.clear()
    bbox=cv2.selectROI("MultiTracker",frame)
    bboxes.append(bbox)
    colors.append((255, 255, 255))
    return bboxes

def draw(multiTracker):
    if cap.isOpened():
        success, frame = cap.read()
        if not success:
            return
        try:
            success, boxes = multiTracker.update(frame)
        except:
            return frame
        # draw tracked objects
        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
            #cv2.rectangle(frame, (int(xc - num), int(yc - num)), (int(xc + num), int(yc + num)), ((255, 255, 255)), 1,1)

        return frame


def reset(frame):
    global tracker
    global multiTracker
    multiTracker = None
    tracker = None
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
    if tracker_type == 'CSRT':
        tracker = cv2.TrackerCSRT_create()
    if tracker_type=='MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    
    bboxes = select2(frame)
    multiTracker = createMultitracker(bboxes, frame)


if __name__ == '__main__':

    global multiTracker
    name="tennis4"
    #a="/Downloads/"+name+".mp4"

    a = 0

    cap = cv2.VideoCapture(a)
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH);
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT);
    for x in range(1,3):
        success, frame = cap.read()
    success, frame = cap.read()

    if save_video: 
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        out = cv2.VideoWriter(name+"_"+tracker_type+".mp4", fourcc, 30, (int(w),int(h)))

    height = frame.shape[0]
    width  = frame.shape[1]

    xc, yc = width / 2, height / 2

    bboxes = []
    colors = []

    bboxes = select2(frame)

    multiTracker = createMultitracker(bboxes, frame)

    cv2.namedWindow("MultiTracker")
    x = "hello"

    while True:
        img = draw(multiTracker)
        #cv2.rectangle(frame, (int(xc - num), int(yc - num)), (int(xc + num), int(yc + num)), ((255, 255, 255)), 1, 1)
        cv2.imshow('MultiTracker', img)
        if save_video:
                out.write(img)
        if cv2.waitKey(1) & 0xFF == 110:
            reset(img)

    out.release()