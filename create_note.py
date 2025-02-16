# create a note 

from aqt import mw

def create_note(question, answer):
    assert len(question) and len(answer), 'need question and answer'
    
    note = mw.col.newNote()
    note.fields = (question, answer)

    # lazy
    count = mw.col.card_count()
    mw.col.addNote(note)
    assert mw.col.card_count == count + 1, 'need to save card'
