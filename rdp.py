import numpy as np
import cv2


cv2.namedWindow("Demo")


def do_nothing(val):
    pass


cv2.createTrackbar("eps", 'Demo', 0, 100, do_nothing)

eps = 0

drawing = np.zeros((600, 800, 3))


use_backscreen = True

cv2.putText(drawing, "Please draw some curves", (100, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
drawing_backscreen = drawing.copy()

pre_x, pre_y = 0, 0
is_mouse_down = False
x_arr = []
y_arr = []

colors = [
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255)
]


def RDP(points, left, right, eps=20):
    if left > right:
        return None
    idx = None
    max_d = 0
    for i in range(left, right):
        d = np.cross(points[right]-points[left], points[i] -
                     points[left])/np.linalg.norm(points[right]-points[left])
        d = abs(d)
        if d > max_d:
            max_d = d
            idx = i
    if max_d > eps:
        left_arr = RDP(points, left, idx, eps)
        right_arr = RDP(points, idx, right, eps)
        return np.concatenate([left_arr[:-1], right_arr])
    return np.array([points[left], points[right]])


def mouse_callback(event, x, y, flags, param):
    global drawing, pre_x, pre_y, is_mouse_down, x_arr, y_arr, eps
    if event == cv2.EVENT_LBUTTONDOWN:
        pre_x, pre_y = x, y
        is_mouse_down = True
        x_arr = []
        y_arr = []
    elif event == cv2.EVENT_LBUTTONUP:
        is_mouse_down = False

    elif event == cv2.EVENT_MOUSEMOVE:
        if is_mouse_down:
            cv2.line(drawing, (pre_x, pre_y), (x, y), (255, 255, 255))
            x_arr.append(x)
            y_arr.append(y)
            pre_x, pre_y = x, y


cv2.setMouseCallback("Demo", mouse_callback)

while True:
    if not is_mouse_down and x_arr:
        eps = cv2.getTrackbarPos("eps", "Demo")
        drawing_backscreen = np.zeros((600, 800, 3))
        cv2.putText(drawing_backscreen, "Please draw a curve", (100, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        points = np.array(list(zip(x_arr, y_arr)))
        cv2.polylines(drawing_backscreen, np.int32(
            [points]), False, (255, 255, 255), thickness=1)
        points = RDP(points, 0, len(points)-1, eps)
        cv2.polylines(drawing_backscreen, np.int32(
            [points]), False, (0, 255, 0), thickness=2)
        for point in points:
            cv2.circle(drawing_backscreen, point, 5, (255,0,0), -1)
        drawing = drawing_backscreen.copy()

    cv2.imshow("Demo", drawing)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
