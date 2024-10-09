import random as rd
import numpy as np
import getpass
import time


 
import random as rd
import numpy as np

def is_punctuation(input):
    if input in ",.?;:\()!'" or input == '"':
        return 1
    return 0

def decapitalize(word):
  return ''.join([word[:1].lower(), word[1:]])

def capitalize(word):
  return ''.join([word[:1].upper(), word[1:]])

def split_input(filepath):
    file = open(filepath, "r")
    training_text = file.read()
    training_set = training_text.split()
    new_set = []
    for word in training_set:
        if word[0].isupper():
            word = decapitalize(word)
        if is_punctuation(word[0]) and len(word) > 1:
            new_set.append(word[0])
            word = word[1 :]
        if is_punctuation(word[-1]):
            new_set.append(word[0 : -1])
            new_set.append(word[-1]) # a se comenta pt generare fara semne de punctuatie
        else:
            new_set.append(word)
    file.close()
    return new_set

def unique(words):
    result = []
    for word in words:
        if word not in result:
            result.append(word)
    result.sort()
    return result

def create_seq(words, k=3):
    seqs = []
    for i in range(len(words) + 1 - k):
        seq = words[i]
        for j in range(1, k):
            if is_punctuation(words[i + j]):
                seq = seq + words[i + j]
            else:
                seq = seq + ' ' + words[i + j]
        seqs.append(seq)
    return seqs

def create_dict(items):
    result = {}
    count = 0
    for itm in items:
        result[itm] = count
        count = count + 1
    return result

def stochastic(seq_unq, word_unq, seqs, words, k = 3):
    result = np.zeros((len(seq_unq), len(word_unq)), dtype=float)
    seq_dict = create_dict(seq_unq)
    word_dict = create_dict(word_unq)
    for i in range(len(seqs) - 1):
        seq = seqs[i]
        word = words[i + k]
        result[seq_dict[seq], word_dict[word]] += 1
    return result

def sample_next_word(text_file, word_dict, seq_dict, stoch, k=3):
    text_words = split_input(text_file)
    result = []

    if len(text_words) < k:
        raise TypeError
    else:
        final_seq = create_seq(text_words[len(text_words) - k : len(text_words)], k)
        if final_seq != "END~"and final_seq[0] not in seq_dict.keys():
            raise KeyError("S-a ajuns la o secventa care nu exista.")
        else:
            if final_seq == "END~":
                raise ValueError
            else:
                return stoch[seq_dict[final_seq[0]]]
        

def sample_n_words(text_file, word_dict, seq_dict, stoch, words_unq, n, k):
    for i in range(n):
        with open(text_file, 'r') as file:
            for line in file:
                pass
            last_line = line
        new_line = 0
        if len(last_line) > 100:
            new_line = 1
            with open(text_file, 'a') as file:
                file.write("\n")
        words = split_input(text_file)
        if words[len(words) - 1] == "END~":
            break
        try:
            probs = sample_next_word(text_file, word_dict, seq_dict, stoch, k)
        except TypeError:
            print("\nTextul de input este prea scurt. Accuracy-ul trebuie sa fie mai mic sau egal cu lungimea șirului.")
            return 0
        except KeyError:
            print("S-a ajuns la o secvență inexistentă în setul de antrenament (imens ghinion)")
            error_input = input("Reîncercăm cu o secvență aleatorie? Y/N ")
            if error_input == 'N':
                with open(text_file, 'a') as file:
                    file.write('\n\t\t~THE END~\n')
                return 0
            else:
                if error_input == 'Y':
                    word = '.'
                    while is_punctuation(word):
                        random_idx = int(rd.uniform(0, len(words) - 1))
                        word = words[random_idx]
                    with open(text_file, 'a') as file:
                        if new_line:
                            new_line = 0
                            file.write(word)
                        else:
                            file.write(' ' + word)
        except ValueError:
            return 0
        else:
            if array_sum(probs) == 0:
                print("S-a ajuns la o ultima secvență din setul de antrenament, iar aceasta este unică (imens ghinion)")
                error_input = input("Reîncercăm cu o secvență aleatorie? Y/N ")
                if error_input == 'N':
                    with open(text_file, 'a') as file:
                        file.write('.\n\t\t~THE END~\n')
                    return 0
                else:
                    if error_input == 'Y':
                        word = '.'
                        while is_punctuation(word):
                            random_idx = int(rd.uniform(0, len(words) - 1))
                            word = words[random_idx]
                        with open(text_file, 'a') as file:
                            file.write(' >>> ' + word)
            else:
                if array_sum(probs) > 1:
                    probs = probs * (1 / array_sum(probs))
                corpus = split_input(text_file)
                last_word = corpus[-1]
                chosen = np.random.choice(range(len(probs)), 1, p=probs)
                word = words_unq[chosen[0]]

                if last_word in ".!?":
                    word = capitalize(word)
                with open(text_file, 'a') as file:
                    if is_punctuation(word):
                        file.write(word)
                    else:
                        if new_line:
                            new_line = 0
                            file.write(word)
                        else:
                            file.write(' ' + word)
            
def array_sum(array):
    sum = 0.0
    for i in array:
        sum += i
    return sum

print("-------------------------------------\n")
print(" Welcome to our C.L.I. TextGenerator\n")
print(" version : 1.0\n")

ok = 0
while ok == 0:
    print("--------------------------------------\n\n") 
    print("Main Menu\n\nOptions:\n1 -> Start\n2 -> Quit")
    option = getpass.getpass('')
    if option != '1' and option != '2':
        while option != '1' and option != '2':
            print("The option introduced does not exist\nRestarting", end = '')
            for _ in range(4):  # va printa 4 puncte
                print('.', end = '', flush = True)
                time.sleep(1)
            print('\n\n\n')
            print("--------------------------------------\n") 
            print("Main Menu\n\nOptions:\n1 -> Start\n2 -> Quit")
            option = getpass.getpass('')
    if option == '2':
        ok = 1
        print("Shutting down")
        for _ in range(5):  # va printa 4 puncte
                print('.', end = '', flush = True)
                time.sleep(1)
        print('\n')
    if option == '1':
        print("--------------------------------------------------------------------")
        print("Let's start with choosing the language in which I will operate:")
        language = str(input("1. ENGLISH\n2. ROMANIAN\nYour choice : "))
        print("Loading..............................................................\n")
        if language == '1' or language == "ENGLISH":
            
            print("We have 3 training sets\n\n!! Disclaimer:Every training set determines a different result!!\n!!            because of its dimensions/complexity            !!\n\nOptions :\n", end = '')
            print("Option 1 .................................... Training Set 1 (small size, strong coherence)(type 'S')")
            print("Option 2 .................................... Training Set 2 (medium size, medium coherence)(type 'M')")
            print("Option 3 .................................... Training Set 3 (large size, low coherence)(type 'L')\n")
            
            Option10 = str(input("Enter your option -> "))
            if Option10 == 'L':
                with open ('tests/output/outputS.txt', 'w') as file:  
                    file.write('rivers of your blood')
                filepath = "tests/training_input/english/large_20k_tinyshakespeare.txt"
                output = "tests/output/outputS.txt"
                n = int(input("Enter the number of words you want to generate: "))
                seq_num = int(input("Enter a number from 1 to 4 for accuracy (higher is better): "))
                words = split_input(filepath)
                seqs = create_seq(words, seq_num)
                
                print("Working", end = '')
                for _ in range(3):
                        print('.', end = '', flush = True)
                        time.sleep(0.5)
                seq_dict = create_dict(unique(seqs))
                word_dict = create_dict(unique(words))
                stoch = stochastic(unique(seqs), unique(words), seqs, words, seq_num)
                for _ in range(3):
                        print('.', end = '', flush = True)
                        time.sleep(0.5)
                sample_n_words(output, word_dict, seq_dict, stoch, unique(words), n, seq_num)
                print("\n\nDone! Check outputS.txt")

                INPUT = str(input("Return to main menu ?  Y/N\n-> "))
                if INPUT == "Y":
                    ok = 0
                else:
                    ok = 1
                print()
                
                sample_n_words(output, word_dict, seq_dict, stoch, unique(words), n, seq_num)
            elif Option10 == 'M':
                with open ('tests/output/outputS.txt', 'w') as file:  
                    file.write('STORY OF THE')
                filepath = "tests/training_input/english/medium_2k_jekyll_and_hyde.txt"
                output = "tests/output/outputS.txt"
                n = int(input("Enter the number of words you want to generate: "))
                seq_num = int(input("Enter a number from 1 to 3 for accuracy (higher is better): "))
                words = split_input(filepath)
                seqs = create_seq(words, seq_num)
                
                print("Working", end = '')
                for _ in range(3):
                        print('.', end = '', flush = True)
                        time.sleep(0.5)
                seq_dict = create_dict(unique(seqs))
                word_dict = create_dict(unique(words))
                stoch = stochastic(unique(seqs), unique(words), seqs, words, seq_num)
                for _ in range(3):
                        print('.', end = '', flush = True)
                        time.sleep(0.5)
                sample_n_words(output, word_dict, seq_dict, stoch, unique(words), n, seq_num)
                print("\n\nDone! Check outputS.txt")

                INPUT = str(input("Return to main menu ?  Y/N\n-> "))
                if INPUT == "Y":
                    ok = 0
                else:
                    ok = 1
                print("\n")

                sample_n_words(output, word_dict, seq_dict, stoch, unique(words), n, seq_num)
            elif Option10 == 'S':
                with open ('tests/output/outputS.txt', 'w') as file:  
                    file.write('Once upon a')
                filepath = "tests/training_input/english/small_100_poe.txt"
                output = "tests/output/outputS.txt"
                n = int(input("Enter the number of words you want to generate: "))
                seq_num = int(input("Enter a number from 1 to 3 for accuracy (higher is better): "))
                words = split_input(filepath)
                seqs = create_seq(words, seq_num)
                
                print("Working", end = '')
                for _ in range(3):
                        print('.', end = '', flush = True)
                        time.sleep(0.5)
                seq_dict = create_dict(unique(seqs))
                word_dict = create_dict(unique(words))
                stoch = stochastic(unique(seqs), unique(words), seqs, words, seq_num)
                for _ in range(3):
                        print('.', end = '', flush = True)
                        time.sleep(0.5)
                sample_n_words(output, word_dict, seq_dict, stoch, unique(words), n, seq_num)
                print("\n\nDone! Check outputS.txt")

                INPUT = str(input("Return to main menu ?  Y/N\n-> "))
                if INPUT == "Y":
                    ok = 0
                else:
                    ok = 1
                print("\n")
            else:
                print("Option does not exist !!!\nShutting down", end = '')
                for _ in range(3):
                        print('.', end = '', flush = True)
                        time.sleep(1)
                print('\n')
                ok = 1
        elif language == '2' or language == "ROMANIAN":
            print("You chose ROMANIAN\n\nROMANIAN generator is still in beta, so be patient and don't expect the best results\n\n")
            print("!!---------------------------------------------------------------------------!!\n")
            print("Info : Romanian mode basically generates stories for kids containing parts from\nother well-known stories\n")
            print("!!---------------------------------------------------------------------------!!\n")
            n = int(input("Enter the number of words you want to generate: "))
            seq_num = int(input("Enter a number from 1 to 5 for accuracy (higher is better): "))
            with open ('tests/output/outputS.txt', 'w') as file:  
                    file.write('A fost odată')
            filepath = "tests/training_input/romanian/romanian_data.txt"
            output = "tests/output/outputS.txt"
            if seq_num > 3:
                print("DISCLAIMER: for the chosen accuracy, %d extra words will be generated at the beginning with accuracy 3.\n" % (seq_num - 3))
                words_aux = split_input(filepath)
                seqs_aux = create_seq(words_aux, 3)
                seq_dict_aux = create_dict(unique(seqs_aux))
                word_dict_aux = create_dict(unique(words_aux))
                stoch_aux = stochastic(unique(seqs_aux), unique(words_aux), seqs_aux, words_aux, 3)
                sample_n_words(output, word_dict_aux, seq_dict_aux, stoch_aux, unique(words_aux), seq_num - 3, 3)

            words = split_input(filepath)
            seqs = create_seq(words, seq_num)
            print("Working", end = '')
            for _ in range(3):
                    print('.', end = '', flush = True)
                    time.sleep(0.5)
            seq_dict = create_dict(unique(seqs))
            word_dict = create_dict(unique(words))
            stoch = stochastic(unique(seqs), unique(words), seqs, words, seq_num)
            for _ in range(3):
                    print('.', end = '', flush = True)
                    time.sleep(0.5)
            sample_n_words(output, word_dict, seq_dict, stoch, unique(words), n, seq_num)
            print("\n\nDone! Check outputS.txt")

            INPUT = str(input("Return to main menu ?  Y/N\n-> "))
            if INPUT == "Y":
                ok = 0
            else:
                ok = 1
            print("\n")