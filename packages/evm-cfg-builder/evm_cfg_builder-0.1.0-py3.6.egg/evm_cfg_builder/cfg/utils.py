from .function import Function

def bb_can_be_in_dispatcher(bb):
    return not bb.fathers or all(key == Function.DISPATCHER_ID for key in bb.fathers.keys())
