import codecs
import os

def normalizing_text():
    with codecs.open("data.txt", "r", "utf-8") as myfile:
        line = myfile.readlines()
        for i in range(len(line)):
            data = line[i].split("|")
            ans = str(i) + " ; "
            for item in data:
                items = item.split(": ")
                print(items[0])
                ans = ans + items[1] + " ; "
            ans = ans[:-2]
            ans = ans + "\n"
            cwd = os.getcwd()
            cwd = cwd + "/tocsv.txt"
            if (os.path.isfile(cwd)):
                with codecs.open("tocsv.txt", "a", "utf-8") as myfile:
                    myfile.write(str(ans))
            else:
                with codecs.open("tocsv.txt", "w", "utf-8") as myfile:
                    myfile.write(str(ans))



def main():
    normalizing_text()

main()
