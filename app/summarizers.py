from app import app
import gensim
import numpy
import math

from numpy.linalg import svd as singular_value_decomposition
from gensim.summarization import summarize
from gensim import corpora, models, similarities
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict

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

def page_rank_summary(text, limit=1):

  [dictionary, proc_text, sentences] = save_word_dict(text)
  raw_corpus = [dictionary.doc2bow(t) for t in proc_text]

  if(len(raw_corpus) <= 1):
    return -1

  tfidf        = models.TfidfModel(raw_corpus)
  corpus_tfidf = tfidf[raw_corpus]
  simMat       = similarities.MatrixSimilarity(tfidf[raw_corpus])
  similarityMatrix = simMat[corpus_tfidf]
  
  converged = False
  
  W = {}
  for i, s1 in enumerate(simMat):
    for j, s2 in enumerate(s1):
      W[(i, j)] = s2

  ranks = [1.0]*len(proc_text)
  temp_ranks = [1.0]*len(proc_text)
  damping_factor = 0.5
  num_sent = len(proc_text)

  while(not converged):
    for i in range(0, num_sent):
      total_sum  = 0.0
      for j in range(0, num_sent):
        if(j == i):
          continue
        
        if(j < i):
          W[(j, i)] = similarityMatrix[j][i]
        else:
          W[(j, i)] = similarityMatrix[i][j]
        
        den_sum = 0.0
        for k in range(0, num_sent):
          if(k == j):
            continue
          if(j < k):
            W[(j, k)] = similarityMatrix[j][k]
          else:
            W[(j, k)] = similarityMatrix[k][j]
          den_sum = den_sum + W[(j, k)]
        # end k loop
        
        if(den_sum != 0.0):
          total_sum = total_sum + (W[(j, i)] * ranks[j] / den_sum)
      # end j loop
      rank = (1 - damping_factor) + (damping_factor * total_sum)
      temp_ranks[i] = rank
    # end i loop

    if(temp_ranks == ranks):
      converged = True  
    else:
      ranks = temp_ranks

  ranked_sentences = sorted(range(len(ranks)),key=lambda x:ranks[x], reverse=True)
  
  result_summary = ''
  for i in range(0, limit):
    result_summary = result_summary + ' ' + sentences[ranked_sentences[i]]

  return result_summary

def lsa_summary(text, limit=1):
  
  [dictionary, proc_text, sentences] = save_word_dict(text)
  
  tf_matrix = create_tf_matrix(proc_text, dictionary)
  tf_matrix = normalize_tf_matrix(tf_matrix, 0.3)

  # decompose in U x S X V matrices using SVD
  [u, s, v] = singular_value_decomposition(tf_matrix, full_matrices=False)

  reduction_ratio = 1.0
  dimension = len(s)
  reduced_dimension = int(dimension * reduction_ratio)

  min_dimension = 5

  if(reduced_dimension < min_dimension):
    reduced_dimension = min_dimension

  s2 = numpy.array(s, copy=True)
  s2 = numpy.square(s2).tolist()

  for i in range(reduced_dimension, dimension):
    s2[i,:] *= 0.0

  # http://textmining.zcu.cz/publications/PhDThesis-Steinberger.pdf
  # see page 25 - Sk = sqrt(sum(v * sigma^2 ))
  ranks = numpy.sqrt(numpy.square(v.T*s2).sum(axis=1))
  ranked_sentences = sorted(range(len(ranks)),key=lambda x:ranks[x], reverse=True)
  
  result_summary = ''
  for i in range(0, limit):
    result_summary = result_summary + ' ' + sentences[ranked_sentences[i]]

  return result_summary

def compute_tf_idf(dictionary, proc_text):
  
  words_count = len(dictionary)
  sentences_count = len(proc_text)
  
  raw_corpus = [dictionary.doc2bow(t) for t in proc_text]
  tf_matrix = numpy.zeros((words_count, sentences_count), dtype=numpy.float)

  for sentence_id, word_counts in enumerate(raw_corpus):
    for (word_id, count) in word_counts:
      tf_matrix[word_id, sentence_id] = count

  idf_values = {}
  for (word_id, word) in dictionary.iteritems():
    word_count = 0
    for sentence in proc_text:
      if word in sentence:
        word_count = word_count + 1

    if(word_count == 0):
      term_ratio = 0
    else:
      term_ratio = float(sentences_count)/float(word_count)
    
    idf_values[word_id] = math.log(1 + term_ratio)

  return [tf_matrix, idf_values]

def lex_summary(text, limit=1):
  
  [dictionary, proc_text, sentences] = save_word_dict(text)
  [tf_matrix, idf_values] = compute_tf_idf(dictionary, proc_text)

  sentence_matrix = compute_sentence_similarity_matrix(dictionary, proc_text, tf_matrix, idf_values)
  
  scores = power(sentence_matrix, 0.25)
  
  ranked_sentences = sorted(range(len(scores)),key=lambda x:scores[x], reverse=True)
  
  result_summary = ''
  for i in range(0, limit):
    result_summary = result_summary + ' ' + sentences[ranked_sentences[i]]

  return result_summary

def power(m, e):
  mT = m.T
  num_sentences = len(m)
  pVc = numpy.array(num_sentences*[1.0/num_sentences])
  l = 1.0
  while l > e:
      pNex = numpy.dot(mT, pVc)
      l = numpy.linalg.norm(numpy.subtract(pNex, pVc))
      pVc = pNex
  return pVc

def compute_sentence_similarity_matrix(dictionary, proc_text, tf_matrix, idf_values, threshold=0.001):

  sentence_length = len(proc_text)
  sentence_matrix = numpy.zeros((sentence_length, sentence_length), dtype=numpy.float)
  degree_matrix   = numpy.zeros((sentence_length, ), dtype=numpy.float)

  raw_corpus = [dictionary.doc2bow(t) for t in proc_text]

  for s_1, sentence1 in enumerate(raw_corpus):
    s1 = [i[0] for i in sentence1]

    for s_2, sentence2 in enumerate(raw_corpus):
      
      if(s_1 == s_2):
        continue

      s2 = [i[0] for i in sentence2]
      
      common_words = intersect(s1, s2)

      if(len(common_words) == 0):
        continue

      sentence_matrix[s_1, s_2] = idf_modified_cosine(common_words, s_1, s_2, s1, s2, tf_matrix, idf_values)

      if(sentence_matrix[s_1, s_2] > threshold):
        degree_matrix[s_1] = degree_matrix[s_1] + 1.0
      else:
        sentence_matrix[s_1, s_2] = 0.0

  return sentence_matrix

def idf_modified_cosine(common_words, s_1, s_2, s1, s2, tf_matrix, idf_values):
  # print common_words
  sentence_score = 0.0
  for word_id in common_words:
    sentence_score = sentence_score + (tf_matrix[word_id, s_1] * tf_matrix[word_id, s_2] * pow(idf_values[word_id], 2) )

  sentence1_sum = 0.0
  for word_id in s1:
    sentence1_sum = sentence1_sum  + pow((tf_matrix[word_id, s_1] * idf_values[word_id] ), 2)

  sentence2_sum = 0.0
  for word_id in s2:
    sentence2_sum = sentence2_sum  + pow((tf_matrix[word_id, s_2] * idf_values[word_id] ), 2)

  if(sentence1_sum == 0.0 or sentence2_sum == 0.0):
    return 0.0
  else:
    return sentence_score/(sentence2_sum * sentence1_sum)

def intersect(a, b):
  return list(set(a) & set(b))

def gensim_summarize(text):
  return gensim.summarization.summarize(text, word_count=50)
