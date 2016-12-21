import os
import subprocess
import pymorphy2
from cleaning import *
import multiprocessing.dummy as multiprocessing
from multiprocessing import Process

def filewrite(subf, fp, test):
        filePath =fp + "/" + subf
        if ".txt" in subf:
            docName = subf.split(".")[0]
            mpath = os.getcwd().replace("\\", "/") + '/ourtest/' + test + 'set/' + docName
            mconf = open("Fortest/" + test + "-" + docName + '.proto', "w", encoding="cp1251")
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
            subprocess.call('Fortest\\tomitaparser.exe ourtest\\Fortest\\' + test + "-" + docName + '.proto',
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            # print('ourtest/Fortest/tomitaparser.exe ' + test + "-" + docName + '.proto')
            # subprocess.Popen('ourtest/Fortest/tomitaparser.exe ' + test + "-" + docName + '.proto', shell=True,
            #                  stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            # print(tomitarun.stdout.readlines())
            # i = tomitarun.stdout.readlines()
        # print (filePath)

def runtest (test):
    devSetPatterns = os.getcwd() + '\\factRuEval-2016\\' + test + 'set'
    mainTree = os.walk(devSetPatterns)
    for d in mainTree:
        # print(d)
        p = multiprocessing.Pool()
        p.map(lambda x: filewrite(x , d[0] ,  test), d[2])
        p.close()
        p.join()
    print("томита извлекла данные",test)


def cleaneval(st):
    del(st[0])
    del(st[0])
    # res = st
    res = [x for x in st if not (('span' in x) or ('obj' in x))]
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


def cleanour(t):
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
    try:
        if isinstance(f,list):
            result = list(map(lambda k: list(map(lambda x: morph.parse(x.replace("\"", "")
                                                                       .replace("«", "")
                                                                       .replace("»", "")
                                                                       )[0].normal_form, k.split(' '))), f))
            # print (result)
        else:
            result = list(map(lambda x: morph.parse(x)[0].normal_form,f.split(' ')))
    except Exception as ex:
        print(ex)
    return result


def printerffors(err1,err2,err3,err4,overflow,errors):
    errors.write("1. В этом разделе перечислены факты, найденные с недочётами\n")
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


def bootostr(s):
    if type(s) is bool:
        return str(s)
    else:
        return s


def testPHw(ou, th):
    result = 0
    # print (ou," ",th)
    try:
        if ou in th:
            result = 1
        else:
            our = normal(ou)
            test = normal(th)
            count = 0
            for o in our:
                for t in test:
                    if o in t:
                        count += 1
                        break
            result = count / len(our)
            # print(our,test,result)
    except Exception:
        None
    return result

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


def testPHexact(ourfact,testfact):
    return (ourfact.get('Who') in testfact.get('Who')) and (ourfact.get('Where') in testfact.get('Where')) \
                            and (ourfact.get('Position') in testfact.get('Position'))

def testPHabout(ourfact,testfact):
    return testPH(ourfact.get('Who'), testfact.get('Who')) and testPH(ourfact.get('Where'), testfact.get('Where')) \
                    and testPH(ourfact.get('Position'), testfact.get('Position'))

def testPHaboutOR(ourfact,testfact, k =2):
    test = testPHw(ourfact.get('Who'), testfact.get('Who')) + testPHw(ourfact.get('Where'), testfact.get('Where')) \
           + testPHw(ourfact.get('Position'), testfact.get('Position'))
    # print(test)
    return test >= k

def analyse(ob, ourbook, book, testP):
    err1 = ""
    err2 = ""
    err3 = ""
    print("\t\tАнализируется", book)
    trueFactsPatternsCount = 0
    fard = 0
    collected = []
    for k in ourbook:
        ourfact = ourbook.get(k)
        FL = True
        for testf in ob:
            testfact = ob.get(testf)
            # print(book, testfact,"\n")
            if testP(ourfact, testfact):
                trueFactsPatternsCount += 1
                if testfact['Hard']:
                    fard += 1
                collected.append(testfact)
                FL = False
            else:
                if testPHaboutOR(ourfact, testfact):
                    collected.append(testfact)
                    err1 += "\nФакты из источника " + book + " не совпали\n\tДолжно быть"
                    for n in testfact:
                        err1 += "\n\t\t" + str(n) + ": " + " | ".join(bootostr(testfact.get(n)))
                    err1 += "\n\t получилось:"
                    for n in ourfact:
                        err1 += "\n\t\t" + str(n) + ": " + ourfact.get(n)
        if FL:
            err3 += ("\nИз источника " + book + " извлечён лишний факт")
            for n in ourfact:
                err3 += ("\n\t\t" + str(n) + ": " + ourfact.get(n))

    if not len(collected) == len(ob):
        err2 += ("\nВ источнике " + book + " парсером не найдены следующие факты:")
        for testf in ob:
            if not testf in collected:
                err2 += ("\n\t" + str(testf) + ":")
                testfact = ob.get(testf)
                for n in testfact:
                    err2 += "\n\t\t" + str(n) + ": " + " | ".join(bootostr(testfact.get(n)))
    return {'count': trueFactsPatternsCount, "err1": err1, "err2": err2, "err3": err3, "err4": "", "hard": fard}


def analyse_results(test, factsRuFactEval, factsPatterns, PH, type):
    trueFactsPatternsCount = 0
    err1 = ""
    err2 = ""
    err3 = ""
    err4 = ""
    hard = 0
    p = multiprocessing.Pool()
    results = p.map(lambda x: analyse(factsRuFactEval.get(x),  factsPatterns.pop(x), x, PH) if x in factsPatterns else \
        er4(factsRuFactEval.get(x), x), factsRuFactEval.keys())
    p.close()
    p.join()
    print("\tЗапись результатов", test, type)
    for i in results:
        err1 += i['err1']
        err2 += i['err2']
        err3 += i['err3']
        err4 += i['err4']
        trueFactsPatternsCount += i['count']
        hard += i['hard']
    errors = open("OurErros - "+test+"set - "+type+".txt", "w", encoding="cp1251")
    printerffors(err1, err2, err3, err4, factsPatterns, errors) # factsPatterns  - неправильно стоит
    print("\tАнализ", test, type, "завершен")
    return [trueFactsPatternsCount, hard]


def er4(ob, book):
    err4 = ""
    err4 += ("\nВ источнике " + book + " парсер не нашёл ни одного факта, а т.е.:")
    for k in ob.keys():
        err4 += ("\n\t" + str(k) + ":")
        obk = ob.get(k)
        for n in obk.keys():
            err4 += ("\n\t\t" + str(n) + ": " + " | ".join(bootostr(obk.get(n))))
    return {'count': 0,"err1": "","err2": "","err3": "", "err4": err4, "hard": 0}


def PRF(trueFactsPatternsCount,allFactsPatternsCount,allFactsRuFactEvalCount):
    Precision = trueFactsPatternsCount / allFactsPatternsCount
    Recall = trueFactsPatternsCount / allFactsRuFactEvalCount
    Fmeasure = 2 * (Precision * Recall) / (Precision + Recall)
    return ("\nPrecision:\t" + str(Precision) + "\nRecall:\t" + str(Recall) + "\nFmeasure:\t" + str(Fmeasure))

def main(test, m):
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
    allFactsRuFactEvalCount = 0
    for book in factsRuFactEval:
        allFactsRuFactEvalCount += len(factsRuFactEval[book])

    gaz = cleanBYgaz(factsRuFactEval)
    hard = cleanBYhard(factsRuFactEval)
    sent = cleanBYsent(test, factsRuFactEval)
    all = cleanBYhard(cleanBYgaz((sent)))
    print("Отфильтрованные базы для",test,"получены")

    p = multiprocessing.Pool()
    run = [
        [testPHexact, "EQ",                     factsRuFactEval.copy()],
        [testPHabout, "Normalize",              factsRuFactEval.copy()],
        [testPHexact, "EQ-gaz-filter",          gaz.copy()],
        [testPHabout, "Normalize-gaz-filter",   gaz.copy()],
        [testPHexact, "EQ-hard-filter",         hard.copy()],
        [testPHabout, "Normalize-hard-filter",  hard.copy()],
        [testPHexact, "EQ-sent-filter",         sent.copy()],
        [testPHabout, "Normalize-sent-filter",  sent.copy()],
        [testPHexact, "EQ-all-filter",          all.copy()],
        [testPHabout, "Normalize-all-filter",   all.copy()]
    ]
    results = p.map(lambda f: analyse_results(test, f[2], factsPatterns.copy(), f[0],f[1]), run)
    # print(results)
    p.close()
    p.join()

    trueFactsPatternsCount = results[0][0]
    trueFactsPatternsCount2 = results[1][0]
    th1 = results[0][1]
    th2 = results[1][1]

    data = ""
    data += m
    data += ("\n\nВсего извлечено = \t" + str(allFactsPatternsCount))
    data += ("\nВсего должно быть извлечено = \t" + str(allFactsRuFactEvalCount))
    data += ("\n\nИзвлечено правильно (точное совпадение) = \t" + str(trueFactsPatternsCount))
    data += ("\n\nИз них повышенной сложности = \t" + str(th1))
    if trueFactsPatternsCount>0:
        data += PRF(trueFactsPatternsCount, allFactsPatternsCount, allFactsRuFactEvalCount)
    if trueFactsPatternsCount2 > 0:
        # print("\nА ещё мы посчитали результаты с учётом форм слов")
        data += ("\n\nИзвлечено правильно, с учётом форм слов = " + str(trueFactsPatternsCount2))
        data += ("\n\nИз них повышенной сложности = \t" + str(th2))
        data += PRF(trueFactsPatternsCount2, allFactsPatternsCount, allFactsRuFactEvalCount)
    k = 1

    k += 1
    ro = results[k][0]
    if ro > 0:
        data += ("\n\nРезульаты с очисткой по газеттиру (точное совпадение), правильно = \t" + str(ro))
        data += ("\n\nРазмер словаря правильных ответов = \t" + str(len(gaz)))
        data += PRF(ro, allFactsPatternsCount, allFactsRuFactEvalCount)

    k += 1
    ro = results[k][0]
    if ro > 0:
        data += ("\n\nРезульаты с очисткой по газеттиру (нормализация), правильно = " + str(ro))
        data += PRF(ro, allFactsPatternsCount, allFactsRuFactEvalCount)

    k += 1
    ro = results[k][0]
    if ro > 0:
        data += ("\n\nРезульаты с очисткой по сложности (точное совпадение), правильно = " + str(ro))
        data += ("\n\nРазмер словаря правильных ответов = \t" + str(len(hard)))
        data += PRF(ro, allFactsPatternsCount, allFactsRuFactEvalCount)

    k += 1
    ro = results[k][0]
    if ro > 0:
        data += ("\n\nРезульаты с очисткой по сложности (нормализация), правильно = " + str(ro))
        data += PRF(ro, allFactsPatternsCount, allFactsRuFactEvalCount)

    k += 1
    ro = results[k][0]
    if ro > 0:
        data += ("\n\nРезульаты с очисткой по предложениям (точное совпадение), правильно = " + str(ro))
        data += ("\n\nРазмер словаря правильных ответов = \t" + str(len(sent)))
        data += PRF(ro, allFactsPatternsCount, allFactsRuFactEvalCount)

    k += 1
    ro = results[k][0]
    if ro > 0:
        data += ("\n\nРезульаты с очисткой по предложениям (нормализация), правильно = " + str(ro))
        data += PRF(ro, allFactsPatternsCount, allFactsRuFactEvalCount)

    k += 1
    ro = results[k][0]
    if ro > 0:
        data += ("\n\nРезульаты с полной очисткой (точное совпадение), правильно = " + str(ro))
        data += ("\n\nРазмер словаря правильных ответов = \t" + str(len(all)))
        data += PRF(ro, allFactsPatternsCount, allFactsRuFactEvalCount)

    k += 1
    ro  = results[k][0]
    if ro > 0:
        data += ("\n\nРезульаты с полной очисткой (нормализация), правильно = " + str(ro))
        data += PRF(ro, allFactsPatternsCount, allFactsRuFactEvalCount)

    wfile = open("Results.txt", "a", encoding="cp1251")
    wfile.write(data)
    wfile.close()
    print("результаты записаны:", test)


if __name__ == "__main__":
    open("Results.txt", "w", encoding="cp1251").close()
    Process(target=main, args=("dev", "\n\nПроверка на тренировочной выборке " + ("-" * 15))).start()
    print("запущен тест на тренировочном")
    Process(target=main, args=("test","\n\nПроверка на боевой выборке " + ("-"*22))).start()
    print("запущен тест на боевом")
    # main("dev", "Проверяемся на тренировочной выборке " + ("-" * 15) + "\n")
    # main("test","\n\nПроверяемся на боевой выборке " + ("-"*22) + "\n")
