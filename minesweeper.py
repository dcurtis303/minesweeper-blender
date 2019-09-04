import bpy
import bmesh
from random import randint, seed

clean_scene = False
show_entries = False

# game_board = [ 100, 100, 1000 ]
# game_board = [ 30, 16, 99 ]
game_board = [ 15, 8, 32 ]
# game_board = [ 6, 4, 6 ]
# game_board = [ 4, 4, 2 ]

game_seed = 1

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


def SetTile(i, j, e):
    grid[i][j] = e
#    frame = bpy.context.scene.frame_current + 1
#    bpy.context.scene.frame_set(frame)
#    tile = bpy.data.objects["MineTile." + str(i) + "." + str(j)]
#    tile.keyframe_insert("pass_index")


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
                SetTile(ip, jp, grid[ip][jp] ^ b_blank)


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


def RevealAdjacentTiles(i, j):
    nis = 0 if i == 0 else i - 1
    nie = col_i if i == col_i else i + 1
    njs = 0 if j == 0 else j - 1
    nje = row_i if j == row_i else j + 1
    
    for ip in range(nis, nie + 1):
        for jp in range(njs, nje + 1):
            if IsUnrevealed(ip, jp):
                SetTile(ip, jp, grid[ip][jp] ^ b_blank)


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
                                    if grid[ip][jp][gm] == m2_cnt + 1
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
                SetTile(ip, jp, grid[ip][jp] | b_flag)


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


def SetTileMaterialIndex():
    for i in range(col):
        for j in range(row):
            if grid[i][j] & b_blank and not grid[i][j] & b_flag:
                pi = 9
            elif grid[i][j] & b_flag:
                pi = 10
            else:
                pi = grid[i][j]

            tile = bpy.data.objects["MineTile." + str(i) + "." + str(j)]
            tile.pass_index = pi


def SetKeyframes():
    for i in range(col):
        for j in range(row):
            tile = bpy.data.objects["MineTile." + str(i) + "." + str(j)]
            tile.keyframe_insert("pass_index")
            # tile.interpolation = 'Constant'


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

    grid[9][5] ^= b_blank

#    for i in range(5):
    print("Matching blanks...")
    MatchBlank()
    
    print("Matching Unrevealed...")
    MatchUnrevealed()

    print("Matching flagged...")
    MatchFlagged()
    
    print("Matching patterns...")
    MatchPatterns()

    print("Setting Tile Material Index...")
    SetTileMaterialIndex()
    # bpy.context.scene.frame_set()

    print("Setting keyframes...")
    SetKeyframes()

    print("script complete\n")


Scene()

