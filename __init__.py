# main window
from aqt import mw
# print to screen; bind callbacks
from aqt.utils import showInfo, qconnect
# qt component
from aqt.qt import QAction

# callback
def on_test_action():
    showInfo("hello world")

# add item to main window
def setup_menu():
    if not hasattr(mw.form, 'menuTools'):
        print('menuTools not ready yet')

    action = QAction("test item", mw)  
    qconnect(action.triggered, on_test_action)  
    mw.form.menuTools.addAction(action)  

# load 
setup_menu()
