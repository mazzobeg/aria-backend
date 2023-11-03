"""
This module contains the Summarizer_Mode class and functions for summarizing text.
"""
# pylint: disable=R0903
import logging as log
import requests
from sqlalchemy import or_
from nltk.tokenize import sent_tokenize
from transformers import pipeline
from flask import current_app
from aria.articles.models import Article

class SummarizerMode:
    """
    Enum for Summarizer Modes
    """

    FAST = "fast"
    CONSERVATIVE = "conservative"


def summarize_text_fast(full_text: str) -> str:
    """
    Summarizes a long piece of text into smaller chunks using the BART model from Facebook AI.

    Args:
        full_text (str): The full text to be summarized.

    Returns:
        str: A summarized version of the input text.
    """
    log.debug("Summarize %s", full_text)
    chunks = sent_tokenize(full_text)
    summary = []
    chunk_length = 25
    for i in range(0, len(chunks), chunk_length):
        sentence = " ".join(chunks[i : i + chunk_length])
        if sentence:
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            max_length = min(int(0.1 * len(sentence)), 200)
            min_length = min(int(0.05 * len(sentence)), 100)
            try:
                summary.append(
                    summarizer(
                        sentence,
                        max_length=max_length,
                        min_length=min_length,
                        do_sample=False,
                    )[0]["summary_text"]
                )
            except IndexError:
                pass
    return " ".join(summary)


def summarize_text_conservative(full_text: str) -> str:
    """
    Summarizes a long piece of text into smaller chunks using the BART model from Facebook AI.

    Args:
        full_text (str): The full text to be summarized.

    Returns:
        str: A summarized version of the input text.
    """
    log.debug("convert %s", full_text)
    chunks = sent_tokenize(full_text)
    summary = []
    chunk_length = 25
    chunk_idx_start = 0
    while chunk_idx_start < len(chunks):
        if chunk_length == 0:
            chunk_length = 25
            chunk_idx_start += 1
            continue
        sentence = " ".join(chunks[chunk_idx_start : chunk_idx_start + chunk_length])
        if sentence:
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            max_length = min(int(0.1 * len(sentence)), 200)
            min_length = min(int(0.05 * len(sentence)), 100)
            try:
                summary.append(
                    summarizer(
                        sentence,
                        max_length=max_length,
                        min_length=min_length,
                        do_sample=False,
                    )[0]["summary_text"]
                )
                chunk_idx_start += chunk_length
                chunk_length = 25
            except IndexError:
                chunk_length = int(chunk_length / 2)
    return " ".join(summary)


def summarize_text(
    full_text: str, summarizer_mode: SummarizerMode = SummarizerMode.CONSERVATIVE
) -> str:
    """
    Summarizes a long piece of text based on the given summarizer mode.

    Args:
        full_text (str): The full text to be summarized.
        summarizer_mode (SummarizerMode): The summarizer mode to be used.

    Returns:
        str: A summarized version of the input text.
    """
    if summarizer_mode == SummarizerMode.FAST:
        return summarize_text_fast(full_text)
    if summarizer_mode == SummarizerMode.CONSERVATIVE:
        return summarize_text_conservative(full_text)
    raise ValueError("Invalid summarizer mode.")


def summarize_articles(articles_id, articles_summary, callback_endpoint: str):
    """
    Summarizes a list of articles and sends the summaries to a callback endpoint.

    Args:
        articles_id (list): The IDs of the articles to be summarized.
        articles_summary (list): The summaries of the articles to be summarized.
        callback_endpoint (str): The callback endpoint to send the summaries to.
    """
    if len(articles_id) != len(articles_summary):
        raise ValueError("articles_id and articles_summary must have the same length.")
    for i, summary in enumerate(articles_summary):
        summary_text = summarize_text(summary)
        callback_endpoint = callback_endpoint.replace("localhost", "127.0.0.1")
        log.info(callback_endpoint)
        requests.post(
            callback_endpoint,
            json={"id": articles_id[i], "summary": summary_text},
            timeout=10,
        )
        log.info("Article %s summarized.", articles_id[i])

def get_articles_without_summary():
    """
    Returns all articles without a summary.
    """
    with current_app.app_context():
        return Article.query.filter(or_(Article.summary.is_(None))).all()
