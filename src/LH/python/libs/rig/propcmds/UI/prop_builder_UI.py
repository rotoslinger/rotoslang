from maya import cmds

def lock_unlock_transform(lock_attrs = ["all"], transform="", lock=True):
    # We want to invert the lock and use the value to remove things or add them to the channel box.
    # If locking attributes, they will be removed from the channel box and visa-versa
    # if lock == True: channelbox = False & if lock == False: channelBox = True.
    channelBox = not lock
    if lock_attrs == ["all"]:
        lock_attrs = ["tx","ty","tz","rx","ry","rz","sx","sy","sz","v"]
    for i in range(len(lock_attrs)):
        cmds.setAttr(ctrl="" + "." + lock_attrs[i],
                    lock = lock,
                    keyable = False,
                    channelBox = channelBox)
