import re

inp = "When did William Wordsworth die? 23rd April 1850. When did William Wordsworth die? 23rd April 1850."

n_questions = inp.count('?')
n_standards = inp.count('.')
n_exclamaitions = inp.count('!')
n_sentence = n_questions + n_standards + n_exclamaitions

print(n_questions, n_standards, n_exclamaitions)
print(n_sentence)