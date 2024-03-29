#!/usr/bin/env python
# -*- coding: utf-8 -*-
import lxml.etree as ET
import codecs
import re, sys
dictWords = {}
countTerm = 1
textSyntax = ""

def to_txt(filename, args):
    """
    Erzeugt den Rohtext aus der XML-Datei
    @parm filename: Filename
    @param args: erwartet die Argumente von der Konsole,
        args[0] ist die Ordnerstruktur inklusive Dateiname (ohne Endung) in welchem der Text gespeichert wird

    @var text: speichert den Rohtext
    @var o1: offset1 des aktuellen W-Tags
    @var o2: offset2 des vorherigen W-Tags
    @var firstLine: verhindert einen Leerschlag bei der ersten Zeile
    @var countTerm: globale Variabel um die TermID hoch zu zählen
    @var textSyntax: speichert die Wordannotation für die Syntax-Annotation
    @var dictWord: speichert alle Wörter in einem Dictonary nach TermID für syntax()
    """
    text = ""
    o1 = 0
    o2 = 0
    firstLine = True
    global countTerm, textSyntax, dictWords

    data = ET.parse(filename)
    allWords = data.findall("//W") #alle W-Tags
    for word in allWords:
        o1 = int(word.get("o1"))
        if o1 > o2 and firstLine == False: #white-space
            text += " "* (o1-o2)

        text += word.text
        o2 = int(word.get("o2"))
        firstLine = False
        attr = word.get("C")
        termID = "T" + str(countTerm)
        textSyntax += termID +"\t"
        textSyntax += attr + " " + word.get("o1") + " " + word.get("o2") +"\t"
        textSyntax += word.text +"\n"
        countTerm += 1
        # im Dictionary speichern für syntax()
        dictWords[word.get("id")] = termID

    #Rohtext speichern
    outfile = codecs.open(args[0] +".txt", "w", encoding = "utf-8")
    outfile.write(text)
    outfile.close()


def term(filename, args):
    """
    Erzeugt die Termannotation aus der XML-Datei
    @param filename: Filename
    @param args: erwartet die Argumente von der Konsole,
        args[0] ist die Ordnerstruktur inklusive Dateiname (ohne Endung) in welchem die Termannotation gespeichert wird

    @var text: speichert die Termannotation
    @var countTerm: globale Variabel um die TermID hoch zu zählen
    """
    text = ""
    data = ET.parse(filename)
    allTerms = data.findall(".//Term")

    global countTerm
    for term in allTerms:
        allAttr = term.get("values").split(" ")
        allAttr = set(re.sub(r'[^:]*:','',attr) for attr in allAttr)
        allWords = term.findall("./W")
        #geht alle Attribute und Wörter in dem "Term"-Tag durch
        for attr in allAttr:

            text += "T" + str(countTerm) + '\t' + attr + " " + allWords[0].get('o1') + ' ' + allWords[-1].get('o2') + '\t'
            word_text = string_of_w(allWords)
            text += word_text + '\n'
            countTerm += 1

    #speichern der Termannotation
    outfile = codecs.open(args[0] +".ann", "a", encoding = "utf-8")
    outfile.write(text)
    outfile.close()


def chunk(filename, args):
    """
    Erzeugt die Chunk-Annotation aus der XML-Datei
    @param filename: Filename
    @param args: erwartet die Argumente von der Konsole,
        args[0] ist die Ordnerstruktur inklusive Dateiname (ohne Endung) in welchem die Chunk-Annotation gespeichert wird

    @var text: speichert die Chunk-Annotation
    @var countChunk: zählt von 1 hoch für ID
    """
    text = ""
    data = ET.parse(filename)
    allTerms = data.findall(".//NG")

    global countTerm
    for term in allTerms:
        allWords = term.findall("./W")
        print >> sys.stderr, '# ',len(allWords)
        if len(allWords) == 1: continue
        text += "T" + str(countTerm) + '\t' + 'NG' + " " + allWords[0].get('o1') + ' ' + allWords[-1].get('o2') + '\t'
        word_text = string_of_w(allWords)
        text += word_text + '\n'
        countTerm += 1

    #speichern der Termannotation
    outfile = codecs.open(args[0] +".ann", "a", encoding = "utf-8")
    outfile.write(text)
    outfile.close()


def pos(filename, args):
    """
    Erzeugt die Chunk-Annotation aus der XML-Datei
    @param filename: Filename
    @param args: erwartet die Argumente von der Konsole,
        args[0] ist die Ordnerstruktur inklusive Dateiname (ohne Endung) in welchem die Chunk-Annotation gespeichert wird

    @var text: speichert die Chunk-Annotation
    @var countChunk: zählt von 1 hoch für ID
    """
    text = ""
    data = ET.parse(filename)
    allChunk = data.findall(".//W")
    print allChunk

    countChunk = 1
    for chunk in allChunk:
        attr = chunk.get("C")
        chunkID = "C" + str(countChunk)
        text += chunkID +"\t"
        text += attr + " " + chunk.get("o1") + " " + chunk.get("o2") +"\t"
        text += chunk.text + "\n"
        countChunk += 1

    #speichern der Chunk-Annotation
    outfile = codecs.open(args[0] +".ann", "a", encoding = "utf-8")
    outfile.write(text)
    outfile.close()

def syntax(filename, args):
    """
    Erzeugt die Syntax-Annotation aus der XML-Datei
    @param filename: Filename
    @param args: erwartet die Argumente von der Konsole,
        args[0] ist die Ordnerstruktur inklusive Dateiname (ohne Endung) in welchem die Syntax-Annotation gespeichert wird

    @var textSyntax: globale Variable in welcher die Syntax-Annotation gespeichert wird
    @var dictWords: die gespeicherten Wörter mit TermID (value) und WordID (key)
    @var countRel: zählt von 1 hoch für ID
    """
    global textSyntax, dictWords

    data = ET.parse(filename)
    allRel = data.findall("//Rel")

    countRel = 1
    for rel in allRel:
        relID = "R"  + str(countRel)
        textSyntax += relID +"\t"
        textSyntax += rel.get("type")
        textSyntax += " Arg1:"+ dictWords[rel.get("head")]
        textSyntax += " Arg2:"+ dictWords[rel.get("dep")]
        textSyntax += "\n"
        countRel += 1

    #speichern der Chunk-Annotation
    outfile = codecs.open(args[0] +".ann", "a", encoding = "utf-8")
    outfile.write(textSyntax)
    outfile.close()

def string_of_w(allwords):
    """Return string representation of list of w elements."""
    result = ''
    if len(allwords) == 1: return allwords[0].text
    prev_o2 = int(allwords[0].get('o1'))
    for i,w in enumerate(allwords):
        curr_o1 = int(w.get('o1'))
        result += ' ' *(curr_o1-prev_o2) + w.text
        prev_o2 = int(w.get('o2'))
    return result


