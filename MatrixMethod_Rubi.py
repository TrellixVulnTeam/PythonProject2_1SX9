#!/usr/bin/env python3
# Python Project : Python script to determine stoichiometric ratios of chemical reactions #2
# Handle imports

import re # importing regular expression library
from sympy import Matrix, lcm # importing matrix and least common multiple

# Welcome to the tool. Input equation reactants and products

def addToMatrix(element, index, count, side):
    if index == len(elementMatrix):
        elementMatrix.append([])
        for x in elementList:
            elementMatrix[index].append(0)
    if (element not in elementList):
        elementList.append(element)
        for i in range(len(elementMatrix)):
            elementMatrix[i].append(0)
    column = elementList.index(element)
    elementMatrix[index][column] += count * side

def findElements(segment, index, multiplier, side):
    elementsAndNumbers = re.split('([A-Z][a-z]?)', segment)
    i = 0
    while (i < len(elementsAndNumbers) - 1):  # last element always blank
        i += 1
        if (len(elementsAndNumbers[i]) > 0):
            if (elementsAndNumbers[i + 1].isdigit()):
                count = int(elementsAndNumbers[i + 1]) * multiplier
                addToMatrix(elementsAndNumbers[i], index, count, side)
                i += 1
            else:
                addToMatrix(elementsAndNumbers[i], index, multiplier, side)

def compoundDecipher(compound, index, side):
    segments = re.split('(\([A-Za-z0-9]*\)[0-9]*)', compound)
    for segment in segments:
        if segment.startswith("("):
            segment = re.split('\)([0-9]*)', segment)
            multiplier = int(segment[1])
            segment = segment[0][1:]
        else:
            multiplier = 1
        findElements(segment, index, multiplier, side)

elementList = []
elementMatrix = []
print("Hello aspiring chemist! Please input your reactants. This is case sensitive.")
print("For example, your input should look like: H2O+Ag3(Fe3O)4")
reactants = input("Reactants: ")
print("Please input your products. Again, this is case sensitive.")
products = input("Products: ")
reactants = reactants.replace(' ', '').split("+")
products = products.replace(' ', '').split("+")
print(reactants)
print(products)

for i in range(len(reactants)):
    compoundDecipher(reactants[i], i, 1) #value is positive
for i in range(len(products)):
    compoundDecipher(products[i], i + len(reactants), -1) #value is negative
elementMatrix = Matrix(elementMatrix)
elementMatrix = elementMatrix.transpose()
solution = elementMatrix.nullspace()[0]
multiple = lcm([val.q for val in solution])
solution = multiple * solution
coEffi = solution.tolist()
output = ""
for i in range(len(reactants)):
    output += str(coEffi[i][0]) + reactants[i]
    if i < len(reactants) - 1:
        output += " + "
output += " -> "
for i in range(len(products)):
    output += str(coEffi[i + len(reactants)][0]) + products[i]
    if i < len(products) - 1:
        output += " + "
print(output)
