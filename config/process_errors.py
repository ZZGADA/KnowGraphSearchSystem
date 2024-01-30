from dataclasses import dataclass

#状态信息类的定义
@dataclass
class ProcessInfo:
    status_code:int #状态码
    message:str  #返回信息说明


#状态码的存放
class Status_codes:
    #200X表示操作种类 1表示成功 0表示失败
    ok=200
    error=100

    cypher_query=200
    cypher_update = 201
    cypher_add=202
    cypher_delete=203


    SAVE_OK=ok
    DELETE_OK=ok
    UPDATE_OK=ok
    GET_OK=ok
    POST_OK=ok

    SAVE_ERROR = error
    DELETE_ERROR = error
    UPDATE_ERROR = error
    GET_ERROR = error
    POST_ERROR = error

#状态信息的存放
class Status_messages:
    success="success"
    failed="failed"
    SAVE_OK = success
    DELETE_OK = success
    UPDATE_OK = success
    GET_OK = success
    POST_OK = success

    SAVE_ERROR = failed
    DELETE_ERROR = failed
    UPDATE_ERROR = failed
    GET_ERROR = failed
    POST_ERROR = failed

class ProcessInfos:
    ADD_SUCCEED = ProcessInfo(status_code=Status_codes.SAVE_OK,message=Status_messages.SAVE_OK)
    DELETE_SUCCEED = ProcessInfo(status_code=Status_codes.DELETE_OK,message=Status_messages.DELETE_OK)
    UPDATE_SUCCEED = ProcessInfo(status_code=Status_codes.UPDATE_OK,message=Status_messages.UPDATE_OK)
    GET_SUCCEED = ProcessInfo(status_code=Status_codes.GET_OK,message=Status_messages.GET_OK,)
    POST_SUCCEED = ProcessInfo(status_code=Status_codes.POST_OK,message=Status_messages.POST_OK)

    ADD_FAILED = ProcessInfo(status_code=Status_codes.SAVE_ERROR,message=Status_messages.SAVE_ERROR)
    DELETE_FAILED = ProcessInfo(status_code=Status_codes.DELETE_ERROR,message=Status_messages.DELETE_ERROR)
    UPDATE_FAILED = ProcessInfo(status_code=Status_codes.UPDATE_ERROR,message=Status_messages.UPDATE_ERROR)
    GET_FAILED = ProcessInfo(status_code=Status_codes.GET_ERROR,message=Status_messages.GET_ERROR)
    POST_FAILED = ProcessInfo(status_code=Status_codes.POST_ERROR,message=Status_messages.POST_ERROR)