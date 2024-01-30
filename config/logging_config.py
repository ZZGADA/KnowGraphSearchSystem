import logging,os,datetime
import time
import sys
sys.path.append(r"../")  #返回上级目录

#自定义的logging配置 提高logging的可用性
class logging_self_define:

    def make_log_dir(self, dirname='logs'):  # 创建存放日志的目录，并返回目录的路径
        now_dir = os.path.dirname(__file__)
        father_path = os.path.split(now_dir)[0]
        date_month = "{}".format(time.strftime("%Y-%m", time.localtime()))  ##获取当月并创建文件夹
        path = os.path.join(father_path, dirname,date_month) #D:\python\Knowledge_Graph_HUAYUN\logs\2023-08-17   绝对路径
        path = os.path.normpath(path)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def get_log_filename(self):  # 创建日志文件的文件名格式，便于区分每天的日志
        filename = "{}.log".format(time.strftime("%Y-%m-%d", time.localtime()))
        filename = os.path.join(self.make_log_dir(), filename)
        filename = os.path.normpath(filename)
        return filename


    def log(self,level='INFO',name="root"):#生成日志的主方法,传入对那些级别及以上的日志进行处理
        logger = logging.getLogger(name)#创建日志器
        # print(logger.name)
        level = getattr(logging, level)  # 获取日志模块的的级别对象属性

        logger.setLevel(level)  # 设置日志级别
        if not logger.handlers:  # 作用,防止重新生成处理器
            sh = logging.StreamHandler()  # 创建控制台日志处理器
            # fh = logging.FileHandler(filename=self.get_log_filename(), mode='a', encoding="utf-8")  # 创建日志文件处理器
            # 创建格式器
            fmt = logging.Formatter("%(asctime)s-%(levelname)s-%(filename)s-%(funcName)s-Line:%(lineno)d-Message:%(message)s")
            # 给处理器添加格式
            sh.setFormatter(fmt=fmt)
            # fh.setFormatter(fmt=fmt)
            # 给日志器添加处理器，过滤器一般在工作中用的比较少，如果需要精确过滤，可以使用过滤器
            logger.addHandler(sh)
            # logger.addHandler(fh)

        return logger  # 返回日志器






if __name__=="__main__":


    '''
    logger：日志器，提供程序可使用的接口

    handler：处理器，用于写入日志文件并输出到指定位置，如文件、控制台或网络等

    filter：过滤器，用于输出符合指定条件的日志记录

    formatter：格式器，决定日志记录的输出格式
    
    DEBUG、INFO、WARNING、ERROR、CRITICAL  顺序从小到大
    '''
