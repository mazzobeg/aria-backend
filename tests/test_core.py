from app.core import summarize_text
    
def test_summarize_text():
    text_to_test = "Lorem ipsum."
    summary = summarize_text(text_to_test)
    assert summary is not None
    assert summary != ""