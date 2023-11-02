from tests.utils import get_resources
from aria.articles.services import summarize_text, Summarizer_Mode

def test_summarize_text():
    with open(get_resources("long_article.txt"), 'r') as f:
        summary = summarize_text(f.read(), Summarizer_Mode.FAST)
        print(summary)
    assert 1 == 1