#!/usr/local/bin/python3

def main():
    #inefficient but fun to watch!
    f = open("words.txt", 'r')
    words = f.read().strip()
    f.close()
    word_list = [w.strip() for w in words.split('\n')]
    ret = []
    words_checked = 0
    num_words = len(word_list)
    last_plural = ""
    for word in word_list:
        is_plural = False
        for other_word in word_list:
            if other_word + "s" == word:
                last_plural = word
                is_plural = True
        words_checked += 1
        percentage = (words_checked / num_words) * 100
        if not is_plural:
            print("{:.4f}% last plural found: {}".format(percentage, last_plural), end='\r')
            ret.append(word)
        else:
            print("{:.4f}% last plural found: {}".format(percentage, last_plural), end='\n')

    wr = open("noplurals.txt", 'w')
    wr.write('\n'.join(ret))
    wr.close()


if __name__ == '__main__':
    main()
