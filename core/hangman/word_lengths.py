#!/usr/local/bin/python3

f = open("noplurals.txt", 'r')
words = f.read().strip()
f.close()
word_list = [w.strip() for w in words.split('\n')]
words_checked = 0
num_words = len(word_list)
'''
max_word = ""
max_length = 0
min_word = ""
min_length = 0xefffffff
'''

wl_dict = {}
for word in word_list:
    if len(word) not in wl_dict.keys():
        wl_dict[len(word)] = 0
    wl_dict[len(word)] += 1
    words_checked += 1
    percentage = (words_checked / num_words) * 100
    print("{:.4f}%".format(percentage), end='\r')

print()
for length in sorted(wl_dict.keys()):
    print(length, wl_dict[length])
