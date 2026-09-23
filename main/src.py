import cv2
import mediapipe as mp
import math
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# -----------------------------
# Initialize Audio
# -----------------------------
devices = AudioUtilities.GetSpeakers()

interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)

volume = cast(interface, POINTER(IAudioEndpointVolume))


# -----------------------------
# Initialize Camera
# -----------------------------
cap = cv2.VideoCapture(0)


# -----------------------------
# Initialize MediaPipe Hands
# -----------------------------
mphands = mp.solutions.hands
hands = mphands.Hands()

mpdraw = mp.solutions.drawing_utils


# -----------------------------
# Main Loop
# -----------------------------
while True:

    success, img = cap.read()

    if not success:
        continue

    # Convert BGR image to RGB
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process hand landmarks
    results = hands.process(imgrgb)

    if results.multi_hand_landmarks:

        for handlms in results.multi_hand_landmarks:

            lmlist = []

            # Get landmark coordinates
            for id, lm in enumerate(handlms.landmark):

                h, w, c = img.shape

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                lmlist.append([id, cx, cy])

            # Draw hand landmarks
            mpdraw.draw_landmarks(
                img,
                handlms,
                mphands.HAND_CONNECTIONS
            )

            # Check if landmarks are available
            if lmlist:

                # Thumb tip
                x1, y1 = lmlist[4][1], lmlist[4][2]

                # Index finger tip
                x2, y2 = lmlist[8][1], lmlist[8][2]

                # Draw circles
                cv2.circle(
                    img,
                    (x1, y1),
                    15,
                    (255, 0, 255),
                    cv2.FILLED
                )

                cv2.circle(
                    img,
                    (x2, y2),
                    15,
                    (255, 0, 255),
                    cv2.FILLED
                )

                # Draw line between thumb and index finger
                cv2.line(
                    img,
                    (x1, y1),
                    (x2, y2),
                    (100, 255, 100),
                    5
                )

                # Calculate distance
                distance = math.hypot(
                    x2 - x1,
                    y2 - y1
                )

                # Show middle point when distance is outside range
                if distance < 70 or distance > 200:

                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2

                    cv2.circle(
                        img,
                        (center_x, center_y),
                        15,
                        (255, 0, 0),
                        cv2.FILLED
                    )

                # Get system volume range
                volrange = volume.GetVolumeRange()

                minvol = volrange[0]
                maxvol = volrange[1]

                # Convert finger distance to system volume
                vol = np.interp(
                    distance,
                    [70, 200],
                    [minvol, maxvol]
                )

                volume.SetMasterVolumeLevel(
                    vol,
                    None
                )

                # Convert distance to percentage
                volper = np.interp(
                    distance,
                    [70, 200],
                    [0, 100]
                )

                # Display volume percentage
                cv2.putText(
                    img,
                    str(int(volper)),
                    (225, 100),
                    cv2.FONT_HERSHEY_COMPLEX,
                    5,
                    (0, 0, 300)
                )

    # Display camera window
    cv2.imshow("Image", img)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# -----------------------------
# Release Resources
# -----------------------------
cap.release()
cv2.destroyAllWindows()