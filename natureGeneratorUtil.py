from maya import cmds

THEME_COLORS = {
    "Spring": {"leaf":(0.2,1,0.2),"trunk":(0.55,0.27,0.07),"petal":(1,0.5,0.5),"stem":(0.2,1,0.2),"grass":(0.3,0.9,0.3),"rock":(0.6,0.6,0.6)},
    "Autumn": {"leaf":(1,0.5,0),"trunk":(0.55,0.27,0.07),"petal":(1,0.6,0.3),"stem":(0.4,0.3,0.1),"grass":(0.8,0.6,0.2),"rock":(0.5,0.4,0.3)},
    "Winter": {"leaf":(1,1,1),"trunk":(0.55,0.27,0.07),"petal":(1,1,1),"stem":(0.9,0.9,0.9),"grass":(0.9,0.9,0.9),"rock":(0.8,0.8,0.8)}
}

def apply_theme(theme):
    colors = THEME_COLORS.get(theme)
    if not colors: return

    meshes = cmds.ls(type='mesh', long=True)
    for mesh in meshes:
        for sg in cmds.listConnections(mesh, type='shadingEngine') or []:
            for mat in cmds.ls(cmds.listConnections(sg+'.surfaceShader') or [], materials=True):
                attr = "baseColor" if cmds.nodeType(mat)=="aiStandardSurface" else "color"
                for key,col in colors.items():
                    if key in mat.lower() and cmds.objExists(mat+'.'+attr):
                        cmds.setAttr(mat+'.'+attr,*col,type="double3")
                        break

apply_theme("Autumn")
