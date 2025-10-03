def reverse_words(sentence):
    words = sentence.split()          
    reversed_words = words[::-1]    
    return " ".join(reversed_words)   


s = input("Введите предложение: ")
print("Результат:", reverse_words(s))
