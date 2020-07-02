#GEO_PLANE_BUILDER v0.1
#By Emilio ramos

import maya.cmds as cmds


def make_planes():
    coords= []

    n = raw_input("North")
    w = raw_input("West")

    coords.append([n,w])

    for location in coords:
        new_plane = cmds.polyPlane(height=1, width =1, axis=[0,0,1], sh= 1, sw=1, n="GEO_PLANE_N"+str(location[0]).zfill(3)+"W"+str(location[1]).zfill(3))
        print (new_plane)
        cmds.polyMoveVertex( new_plane[0]+".vtx[0:3]", tz=57.2965067401)
        cmds.setAttr(new_plane[0]+".rx",-1*float(location[0]))
        cmds.setAttr(new_plane[0]+".ry", -1*float(location[1]))
        #cmds.polyExtrudeFacet(new_plane[0]+".f[0]", kft=True, ltz=float(location[-1][-1])/20.0)


make_planes()
