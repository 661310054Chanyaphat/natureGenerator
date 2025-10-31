from maya import cmds


THEME_COLORS = {
    "Spring": {
        "leaf":  (0.647, 0.843, 0.169),
        "trunk": (0.553, 0.388, 0.153),
        "petal": (0.957, 0.545, 1.000),
        "stem":  (0.647, 0.843, 0.169),
        "grass": (0.647, 0.843, 0.169),
        "rock":  (0.431, 0.522, 0.384)
    },
    "Autumn": {
        "leaf":  (0.863, 0.459, 0.188),
        "trunk": (0.475, 0.325, 0.137),
        "petal": (1.0, 0.6, 0.3),
        "stem":  (0.4, 0.3, 0.1),
        "grass": (0.8, 0.6, 0.2),
        "rock":  (0.5, 0.4, 0.3)
    },
    "Winter": {
        "leaf":  (0.4627, 0.8118, 0.7529),
        "trunk": (0.3686, 0.2941, 0.2275),
        "petal": (0.620, 0.529, 0.941),
        "stem":  (0.4627, 0.8118, 0.7529),
        "grass": (0.639, 0.471, 0.882),
        "rock":  (0.8, 0.8, 0.8)
    }
}


def apply_theme_colors_by_material(obj, obj_type, theme):

    colors = THEME_COLORS.get(theme)
    if not colors:
        cmds.warning(f"Theme '{theme}' not found.")
        return

    meshes = cmds.listRelatives(obj, allDescendents=True, type='mesh', fullPath=True) or []
    for mesh in meshes:
        
        shading_groups = cmds.listConnections(mesh, type='shadingEngine') or []
        for sg in shading_groups:
            materials = cmds.ls(cmds.listConnections(sg + '.surfaceShader') or [], materials=True)
            for mat in materials:
                attr = "baseColor" if cmds.nodeType(mat) == "aiStandardSurface" else "color"
                mat_lower = mat.lower()

               
                if any(k in mat_lower for k in ["leaf_"]):
                    color = colors.get("leaf")
                elif any(k in mat_lower for k in ["trunk_"]):
                    color = colors.get("trunk")
                elif any(k in mat_lower for k in ["petal_"]):
                    color = colors.get("petal")
                elif "stem" in mat_lower:
                    color = colors.get("stem")
                elif "grass_" in mat_lower:
                    color = colors.get("grass")
                elif "rock_" in mat_lower:
                    color = colors.get("rock")
                else:
                    color = None

          
                if color and cmds.objExists(mat + '.' + attr):
                    cmds.setAttr(mat + '.' + attr, *color, type="double3")
