import pydobot
import ast
import cv2
import numpy as np
from operator import itemgetter

colorData_initial = []
colorData_final = []
position_log = []
position_skip_log = []

def camera_leveling_setup():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        W = None
        H = None
        if W is None or H is None:
            (H, W) = frame.shape[:2]
        cv2.line(frame, ((W//2)-60, 0), ((W//2)-60, H), (255,183,197), 2)
        cv2.imshow("frame",frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

def color_detection():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    x = 0
    while x < 250 :
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # define the list of boundaries red,green,blue,yellow
        boundaries = [
            ([0, 140, 157], [12, 183, 181]),
            ([33, 65, 116], [73, 201, 230]),
            ([61, 164, 116], [115, 222, 180]),
            ([21, 62, 62], [38, 198, 231])
        ]
        str_color = ["Red", "Green", "Blue", "Yellow"]
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        # loop over the boundaries
        for idx_color,(lower, upper) in enumerate(boundaries):
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype = "uint8")
            # find the colors within the specified boundaries and apply
            # the mask
            mask = cv2.inRange(image, lower, upper)
            median = cv2.medianBlur(mask,5)
            output = cv2.bitwise_and(image, image, mask = median)
            contours , _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            for i,c in enumerate(contours):
                area = cv2.contourArea(c)
                if area < 650:
                    continue
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.intp(box)
                cv2.drawContours(image, [box], 0, (221, 160, 221), 3)
                M = cv2.moments(c)
                print(M)
                try:
                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])
                except:
                    cx = 0
                    cy = 0
                print('center x=%.2f,y=%.2f'%(cx,cy))
                print(str_color[idx_color])
                if(cx < 260 and x > 248):
                    colorData_initial.append([str_color[idx_color],cx,cy])
                elif(cx > 260 and x > 248):
                    colorData_final.append([str_color[idx_color],cx,cy])
                cv2.circle(image,(cx,cy),5,(255,255,255),-1)
                cv2.putText(image,str_color[idx_color],(cx-25,cy-25),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2)
                # show the images
        cv2.imshow("images", np.hstack([image, output,frame]))
        cv2.waitKey(10)
        x = x + 1
    cv2.destroyAllWindows()

def stacking_system():
    zo = -48 #get z origin value from user
    z = 28.862 #get z value from user(height of z)
    red_counter = 0
    green_counter = 0
    blue_counter = 0
    yellow_counter = 0
    object_position_i = []
    object_position_f = []
    object_sort_i = []
    object_sort_f = []
    red_z = []
    green_z = []
    blue_z = []
    yellow_z = []
    for i in range(len(colorData_initial)):
        color_string = colorData_initial[i][0]
        center_x = colorData_initial[i][1]
        if(color_string =="Red"):
            red_counter+=1
            zr = zo + (red_counter * z)
            red_z.append(zr)
            colorlist = ['Color','Positionx']
            pixelposition = ['RED',center_x]
            object_position_i = dict(zip(colorlist, pixelposition))
            object_sort_i.append(object_position_i)  
        elif(color_string == "Green"):
            green_counter+=1
            zg = zo + (green_counter * z)
            green_z.append(zg)
            colorlist = ['Color','Positionx']
            pixelposition = ['GREEN',center_x]
            object_position_i = dict(zip(colorlist, pixelposition))
            object_sort_i.append(object_position_i)    
        elif(color_string == "Blue"):
            blue_counter+=1
            zb = zo + (blue_counter * z)
            blue_z.append(zb)
            colorlist = ['Color','Positionx']
            pixelposition = ['BLUE',center_x]
            object_position_i = dict(zip(colorlist, pixelposition))
            object_sort_i.append(object_position_i)    
        elif(color_string == "Yellow"):
            yellow_counter+=1
            zy = zo + (yellow_counter * z)
            yellow_z.append(zy)
            colorlist = ['Color','Positionx']
            pixelposition = ['YELLOW',center_x]
            object_position_i = dict(zip(colorlist, pixelposition))
            object_sort_i.append(object_position_i)
    print("object_sort_i:",object_sort_i)
    object_sort_i = sorted(object_sort_i, key=itemgetter('Positionx'), reverse=True)

    for j in range(len(colorData_final)):
        color_string = colorData_final[j][0]
        center_x = colorData_final[j][1]
        if(color_string =="Red"):
            colorlist = ['Color','Positionx']
            pixelposition = ['RED',center_x]
            object_position_f = dict(zip(colorlist, pixelposition))
            object_sort_f.append(object_position_f)  
        elif(color_string == "Green"):
            colorlist = ['Color','Positionx']
            pixelposition = ['GREEN',center_x]
            object_position_f = dict(zip(colorlist, pixelposition))
            object_sort_f.append(object_position_f)    
        elif(color_string == "Blue"):
            colorlist = ['Color','Positionx']
            pixelposition = ['BLUE',center_x]
            object_position_f = dict(zip(colorlist, pixelposition))
            object_sort_f.append(object_position_f)    
        elif(color_string == "Yellow"):
            colorlist = ['Color','Positionx']
            pixelposition = ['YELLOW',center_x]
            object_position_f = dict(zip(colorlist, pixelposition))
            object_sort_f.append(object_position_f)
    print("object_sort_f:",object_sort_f)
    object_sort_f = sorted(object_sort_f, key=itemgetter('Positionx'), reverse=False)
    print("Initial_Value:",object_sort_i)
    print("Final_Value:",object_sort_f)
    for m in range(len(object_sort_i)):
        original_list_size = len(position_log)
        for n in range(len(object_sort_f)):
            if(object_sort_i[m]['Color'] == object_sort_f[n]['Color'] ):
                o = str(open("/home/sakucom/Documents/Intro_to_Eng_Work/Introduction_to_Dobot_KMUTNB/"+filename).readlines())
                positionData = ast.literal_eval(o[2:-2])
                #planing start
                if(n ==  0):
                    q = positionData[2][0] 
                    w = positionData[2][1]
                    if(object_sort_f[n]['Color'] == "RED"):
                        e = red_z[0]
                        position_log.append([q,w,e])
                        del red_z[0]
                    elif(object_sort_f[n]['Color'] == "GREEN"):
                        e = green_z[0]
                        position_log.append([q,w,e])
                        del green_z[0]
                    elif(object_sort_f[n]['Color'] == "BLUE"):
                        e = blue_z[0]
                        position_log.append([q,w,e])
                        del blue_z[0]
                    elif(object_sort_f[n]['Color'] == "YELLOW"):
                        e = yellow_z[0]
                        position_log.append([q,w,e])
                        del yellow_z[0]
                elif(n == 1):
                    q = positionData[4][0]
                    w = positionData[4][1]
                    if(object_sort_f[n]['Color'] == "RED"):
                        e = red_z[0]
                        position_log.append([q,w,e])
                        del red_z[0]
                    elif(object_sort_f[n]['Color'] == "GREEN"):
                        e = green_z[0]
                        position_log.append([q,w,e])
                        del green_z[0]
                    elif(object_sort_f[n]['Color'] == "BLUE"):
                        e = blue_z[0]
                        position_log.append([q,w,e])
                        del blue_z[0]
                    elif(object_sort_f[n]['Color'] == "YELLOW"):
                        e = yellow_z[0]
                        position_log.append([q,w,e])
                        del yellow_z[0]
                elif(n == 2):
                    q = positionData[6][0]
                    w = positionData[6][1]
                    if(object_sort_f[n]['Color'] == "RED"):
                        e = red_z[0]
                        position_log.append([q,w,e])
                        del red_z[0]
                    elif(object_sort_f[n]['Color'] == "GREEN"):
                        e = green_z[0]
                        position_log.append([q,w,e])
                        del green_z[0]
                    elif(object_sort_f[n]['Color'] == "BLUE"):
                        e = blue_z[0]
                        position_log.append([q,w,e])
                        del blue_z[0]
                    elif(object_sort_f[n]['Color'] == "YELLOW"):
                        e = yellow_z[0]
                        position_log.append([q,w,e])
                        del yellow_z[0]
                elif(n == 3):
                    q = positionData[8][0]
                    w = positionData[8][1]
                    if(object_sort_f[n]['Color'] == "RED"):
                        e = red_z[0]
                        position_log.append([q,w,e])
                        del red_z[0]
                    elif(object_sort_f[n]['Color'] == "GREEN"):
                        e = green_z[0]
                        position_log.append([q,w,e])
                        del green_z[0]
                    elif(object_sort_f[n]['Color'] == "BLUE"):
                        e = blue_z[0]
                        position_log.append([q,w,e])
                        del blue_z[0]
                    elif(object_sort_f[n]['Color'] == "YELLOW"):
                        e = yellow_z[0]
                        position_log.append([q,w,e])
                        del yellow_z[0]
        if(len(position_log) == original_list_size):
            q = 999
            position_skip_log.append([q])
        else:
            q = 1000
            position_skip_log.append([q])
    if(len(object_sort_i) < len(object_sort_f) or len(object_sort_i) + len(object_sort_f) == 6):
        q = 999
        position_skip_log.append([q])

    return position_log,position_skip_log

#Auto_Custom_Position
filename = "DoBot_position_info" #change file for replay movement or create new trajectory plan
device = pydobot.Dobot(port= "/dev/ttyUSB0")#if Acess denied occur. Install minicom and run sudo minicom -b 115200 -o -D /dev/ttyUSB0 in terminal
positionData = []#position data list
counter = []#counter of Number of movement list
selectmode = input('Insert Command please! [HELP(-h)]:')#recieve string
if(selectmode == "-np"):
    f = open("/home/sakucom/Documents/Intro_to_Eng_Work/Introduction_to_Dobot_KMUTNB/"+filename, "w")
    (i,j,k,m,j1,j2,j3,j4) = device.pose()#get pose
    positionxyz = [i,j,k]
    positionData.append(positionxyz)
    en = 8
    counter.append(en)
    for i in range(en):
        k = input('please place your end factor to destination position then type y for continue:')
        if(k == "y"):
            (x,y,z,r,j1,j2,j3,j4) = device.pose()
            positionxyz = [x,y,z]
            positionData.append(positionxyz)
            print("Setting new position:",str(i+1),positionxyz)
        else:
            print("Error")
    f.writelines(str(positionData))
    f.close()
    camera_leveling_setup() #camera leveling setup
    print("New profile is ready to use!")
elif(selectmode == "y"):
    o = str(open("/home/sakucom/Documents/Intro_to_Eng_Work/Introduction_to_Dobot_KMUTNB/"+filename).readlines())
    positionData = ast.literal_eval(o[2:-2])
    print(positionData)
    q = positionData[0][0]
    w = positionData[0][1]
    e = positionData[0][1]
    print("Home position is:",q,w,e,0) 
    color_detection() #initialize color_detection()
    moveto = stacking_system() #initialize stacking_system()
    print(moveto[0])
    print(moveto[1])
    device.move_to(q,w,e,0)
    for j in range(1,len(positionData)):
        if(j%2 != 0 and moveto[1][0][0] != 999):
            x = positionData[j][0]
            y = positionData[j][1]
            z = -49 #z coordinate defined by user 
            device.move_to_J(x,y,z,r=0)
            print("Position:",str(j),":","x="+str(x),"y="+str(y),"z="+str(z)) 
            device.suck(True)
            device.move_to_J(moveto[0][0][0], moveto[0][0][1], moveto[0][0][2], 0)
            print("Position_final:",str(j),":","x="+str(moveto[0][0][0]),"y="+str(moveto[0][0][1]),"z="+str(moveto[0][0][2]))
            device.suck(False)
            print(moveto[1])
            del moveto[0][0]
            del moveto[1][0]
        elif(j%2 != 0 and moveto[1][0][0] == 999):
            del moveto[1][0]
    device.move_to_J(q,w,e,0)
elif(selectmode == "-hm"):
    device.home()
elif(selectmode == "-h"):
    print("     -h  --> help")
    print("     -np --> new profile")
    print("      y  --> start")
    print("     -hm --> home")
else:
     print("Error")
device.close()


