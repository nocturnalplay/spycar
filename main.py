from handGesture import hand
import cv2
import math
import json
import sys
from websockets import serve
import asyncio
import os

# ----------------------------------------------------------------
# car gesture arch
# ----------------------------------------------------------------

# find the actual percentage for the inbetween values

host = sys.argv[1]
port = sys.argv[2]


def findPercents(inp, mi, ma, v):
    va = (inp - mi) * 100 / (ma - mi)
    if v == 100:
        va = v - va
    if va > 100:
        return 100
    elif va < 0:
        return 0
    else:
        return int(va)


cam = cv2.VideoCapture(0)
Wcam = 640
Hcam = 480
cam.set(3, Wcam)
cam.set(4, Hcam)

hands = hand.Hand(max_hands=2)


async def Handler(websocket):
    print("waiting for the client messgae")
    print("data from the client:", await websocket.recv())
    try:
        while 1:
            success, img = cam.read()
            res = hand.DetectHands(img, hands)
            if not res['status']:
                break
            img = res["image"]
            left = res["data"]["left"]
            right = res["data"]["right"]
            enddata = {}
            if right:
                # circle shape x and y axis point
                cv2.circle(img, (right[4][0], right[4][1]),
                           8, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (right[8][0], right[8][1]),
                           8, (0, 255, 0), cv2.FILLED)
                # data for the car
                enddata["acspeed"] = findPercents(math.hypot(
                    right[4][0]-right[8][0], right[4][1]-right[8][1]), 20, 100, 0)
                if enddata["acspeed"] > 0:
                    if right[12][1] < right[11][1]:
                        enddata["acdirection"] = "backward"
                        # lines for the eache shape in rgb
                        cv2.line(img, (right[4][0], right[4][1]),
                                 (right[8][0], right[8][1]), (0, 0, 0), 2)
                    else:
                        enddata["acdirection"] = "forward"
                        # lines for the eache shape in rgb
                        cv2.line(img, (right[4][0], right[4][1]),
                                 (right[8][0], right[8][1]), (255, 255, 255), 2)
                else:
                    enddata["acdirection"] = "neutral"
            if left:
                # circle shape x and y axis point
                cv2.circle(img, (left[4][0], left[4][1]),
                           8, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (left[8][0], left[8][1]),
                           8, (0, 255, 0), cv2.FILLED)
                # data for the car
                enddata["rospeed"] = findPercents(math.hypot(
                    left[4][0]-left[8][0], left[4][1]-left[8][1]), 30, 100, 0)
                if enddata["rospeed"] > 0:
                    if left[4][0] < left[8][0]:
                        enddata["rodirection"] = "left"
                        # lines for the eache shape in rgb
                        cv2.line(img, (left[4][0], left[4][1]),
                                 (left[8][0], left[8][1]), (0, 0, 0), 2)
                    elif left[4][0] > left[8][0]:
                        enddata["rodirection"] = "right"
                        # lines for the eache shape in rgb
                        cv2.line(img, (left[4][0], left[4][1]),
                                 (left[8][0], left[8][1]), (255, 255, 255), 2)
                else:
                    enddata["rodirection"] = "neutral"
            d = json.dumps(enddata)
            await websocket.send(d)
            cv2.imshow("Images", img)
            cv2.waitKey(1)
    except KeyboardInterrupt:
        cam.release()
        cv2.destroyAllWindows()

    # kill the process
    cam.release()
    cv2.destroyAllWindows()
    sys.exit()


async def main():
    print("server created on 9000 port")
    async with serve(Handler, host, port, ping_interval=None):
        await asyncio.Future()  # run forever

asyncio.run(main())
