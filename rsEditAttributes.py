# rsEditAttributes
# @author Roberto Rubio
# @date 2013-07-30
# @file rsEditAttributes.py

import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

kPluginCmdRsEditAtt = "rsEditAttributesUI"


##
# rs Edit Attributes command class.
# Launch UI for reset Attributes.
class rsEditAttributesUIClass(OpenMayaMPx.MPxCommand):

    ##
    # rsEditAttributesUI Constructor.
    # @param self: Object pointer.
    # @return none
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    ##
    # Do it function.
    # @param self: Object pointer.
    # @param argList: Command arguments.
    # @return none
    def doIt(self, argList):
        mainEditAt()


##
# Creating instance event.
# @param none.
# @return cmdCreatorRsEditAtt instance
def cmdCreatorRsEditAtt():
    return OpenMayaMPx.asMPxPtr(rsEditAttributesUIClass())


##
# Load Plugin event.
# @param obj.
# @return none
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, 'Rig Studio - Developer: Roberto Rubio', '1.2', 'Any')
    try:
        mplugin.registerCommand(kPluginCmdRsEditAtt, cmdCreatorRsEditAtt)
        mplugin.addMenuItem("rsEdit Attributes", "MayaWindow|mainModifyMenu", "rsEditAttributesUI()", "")
    except:
        raise RuntimeError("Failed to register command: %s\ n" % kPluginCmdRsEditAtt)


##
# Unload Plugin event.
# @param obj.
# @return none
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdRsEditAtt)
        cmds.deleteUI("MayaWindow|mainModifyMenu|rsEdit_Attributes")
    except:
        raise RuntimeError("Failed to unregister command: %s\n" % kPluginCmdRsEditAtt)


##
# Main edit attribute function.
# @param none.
# @return none.
def mainEditAt():
    l_oSels = cmds.ls(selection=True)
    if len(l_oSels) == 1:
        editAtUI(l_oSels)
        l_ChannelAtList = rsChannelAtList()
        l_AttrKey = l_ChannelAtList[0]
        l_AttrKeyHidden = l_ChannelAtList[1]
        if l_AttrKey or l_AttrKeyHidden:
            cmds.textScrollList("rsAttributeScroll", edit=True, removeAll=True, append=l_AttrKey, selectItem=l_AttrKey[0])
            cmds.textScrollList("rsAttributeScrollHidden", edit=True, removeAll=True, append=l_AttrKeyHidden)
            attSelected()
        else:
            rsAttNoEnable()
            rsEnumNoEnable()
            rsLockNoEnable()
            rsPropertyNoEnable()
            rsMinNoEnable()
            rsMaxNoEnable()
            rsAttDefaultNoEnable()
            rsCheckNoEnable()
    else:
        editAtUI(l_oSels)
        rsAttNoEnable()
        rsEnumNoEnable()
        rsLockNoEnable()
        rsPropertyNoEnable()
        rsMinNoEnable()
        rsMaxNoEnable()
        rsAttDefaultNoEnable()
        rsCheckNoEnable()


##
# UI creator function.
# @param i_s_oSels: 3D object.
# @return Boolean
def editAtUI(i_s_oSels):
    import platform
    if platform.system() == "Windows":
        i_windowSize = (410, 406)
        i_LockAtNumEight = 100
        i_ReAtEnumEight = 215
        i_NumRows = (5, 90, 50)
        i_UpRows = (86, 150, 155)
        i_names = (73, 118, 73, 118)
        i_attrColumWidth = (30, 120)
        i_EnumEight = 134
        i_enumScrollEight = 77
        i_EnumWidth = 152
        i_NameEight = 27
        i_NameWidth = 394
        i_ReaSep = 10
        i_ReaSep2 = 15
        i_NameFrame = 386
        i_numWidth = 50
        i_AddEight = 30
        i_AddButtonWidth = 83
    elif platform.system() == "Linux":
        i_windowSize = (415, 395)
        i_LockAtNumEight = 97
        i_ReAtEnumEight = 209
        i_NumRows = (5, 91, 51)
        i_UpRows = (87, 151, 156)
        i_names = (74, 119, 74, 119)
        i_attrColumWidth = (31, 121)
        i_EnumEight = 130
        i_enumScrollEight = 75
        i_EnumWidth = 153
        i_NameEight = 26
        i_NameWidth = 398
        i_ReaSep = 10
        i_ReaSep2 = 15
        i_NameFrame = 390
        i_numWidth = 51
        i_AddEight = 29
        i_AddButtonWidth = 84
    else:
        print "It is not configured for this operating system."
    s_sel = "select one object"
    if len(i_s_oSels) == 1:
        s_sel = i_s_oSels[0]
    s_UiName = "rs Edit Atribute >> " + s_sel
    if cmds.window("rsEditAtribute", exists=True):
        cmds.deleteUI("rsEditAtribute")
    s_window = cmds.window("rsEditAtribute", title=s_UiName)
    s_wincol1 = cmds.columnLayout(columnAttach=('both', 5), rowSpacing=1, columnWidth=i_windowSize[0], parent=s_window)
    cmds.separator(parent=s_wincol1, height=i_ReaSep, style="none", hr=True)
    s_winRow1 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(i_UpRows), columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)], parent=s_wincol1)
    s_winColOr = cmds.columnLayout(adjustableColumn=True, parent=s_winRow1)
    s_winLayOr = cmds.frameLayout(label='Rearrange', labelAlign='bottom', borderStyle='etchedIn', height=i_ReAtEnumEight, parent=s_winColOr)
    s_winColOr1 = cmds.columnLayout(adjustableColumn=True, parent=s_winLayOr)
    cmds.separator(height=i_ReaSep, style="none", parent=s_winColOr1)
    srsUpAtt = lambda: rsMvAtt(-1)
    srsDwAtt = lambda: rsMvAtt(1)
    cmds.iconTextButton(style='iconAndTextVertical', image1='Up.png', font="smallFixedWidthFont", label='Up', command=srsUpAtt, parent=s_winColOr1)
    cmds.iconTextButton(style='iconAndTextVertical', image1='Down.png', font="smallFixedWidthFont", label='Down', command=srsDwAtt, parent=s_winColOr1)
    cmds.iconTextButton(style='iconAndTextVertical', image1='ReOrder.png', font="smallFixedWidthFont", label='Rearrange', command=rsReAtt, parent=s_winColOr1)
    cmds.separator(height=i_ReaSep2, style="none", parent=s_winColOr1)
    cmds.checkBox("rsLockVectors", label='Lock Vectors', align='center', value=True, parent=s_winColOr1)
    s_winColAt = cmds.columnLayout(adjustableColumn=True, parent=s_winRow1)
    s_winLayAtDisplay = cmds.frameLayout(label='Display Attributes', labelAlign='bottom', borderStyle='etchedIn', height=i_ReAtEnumEight, parent=s_winColAt)
    cmds.textScrollList("rsAttributeScroll", allowMultiSelection=False, sc=attSelected, parent=s_winLayAtDisplay)
    s_winColEn = cmds.columnLayout(adjustableColumn=True, width=i_EnumWidth, parent=s_winRow1)
    s_winLayAtHidden = cmds.frameLayout(label='Hidden Attributes', labelAlign='bottom', borderStyle='etchedIn', parent=s_winColEn)
    cmds.textScrollList("rsAttributeScrollHidden", numberOfRows=4, allowMultiSelection=False, sc=attSelectedHidden, parent=s_winLayAtHidden)
    s_winLayEn = cmds.frameLayout(label='Enum Strings', labelAlign='bottom', borderStyle='etchedIn', height=i_EnumEight, parent=s_winColEn)
    s_winColEn1 = cmds.columnLayout(adjustableColumn=True, parent=s_winLayEn)
    cmds.textScrollList("rsEnumScroll", numberOfRows=8, allowMultiSelection=False, sc=attEnumSelected, height=i_enumScrollEight, parent=s_winColEn1)
    cmds.text(label='New String')
    cmds.textField("StringText", enterCommand=attEnumModify, parent=s_winColEn1)
    lNewName = lambda x: rsChName(x, "NewName")
    lNiceName = lambda x: rsChName(x, "NiceName")
    s_winColEnum = cmds.columnLayout(adjustableColumn=False, width=i_NameFrame, parent=s_wincol1)
    s_winLayNames = cmds.frameLayout(label=' Names', labelVisible=False, labelAlign='bottom', borderStyle='etchedIn', height=i_NameEight, width=i_NameWidth, parent=s_winColEnum)
    s_winRowNammes = cmds.rowLayout(numberOfColumns=4, columnWidth4=(i_names), columnAttach=[(1, 'both', 7), (2, 'both', 0), (3, 'both', 7), (4, 'both', 0)], parent=s_winLayNames)
    cmds.text(label='New Name', align='center', parent=s_winRowNammes)
    cmds.textField("rsNewNameText", enterCommand=lNewName, parent=s_winRowNammes)
    cmds.text(label='Nice Name', align='center', parent=s_winRowNammes)
    cmds.textField("rsNiceNameText", enterCommand=lNiceName, parent=s_winRowNammes)
    s_winRow2 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(i_UpRows), columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)], parent=s_wincol1)
    lockButton = lambda x: rsChLock(x, "Lock")
    UnlockButton = lambda x: rsChLock(x, "UnLock")
    s_winColLck = cmds.columnLayout(adjustableColumn=True, parent=s_winRow2)
    s_winLayLck = cmds.frameLayout(label=' Lock', labelAlign='bottom', borderStyle='etchedIn', height=i_LockAtNumEight, parent=s_winColLck)
    s_winColLck2 = cmds.columnLayout(adjustableColumn=True, parent=s_winLayLck)
    cmds.separator(parent=s_winColLck2, height=i_ReaSep, style="none")
    cmds.radioCollection(parent=s_winColLck2)
    cmds.radioButton("rsLock", label='Lock', align='center', onCommand=lockButton)
    cmds.radioButton("rsUnLock", label='UnLock', align='center', onCommand=UnlockButton)
    s_winColPro = cmds.columnLayout(adjustableColumn=True, parent=s_winRow2)
    s_winLayPro = cmds.frameLayout(label='Attribute Properties', labelAlign='bottom', borderStyle='etchedIn', height=i_LockAtNumEight, parent=s_winColPro)
    s_winColPro2 = cmds.columnLayout(adjustableColumn=True, parent=s_winLayPro)
    cmds.separator(parent=s_winColPro2, height=i_ReaSep, style="none")
    cmds.radioCollection()
    s_winRowPro1 = cmds.rowLayout(numberOfColumns=2, columnWidth2=(i_attrColumWidth), parent=s_winColPro2)
    cmds.separator(style='none', parent=s_winRowPro1)
    dbutton = lambda x: rsChProperties(x, "rsDisplayable")
    kbutton = lambda x: rsChProperties(x, "rsKeyable")
    hbutton = lambda x: rsChProperties(x, "rsHidden")
    cmds.radioButton("rsDisplayable", label='Displayable', align='center', onCommand=dbutton, parent=s_winRowPro1)
    s_winRowPro2 = cmds.rowLayout(numberOfColumns=2, columnWidth2=(i_attrColumWidth), parent=s_winColPro2)
    cmds.separator(style='none', parent=s_winRowPro2)
    cmds.radioButton("rsKeyable", label='Keyable', align='center', onCommand=kbutton, parent=s_winRowPro2)
    s_winRowPro3 = cmds.rowLayout(numberOfColumns=2, columnWidth2=(i_attrColumWidth), parent=s_winColPro2)
    cmds.separator(style='none', parent=s_winRowPro3)
    cmds.radioButton("rsHidden", label='Hidden', align='center', onCommand=hbutton, parent=s_winRowPro3)
    fMin = lambda x: rsChangeCheck(x, "rsMinField")
    fMax = lambda x: rsChangeCheck(x, "rsMaxField")
    s_winColNum = cmds.columnLayout(adjustableColumn=True, parent=s_winRow2)
    s_winLayNum = cmds.frameLayout(label='Numeric Values', labelAlign='bottom', borderStyle='etchedIn', height=i_LockAtNumEight, width=149, parent=s_winColNum)
    s_winColNum2 = cmds.columnLayout(adjustableColumn=True, parent=s_winLayNum)
    cmds.separator(parent=s_winColNum2, height=3, style="none")
    s_winRowNum1 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(i_NumRows), parent=s_winColNum2)
    cmds.separator(style='none', parent=s_winRowNum1)
    fieldMin = lambda x: rsSetValue(x, "minValue")
    fieldMax = lambda x: rsSetValue(x, "maxValue")
    cmds.checkBox("rsMinBox", label='Minimum', align='center', changeCommand=fMin, parent=s_winRowNum1)
    cmds.floatField("rsMinField", width=i_numWidth, precision=3, enterCommand=fieldMin, parent=s_winRowNum1)
    s_winRowNum2 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(i_NumRows), parent=s_winColNum2)
    cmds.separator(style='none', parent=s_winRowNum2)
    cmds.checkBox("rsMaxBox", label='Maximum', align='center', changeCommand=fMax, parent=s_winRowNum2)
    cmds.floatField("rsMaxField", width=i_numWidth, precision=3, enterCommand=fieldMax, parent=s_winRowNum2)
    s_winRowNum3 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(i_NumRows), parent=s_winColNum2)
    cmds.separator(style='none', parent=s_winRowNum3)
    cmds.button("rsDefaultButton", label='Set Default', command=rsChangeDefault, parent=s_winRowNum3)
    cmds.floatField("rsDefaultField", width=i_numWidth, precision=3, parent=s_winRowNum3)
    cmds.scriptJob(event=["SelectionChanged", rsSelChange], parent=s_window)
    s_addsColEnum = cmds.rowLayout(numberOfColumns=3, parent=s_wincol1)
    s_addsLayNames = cmds.frameLayout(label=' Adds', labelVisible=False, labelAlign='bottom', borderStyle='etchedIn', height=i_AddEight, width=(3 * i_NameFrame / 5) + 5, parent=s_addsColEnum)
    s_addsRowNammes = cmds.rowLayout(numberOfColumns=3, adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)], parent=s_addsLayNames)
    cmds.button(label='Add Separator', command=rsAddSeparator, width=i_AddButtonWidth, align='left', parent=s_addsRowNammes)
    cmds.textField("rsSeparatorName", text="Separator", parent=s_addsRowNammes)
    cmds.separator(style='none', width=1, parent=s_addsColEnum)
    s_addAttLayNames = cmds.frameLayout(label=' AddAtt', labelVisible=False, labelAlign='bottom', borderStyle='etchedIn', height=i_AddEight, width=(2 * i_NameFrame / 5) - 1, parent=s_addsColEnum)
    s_addAttRow = cmds.rowLayout(numberOfColumns=2, parent=s_addAttLayNames)
    cmds.button(label='Del Attribute', command=rsDeleteAttr, align='center', parent=s_addAttRow)
    cmds.button(label='Add Attribute', command=rsAddAttr, align='center', parent=s_addAttRow)
    cmds.showWindow(s_window)
    cmds.window(s_window, edit=True, widthHeight=(i_windowSize), s=False)
    return True


##
# Add Attribute function.
# @param i_s_button - 3d object.
# @return boolean.
def rsAddAttr(i_s_button):
    cmds.AddAttribute()


##
# Delete Attribute function.
# @param i_s_button - 3d object.
# @return boolean.
def rsDeleteAttr(i_s_button):
    l_oSels = rsObjList()
    l_ChangeAttribute = rsChangeAttribute()
    if l_ChangeAttribute[5]:
        cmds.setAttr(l_ChangeAttribute[3], lock=0)
    l_OutcomingConnections = cmds.listConnections(l_ChangeAttribute[3], plugs=True, destination=True, source=False)
    b_delete = True
    if l_OutcomingConnections:
        s_dialog = cmds.confirmDialog(title='Confirm Delete Attribute', icon="warning", message="%s > Has outcoming connections. Are you sure?" % (l_ChangeAttribute[3]), button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        if s_dialog == "No":
            b_delete = False
            print("%s > Has not been deleted" % (l_ChangeAttribute[3]))
    if b_delete:        
        l_paramDest = cmds.listConnections(l_ChangeAttribute[3], plugs=True, destination=True, source=True)
        if l_paramDest:
            for z in range(len(l_paramDest)):
                if cmds.getAttr(l_paramDest[z], lock=True):
                    cmds.setAttr(l_paramDest[z], lock=False)        
        cmds.deleteAttr(l_ChangeAttribute[3])
        print("%s > Has been deleted" % (l_ChangeAttribute[3]))
        cmds.select(cl=True)
        cmds.select(l_oSels[0], r=True)
    return True


##
# Add separator function.
# @param i_s_button - 3d object.
# @return boolean.
def rsAddSeparator(i_s_button):
    l_oSels = rsObjList()
    s_sepName = cmds.textField("rsSeparatorName", query=True, text=True)
    s_sepNameBase = s_sepName
    o_objParam = "%s.%s" % (l_oSels[0], s_sepName)
    i = 1
    while cmds.objExists(o_objParam):
        s_sepName = s_sepNameBase + str(i)
        o_objParam = "%s.%s" % (l_oSels[0], s_sepName)
        i = i + 1
    cmds.addAttr(ln=s_sepName, at="enum", en="---------------:")
    cmds.setAttr(o_objParam, keyable=False, channelBox=True)
    cmds.select(cl=True)
    cmds.select(l_oSels[0], r=True)
    return True


##
# Change default value function.
# @param i_s_button - 3d object.
# @return boolean.
def rsChangeDefault(i_s_button):
    l_ChangeAttribute = rsChangeAttribute()
    if l_ChangeAttribute[5]:
        cmds.setAttr(l_ChangeAttribute[3], lock=0)
    f_NewValue = cmds.floatField("rsDefaultField", query=True, value=True)
    cmds.addAttr(longName=(l_ChangeAttribute[2] + "_cons"), niceName=l_ChangeAttribute[4], attributeType=l_ChangeAttribute[0], hasMinValue=l_ChangeAttribute[8], hasMaxValue=l_ChangeAttribute[10], defaultValue=f_NewValue)
    s_NewAt = l_ChangeAttribute[1] + "." + l_ChangeAttribute[2] + "_cons"
    if l_ChangeAttribute[10]:
        cmds.addAttr(s_NewAt, edit=True, maxValue=l_ChangeAttribute[11])
    if l_ChangeAttribute[8]:
        cmds.addAttr(s_NewAt, edit=True, minValue=l_ChangeAttribute[9])
    if l_ChangeAttribute[6]:
        cmds.setAttr(s_NewAt, keyable=True, channelBox=False)
    if not l_ChangeAttribute[6] and l_ChangeAttribute[7]:
        cmds.setAttr(s_NewAt, keyable=False, channelBox=True)
    if not l_ChangeAttribute[6] and not l_ChangeAttribute[7]:
        cmds.setAttr(s_NewAt, keyable=False, channelBox=False)
    l_IncomingConnections = cmds.listConnections(l_ChangeAttribute[3], plugs=True, destination=False, source=True)
    if l_IncomingConnections:
        print "l_IncomingConnections"
        print l_IncomingConnections
        for s_InConn in l_IncomingConnections:
            cmds.connectAttr(s_InConn, s_NewAt, force=True)
    l_OutcomingConnections = cmds.listConnections(l_ChangeAttribute[3], plugs=True, destination=True, source=False)
    if l_OutcomingConnections:
        print "l_OutcomingConnections"
        print l_OutcomingConnections
        for s_OutConn in l_OutcomingConnections:
            cmds.connectAttr(s_NewAt, s_OutConn, force=True)
    cmds.deleteAttr(l_ChangeAttribute[3])
    cmds.renameAttr(s_NewAt, l_ChangeAttribute[2])
    rsReAtt()
    cmds.setAttr(l_ChangeAttribute[3], lock=l_ChangeAttribute[5])
    l_ChannelAtList = rsChannelAtList()
    l_AttrKey = l_ChannelAtList[0]
    l_AttrKeyHidden = l_ChannelAtList[1]
    if l_AttrKey or l_AttrKeyHidden:
        cmds.textScrollList("rsAttributeScroll", edit=True, removeAll=True, append=l_AttrKey)
        cmds.textScrollList("rsAttributeScrollHidden", edit=True, removeAll=True, append=l_AttrKeyHidden)
    rsSearchInScroll(l_ChangeAttribute[2])
    return True


##
# Attribute data collection function.
# @param none.
# @return l_changeAttribute - Attribute data collection.
def rsChangeAttribute():
    l_oSels = rsObjList()
    s_atType = cmds.getAttr(l_oSels[2], type=True)
    s_atNiceName = cmds.attributeQuery(l_oSels[1], node=l_oSels[0], niceName=True)
    i_atLock = cmds.getAttr(l_oSels[2], lock=True)
    l_changeAttribute = [s_atType, l_oSels[0], l_oSels[1], l_oSels[2], s_atNiceName, i_atLock]
    if s_atType == "double3":
            return l_changeAttribute
    if s_atType == "string":
        s_stringValue = cmds.getAttr(l_oSels[2])
        l_changeAttribute.append(s_stringValue)
        return l_changeAttribute
    i_atKey = cmds.getAttr(l_oSels[2], keyable=True)
    i_atHidden = cmds.getAttr(l_oSels[2], channelBox=True)
    l_changeAttribute.append(i_atKey)
    l_changeAttribute.append(i_atHidden)
    if s_atType == "enum":
        s_enum = (cmds.attributeQuery(l_oSels[1], node=l_oSels[0], listEnum=True))[0]
        l_enum = s_enum.split(':')
        l_changeAttribute.append(l_enum)
        return l_changeAttribute
    s_hasMin = cmds.addAttr(l_oSels[2], query=True, hasMinValue=True)
    f_atMinValue = 0
    if s_hasMin:
        f_atMinValue = (cmds.attributeQuery(l_oSels[1], node=l_oSels[0], minimum=True))[0]
    s_hasMax = cmds.addAttr(l_oSels[2], query=True, hasMaxValue=True)
    f_atMaxValue = 0
    if s_hasMax:
        f_atMaxValue = (cmds.attributeQuery(l_oSels[1], node=l_oSels[0], maximum=True))[0]
    f_atDefValue = (cmds.attributeQuery(l_oSels[1], node=l_oSels[0], listDefault=True))[0]
    l_Siblings = cmds.attributeQuery(l_oSels[1], node=l_oSels[0], listSiblings=True)
    l_rest = [s_hasMin, f_atMinValue, s_hasMax, f_atMaxValue, f_atDefValue]
    l_changeAttribute.extend(l_rest)
    if l_Siblings:
        l_changeAttribute.append(l_Siblings)
    return l_changeAttribute


##
# Change object selected function.
# @param none.
# @return boolean.
def rsSelChange():
    l_oSels = cmds.ls(selection=True)
    s_sel = "select one object"
    if len(l_oSels) == 1:
        s_sel = l_oSels[0]
        l_ChannelAtList = rsChannelAtList()
        l_AttrKey = l_ChannelAtList[0]
        l_AttrKeyHidden = l_ChannelAtList[1]
        if l_AttrKey or l_AttrKeyHidden:
            cmds.textScrollList("rsAttributeScroll", edit=True, removeAll=True, append=l_AttrKey, selectItem=l_AttrKey[0])
            cmds.textScrollList("rsAttributeScrollHidden", edit=True, removeAll=True, append=l_AttrKeyHidden)
            attSelected()
        else:
            rsAttNoEnable()
            rsEnumNoEnable()
            rsLockNoEnable()
            rsPropertyNoEnable()
            rsMinNoEnable()
            rsMaxNoEnable()
            rsAttDefaultNoEnable()
            rsCheckNoEnable()
    else:
        rsAttNoEnable()
        rsEnumNoEnable()
        rsLockNoEnable()
        rsPropertyNoEnable()
        rsMinNoEnable()
        rsMaxNoEnable()
        rsAttDefaultNoEnable()
        rsCheckNoEnable()
    s_UiName = "rs Edit Atribute >> " + s_sel
    cmds.window("rsEditAtribute", edit=True, title=s_UiName)
    return True


##
# Activation function of Default Value option.
# @param none.
# @return boolean.
def rsAttDefaultEnable():
    cmds.button("rsDefaultButton", edit=True, enable=True)
    cmds.floatField("rsDefaultField", edit=True, value=0, enable=True)
    return True


##
# Deactivation function of the Default Value option.
# @param none.
# @return boolean.
def rsAttDefaultNoEnable():
    cmds.button("rsDefaultButton", edit=True, enable=False)
    cmds.floatField("rsDefaultField", edit=True, value=0, enable=False)
    return True


##
# Activation function of the Attribute scroll options.
# @param none.
# @return boolean.
def rsAttEnable():
    cmds.textScrollList("rsAttributeScroll", edit=True, enable=True)
    cmds.textScrollList("rsAttributeScrollHidden", edit=True, enable=True)
    cmds.textField("rsNewNameText", edit=True, text="", enable=True)
    cmds.textField("rsNiceNameText", edit=True, text="", enable=True)
    return True


##
# Deactivation function of the Attribute scroll options.
# @param none.
# @return boolean.
def rsAttNoEnable():
    cmds.textScrollList("rsAttributeScroll", removeAll=True, edit=True, append="no editable attribute", enable=False)
    cmds.textScrollList("rsAttributeScrollHidden", removeAll=True, edit=True, enable=False)
    cmds.textField("rsNewNameText", edit=True, text="", enable=False)
    cmds.textField("rsNiceNameText", edit=True, text="", enable=False)
    return True


##
# Deactivation function of the Enum scroll options.
# @param none.
# @return boolean.
def rsEnumNoEnable():
    cmds.textScrollList("rsEnumScroll", removeAll=True, edit=True, append="", enable=False)
    cmds.textField("StringText", edit=True, text="", enable=False)
    return True


##
# Activation function of the Enum scroll options.
# @param none.
# @return boolean.
def rsEnumEnable():
    cmds.textScrollList("rsEnumScroll", removeAll=True, edit=True, append="", enable=True)
    cmds.textField("StringText", edit=True, text="", enable=True)
    return True


##
# Activation function of the Button lock options.
# @param none.
# @return boolean.
def rsLockEnable():
    cmds.radioButton("rsLock", edit=True, enable=True)
    cmds.radioButton("rsUnLock", edit=True, enable=True)
    return True


##
# Deactivation function of the Button lock options.
# @param none.
# @return boolean.
def rsLockNoEnable():
    cmds.radioButton("rsLock", edit=True, enable=False, select=False)
    cmds.radioButton("rsUnLock", edit=True, enable=False, select=False)
    return True


##
# Activation function of the Property options.
# @param none.
# @return boolean.
def rsPropertyEnable():
    cmds.radioButton("rsDisplayable", edit=True, enable=True)
    cmds.radioButton("rsKeyable", edit=True, enable=True)
    cmds.radioButton("rsHidden", edit=True, enable=True)
    return True


##
# Deactivation function of the Property options.
# @param none.
# @return boolean.
def rsPropertyNoEnable():
    cmds.radioButton("rsDisplayable", edit=True, enable=False, select=False)
    cmds.radioButton("rsKeyable", edit=True, enable=False, select=False)
    cmds.radioButton("rsHidden", edit=True, enable=False, select=False)
    return True


##
# Deactivation function of the Minimum value field.
# @param none.
# @return boolean.
def rsMinNoEnable():
    cmds.floatField("rsMinField", edit=True, value=0, enable=False)
    return True


##
# Deactivation function of the Maximum value field.
# @param none.
# @return boolean.
def rsMaxNoEnable():
    cmds.floatField("rsMaxField", edit=True, value=0, enable=False)
    return True


##
# Activation function of the Minimum and Maximum checkbox.
# @param none.
# @return boolean.
def rsCheckEnable():
    cmds.checkBox("rsMinBox", edit=True, enable=True, value=False)
    cmds.checkBox("rsMaxBox", edit=True, enable=True, value=False)
    return True


##
# Deactivation function of the Minimum and Maximum checkbox.
# @param none.
# @return boolean.
def rsCheckNoEnable():
    cmds.checkBox("rsMinBox", edit=True, enable=False, value=False)
    cmds.checkBox("rsMaxBox", edit=True, enable=False, value=False)
    return True


##
# Object selected collection function.
# @param none.
# @return l_panel - Object data collection.
def rsObjList():
    s_oSel = cmds.ls(selection=True)
    if s_oSel:
        s_AttSelec = rsAtribute()
        if s_AttSelec != "":
            s_ObjAttr = s_oSel[0] + "." + s_AttSelec
            l_panel = s_oSel[0], s_AttSelec, s_ObjAttr
            return l_panel


##
# Change function of the Minimum and Maximum checkbox.
# @param i_b_state - Minimum or Maximum checkbox value.
# @param i_s_floatField - Name of the checkbox.
# @return boolean.
def rsChangeCheck(i_b_state, i_s_floatField):
    if i_s_floatField == "rsMinField":
        i_b_state = cmds.checkBox("rsMinBox", query=True, value=True)
    else:
        i_b_state = cmds.checkBox("rsMaxBox", query=True, value=True)
    l_oSels = rsObjList()
    if i_b_state == True:
        if i_s_floatField == "rsMinField":
            b_minimum = cmds.attributeQuery(l_oSels[1], node=l_oSels[0], minExists=True)
            f_atValue = 0.0
            if b_minimum == 1:
                f_atValue = (cmds.attributeQuery(l_oSels[1], node=l_oSels[0], minimum=True))[0]
            else:
                cmds.addAttr(l_oSels[2], edit=True, hasMinValue=True)
        if i_s_floatField == "rsMaxField":
            b_maximum = cmds.attributeQuery(l_oSels[1], node=l_oSels[0], maxExists=True)
            f_atValue = 1.0
            if b_maximum == 1:
                f_atValue = (cmds.attributeQuery(l_oSels[1], node=l_oSels[0], maximum=True))[0]
            else:
                cmds.addAttr(l_oSels[2], edit=True, hasMaxValue=True)
                cmds.addAttr(l_oSels[2], edit=True, maxValue=f_atValue)
        cmds.floatField(i_s_floatField, edit=True, value=f_atValue, enable=True)
    else:
        cmds.floatField(i_s_floatField, edit=True, value=0, enable=False)
        if i_s_floatField == "rsMinField":
            cmds.addAttr(l_oSels[2], edit=True, hasMinValue=False)
        else:
            cmds.addAttr(l_oSels[2], edit=True, hasMaxValue=False)
    return True


##
# Change lock state function.
# @param i_s_intro - 3D object.
# @param i_s_button - Name of the radio button.
# @return boolean.
def rsChLock(i_s_intro, i_s_button):
    l_oSels = rsObjList()
    if i_s_button == "Lock":
            cmds.setAttr(l_oSels[2], lock=True)
    else:
            cmds.setAttr(l_oSels[2], lock=False)
    return True


##
# Change Minimum and Maximum value function.
# @param i_f_mmValue - Minimum or Maximum field value.
# @param i_s_mmfield - Name of the checkbox.
# @return boolean.
def rsSetValue(i_f_mmValue, i_s_mmfield):
    l_oSels = rsObjList()
    if i_s_mmfield == "minValue":
        f_minValue = cmds.floatField("rsMinField", query=True, value=True)
        cmds.addAttr(l_oSels[2], edit=True, minValue=f_minValue)
    else:
        f_maxValue = cmds.floatField("rsMaxField", query=True, value=True)
        cmds.addAttr(l_oSels[2], edit=True, maxValue=f_maxValue)
    return True


##
# Change Name and NiceName function.
# @param i_s_textField - Name or NiceName field value.
# @param s_name - Text in field.
# @return boolean.
def rsChName(i_s_textField, s_name):
    l_oSels = rsObjList()
    i_LockState = cmds.getAttr(l_oSels[2], lock=True)
    if i_LockState:
        cmds.setAttr(l_oSels[2], lock=False)
    if s_name == "NewName":
        s_NewName = l_oSels[0] + "." + i_s_textField
        cmds.renameAttr(l_oSels[2], i_s_textField)
        if i_LockState:
            cmds.setAttr(s_NewName, lock=True)
        s_search = i_s_textField
    else:
        cmds.addAttr(l_oSels[2], edit=True, niceName=i_s_textField)
        if i_LockState:
            cmds.setAttr(l_oSels[2], lock=True)
        s_search = l_oSels[1]
    l_ChannelAtList = rsChannelAtList()
    l_AttrKey = l_ChannelAtList[0]
    l_AttrKeyHidden = l_ChannelAtList[1]
    if l_AttrKey or l_AttrKeyHidden:
        cmds.textScrollList("rsAttributeScroll", edit=True, removeAll=True, append=l_AttrKey)
        cmds.textScrollList("rsAttributeScrollHidden", edit=True, removeAll=True, append=l_AttrKeyHidden)
    cmds.select(cl=True)
    cmds.select(l_oSels[0], r=True)
    rsSearchInScroll(s_search)
    return True


##
# Set attribute property function.
# @param i_s_intro - 3D object.
# @param i_s_button - Name of the attribute property radio button.
# @return boolean.
def rsChProperties(i_s_intro, i_s_button):
    l_oSels = rsObjList()
    i_atKey = cmds.getAttr(l_oSels[2], keyable=True)
    s_channel = False
    if i_atKey == 1:
        s_keyable = True
    else:
        s_keyable = False
        i_atHidden = cmds.getAttr(l_oSels[2], channelBox=True)
        if i_atHidden == 0:
            s_channel = False
        else:
            s_channel = True
    cmds.setAttr(l_oSels[2], keyable=s_keyable, channelBox=s_channel)
    if i_s_button == "rsKeyable":
        cmds.setAttr(l_oSels[2], keyable=True, channelBox=False)
    if i_s_button == "rsDisplayable":
        cmds.setAttr(l_oSels[2], keyable=False, channelBox=True)
    if i_s_button == "rsHidden":
        cmds.setAttr(l_oSels[2], keyable=False, channelBox=False)
    l_ChannelAtList = rsChannelAtList()
    l_AttrKey = l_ChannelAtList[0]
    l_AttrKeyHidden = l_ChannelAtList[1]
    if l_AttrKey or l_AttrKeyHidden:
        cmds.textScrollList("rsAttributeScroll", edit=True, removeAll=True, append=l_AttrKey)
        cmds.textScrollList("rsAttributeScrollHidden", edit=True, removeAll=True, append=l_AttrKeyHidden)
    rsSearchInScroll(l_oSels[1])
    return True


##
# Search and selection attribute function.
# @param i_s_search - Name of the attribute.
# @return boolean.
def rsSearchInScroll(i_s_search):
    l_ChannelAtList = rsChannelAtList()
    l_AttrKey = l_ChannelAtList[0]
    l_AttrKeyHidden = l_ChannelAtList[1]
    for i in range(len(l_AttrKey)):
        if l_AttrKey[i] == i_s_search:
            cmds.textScrollList("rsAttributeScroll", edit=True, selectItem=str(l_AttrKey[i]))
    for i in range(len(l_AttrKeyHidden)):
        if l_AttrKeyHidden[i] == i_s_search:
            cmds.textScrollList("rsAttributeScrollHidden", edit=True, selectItem=l_AttrKeyHidden[i])
    return True


##
# Classification function of attributes according visibility.
# @param none.
# @return l_ChannelAtList - Visible objects list..
# @return l_NoChannelAtList - Invisible objects list.
def rsChannelAtList():
    s_oSel = cmds.ls(selection=True)
    l_ChannelAtList = []
    l_NoChannelAtList = []
    l_usDefined = cmds.listAttr(s_oSel[0], userDefined=True)
    if l_usDefined:
        for s_usDef in l_usDefined:
            s_objAtr = (s_oSel[0] + "." + s_usDef)
            i_atKey = cmds.getAttr(s_objAtr, keyable=True)
            i_atHidden = cmds.getAttr(s_objAtr, channelBox=True)
            s_atType = cmds.getAttr(s_objAtr, type=True)
            if s_atType == "double3" or s_atType == "string":
                l_NoChannelAtList.append(s_usDef)
            elif i_atKey == 1:
                l_ChannelAtList.append(s_usDef)
            else:
                if i_atHidden == 1:
                    l_ChannelAtList.append(s_usDef)
                else:
                    l_NoChannelAtList.append(s_usDef)
    return l_ChannelAtList, l_NoChannelAtList


##
# Move function of the textScrollList attribute.
# @param i_value - Value positive for move up and negative for move down.
# @return boolean.
def rsMvAtt(i_value):
    l_oSels = rsObjList()
    if cmds.textScrollList("rsAttributeScroll", query=True, numberOfSelectedItems=True) != 1:
        print "Only \"Display Attributes\" elements can be rearranged."
        return
    l_AttributeList = (cmds.textScrollList("rsAttributeScroll", query=True, allItems=True))
    i_chLockVectors = cmds.checkBox("rsLockVectors", query=True, value=True)
    i_AttOrder = cmds.textScrollList("rsAttributeScroll", query=True, selectIndexedItem=1)[0]
    i_AttNum = cmds.textScrollList("rsAttributeScroll", query=True, numberOfItems=1)
    cmds.attributeQuery((l_AttributeList[i_AttOrder - 1]), node=l_oSels[0], listSiblings=True)
    l_BeforeSiblings = []
    if (i_AttOrder - 2) > -1:
        l_AntSiblings = cmds.attributeQuery((l_AttributeList[i_AttOrder - 2]), node=l_oSels[0], listSiblings=True)
        s_anterior = l_AttributeList[i_AttOrder - 3]
        if l_AntSiblings:
            if l_AttributeList[i_AttOrder - 1] in l_AntSiblings:
                l_BeforeSiblings.append(i_AttOrder)
            l_BeforeSiblings.append(i_AttOrder - 1)
            i_searchSibling = i_AttOrder - 3
            x = 1
            while x > 0:
                if i_searchSibling > -1:
                    if s_anterior in l_AntSiblings:
                        l_BeforeSiblings.append(i_searchSibling + 1)
                    else:
                        x = 0
                    l_AntSiblings = cmds.attributeQuery((l_AttributeList[i_searchSibling]), node=l_oSels[0], listSiblings=True)
                    if l_AntSiblings:
                        i_searchSibling = i_searchSibling - 1
                        s_anterior = l_AttributeList[i_searchSibling]
                    else:
                        x = 0
                else:
                    x = 0
    if l_BeforeSiblings:
        l_BeforeSiblings.reverse()
    l_AfterSiblings = []
    if i_AttOrder < i_AttNum:
        l_PostSiblings = cmds.attributeQuery((l_AttributeList[i_AttOrder]), node=l_oSels[0], listSiblings=True)
        if (i_AttOrder + 1) < i_AttNum:
            s_posterior = l_AttributeList[i_AttOrder + 1]
        if l_PostSiblings:
            if l_AttributeList[i_AttOrder - 1] in l_PostSiblings:
                l_AfterSiblings.append(i_AttOrder)
            l_AfterSiblings.append(i_AttOrder + 1)
            i_searchSibling = i_AttOrder + 1
            x = 1
            while x > 0:
                if i_searchSibling < i_AttNum:
                    if s_posterior in l_PostSiblings:
                        l_AfterSiblings.append(i_searchSibling + 1)
                    else:
                        x = 0
                    l_PostSiblings = cmds.attributeQuery((l_AttributeList[i_searchSibling]), node=l_oSels[0], listSiblings=True)
                    if l_PostSiblings and i_searchSibling < i_AttNum - 1:
                        i_searchSibling = i_searchSibling + 1
                        s_posterior = l_AttributeList[i_searchSibling]
                    else:
                        x = 0
                else:
                    x = 0
    i_exist = 1
    l_siblings = []
    if l_BeforeSiblings or l_AfterSiblings:
        if i_AttOrder in l_BeforeSiblings and i_AttOrder in l_AfterSiblings:
            l_siblings = l_BeforeSiblings
            for s_after in l_AfterSiblings:
                if s_after not in l_siblings:
                    l_siblings.append(s_after)
        elif i_AttOrder in l_BeforeSiblings and i_AttOrder not in l_AfterSiblings and i_value == 1:
            l_siblings = l_BeforeSiblings
        elif i_AttOrder not in l_BeforeSiblings and i_AttOrder in l_AfterSiblings and i_value == -1:
            l_siblings = l_AfterSiblings
        else:
            if l_BeforeSiblings and i_value == -1:
                l_siblings = l_BeforeSiblings
            if l_AfterSiblings and i_value == 1:
                l_siblings = l_AfterSiblings
        if i_AttOrder not in l_BeforeSiblings and i_AttOrder not in l_AfterSiblings:
            i_exist = 0
        l_s_siblings = []
        if l_siblings:
            if i_value == 1:
                l_siblings.reverse()
            for l_i_sib in l_siblings:
                l_s_siblings.append(l_AttributeList[l_i_sib - 1])
    s_att = l_AttributeList[i_AttOrder - 1]
    if i_AttOrder < i_AttNum and i_value == 1 or i_AttOrder > 1 and i_value == -1:
        if not i_chLockVectors:
            rsMoveList(i_AttOrder, s_att, i_value, i_AttOrder)
        else:
            if l_siblings:
                if i_exist == 0:
                    i_move = len(l_siblings) * i_value
                    rsMoveList(i_AttOrder, s_att, i_move, i_AttOrder)
                elif 1 in l_siblings and i_value == -1 or i_AttNum in l_siblings and i_value == 1:
                    print "..............................................."
                    print "The brothers can not be moved in this direction"
                    print "..............................................."
                else:
                    rsMoveList(l_siblings, l_s_siblings, i_value, i_AttOrder)
            else:
                rsMoveList(i_AttOrder, s_att, i_value, i_AttOrder)
    else:
        print "..............................................."
        print "The attribute cannot be moved in this direction"
        print "..............................................."
    return True


##
# Move action function of the textScrollList attribute.
# @param i_l_i_atts - List index to move.
# @param i_l_s_atts - List name to move.
# @param i_i_pos - Positions number to move.
# @param i_i_AttSel - Selected attribute index.
# @return boolean.
def rsMoveList(i_l_i_atts, i_l_s_atts, i_i_pos, i_i_AttSel):
    if isinstance(i_l_i_atts, list):
        i_len = len(i_l_s_atts)
        for i in range(i_len):
            i_NewAttPos = i_l_i_atts[i] + i_i_pos
            cmds.textScrollList("rsAttributeScroll", edit=True, removeIndexedItem=i_l_i_atts[i])
            cmds.textScrollList("rsAttributeScroll", edit=True, appendPosition=[i_NewAttPos, i_l_s_atts[i]])
    else:
            i_NewAttPos = i_l_i_atts + i_i_pos
            cmds.textScrollList("rsAttributeScroll", edit=True, removeIndexedItem=i_l_i_atts)
            cmds.textScrollList("rsAttributeScroll", edit=True, appendPosition=[i_NewAttPos, i_l_s_atts])
    i_AttSel = i_i_AttSel + i_i_pos
    cmds.textScrollList("rsAttributeScroll", edit=True, selectIndexedItem=i_AttSel)
    return True


##
# ChannelBox attributes reorder function.
# @param none
# @return boolean.
def rsReAtt():
    l_oSels = rsObjList()
    l_AttributeList = (cmds.textScrollList("rsAttributeScroll", query=True, allItems=True))
    for s_Att in l_AttributeList:
        s_orig = l_oSels[0] + "." + s_Att
        i_LockState = cmds.getAttr(s_orig, lock=True)
        if i_LockState:
            cmds.setAttr(s_orig, lock=False)
        l_paramDest = cmds.listConnections(s_orig, plugs=True, destination=True, source=True)
        l_paramDestLock = []
        if l_paramDest:
            for z in range(len(l_paramDest)):
                l_paramDestLock.append(cmds.getAttr(l_paramDest[z], lock=True))
                if l_paramDestLock[z]:
                    cmds.setAttr(l_paramDest[z], lock=False)
        cmds.deleteAttr(l_oSels[0], at=s_Att)
        cmds.undo()
        if l_paramDest:
            for z in range(len(l_paramDest)):
                l_paramDestLock.append(cmds.getAttr(l_paramDest[z], lock=True))
                if l_paramDestLock[z]:
                    cmds.setAttr(l_paramDest[z], lock=True)
        if i_LockState:
            cmds.setAttr(s_orig, lock=True)
    cmds.select(cl=True)
    cmds.select(l_oSels[0], r=True)
    return True


##
# ChannelBox selected attributes function.
# @param none
# @return boolean.
def attSelectedHidden():
    cmds.textScrollList("rsAttributeScroll", edit=True, deselectAll=True)
    rsAttributeScrollSelec()
    return True


##
# Selected hidden attributes function.
# @param none
# @return boolean.
def attSelected():
    cmds.textScrollList("rsAttributeScrollHidden", edit=True, deselectAll=True)
    rsAttributeScrollSelec()
    return True


##
# Selected attributes function.
# @param none
# @return s_AttSelec - Name of the scrollList.
def rsAtribute():
    if cmds.textScrollList("rsAttributeScroll", query=True, numberOfSelectedItems=True):
        s_AttSelec = (cmds.textScrollList("rsAttributeScroll", query=True, selectItem=True))[0]
    else:
        s_AttSelec = (cmds.textScrollList("rsAttributeScrollHidden", query=True, selectItem=True))[0]
    return s_AttSelec


##
# Function of activations of selected attribute properties.
# @param none.
# @return boolean.
def rsAttributeScrollSelec():
    s_AttSelec = rsAtribute()
    l_oSels = cmds.ls(selection=True)
    if not l_oSels:
        return
    i_s_oSele = l_oSels[0]
    s_ObjAttr = i_s_oSele + "." + s_AttSelec
    s_atType = cmds.getAttr(s_ObjAttr, type=True)
    rsAttEnable()
    if s_atType == "double3":
        rsEnumNoEnable()
        rsLockNoEnable()
        rsPropertyNoEnable()
        rsCheckNoEnable()
        rsMinNoEnable()
        rsMaxNoEnable()
        rsAttDefaultNoEnable()
        i_LockState = 0
        i_ProperState = 0
        i_NumericState = 0
        f_atDefValue = 0
    elif s_atType == "enum":
        rsEnumNoEnable()
        rsCheckNoEnable()
        rsMinNoEnable()
        rsMaxNoEnable()
        rsLockEnable()
        rsPropertyEnable()
        rsAttDefaultNoEnable()
        attEnumScroll()
        f_atDefValue = 0
        i_LockState = 1
        i_ProperState = 1
        i_NumericState = 0
    elif s_atType == "string":
        rsEnumNoEnable()
        rsEnumEnable()
        rsLockEnable()
        rsPropertyNoEnable()
        rsCheckNoEnable()
        rsMinNoEnable()
        rsMaxNoEnable()
        s_stringValue = cmds.getAttr(s_ObjAttr)
        cmds.textField("StringText", edit=True, text=s_stringValue)
        rsAttDefaultNoEnable()
        i_LockState = 1
        i_ProperState = 0
        i_NumericState = 0
    else:
        rsAttEnable()
        cmds.textScrollList("rsEnumScroll", edit=True, removeAll=True, enable=False)
        cmds.textField("StringText", edit=True, text="", enable=False)
        rsLockEnable()
        rsPropertyEnable()
        rsCheckEnable()
        rsAttDefaultEnable()
        rsMinNoEnable()
        rsMaxNoEnable()
        f_atDefValue = (cmds.attributeQuery(s_AttSelec, node=i_s_oSele, listDefault=True))[0]
        i_LockState = 1
        i_ProperState = 1
        i_NumericState = 1
    l_oSels = rsObjList()
    l_Siblings = cmds.attributeQuery(l_oSels[1], node=l_oSels[0], listSiblings=True)
    if l_Siblings:
        rsAttDefaultNoEnable()
    cmds.textField("rsNewNameText", edit=True, text=s_AttSelec)
    s_niceName = cmds.attributeQuery(s_AttSelec, node=i_s_oSele, niceName=True)
    cmds.textField("rsNiceNameText", edit=True, text=s_niceName)
    if i_LockState == 1:
        i_atLock = cmds.getAttr(s_ObjAttr, lock=True)
        if i_atLock == 0:
            cmds.radioButton("rsUnLock", edit=True, select=True)
        else:
            cmds.radioButton("rsLock", edit=True, select=True)
    if i_ProperState == 1:
        i_atKey = cmds.getAttr(s_ObjAttr, keyable=True)
        if i_atKey == 1:
            cmds.radioButton("rsKeyable", edit=True, select=True)
        else:
            i_atHidden = cmds.getAttr(s_ObjAttr, channelBox=True)
            if i_atHidden == 0:
                cmds.radioButton("rsHidden", edit=True, select=True)
            else:
                cmds.radioButton("rsDisplayable", edit=True, select=True)
    if i_NumericState == 1:
        i_atMinExist = cmds.attributeQuery(s_AttSelec, node=i_s_oSele, minExists=True)
        if i_atMinExist == 1 and s_atType != "enum":
            cmds.checkBox("rsMinBox", edit=True, value=True)
            f_atMinValue = (cmds.attributeQuery(s_AttSelec, node=i_s_oSele, minimum=True))[0]
            cmds.floatField("rsMinField", edit=True, value=f_atMinValue, enable=True)
        i_atMaxExist = cmds.attributeQuery(s_AttSelec, node=i_s_oSele, maxExists=True)
        if i_atMaxExist == 1 and s_atType != "enum":
            cmds.checkBox("rsMaxBox", edit=True, value=True)
            f_atMaxValue = (cmds.attributeQuery(s_AttSelec, node=i_s_oSele, maximum=True))[0]
            cmds.floatField("rsMaxField", edit=True, value=f_atMaxValue, enable=True)
        cmds.floatField("rsDefaultField", edit=True, value=f_atDefValue)
    return True


##
# Selected Enum element return function.
# @param none.
# @return boolean.
def attEnumSelected():
    l_oSels = cmds.ls(selection=True)
    if not l_oSels:
        return
    s_EnumSelec = (cmds.textScrollList("rsEnumScroll", query=True, selectItem=True))[0]
    if s_EnumSelec == " ":
        s_EnumSelec = ""
    cmds.textField("StringText", edit=True, text=s_EnumSelec)
    return True


##
# Fill Enum list function.
# @param none.
# @return boolean.
def attEnumScroll():
    l_oSels = rsObjList()
    s_enum = (cmds.attributeQuery(l_oSels[1], node=l_oSels[0], listEnum=True))[0]
    l_enum = s_enum.split(':')
    l_enum.append(" ")
    cmds.textScrollList("rsEnumScroll", edit=True, removeAll=True, append=l_enum, selectItem=l_enum[0], enable=True)
    cmds.textField("StringText", edit=True, text=l_enum[0], enable=True)
    return True


##
# Modification of Enum Attribute or selected string function.
# @param i_s_FieldText - 3D object.
# @return boolean.
def attEnumModify(i_s_FieldText):
    l_oSels = rsObjList()
    s_atType = cmds.getAttr(l_oSels[2], type=True)
    s_FieldText = cmds.textField("StringText", query=True, text=True)
    if s_atType == "enum":
        s_enum = (cmds.attributeQuery(l_oSels[1], node=l_oSels[0], listEnum=True))[0]
        s_EnumSelec = (cmds.textScrollList("rsEnumScroll", query=True, selectItem=True))[0]
        if s_EnumSelec != " ":
            s_NewEnum = s_enum.replace(s_EnumSelec, s_FieldText)
        else:
            s_NewEnum = s_enum + ":" + s_FieldText
        cmds.addAttr(l_oSels[2], edit=True, enumName=s_NewEnum)
        attEnumScroll()
    else:
        cmds.setAttr(l_oSels[2], s_FieldText, type="string")
    return True
