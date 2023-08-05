from gensim.models.word2vec import LineSentence

lines, model_out, vector_out = "sources/splited_words.txt", "result/word2vec.model", "result/pre_word2vec.vector"
sentences = LineSentence(lines)