from serial.tools import list_ports
import pydobot
import ast
#manual_custom_Position
'''device = pydobot.Dobot(port= "/dev/ttyUSB0")
(x,y,z,r,j1,j2,j3,j4) = device.pose()
device.move_to(5.1,130.2,1.2)
device.move_to_J(-74.5 , 192.7, -31.9, 0)
device.suck(True)
device.move_to_J(98.9,185.2,-34.1,0)
device.suck(False)
device.move_to_J(x=-103.4, y=231.9, z=-32.3, r=0)
device.suck(True)
device.move_to_J(x=132.2, y=220.3, z=-29.9, r=0)
device.suck(False)
device.move_to_J(x=-77.4, y=226.1, z=-33.9, r=0)
device.suck(True)
device.move_to_J(x=104, y=215.2, z=-32.9, r=0)
device.suck(False)
device.move_to_L(x=104, y=215.2, z=-8, r=0)
device.move_to_L(5.1,130.2,1.2)
device.close()'''

#Auto_Custom_Position
filename = "DoBot_position_info" #change file for replay movement or create new trajectory plan
device = pydobot.Dobot(port= "/dev/ttyUSB0")#if Acess denied occur. Install minicom and run sudo minicom -b 115200 -o -D /dev/ttyUSB0 in terminal
positionData = []#position data list
counter = []#counter of Number of movement list
selectmode = input('New set(-ns),Pre set(press any key and enter):')#recieve string
if(selectmode == "-ns"):
    f = open("/home/sakucom/Documents/Intro_to_Eng_Work/Introduction_to_Dobot_KMUTNB/"+filename, "w")
    (i,j,k,m,j1,j2,j3,j4) = device.pose()#get pose
    positionxyz = [i,j,k]
    positionData.append(positionxyz)
    en = int(input('input your Number Of Movement:'))
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
p = input('Are you ready?(y|n):')
if(p == "y"):
    o = str(open("/home/sakucom/Documents/Intro_to_Eng_Work/Introduction_to_Dobot_KMUTNB/"+filename).readlines())
    positionData = ast.literal_eval(o[2:-2])
    print(positionData)
    q = positionData[0][0]
    w = positionData[0][1]
    e = positionData[0][1]
    device.move_to(q,w,e,0)
    print(q,w,e,0)
    if(len(positionData)%2 == 0):
        print("Automode cannot enable some task because of number of movement. so the program will use move_to instead")
        for m in range(1,len(positionData)-1):
        #Edit your condition here
            x = positionData[m][0]
            y = positionData[m][1]
            z = positionData[m][2]
            print("Position:",str(m),":","x="+str(x),"y="+str(y),"z="+str(z))
            device.move_to_J(x, y, z, 0)
            if (m%2 == 0):
                device.suck(False)
            else:
                device.suck(True)
        device.move_to(positionData[-1][0],positionData[-1][1],positionData[-1][2])
    else:
        for j in range(1,len(positionData)):
            #Edit your condition here
            x = positionData[j][0]
            y = positionData[j][1]
            z = positionData[j][2]
            print("Position:",str(j),":","x="+str(x),"y="+str(y),"z="+str(z))
            device.move_to_J(x, y, z, 0)
            if (j%2 == 0):
                device.suck(False)
            else:
                device.suck(True)
    device.move_to_J(q,w,e,0)
else:
    print("Error")
device.close()


