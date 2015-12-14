from app import app
import gensim
import numpy

from gensim.summarization import summarize
from gensim import corpora, models, similarities
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict

global reference_summary_list
global system_summary_list

def save_word_dict(text):
  proc_text = []
  
  sentences = text 
  sentences = sent_tokenize(sentences)
  
  for sentence in sentences:
    proc_sentence = word_tokenize(sentence.lower())

    if(len(proc_sentence) == 0):
      continue
    proc_text.append(proc_sentence)

  dictionary = corpora.Dictionary(proc_text)
  return [dictionary, proc_text, sentences]

def create_tf_matrix(proc_text, dictionary):

  words_count = len(dictionary)
  sentences_count = len(proc_text)
  
  raw_corpus = [dictionary.doc2bow(t) for t in proc_text]
  matrix = numpy.zeros((words_count, sentences_count), dtype=numpy.float)

  for sentence_id, word_counts in enumerate(raw_corpus):
    for (word_id, count) in word_counts:
      matrix[word_id, sentence_id] = count

  return matrix

def normalize_tf_matrix(matrix, alpha=0.7):
  rows = len(matrix)
  cols = len(matrix[0])

  max_freq = numpy.max(matrix, axis=0)
    
  for i in range(0, rows):
    for j in range(0, cols):
      max_f = max_freq[j]
      if max_f == 0:
        continue

      # dividing by max term freq so as to not penalize long sentences
      term_freq = matrix[i, j] / max_f
      matrix[i, j] = alpha + (1.0 - alpha) * term_freq

  return matrix

def baseline_summary(text, limit=1):
  [dictionary, proc_text, sentences] = save_word_dict(text)
  
  tf_matrix = create_tf_matrix(proc_text, dictionary)
  tf_matrix = normalize_tf_matrix(tf_matrix, 0.2)

  scores = []

  for sent_id in range(0, len(proc_text)):
    scores.append(tf_matrix[:,sent_id].sum())

  ranked_sentences = sorted(range(len(scores)),key=lambda x:scores[x], reverse=True)

  result_summary = ''
  for i in range(0, limit):
    result_summary = result_summary + ' ' + sentences[ranked_sentences[i]]

  return result_summary

def gensim_summarize(text):
  return gensim.summarization.summarize(text, word_count=50)

def test():
  return "hello world"