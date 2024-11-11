import os
from gui.settings.Settings import *

SectionLoc = retreiveSectionLoc()
SectionSizes = retreiveSectionSizes()
cam = cameraSource()

def addNewPerson(employee_id):
    openCamera = cv2.VideoCapture(cam)
    ret, frame = openCamera.read()

    while ret:
        ret, frame = openCamera.read()
        id_str = ''
        cv2.namedWindow('ShowUser', cv2.WINDOW_KEEPRATIO)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        DIR = 'models\\face_model\\train'
        nextid = len([employee_id for employee_id in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, employee_id))])
        cv2.imshow('ShowUser', frame)
        cv2.resizeWindow('ShowUser', SectionSizes["cameraframe"][0], SectionSizes["cameraframe"][1])
        cv2.moveWindow('ShowUser', SectionLoc["bodyframe1"][0], SectionLoc["bodyframe1"][1])

        """
        TODO: Add enrol button and cancel button
        """
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite('models\\face_model\\train\\{}.jpg'.format(employee_id), frame)
            print("ID: " + str(nextid + 1))
            break
        elif cv2.waitKey(1) & 0xFF == 27:
            break

    openCamera.release()
    cv2.destroyAllWindows()

# addNewPerson(input("Enter Employee Id: "))
