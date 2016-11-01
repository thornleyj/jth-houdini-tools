#
# JTH Visual effects python bits n bobs
#


import hou
import os
import math

def createCacheRops():
    nodelist = hou.selectedNodes()

    for node in nodelist:
        nodeName = node.name()
        isNull = node.type().name().startswith("null")
        isCache = nodeName.startswith("CACHE")
        if isNull & isCache:
            node.setColor(hou.Color((0,.5,0)))
            ropName = nodeName.replace("CACHE_","")
            
            ropNode = hou.node('/out/').createNode('geometry')
            ropNode.setName(ropName)
            ropNode.setColor(hou.Color((0.75,0.7,0)))
            
            ropNode.parm('soppath').set(node.path())
            
            readNode = node.createOutputNode('file')
            readNode.setName(ropName)
            readNode.setColor(hou.Color((0.75,0.7,0)))
            
            expression = "hou.node('" + ropNode.path() + "').parm('sopoutput').eval()"
            readNode.parm('file').setExpression(expression,hou.exprLanguage.Python)

def reloadAllAlembics():

    sop_node_type=hou.sopNodeTypeCategory().nodeTypes()['alembic']
    obj_node_type=hou.objNodeTypeCategory().nodeTypes()['alembicarchive']

    for child in hou.node('/obj/').children():
        if child.type() == obj_node_type:
            child.parm('buildHierarchy').pressButton()
        else:
            for sopChild in child.allSubChildren():
                if child.type() == sop_node_type:
                    child.parm('reload').pressButton()

def COPloadFromFolder():

    path = hou.ui.selectFile()
    dirPath = hou.expandString(os.path.dirname(path))
    list = os.listdir(dirPath)

    newlist = []

    for item in list:
        basepath = item[:item.rindex(".")]
        basepath = basepath[:basepath.rindex(".")]
        newlist.append(basepath)

    newset = set(newlist)

    for item in newset:
        copnet = hou.node('/img/comp1')
        copnode = copnet.createNode('file')
        copnode.parm('filename1').set(dirPath+ "/" + item + ".$F4.exr")
        copnode.moveToGoodPosition()
        

def COPwedgeContactSheet():

    nodelist = hou.selectedNodes()

    nodeCount = len(nodelist)

    sides = math.ceil(math.sqrt(nodeCount))

    mergeNodes = []

    for index, node in enumerate(nodelist):
        nodeName = node.name()
        overlay = node.parm('filename1').eval()

#        overlay = overlay[:overlay.index("_F4_exr")]
        overlay = overlay[:overlay.index(".exr")-5]
        overlay = overlay[overlay.rindex("_wedge_"):]
        overlay = overlay.replace("_wedge_","")

        fontNode = node.createOutputNode('font')
        fontNode.parm('text').set(overlay)
        fontNode.moveToGoodPosition()

        offsetx = math.fmod(index,sides)
        offsety = math.floor(index/sides)

        transNode = fontNode.createOutputNode('xform')
        transNode.parm('tx').set(offsetx)
        transNode.parm('ty').set(offsety)
        transNode.moveToGoodPosition()

        # scaleNode = transNode.createOutputNode('scale')
        # scaleNode.parm('imagefract1').set(1/sides)
        # scaleNode.parm('imagefract2').set(1/sides)
        # scaleNode.moveToGoodPosition()

        layerNode = transNode.createOutputNode('over')
        layerNode.moveToGoodPosition()

        mergeNodes.append(layerNode)


    bgnode = nodelist[0].createOutputNode('color')
    bgnode.parm('colorr').set(0)
    bgnode.parm('colorg').set(0)
    bgnode.parm('colorb').set(0)

    bgnode.moveToGoodPosition()

    bgnode = bgnode.createOutputNode('scale')
    bgnode.parm('imagefract1').set(sides)
    bgnode.parm('imagefract2').set(sides)
    bgnode.moveToGoodPosition()

    bgnode.moveToGoodPosition()

    print mergeNodes

    mergeNodes[0].setInput(1,bgnode,0)

    for index, node in enumerate(mergeNodes):
        if node != mergeNodes[0]:
            node.setInput(1,mergeNodes[index-1],0)

#    for mergeNode in mergeNodes:
#        layerNode.setInput(1,bgnode,0)




