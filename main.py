import sys
from os import path
# 关键导入：添加 Qt 模块
from PySide6.QtCore import QUrl, QCoreApplication, Qt  # <-- 这里补上 Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterSingletonType
import qml_rc
import js_rc
import res_rc


def singleton_regist():
    """QML 全局单例注册"""
    qmlRegisterSingletonType(QUrl("qrc:/Src/qml/basic/BasicConfig.qml"), 
                            "BasicConfig", 1, 0, "BasicConfig")

def global_regist():
    """C++ 全局注册（留空备用）"""
    pass

def init():
    """初始化操作"""
    singleton_regist()
    global_regist()
    QCoreApplication.setOrganizationName("Some organization")

def model_regist(engine: QQmlApplicationEngine):
    """注册上下文数据模型"""
    # 轮播图数据模型
    carousel_list = [f"/Resources/cherryPick/carouselI{i+1}.png" for i in range(6)]
    engine.rootContext().setContextProperty("carouselListModel", carousel_list)
    
    # 歌单广场模型
    song_square_list = ["你是否也喜欢", "你的专属歌单", "优质歌单甄选", 
                       "新音乐发现", "这些歌单，正合你意"]
    engine.rootContext().setContextProperty("singSquareListModel", song_square_list)

if __name__ == "__main__":
    # 启用高DPI缩放
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # 注册数据模型
    model_regist(engine)
    
    # 加载QML主文件
    qml_file = QUrl("qrc:/main.qml")
    
    def handle_object_created(obj, url):
        if not obj and url == qml_file:
            QCoreApplication.exit(-1)
    
    engine.objectCreated.connect(handle_object_created, Qt.ConnectionType.QueuedConnection)
    engine.load(qml_file)
    
    # 执行初始化
    init()
    
    sys.exit(app.exec())
