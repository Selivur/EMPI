import pymorphy2
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import re
from os import system, name
from array import array

morphUA = pymorphy2.MorphAnalyzer(lang='uk')

stopWordsArr = [
    "авжеж",
    "адже",
    "але",
    "б",
    "без",
    "був",
    "була",
    "були",
    "було",
    "бути",
    "більш",
    "вам",
    "вас",
    "весь",
    "вздовж",
    "ви",
    "вниз",
    "внизу",
    "вона",
    "вони",
    "воно",
    "все",
    "всередині",
    "всіх",
    "від",
    "він",
    "да",
    "давай",
    "давати",
    "де",
    "дещо",
    "для",
    "до",
    "з",
    "завжди",
    "замість",
    "й",
    "коли",
    "ледве",
    "майже",
    "ми",
    "навколо",
    "навіть",
    "нам",
    "от",
    "отже",
    "отож",
    "поза",
    "про",
    "під",
    "та",
    "так",
    "такий",
    "також",
    "те",
    "ти",
    "тобто",
    "тож",
    "тощо",
    "хоча",
    "це",
    "цей",
    "чи",
    "чого",
    "що",
    "як",
    "який",
    "якої",
    "є",
    "із",
    "інших",
    "їх",
    "її",
    "a",
    "а",
    "a",
    "треба",
    "я",
    "якщо",
    "або",
    "краще",
    "в",
    "тільки",
    "не",
    "і",
    "між",
    "за",
    "на",
    "x",
    "xy",
    "y",
    "yx",
    "not",
    "or",
    "and",
]

tokenizeArr = [
    ".",
    ",",
    "?",
    "!",
    ";",
    ":",
    ")",
    "(",
    "=",
    "+",
    "-",
    "<",
    ">",
    "[",
    "]",
    "{",
    "}",
    "x",
    "y",
]

useless_words = [
    "розглядатися ",
    "самообслуговування ",
    "завершити ",
    "застосування ",
    "вивчити ",
    "матеріал ",
    "лекція ",
    "реалізація ",
    "основний ",
    "тога ",
    "який ",
    "знайти ",
    "проект ",
    "існуючий ",
    "існувати ",
    "вид ",
    "година ",
    "відповідний ",
    "відповідно ",
    "елемент ",
    "найбільш ",
    "обслуговування ",
    "решення "
    ]
m=[]
data_list = []
data_exec = []
final_arr = array('b')



def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def removeTokenized(inputString):
    for i in tokenizeArr:
        inputString = inputString.translate({ord(i): None})
    return inputString


def executeTF():
    count = CountVectorizer()
    bag = count.fit_transform(data_exec)
    print(count.get_feature_names())
    print(bag.toarray())
    arr=bag.toarray()
    length, size=bag.get_shape()
    j=0;
    while j<size:
        i=0
        count_of_words =0;
        while i<length:
            count_of_words+=arr[i][j]
            i=i+1
        j=j+1
        final_arr.append(count_of_words)
    j=0
    while j<5:
        global m
        mx = max(final_arr)
        m = [i for i,j in enumerate(final_arr) if j==mx]
        print(m)
        i=0
        while i<len(m):
            print(count.get_feature_names()[m[i]])
            final_arr[m[i]]=-1;
            i=i+1
        j=j+1
    file1 = open("Tf.txt", "w")
    for i in range(0, len(arr)):
        file1.write(str(arr[i]))
    file1.close()


def executeTFIDF():
    count = TfidfVectorizer()
    bag = count.fit_transform(data_exec)
    i=0
    while i < len(m):
        print(count.get_feature_names()[m[i]])
        i=i+1
    print(bag.toarray())
    file1 = open("Tfidf.txt", "w")
    for i in range(0, len(bag.toarray())):
        file1.write(str(bag.toarray()[i]))
    file1.close()


def main():
    while True:
        print("--------------------------")
        print("Список команд:")
        print("1.Запуск аналізу")
        print("2.Розрахунок матриці ТФ")
        print("3.Розрахунок матриці ТФІДФ")
        print("--------------------------")
        cmd = input("Введіть команду: ")
        if cmd == "1":
            inpStr()
        elif cmd == "2":
            executeTF()
        elif cmd == "3":
            executeTFIDF()
        else:
            print("Помилка. Перевірте правильність вводу команди.")
    return 0


def inpStr(n=""):
    num_of_proj=int(input("Введіть кількість проектів для аналізу:"))
    print("Завантаженння даних...")
    i=1
    while i<=num_of_proj:
        name_of_file=str(i)+".txt"
        with open(name_of_file, 'rb') as f: 
            data_list.append(f.read().decode('utf-8').replace('\n', ' '))
        data_exec.append("")
        i=i+1
    print("Дані занесено успішно")
    print("Початок обробки")
    for i in range(0, len(data_list)):
        # Tokenize
        data_exec[i] = removeTokenized(data_list[i]).lower()
        # Delete Stop-words
        tmpDataArr = data_exec[i].split(" ")
        tmpFiltered = [word for word in tmpDataArr if word not in stopWordsArr]
        data_exec[i] = ""
        # Stemming
        for j in tmpFiltered:
            tmp = morphUA.parse(j)[0].normal_form
            if not hasNumbers(tmp) and tmp != '':
                data_exec[i] += tmp.strip() + " "
        # Delete useless words
        for word in useless_words:
            data_exec[i] = data_exec[i].replace(word, "")
    i=0
    while i < len(data_exec):
        print("Data: " + str(i + 1) + "\n" + data_exec[i] + "\n")
        i=i+1


main()
 
