# ----------------------------------------------------------------------
# Description:
#
# TODO
# ----------------------------------------------------------------------

from maya.api import OpenMaya as om2


def attributeType(plug):
    """Return the attribute type of the plug.

    :param plug: The MPlug to get the attribute type from.
    :type plug: om2.MPlug

    :return: The type of the MPlug attribute.
    :rtype: str or None
    """
    attr = plug.attribute()
    apiType = attr.apiType()

    if apiType == om2.MFn.kTypedAttribute:
        attrType = om2.MFnTypedAttribute(attr).attrType()
        if attrType == om2.MFnData.kIntArray:
            return "Int32Array"
        elif attrType == om2.MFnData.kFloatArray:
            return "floatArray"
        elif attrType == om2.MFnData.kDoubleArray:
            return "doubleArray"
        elif attrType == om2.MFnData.kString:
            return "string"
        elif attrType == om2.MFnData.kStringArray:
            return "stringArray"

    elif apiType == om2.MFn.kNumericAttribute:
        attrType = om2.MFnNumericAttribute(attr).numericType()
        if attrType == om2.MFnNumericData.kBoolean:
            return "bool"
        elif attrType == om2.MFnNumericData.kShort:
            return "short"
        elif attrType == om2.MFnNumericData.kInt:
            return "int"
        elif attrType == om2.MFnNumericData.kFloat:
            return "float"
        elif attrType == om2.MFnNumericData.kDouble:
            return "double"

    elif apiType == om2.MFn.kDoubleLinearAttribute:
        return "double"
    elif apiType == om2.MFn.kFloatLinearAttribute:
        return "float"
    elif apiType == om2.MFn.kDoubleAngleAttribute:
        return "double"
    elif apiType == om2.MFn.kFloatAngleAttribute:
        return "float"

    elif apiType == om2.MFn.kEnumAttribute:
        return "enum"

    elif apiType == om2.MFn.kMatrixAttribute:
        return "matrix"

    elif apiType == om2.MFn.kGenericAttribute:
        return "generic"

    elif apiType == om2.MFn.kMessageAttribute:
        return "message"


# ----------------------------------------------------------------------
# Copyright 2021 brave rabbit, Ingo Clemens. All rights reserved.
#
# Use of this software is subject to the terms of the brave rabbit
# SHAPES license agreement provided at the time of installation, or
# which otherwise accompanies this software in electronic form.
# ----------------------------------------------------------------------
