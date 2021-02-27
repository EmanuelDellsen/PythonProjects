
#file = open("transcription.txt", "r")
second_file = open("with_new_line.txt", "w")
trans = ["hello", "hello.", "Hello", ".", "Hellooo."]

#for line in trans:
for word in trans:
    second_file.write(word)
    #print(word, '\n')
    if "." in word:
        second_file.write("\n")

#print(file)
print(second_file)

#file.close()
second_file.close()