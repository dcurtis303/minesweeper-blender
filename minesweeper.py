import bpy
from random import randint, seed

clean_scene = False
show_entries = False


# game_board = [ 100, 100, 1000 ]
# game_board = [ 30, 16, 99 ]
game_board = [ 15, 8, 32 ]
# game_board = [ 6, 4, 6 ]
# game_board = [ 4, 4, 2 ]

game_seed = 4

e_null = 13
e_mine = 12

b_blank = 0x80
b_flag  = 0x40

col   = game_board[0]
row   = game_board[1]
mines = game_board[2]

grid = [[e_null for x in range(row)] for y in range(col)]

col_i = col - 1
row_i = row - 1

changes = 0

def IsNumber(i, j):
    b = grid[i][j] > 0 and grid[i][j] <= 8
    return b

def IsMine(i, j):
    b = grid[i][j] == e_mine
    return b


def IsRevealed(i, j):
    b = grid[i][j] ^ b_blank
    return b


def IsUnrevealed(i, j):
    b = grid[i][j] & b_blank
    return b


def IsFlagged(i, j):
    b = grid[i][j] & b_flag
    return b


def SetTile(i, j, e, who):
    global changes
    changes += 1
    prt = "{} : {},{} = {} <- {}"
    print(prt.format(changes, i, j, e, who))
    grid[i][j] = e
    frame = bpy.context.scene.frame_current + 1
    bpy.context.scene.frame_set(frame)
    pi = GetMaterialIndex(i, j)
    tile = bpy.data.objects["MineTile." + str(i) + "." + str(j)]
    tile.pass_index = pi
    tile.keyframe_insert("pass_index")
    for fcurve in tile.animation_data.action.fcurves:
        kf = fcurve.keyframe_points[-1]
        kf.interpolation = 'CONSTANT'


def InitGrid():
    for i in range(mines):
        grid[randint(0, col_i)][randint(0, row_i)] = e_mine

    for i in range(col):
        for j in range(row):
            if (grid[i][j] != e_mine):
                grid[i][j] = CountAdjacentMines(i, j)

    if not show_entries:
        for i in range(col):
            for j in range(row):
                grid[i][j] |= b_blank


def CountAdjacentMines(i, j):
    cam_cnt = 0

    nis = 0 if i == 0 else i - 1
    nie = col_i if i == col_i else i + 1
    njs = 0 if j == 0 else j - 1
    nje = row_i if j == row_i else j + 1

    for ip in range(nis, nie + 1):
        for jp in range(njs, nje + 1):
            if IsMine(ip, jp):
                cam_cnt += 1

    return cam_cnt


def MatchBlank():
    times = 0
    while True:
        found = False
        for i in range(col):
            for j in range(row):
                if (grid[i][j] == 0):
                    RevealAdjacentTiles(i, j)
                    found = True

        times += 1
        if found == False:
            return
        if times > 10:
            return


def RevealAdjacentTiles(i, j):
    nis = 0 if i == 0 else i - 1
    nie = col_i if i == col_i else i + 1
    njs = 0 if j == 0 else j - 1
    nje = row_i if j == row_i else j + 1

    for ip in range(nis, nie + 1):
        for jp in range(njs, nje + 1):
            if IsUnrevealed(ip, jp) and not IsFlagged(ip, jp):
                SetTile(ip, jp, grid[ip][jp] ^ b_blank, ".RevealAdjacentTiles")


def CountAdjacent_Unrevealed(i, j):
    cau_cnt = 0

    nis = 0 if i == 0 else i - 1
    nie = col_i if i == col_i else i + 1
    njs = 0 if j == 0 else j - 1
    nje = row_i if j == row_i else j + 1

    for ip in range(nis, nie + 1):
        for jp in range(njs, nje + 1):
            if (IsUnrevealed(ip, jp)):
                cau_cnt += 1

    return cau_cnt


def CountAdjacent_Flagged(i, j):
    caf_cnt = 0

    nis = 0 if i == 0 else i - 1
    nie = col_i if i == col_i else i + 1
    njs = 0 if j == 0 else j - 1
    nje = row_i if j == row_i else j + 1

    for ip in range(nis, nie + 1):
        for jp in range(njs, nje + 1):
            if IsFlagged(ip, jp):
                caf_cnt += 1

    return caf_cnt


def MatchUnrevealed():
    for i in range(col):
        for j in range(row):
            if IsNumber(i, j):
                mu_cnt = CountAdjacent_Unrevealed(i, j)
                mu_cnt += CountAdjacent_Flagged(i, j)
                if grid[i][j] == mu_cnt:
                    FlagAdjacentMines(i, j)


def MatchFlagged():
    for i in range(col):
        for j in range(row):
            if IsNumber(i, j) and IsRevealed(i, j):
                mf_cnt = CountAdjacent_Flagged(i, j)
                if grid[i][j] == mf_cnt:
                    RevealAdjacentTiles(i, j)


lau1 = [(0, 0) for x in range(8)] 
lau2 = [(0, 0) for x in range(8)] 
def ListAdjacent_Unrevealed(i, j, list):
    lau_cnt = 0

    nis = 0 if i == 0 else i - 1
    nie = col_i if i == col_i else i + 1
    njs = 0 if j == 0 else j - 1
    nje = row_i if j == row_i else j + 1
    
    for ip in range(nis, nie + 1):
        for jp in range(njs, nje + 1):
            if not ip == i and jp == j:
                if IsUnrevealed(ip, jp):
                    if list == 1:
                        lau1[lau_cnt] = (ip, jp)
                    else:
                        lau2[lau_cnt] = (ip, jp)
                    lau_cnt += 1

    return lau_cnt


def InLAUList1(i, j, c1):
    ill1 = False
    r = 0
    while r < c1:
        if lau1[r][0] == i and lau1[r][1] == j:
            ill1 = True
        r += 1

    return ill1


def CompareLAULists(c1, c2):
    cll_cnt = 0
    r = 0
    while r < c2:
        if InLAUList1(lau2[r][0], lau2[r][1], c1):
            cll_cnt += 1
        r += 1
    return cll_cnt


def RevealLAUList2(c1, c2):
    r = 0
    while r < c2:
        if not InLAUList1(lau2[r][0], lau2[r][1], c1):
            i = lau2[r][0]
            j = lau2[r][1]
            SetTile(i, j, grid[i][j] ^ b_blank, ".RevealLAUList2")
        r += 1


def MatchPatterns():
    for i in range(col):
        for j in range(row):
        
            m1_cnt = IsMissingFlags(i, j)
            if m1_cnt != -1:
                    
                nis = 0 if i == 0 else i - 1
                nie = col_i if i == col_i else i + 1
                njs = 0 if j == 0 else j - 1
                nje = row_i if j == row_i else j + 1

                for ip in range(nis, nie + 1):
                    for jp in range(njs, nje + 1):

                        if not ip == i and jp == j:
                            m2_cnt = IsMissingFlags(ip, jp)
                            if m2_cnt != -1:
                                t1_cnt = ListAdjacent_Unrevealed(i, j, 1)
                                t2_cnt = ListAdjacent_Unrevealed(ip, jp, 2)
                                match_cnt = CompareLAULists(t1_cnt, t2_cnt)
                                if match_cnt == t1_cnt:
                                    if grid[ip][jp] == m2_cnt + 1:
                                        RevealLAUList2(t1_cnt, t2_cnt)


def IsMissingFlags(i, j):
    if IsNumber(i, j) and IsRevealed(i, j):
        imf_cnt = CountAdjacent_Flagged(i, j)
        if imf_cnt != grid[i][j]:
            imf = imf_cnt
        else:
            imf = -1
    else:
        imf = -1

    return imf


def FlagAdjacentMines(i, j):
    nis = 0 if i == 0 else i - 1
    nie = col_i if i == col_i else i + 1
    njs = 0 if j == 0 else j - 1
    nje = row_i if j == row_i else j + 1

    for ip in range(nis, nie + 1):
        for jp in range(njs, nje + 1):
            if IsUnrevealed(ip, jp):
                SetTile(ip, jp, grid[ip][jp] | b_flag, ".FlagAdjacentMines")


def ResetScene():
    for item in bpy.data.objects:
        if item.name.startswith("MineTile"):
            bpy.data.objects.remove(item)

    for mesh in bpy.data.meshes:
        if not mesh.users:
            bpy.data.meshes.remove(mesh)

    for material in bpy.data.materials:
        if material.name.startswith("MineTile"):
            bpy.data.materials.remove(material)

    for img in bpy.data.images:
        if img.name.startswith("tiles"):
            bpy.data.images.remove(img)
            
    for a in bpy.data.actions:
        if not a.users:
            bpy.data.actions.remove(a)


def CreateTileObjects():
    first = True
    for i in range(col):
        for j in range(row):
            if first:
                bpy.ops.mesh.primitive_plane_add(size=1)
                first = False
            else:
                bpy.ops.object.duplicate(linked=True)

            tile = bpy.context.selected_objects[0]
            tile.name = "MineTile." + str(i) + "." + str(j)
            tile.location = (i + 0.5, j + 0.5, 0.0)
            tile.active_material = bpy.data.materials['MineTile']
            tile["tile_entry"] = grid[i][j] & 0x7f


def CreateMaterial():
    mat = bpy.data.materials.new("MineTile")
    mat.use_nodes = True
    tree = mat.node_tree
    nodes = tree.nodes
    nodes.clear()
    links = tree.links
    links.clear()

    node1 = nodes.new("ShaderNodeOutputMaterial")
    node2 = nodes.new("ShaderNodeBsdfPrincipled")
    node3 = nodes.new("ShaderNodeTexImage")
    node4 = nodes.new("ShaderNodeCombineXYZ")
    node5 = nodes.new("ShaderNodeMath")
    node6 = nodes.new("ShaderNodeMath")
    node7 = nodes.new("ShaderNodeMath")
    node8 = nodes.new("ShaderNodeObjectInfo")
    node9 = nodes.new("ShaderNodeSeparateXYZ")
    nodeA = nodes.new("ShaderNodeTexCoord")

    dx = 40
    dy = 175
    node1.location = (0, 0)
    node2.location = (node1.location[0] - node2.width - dx, 0)
    node3.location = (node2.location[0] - node3.width - dx, 0)
    node4.location = (node3.location[0] - node4.width - dx, 0)
    node5.location = (node4.location[0] - node5.width - dx, dy)
    node6.location = (node5.location[0] - node6.width - dx, dy)
    node7.location = (node5.location[0] - node6.width - dx, dy * 2)
    node8.location = (node6.location[0] - node7.width - dx, dy * 2)
    node9.location = (node7.location[0] - node8.width - dx, 0)
    nodeA.location = (node8.location[0] - node9.width - dx, 0)

    node2.inputs[5].default_value = 0
    node2.inputs[7].default_value = 0
    node3.image = bpy.data.images.load("tiles.png")
    node3.interpolation = 'Closest'
    node6.operation = 'MULTIPLY'
    node6.inputs[0].default_value = 1 / 14
    node7.operation = 'MULTIPLY'
    node7.inputs[0].default_value = 1 / 14

    links.new(node2.outputs[0], node1.inputs[0])
    links.new(node3.outputs[0], node2.inputs[0])
    links.new(node4.outputs[0], node3.inputs[0])
    links.new(node5.outputs[0], node4.inputs[0])
    links.new(node6.outputs[0], node5.inputs[1])
    links.new(node7.outputs[0], node5.inputs[0])
    links.new(node8.outputs[1], node7.inputs[1])
    links.new(node9.outputs[0], node6.inputs[1])
    links.new(node9.outputs[1], node4.inputs[1])
    links.new(node9.outputs[2], node4.inputs[2])
    links.new(nodeA.outputs[2], node9.inputs[0])


def GetMaterialIndex(i, j):
    pi = e_null
    if grid[i][j] & b_blank and not grid[i][j] & b_flag:
        pi = 9
    elif grid[i][j] & b_flag:
        pi = 10
    else:
        pi = grid[i][j]

    return pi


def SetTilesMaterialIndex():
    for i in range(col):
        for j in range(row):
            pi = GetMaterialIndex(i, j)
            tile = bpy.data.objects["MineTile." + str(i) + "." + str(j)]
            tile.pass_index = pi


def SetInitialKeyframes():
    bpy.context.scene.frame_set(1)
    for i in range(col):
        for j in range(row):
            tile = bpy.data.objects["MineTile." + str(i) + "." + str(j)]
            tile.keyframe_insert("pass_index")
            for fcurve in tile.animation_data.action.fcurves:
                kf = fcurve.keyframe_points[-1]
                kf.interpolation = 'CONSTANT'

    
    

def RandomPress():
    x = 0
    while True:
        i = randint(0, col_i)
        j = randint(0, row_i)
        if grid[i][j] & b_blank:
            grid[i][j] ^= b_blank
            break
        x += 1
        if x > col * row:
            break


def Scene():
    print("\n\nResetting Scene...")
    ResetScene()

    if clean_scene:
        return


    seed(game_seed)

    print("Creating Material...")
    CreateMaterial()

    print("Initializing grid...")
    InitGrid()

    print("Creating tile objects...")
    CreateTileObjects()


    grid[5][0] ^= b_blank


    print("Setting Tile Material Index...")
    SetTilesMaterialIndex()

    print("Setting keyframes...")
    SetInitialKeyframes()

    for i in range(1):
        print("Iteration {}".format(i))
        
        print("Matching blanks...")
        MatchBlank()

        print("Matching Unrevealed...")
        MatchUnrevealed()

        print("Matching flagged...")
        MatchFlagged()

        print("Matching patterns...")
        MatchPatterns()


    print("script complete\n")


Scene()

