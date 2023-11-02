from transformers import pipeline
from nltk.tokenize import sent_tokenize
from aria.articles.models import Article
import requests
import logging as log

class Summarizer_Mode:
    FAST="fast"
    CONSERVATIVE="conservative"

def summarize_text_fast(full_text:str) -> str:
    log.debug(f'Summarize {full_text}')
    chunks = sent_tokenize(full_text)
    summary = []
    chunk_length = 25
    for i in range(0, len(chunks), chunk_length):
        sentence = ' '.join(chunks[i:i+chunk_length])
        if len(full_text) > 0 :
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            max_length_percentage = int(0.1*len(sentence))
            max_length_fix = 200
            max_length = max_length_fix if max_length_percentage > max_length_fix  else max_length_percentage
            min_length_percentage = int(0.05*len(sentence))
            min_length_fix = 100
            min_length = min_length_fix if min_length_percentage > min_length_fix  else min_length_percentage
            try:
                summary.append(summarizer(sentence, max_length = max_length , min_length=min_length, do_sample=False)[0]['summary_text'])
            except IndexError:
                pass
    return ' '.join(summary)

def summarize_text_conservative(full_text:str) -> str :
    """
    Summarizes a long piece of text into smaller chunks using the BART model from Facebook AI.

    Args:
        full_text (str): The full text to be summarized.

    Returns:
        str: A summarized version of the input text.
    """
    log.debug(f'convert {full_text}')
    chunks = sent_tokenize(full_text)
    summary = []
    chunk_length = 25
    chunk_idx_start = 0
    while chunk_idx_start < len(chunks):
        if chunk_length == 0:
            chunk_length = 25
            chunk_idx_start += 1
            continue
        sentence = ' '.join(chunks[chunk_idx_start:chunk_idx_start+chunk_length])
        if len(full_text) > 0 :
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            max_length_percentage = int(0.1*len(sentence))
            max_length_fix = 200
            max_length = max_length_fix if max_length_percentage > max_length_fix  else max_length_percentage
            min_length_percentage = int(0.05*len(sentence))
            min_length_fix = 100
            min_length = min_length_fix if min_length_percentage > min_length_fix  else min_length_percentage
            try:
                summary.append(summarizer(sentence, max_length = max_length , min_length=min_length, do_sample=False)[0]['summary_text'])
                chunk_idx_start += chunk_length
                chunk_length = 25
            except IndexError:
                chunk_length = int(chunk_length/2)
    return ' '.join(summary)

def summarize_text(full_text:str, summarizer_mode:Summarizer_Mode=Summarizer_Mode.CONSERVATIVE) -> str :
    if summarizer_mode == Summarizer_Mode.FAST :
        return summarize_text_fast(full_text)
    elif summarizer_mode == Summarizer_Mode.CONSERVATIVE :
        return summarize_text_conservative(full_text)
    else :
        raise Exception('Invalid summarizer mode.')

def summarize_articles(articles_id, articles_summary, callback_endpoint:str):
    if (len(articles_id) != len(articles_summary)) :
        raise Exception('articles_id and articles_summary must have the same length.')
    for i in range(0, len(articles_summary)) :
        summary = summarize_text(articles_summary[i])
        callback_endpoint = callback_endpoint.replace('localhost', '127.0.0.1')
        log.info(callback_endpoint)
        requests.post(callback_endpoint, json={'id': articles_id[i], 'summary': summary})
        log.info(f'Article {articles_id[i]} summarized.')

