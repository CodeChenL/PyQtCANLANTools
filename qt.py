import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from usb_device import *


# 添加工具栏按钮
def addtoolbtn(toolbar: QToolBar, text: str, icon: QIcon, menu: QMenu):
    toolbtn = QToolButton()
    toolbtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
    toolbtn.setIcon(icon)
    toolbtn.setText(text)
    toolbar.addWidget(toolbtn)
    toolbtn.setPopupMode(QToolButton.InstantPopup)
    toolbtn.setMenu(menu)


class devicemanger(QMainWindow):
    def __init__(self):
        super().__init__()
        dock = QDockWidget()
        dock.setWindowTitle("设备管理")
        tw = QTableWidget(9, 4)
        tw.setHorizontalHeaderLabels(["设备", "开启", "关闭", "设备信息"])
        dock.setWidget(tw)
        w.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, dock)
        # 尝试连接can盒子
        DevHandles = (c_uint * 20)()
        # Scan device
        ret = USB_ScanDevice(byref(DevHandles))
        if (ret == 0):
            print("No device connected!")
            exit()
        else:
            print("Have %d device connected!" % ret)
        # Open device
        ret = USB_OpenDevice(DevHandles[0])
        if (bool(ret)):
            print("Open device success!")
        else:
            print("Open device faild!")
            exit()
        # Get device infomation
        USB2XXXInfo = DEVICE_INFO()
        USB2XXXFunctionString = (c_char * 256)()
        ret = DEV_GetDeviceInfo(DevHandles[0], byref(USB2XXXInfo), byref(USB2XXXFunctionString))
        if (bool(ret)):
            print("USB2XXX device infomation:")
            print("--Firmware Name: %s" % bytes(USB2XXXInfo.FirmwareName).decode('ascii'))
            print("--Firmware Version: v%d.%d.%d" % (
            (USB2XXXInfo.FirmwareVersion >> 24) & 0xFF, (USB2XXXInfo.FirmwareVersion >> 16) & 0xFF,
            USB2XXXInfo.FirmwareVersion & 0xFFFF))
            print("--Hardware Version: v%d.%d.%d" % (
            (USB2XXXInfo.HardwareVersion >> 24) & 0xFF, (USB2XXXInfo.HardwareVersion >> 16) & 0xFF,
            USB2XXXInfo.HardwareVersion & 0xFFFF))
            print("--Build Date: %s" % bytes(USB2XXXInfo.BuildDate).decode('ascii'))
            print("--Serial Number: ", end='')
            for i in range(0, len(USB2XXXInfo.SerialNumber)):
                print("%08X" % USB2XXXInfo.SerialNumber[i], end='')
            print("")
            print("--Function String: %s" % bytes(USB2XXXFunctionString.value).decode('ascii'))
        else:
            print("Get device infomation faild!")
            exit()
        device_name = "%s" % bytes(USB2XXXFunctionString.value).decode('ascii')
        device_name += "%08X" % USB2XXXInfo.SerialNumber[len(USB2XXXInfo.SerialNumber) - 1]
        device_name_item = QTableWidgetItem()
        device_name_item.setData(0, device_name)
        tw.setItem(1, 0, device_name_item)
        btn_start = QPushButton("启动")
        tw.setCellWidget(1, 1, btn_start)
        btn_stop = QPushButton("停止")
        tw.setCellWidget(1, 2, btn_stop)
        btn_info = QPushButton("设备信息")
        btn_info.clicked.connect(device_info)
        tw.setCellWidget(1, 3, btn_info)
        w.setMinimumSize(tw.size())
        w.setMinimumSize(w.size().width(), 0)


class add_CAN(QMainWindow):
    def __init__(self):
        super().__init__
        dock = QDockWidget()
        dock.setWindowTitle("CAN视图")
        w.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, dock)
        in_dock = QWidget()
        bvl=QVBoxLayout()
        bhl=QHBoxLayout()
        bvl.addLayout(bhl)
        device_channel_title = QLabel(text="设备及通道:")
        bhl.addWidget(device_channel_title)
        device_channel_list = QComboBox()
        # 尝试连接can盒子
        DevHandles = (c_uint * 20)()
        # Scan device
        ret = USB_ScanDevice(byref(DevHandles))
        if (ret == 0):
            print("No device connected!")
            exit()
        else:
            print("Have %d device connected!" % ret)
        # Open device
        ret = USB_OpenDevice(DevHandles[0])
        if (bool(ret)):
            print("Open device success!")
        else:
            print("Open device faild!")
            exit()
        # Get device infomation
        USB2XXXInfo = DEVICE_INFO()
        USB2XXXFunctionString = (c_char * 256)()
        ret = DEV_GetDeviceInfo(DevHandles[0], byref(USB2XXXInfo), byref(USB2XXXFunctionString))
        if (bool(ret)):
            print("USB2XXX device infomation:")
            print("--Firmware Name: %s" % bytes(USB2XXXInfo.FirmwareName).decode('ascii'))
            print("--Firmware Version: v%d.%d.%d" % (
            (USB2XXXInfo.FirmwareVersion >> 24) & 0xFF, (USB2XXXInfo.FirmwareVersion >> 16) & 0xFF,
            USB2XXXInfo.FirmwareVersion & 0xFFFF))
            print("--Hardware Version: v%d.%d.%d" % (
            (USB2XXXInfo.HardwareVersion >> 24) & 0xFF, (USB2XXXInfo.HardwareVersion >> 16) & 0xFF,
            USB2XXXInfo.HardwareVersion & 0xFFFF))
            print("--Build Date: %s" % bytes(USB2XXXInfo.BuildDate).decode('ascii'))
            print("--Serial Number: ", end='')
            for i in range(0, len(USB2XXXInfo.SerialNumber)):
                print("%08X" % USB2XXXInfo.SerialNumber[i], end='')
            print("")
            print("--Function String: %s" % bytes(USB2XXXFunctionString.value).decode('ascii'))
        else:
            print("Get device infomation faild!")
            exit()
        can = ["[%08X] [CAN1]" % USB2XXXInfo.SerialNumber[len(USB2XXXInfo.SerialNumber) - 1],
               "[%08X] [CAN2]" % USB2XXXInfo.SerialNumber[len(USB2XXXInfo.SerialNumber) - 1]]
        device_channel_list.addItems(can)
        bhl.addWidget(device_channel_list)
        save=QPushButton("保存数据")
        bhl.addWidget(save)
        delete=QPushButton("清除数据")
        bhl.addWidget(delete)
        stop=QPushButton("暂停显示")
        bhl.addWidget(stop)
        run=QPushButton("滚动显示")
        bhl.addWidget(run)
        Filter=QPushButton("数据过滤")
        bhl.addWidget(Filter)
        setting=QPushButton("显示设置")
        bhl.addWidget(setting)
        update=QPushButton("更新显示")
        bhl.addWidget(update)
        tw = QTableWidget(10, 10)
        bvl.addWidget(tw)
        tw.setHorizontalHeaderLabels(['序号', '帧ID', '长度', '数据', '时间戳', '方向', '帧类型', 'CAN类型', '通道号', '设备号'])
        in_dock.setLayout(bvl)
        dock.setWidget(in_dock)


class device_info(QMainWindow):
    def __init__(self):
        super().__init__
        info = QDialog()
        info_ql = QLabel(info, text=device_info_toString())
        info.setFixedSize(310, 100)
        info.show()
        info.exec_()


def device_info_toString():
    # 尝试连接can盒子
    text = ""
    DevHandles = (c_uint * 20)()
    # Scan device
    ret = USB_ScanDevice(byref(DevHandles))
    if (ret == 0):
        print("No device connected!")
        exit()
    else:
        print("Have %d device connected!" % ret)
    # Open device
    ret = USB_OpenDevice(DevHandles[0])
    if (bool(ret)):
        print("Open device success!")
    else:
        print("Open device faild!")
        exit()
    # Get device infomation
    USB2XXXInfo = DEVICE_INFO()
    USB2XXXFunctionString = (c_char * 256)()
    ret = DEV_GetDeviceInfo(DevHandles[0], byref(USB2XXXInfo), byref(USB2XXXFunctionString))
    if (bool(ret)):
        text += "USB2XXX device infomation:\n"
        text += "--Firmware Name: %s\n" % bytes(USB2XXXInfo.FirmwareName).decode('ascii')
        text += "--Firmware Version: v%d.%d.%d\n" % (
        (USB2XXXInfo.FirmwareVersion >> 24) & 0xFF, (USB2XXXInfo.FirmwareVersion >> 16) & 0xFF,
        USB2XXXInfo.FirmwareVersion & 0xFFFF)
        text += "--Hardware Version: v%d.%d.%d\n" % (
        (USB2XXXInfo.HardwareVersion >> 24) & 0xFF, (USB2XXXInfo.HardwareVersion >> 16) & 0xFF,
        USB2XXXInfo.HardwareVersion & 0xFFFF)
        text += "--Build Date: %s\n" % bytes(USB2XXXInfo.BuildDate).decode('ascii')
        text += "--Serial Number: "
        for i in range(0, len(USB2XXXInfo.SerialNumber)):
            text += "%08X" % USB2XXXInfo.SerialNumber[i]
        text += "\n"
        text += "--Function String: %s\n" % bytes(USB2XXXFunctionString.value).decode('ascii')
    else:
        print("Get device infomation faild!")
        exit()
    return text


if __name__ == "__main__":
    # 创建程序
    app = QApplication(sys.argv)
    # 创建主界面
    w = QMainWindow()
    w.setWindowTitle("PyQtCANLINTools")
    w.setWindowIcon(QIcon("./pycharm.ico"))
    # 创建动作
    exitAct = QAction(QIcon('./pycharm.ico'), '设备管理')
    exitAct.triggered.connect(devicemanger)

    add_CAN_act = QAction(QIcon("./pycharm.ico"), "新增CAN视图")
    add_CAN_act.triggered.connect(add_CAN)

    device_info_act = QAction(QIcon("./pycharm.ico"), "设备信息")
    device_info_act.triggered.connect(device_info)
    # 创建工具栏
    toolbar = QToolBar('工具栏')
    w.addToolBar(toolbar)
    # 创建工具栏按钮的下拉菜单
    devicetool = QMenu()
    devicetool.addActions([exitAct])

    CANtool = QMenu()
    CANtool.addActions([add_CAN_act])

    addtoolbtn(toolbar, "设备管理", QIcon("./img/设备管理.svg"), devicetool)
    addtoolbtn(toolbar, "新增CAN视图", QIcon("./img/视图模式.svg"), CANtool)
    addtoolbtn(toolbar, "新增LIN视图", QIcon("./img/视图模式.svg"), devicetool)
    addtoolbtn(toolbar, "视图管理", QIcon("./img/视图配置.svg"), devicetool)
    toolbar.addSeparator()
    addtoolbtn(toolbar, "发送CAN数据", QIcon("./img/上传.svg"), devicetool)
    addtoolbtn(toolbar, "发送LIN数据", QIcon("./img/上传.svg"), devicetool)
    toolbar.addSeparator()
    addtoolbtn(toolbar, "高级功能", QIcon("./img/高级功能.svg"), devicetool)
    addtoolbtn(toolbar, "工具合集", QIcon("./img/设置.svg"), devicetool)
    toolbar.addSeparator()
    addtoolbtn(toolbar, "帮助", QIcon("./img/帮 助.svg"), devicetool)
    addtoolbtn(toolbar, "关于", QIcon("./img/关于.svg"), devicetool)
    addtoolbtn(toolbar, "语言", QIcon("./img/语言.svg"), devicetool)
    # 开启事件循环
    w.showMaximized()
    sys.exit(app.exec_())
