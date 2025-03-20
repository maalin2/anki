# create a note 

from aqt import mw

def create_note(question, answer):
    assert len(question) and len(answer), f'need question and answer\n{question}\t{answer}'
    
    note = mw.col.newNote()
    note.fields = (question, answer)

    # lazy
    count = mw.col.card_count()
    mw.col.addNote(note)
    assert count + 1 == mw.col.card_count(), f'need to save card {question} {answer}'
