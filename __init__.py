import subprocess
import sys
import os

# anki window literals
from aqt.utils import showInfo, qconnect
from aqt.qt import QAction
from aqt import mw

from .create_note import create_note

def handle_note():
    """example note"""
    create_note('test note', 'test note\'s answer')
    showInfo("new note succesfully created")

def parse(out):
    """parse the stdout into list of (question, answer) tuples"""
    res = []

    lines = out.decode('utf-8').split('\n')[:-1]

    for line in lines:
        splitted = line.split('@@@')
        assert len(splitted) == 2, f'must have question, answer:\n {line} -> {splitted}\n{out}'
        q, a = splitted
        res.append((q, a))

    return res

def handle_api():
    """call read_pdf and generate some flashcards"""
    showInfo("be patient this will take a while")
    p = subprocess.Popen('./read_pdf', stdout=subprocess.PIPE)
    out, _ = p.communicate()

    parsed = parse(out)
    for q, a in parsed:
        create_note(q, a)

    showInfo(f"created {len(parsed)} new notes")

# add dropdown items to main window
def setup_menu():
    """bind handle_api, handle_note to mw"""
    if not hasattr(mw.form, 'menuTools'):
        print('menuTools not ready yet')

    # callback
    test_note = QAction("create test note", mw)  
    qconnect(test_note.triggered, handle_note)  
    mw.form.menuTools.addAction(test_note)  

    read_pdf = QAction("read pdf", mw)  
    qconnect(read_pdf.triggered, handle_api)  
    mw.form.menuTools.addAction(read_pdf)  

setup_menu()
