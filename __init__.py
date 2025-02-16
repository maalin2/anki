# main window
from aqt import mw
# print to screen; bind callbacks
from aqt.utils import showInfo, qconnect
# qt component
from aqt.qt import QAction

from .create_note import create_note

# callback
def handle_note():
    create_note('test note', 'test note\'s answer')
    showInfo("new note succesfully created")

# add dropdown item to main window
def setup_menu():
    if not hasattr(mw.form, 'menuTools'):
        print('menuTools not ready yet')

    # create tools thingy and use callback 
    action = QAction("create test note", mw)  
    qconnect(action.triggered, handle_note)  
    mw.form.menuTools.addAction(action)  

# load 
setup_menu()
