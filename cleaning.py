from nltk.tokenize import sent_tokenize
import pymorphy2
import multiprocessing.dummy as multiprocessing

def getgaz():
    gaz = open("Fortest/keywords.gzt", "r", encoding="cp1251")
    wok = []
    for line in gaz:
        # print(line)
        lineSplt = line.split()
        if len(lineSplt) > 0 and lineSplt[0] in ["key","lemma"]:
            del(lineSplt[0])
            del(lineSplt[0])
            if lineSplt[0][0] != "\"":
                continue
            lineSplt = " ".join(lineSplt).replace("\"","").split(" | ")
            wok.extend(lineSplt)
    gaz.close()
    return wok

def cleanBYgaz(RuF):
    gaz = getgaz()
    gaf = open("NotInGaz.txt", "w", encoding="cp1251")
    gaf.write("Газеттир:\n" + ", ".join(gaz)+"\n\nСовсем не найдены:\n")
    result = {}
    for book in RuF:
        b = RuF.get(book)
        temp = {}
        for fact in b:
            f = b.get(fact)
            state = False
            for key in f:
                k = f.get(key)
                r = False
                # print (k)
                if not type(k) is bool:
                    for wo in k:
                        for w in wo.split():
                            if w in gaz:
                                r = True
                    if not r:
                        gaf.write("Book: " + book +"\tfact: "+ str(fact)+"\tType: "+ key +"\t\t\t text: " + " | ".join(k) + "\n")
                state = state or r
            if state:
                temp.update([[fact, f]])
            # else:
            #     print("выкинули", f)
        result.update([[book, temp]])
    gaf.close()
    return result

def cleanBYhard(RuF):
    result = {}
    for book in RuF:
        b = RuF.get(book)
        temp = {}
        for fact in b:
            f = b.get(fact)
            if not f['Hard']:
                temp.update([[fact, f]])
            # else:
            #     print("выкинули", f)
        result.update([[book, temp]])
    return result

def fa(s):
    v = []
    morph = pymorphy2.MorphAnalyzer()
    if "Who" in s.keys():
        for a in s["Who"]:
            if "Where" in s.keys():
                for b in s["Where"]:
                    if "Position" in s.keys():
                        for c in s["Position"]:
                            v.append(a + " " + b + " " + c)
                    else:
                        v.append(a + " " + b)
            else:
                if "Position" in s.keys():
                    for c in s["Position"]:
                        v.append(a + " " + c)
                else:
                    v.append(a)
    else:
        print ("!!!! - no WHO", s)
        if "Where" in s.keys():
            for b in s["Where"]:
                if "Position" in s.keys():
                    for c in s["Position"]:
                        v.append( b + " " + c)
                else:
                    v.append(b)
        else:
            if "Position" in s.keys():
                for c in s["Position"]:
                    v.append(c)
    r = (list(map(lambda k: list(map(lambda x: morph.parse(x.replace("\"", ""))[0].normal_form,
                                         k.split(' '))), v)))
    # print(r)
    return r

def cpar(test, book, RuF):
    print ("\t\t\tЧистим", book)
    morph = pymorphy2.MorphAnalyzer()
    d = open("factRuEval-2016/" + test + "set/" + book + ".txt", "r", encoding="utf-8").read()
    doc = sent_tokenize(d)
    # print(doc)
    b = RuF.get(book)
    temp = {}
    for fact in b:
        f = b.get(fact)
        no = fa(f)
        for i in doc:
            dd = list(map(lambda x: morph.parse(x)[0].normal_form, i.split()))
            # print(dd)
            for jj in no:
                ress = True
                for j in jj:
                    if not j in dd:
                        ress = False
                        break
                if ress:
                    temp.update([[fact, f]])
                    print("\t\t\t\tКнига", book, "Взят", f)
                    break
            if ress:
                break
        if not ress:
            print("\t\t\t\tКнига", book, "!!! - Выбросили", f)
    return [book, temp]

def cleanBYsent(test, RuF):
    result = {}
    p = multiprocessing.Pool()
    results = p.map(lambda x: result.update([cpar(test, x, RuF)]), RuF)
    p.close()
    p.join()
    print(result)
    return result

# if __name__ == "__main__":
    # RuF = evaluation.read_RuFactEval("dev")
    # cleanBYgaz(RuF)
    # cleanBYhard(RuF)
    # cleanBYsent("dev", RuF)