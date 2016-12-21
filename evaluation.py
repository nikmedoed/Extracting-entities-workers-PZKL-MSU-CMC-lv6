import os
import subprocess
import pymorphy2
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import re
import multiprocessing.dummy as multiprocessing


def runtest (test):
    devSetPatterns = os.getcwd() + '\\factRuEval-2016\\' + test + 'set'
    mainTree = os.walk(devSetPatterns)
    for d in mainTree:
        for subf in d[2]:
            filePath = d[0] + "/" + subf
            if ".txt" in subf:
                docName = subf.split(".")[0]
                mpath = os.getcwd().replace("\\", "/") + '/ourtest/' + test + 'set/' + docName
                mconf = open('config.proto', "w", encoding="cp1251")
                data = 'encoding "cp1251";\n\nTTextMinerConfig {\n\tDictionary = "keywords.gzt";\n\n'
                data += '\tPrettyOutput = "' + mpath + '.html";\n\n'
                data += '\tInput = {\n\t\tFile = "' + filePath.replace("\\", "/") + '";\n\t\tEncoding = "UTF-8";\n\t}\n\n'
                data += '\tArticles = [{ Name = "работа"}]\n\tFacts = [{ Name = "Occupation" }]\n\n'
                data += '\tOutput = {\n\t\tFile = "' + mpath + '.facts";\n\t\tFormat = text;\n\t}\n\n'
                data += '\tPrintRules="' + mpath + '.rules";\n\n'
                data += '\tPrintTree="' + mpath + '.tree";\n\n'
                data += '}'
                mconf.write(data)
                mconf.close()
                # print(test + 'set/' + docName + ":")
                # tomitarun = subprocess.Popen('tomitaparser.exe config.proto', shell=True, stdout=subprocess.DEVNULL)
                subprocess.call('tomitaparser.exe config.proto', stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, shell=True)
                # print(tomitarun.stdout.readlines())
                # i = tomitarun.stdout.readlines()


def cleaneval(st):
    del(st[0])
    del(st[0])
    res = st
    # res = [x for x in st if not (('span' in x) or ('obj' in x))]
    # print(res)
    return ' '.join(res).split(" | ")


def read_RuFactEval(test):
    devSetPatterns = os.getcwd() + '\\factRuEval-2016\\' + test + 'set'
    factsPatterns = {}
    mainTree = os.walk(devSetPatterns)
    for d in mainTree:
        for subf in d[2]:
            filePath = d[0] + "/" + subf
            if ".facts" in subf:
                openFile = open(filePath,"r",encoding = "utf-8")
                docNum = None
                factNum = None
                newFact = True
                for line in openFile:
                    # print(line)
                    lineSplt = line.split() # очередную считанную линию разделить по словам
                    # print(lineSplt)
                    if "Occupation" in lineSplt:
                        newFact = True
                        docNum = subf.split(".")[0]
                        # print (docNum)
                        if not docNum in factsPatterns:
                            factsPatterns[docNum] = {}
                        factNum = lineSplt[0].split('-')[1]
                        # print(factNum)
                        factsPatterns[docNum][factNum] = {}
                        factsPatterns[docNum][factNum]["Hard"] = False
                    elif "Who" in lineSplt and newFact:
                        factsPatterns[docNum][factNum]["Who"] = cleaneval(lineSplt)
                    elif ("Position" in lineSplt) or ("Job" in lineSplt) and newFact:
                        factsPatterns[docNum][factNum]["Position"] = cleaneval(lineSplt)
                    elif "Where" in lineSplt and newFact:
                        factsPatterns[docNum][factNum]["Where"] = cleaneval(lineSplt)
                    elif "Сложность" in lineSplt and newFact:
                        factsPatterns[docNum][factNum]["Hard"] = True
                    else:
                        # print(factsPatterns[docNum][factNum])
                        newFact = False
                openFile.close()
    # print(factsPatterns)
    return factsPatterns


def cleanour (t):
    del t[0]
    del t[0]
    return ' '.join(t)


def read_OurFact (test):
    devSetPatterns = os.getcwd() + '\\ourtest\\' + test + 'set'
    factsPatterns = {}
    mainTree = os.walk(devSetPatterns)
    for d in mainTree:
        for subf in d[2]:
            filePath = d[0] + "/" + subf
            if ".facts" in subf:
                openFile = open(filePath,"r",encoding = "utf-8")
                docNum = None
                factNum = 0
                newFact = True
                for line in openFile:
                    # print(line)
                    lineSplt = line.split() # очередную считанную линию разделить по словам
                    # print(lineSplt)
                    if "Occupation" in lineSplt:
                        newFact = True
                        docNum = subf.split(".")[0]
                        # print (docNum)
                        if not docNum in factsPatterns:
                            factsPatterns[docNum] = {}
                        factNum += 1
                        # print(factNum)
                        factsPatterns[docNum][factNum] = {}
                    elif "Who" in lineSplt and newFact:
                        factsPatterns[docNum][factNum]["Who"] = cleanour(lineSplt)
                    elif "Position" in lineSplt and newFact:
                        factsPatterns[docNum][factNum]["Position"] = cleanour(lineSplt)
                    elif "Where" in lineSplt and newFact:
                        factsPatterns[docNum][factNum]["Where"] = cleanour(lineSplt)
                    elif not("{" in lineSplt):
                        newFact = False
                openFile.close()
    # print(factsPatterns)
    return factsPatterns


def normal(f):
    morph = pymorphy2.MorphAnalyzer()
    if isinstance(f,list) :
        result = list(map(lambda k: list(map(lambda x: morph.parse(x)[0].normal_form, k.split(' '))) ,f))
        # print (result)
    else:
        result = list(map(lambda x: morph.parse(x)[0].normal_form,f.split(' ')))
    return result

# def testPHw(ou, th):
#     def testPH():  # EQ or Левенштейна
#         result = False
#         # print (ou," ",th)
#         try:
#             if ou in th:
#                 result = True
#             else:
#                 our = normal(ou)
#                 test = normal(th)
#                 count = 0
#                 for o in our:
#                     for t in test:
#                         if o in t:
#                             count += 1
#                             break
#
#                 if count / len(our) > 0.75:
#                     result = True
#                     # print(our,test,result)
#         except Exception:
#             None
#         return result


def testPH(ou, th): # EQ or Левенштейна
    result = False
    # print (ou," ",th)
    try:
        if ou in th:
            result = True
        else:
            our = normal(ou)
            test = normal(th)
            count = 0
            for o in our:
                for t in test:
                    if o in t:
                        count += 1
                        break

            if count/len(our)>0.75:
                result = True
            # print(our,test,result)
    except Exception:
        None
    return result


def printerffors(err1,err2,err3,err4,overflow,errors):
    errors.write("1. В этом разделе перечислены факты найденые с недочётами\n")
    errors.write(err1)
    errors.write("\n\n2. В этом разделе перечислены факты, которые мы не нашли\n")
    errors.write(err2)
    errors.write("\n\n3. В этом разделе перечислены источники, которые ты нашёл, но эксперты нет\n")
    errors.write(err3)
    errors.write("\n\n4. В этом разделе перечислены источники, в которых ты ничего не нашел\n")
    errors.write(err4)
    if len(overflow) > 0:
        errors.write("\n\n5. В этом разделе перечислены источники, которые ты нашёл, но эксперты нет\n\n")
        for book in overflow.keys():
            errors.write("\n" + book + ":")
            ob = overflow.get(book)
            for k in ob.keys():
                errors.write("\n\t" + str(k) + ":")
                obk = ob.get(k)
                for n in obk.keys():
                    errors.write("\n\t\t" + str(n) + ": " + str(obk.get(n)))

    errors.close()


def analyse_results_exact(test, factsRuFactEval, factsPatterns):
    errors = open("OurErros - " + test + "set - EQ.txt", "w", encoding = "cp1251")
    trueFactsPatternsCount = 0
    err1 = ""
    err2 = ""
    err3 = ""
    err4 = ""
    overflow = factsPatterns
    for book in factsRuFactEval.keys():
        ob = factsRuFactEval.get(book)
        if book in factsPatterns:
            ourbook = factsPatterns.pop(book)
            for k in ourbook:
                ourfact = ourbook.get(k)
                FL = True
                collected=[]
                for testf in ob:
                    testfact = ob.get(testf)
                    # print(book, testfact,"\n")
                    if (ourfact.get('Who') in testfact.get('Who')) and (ourfact.get('Where') in testfact.get('Where')) \
                            and (ourfact.get('Position') in testfact.get('Position')):
                        trueFactsPatternsCount += 1
                        collected.append(testfact)
                        FL = False
                    else:
                        if testPH(ourfact.get('Who') ,testfact.get('Who')) and  testPH(ourfact.get('Where') ,testfact.get('Where')) \
                                and  testPH(ourfact.get('Position') , testfact.get('Position')):
                            collected.append(testfact)
                            err1 += "\nФакты из источника " + book + " не совпали\n\tДолжно быть"
                            for n in testfact:
                                err1 += "\n\t\t" + str(n) + ": " + " | ".join(list(testfact.get(n)))
                            err1 += "\n\t получилось:"
                            for n in ourfact:
                                err1 += "\n\t\t" + str(n) + ": " + ourfact.get(n)
                if FL:
                    err3+=("\nИз источника " + book + " извлечён лишний факт")
                    for n in ourfact:
                        err3+=("\n\t\t" + str(n) + ": " + ourfact.get(n))
            if not len(collected ) == len(testf):
                err2 += ("\nВ источнике " + book + " парсером не найдены следующие факты:")
                for testf in ob:
                    if not testf in collected:
                        err2 += ("\n\t" + str(testf) + ":")
                        testfact = ob.get(testf)
                        for n in testfact:
                            err2 += "\n\t\t" + str(n) + ": " + " | ".join(list(testfact.get(n)))
        else:
            err4 += ("\nВ источнике " + book + " парсер не нашёл ни одного факта, а т.е.:")
            for k in ob.keys():
                err4 += ("\n\t" + str(k) + ":")
                obk = ob.get(k)
                for n in obk.keys():
                    err4 += ("\n\t\t" + str(n) + ": " + " | ".join(list(obk.get(n))))
    printerffors(err1, err2, err3, err4, overflow, errors)
    return trueFactsPatternsCount


def analyse_result_about(test,factsRuFactEval, factsPatterns):
    errors = open("OurErros - "+test+"set - Normalize.txt", "w", encoding="cp1251")
    trueFactsPatternsCount = 0
    err1 = ""
    err2 = ""
    err3 = ""
    err4 = ""
    overflow = factsPatterns
    for book in factsRuFactEval.keys():
        ob = factsRuFactEval.get(book)
        if book in factsPatterns:
            ourbook = factsPatterns.pop(book)
            for k in ourbook:
                ourfact = ourbook.get(k)
                FL = True
                collected=[]
                for testf in ob:
                    testfact = ob.get(testf)
                    # print(book, testfact,"\n")
                    if testPH(ourfact.get('Who') ,testfact.get('Who')) and  testPH(ourfact.get('Where') ,testfact.get('Where')) \
                                and  testPH(ourfact.get('Position') , testfact.get('Position')):
                        trueFactsPatternsCount += 1
                        collected.append(testfact)
                        FL = False
                    else:
                        if testPH(ourfact.get('Who') ,testfact.get('Who')) or  testPH(ourfact.get('Where') ,testfact.get('Where')) \
                                or  testPH(ourfact.get('Position') , testfact.get('Position')):
                            collected.append(testfact)
                            err1 += "\nФакты из источника " + book + " не совпали\n\tДолжно быть"
                            for n in testfact:
                                err1 += "\n\t\t" + str(n) + ": " + " | ".join(list(testfact.get(n)))
                            err1 += "\n\t получилось:"
                            for n in ourfact:
                                err1 += "\n\t\t" + str(n) + ": " + ourfact.get(n)
                if FL:
                    err3+=("\nИз источника " + book + " извлечён лишний факт")
                    for n in ourfact:
                        err3+=("\n\t\t" + str(n) + ": " + ourfact.get(n))
            if not len(collected ) == len(testf):
                err2 += ("\nВ источнике " + book + " парсером не найдены следующие факты:")
                for testf in ob:
                    if not testf in collected:
                        err2 += ("\n\t" + str(testf) + ":")
                        testfact = ob.get(testf)
                        for n in testfact:
                            err2 += "\n\t\t" + str(n) + ": " + " | ".join(list(testfact.get(n)))

        else:
            err4 += ("\nВ источнике " + book + " парсер не нашёл ни одного факта, а т.е.:")
            for k in ob.keys():
                err4 += ("\n\t" + str(k) + ":")
                obk = ob.get(k)
                for n in obk.keys():
                    err4 += ("\n\t\t" + str(n) + ": " + " | ".join(list(obk.get(n))))
    printerffors(err1, err2, err3, err4, overflow, errors)
    return trueFactsPatternsCount


def PRF(trueFactsPatternsCount,allFactsPatternsCount,allFactsRuFactEvalCount):
    Precision = trueFactsPatternsCount / allFactsPatternsCount
    Recall = trueFactsPatternsCount / allFactsRuFactEvalCount
    Fmeasure = 2 * (Precision * Recall) / (Precision + Recall)
    return [Precision,Recall,Fmeasure]


def main(test):
    p = multiprocessing.Pool()
    results = p.map(lambda f: f(test), [read_RuFactEval, runtest])
    p.close()
    p.join()
    factsRuFactEval = results[0]

    #  runtest(test) #если есть результат, то не нужно запускать повторно
    # factsRuFactEval = read_RuFactEval(test)
    factsPatterns = read_OurFact(test)
    allFactsPatternsCount = 0
    for book in factsPatterns:
        allFactsPatternsCount += len(factsPatterns[book])
    print("Всего извлечено = \t", allFactsPatternsCount)
    allFactsRuFactEvalCount = 0
    for book in factsRuFactEval:
        allFactsRuFactEvalCount += len(factsRuFactEval[book])
    print("Всего должно быть извлечено = \t", allFactsRuFactEvalCount)

    p = multiprocessing.Pool()
    results = p.map(lambda f: f(test,factsRuFactEval.copy(), factsPatterns.copy()), [analyse_results_exact, analyse_result_about])
    # print(results)
    p.close()
    p.join()

    trueFactsPatternsCount = results [0]
    print("Извлечено правильно (точное совпадение) = \t", trueFactsPatternsCount)
    if trueFactsPatternsCount>0:
        res = PRF(trueFactsPatternsCount,allFactsPatternsCount, allFactsRuFactEvalCount )
        print("Precision:\t", res[0],"\nRecall:\t",  res[1],"\nFmeasure:\t", res[2])

    trueFactsPatternsCount2 = results [1]
    if trueFactsPatternsCount2 > 0:
        # print("\nА ещё мы посчитали результаты с учётом форм слов")
        print("\nИзвлечено правильно, с учётом форм слов = ", trueFactsPatternsCount2)
        res = PRF(trueFactsPatternsCount2,allFactsPatternsCount, allFactsRuFactEvalCount )
        print("Precision:\t", res[0],"\nRecall:\t",  res[1],"\nFmeasure:\t", res[2])


if __name__ == "__main__":
    print("Проверяемся на тренировочной выборке","-"*15,"\n")
    main("dev")
    print("\n\nПроверяемся на боевой выборке","-"*22,"\n")
    main("test")
