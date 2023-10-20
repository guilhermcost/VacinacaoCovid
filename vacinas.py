# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 07:34:49 2021

@author: Guilherme Costa
"""
from queue import PriorityQueue
from copy import deepcopy

dist_real = [[0,270,475,675,-1,-1,-1,980,-1,1093,-1,-1],
            [270,0,225,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [475,225,0,205,-1,-1,-1,-1,-1,-1,-1,-1],
            [675,-1,205,0,99,-1,623,933,-1,-1,-1,-1],
            [-1,-1,-1,99,0,152,551,-1,-1,-1,-1,1],
            [-1,-1,-1,-1,152,0,430,-1,-1,-1,-1,-1],
            [-1,-1,-1,623,551,430,0,493,-1,-1,-1,-1],
            [980,-1,-1,933,-1,-1,493,0,325,845,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,325,0,957,488,-1],
            [1093,-1,-1,-1,-1,-1,-1,845,957,0,965,1032],
            [-1,-1,-1,-1,-1,-1,-1,-1,488,965,0,1787],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,1032,1787,0]]

dist_reta = [[0, 270, 475, 675, 749, 828, 1017, 980, 1318, 1093, 1664, 1924],
            [270, 0, 225, 394, 484, 612, 837, 938, 1236, 1238, 1646, 2128],
            [475, 225, 0, 205, 290, 426, 712, 933, 1230, 1376, 1683, 2343],
            [675, 394, 205, 0, 99, 247, 623, 933, 1190, 1508, 1673, 2457],
            [749, 484, 290, 99, 0, 152, 551, 902, 1158, 1524, 1632, 2508],
            [828, 612, 426, 247, 152, 0, 430, 846, 1078, 1545, 1553, 2533],
            [1017, 837, 712, 623, 551, 430, 0, 493, 657, 1298, 1227, 2334],
            [980, 938, 933, 933, 902, 846, 493,  0, 325, 845, 746, 1860],
            [1318, 1236, 1230, 1190, 1158, 1078, 657, 325, 0, 957, 488, 1938],
            [1093, 1238, 1376, 1508, 1524, 1545, 1298, 845, 957, 0, 965, 1032],
            [1664, 1646, 1683, 1673, 1632, 1553, 1227, 746, 488, 965, 0, 1787],
            [1924, 2128, 2343, 2457, 2508, 2533,2334, 1860,1938,1032,1787, 0]]

##Variavel que guarda os estados que podem ser visitadas por cada nó ##
estados_vizinhos = [[2, 3, 4, 8, 10],#E1
           [1,3],#E2
           [1,2,4],#E3
           [1,3,5,7,8],#E4
           [4,6,7],#E5
           [5,7],#E6
           [4,5,6,8],#E7
           [1,4,7,9,10],#E8
           [8,10,11],#E9
           [1,8,9,11,12],#E10
           [9,10,12],#E11
           [10,11]]#E12

#Classe Estado - Guarda os valores do estado atual

class Estado(object):
    def __init__(self, valor, pai, numVacinas, inicio = 0, destino = 0):
        self.filhos = []
        self.pai = pai
        self.valor = valor
        self.numVacinas = numVacinas

        
        if pai:
            self.caminho = pai.caminho
            self.caminho.append(valor)
            self.inicio = pai.inicio
            self.destino = pai.destino
        
        else: # Se não tiver pai, significa que é o estado inicial. adicionamos o valor ao caminho e defininmos o inicio e o destino
        
            self.caminho = [valor]
            self.inicio = inicio
            self.destino = destino
    
    #funções implementadas na classe filha Estado_Atual
    def GetDistanciaReal(self):
        pass
    
    def GetVacinasRestantes(self):
        pass
        
    def GetDistanciaReta(self):
        pass
    
    def CriarFilhos(self):
        pass
    
class Estado_Atual(Estado): #herda da classe Estado
    
    def __init__(self, valor, pai, taxaVacinados, numVacinas , vacinasRestantes, inicio = 0, destino = 0):
        super(Estado_Atual, self).__init__(valor, pai, numVacinas, inicio, destino)
        self.distanciaReta = self.GetDistanciaReta()
        self.taxasEstados = taxaVacinados
        self.taxaIndividual = self.taxasEstados.get(self.valor)
        self.taxaNaoVacinados = 1 - self.taxaIndividual
        self.custo = self.GetCusto()
        self.vacinasRestantes = vacinasRestantes
        self.vacinasRestantes = self.distribuirVacina()
#         print("Valor: ", self.valor, "Custo", self.custo, "Vacinas Restantes", self.vacinasRestantes)
        
    #retorna o custo da aresta
#     def GetDistanciaReal(self):
        
#         return self.distanciaReal
        
    #Calcula o valor da heurística
    def GetDistanciaReta(self):
        if self.valor == self.destino:
            return 0
        return dist_reta[self.valor-1][self.destino-1]
    
    def GetCusto(self): # o custo associado ao problema é h(i) = distancia(i,t) * pi, sendo pi a taxa de vacinados no estado i
        if self.pai == 0:
            return 0
        return (self.distanciaReta * self.taxaIndividual)
        
    def CriarFilhos(self):
        if not self.filhos:
            for i in estados_vizinhos[self.valor - 1]:
                proximo_valor = i
                copiaPai = deepcopy(self)
                self.filho = Estado_Atual(proximo_valor, copiaPai, self.taxasEstados, self.numVacinas, self.vacinasRestantes)
                self.filhos.append(self.filho)
                
    def distribuirVacina(self):
        vacinasDistribuidas = int(self.numVacinas * 0.2 * (self.taxaNaoVacinados)) 
        return (self.vacinasRestantes - vacinasDistribuidas)
    
    
class A_Estrela:
    
    def __init__(self, vacinadosEstado, numVacinas, inicio, destino):
        self.caminho = []
        self.nosVisitados = []
        self.vacinadosEstado = vacinadosEstado
        self.numVacinas = numVacinas
        self.vacinasRestantes = numVacinas
        self.filaPrioridade = PriorityQueue()
        self.inicio = inicio
        self.destino = destino
        
    def solucao(self):
        estadoInicial = Estado_Atual(self.inicio, 0, self.vacinadosEstado, self.numVacinas, self.numVacinas, self.inicio, self.destino)
        if self.inicio == self.destino:
            self.vacinasRestantes = estadoInicial.vacinasRestantes
            return
        count = 0
        self.filaPrioridade.put((0, count, estadoInicial))
        while(not self.caminho and self.filaPrioridade.qsize()): #enquanto o caminho não existir e a fila de prioridade nao for vazia
            proximoEstado = self.filaPrioridade.get()[2]                    
            proximoEstado.CriarFilhos()
            self.nosVisitados.append(proximoEstado.valor)
            for t in proximoEstado.filhos:
                if t.valor not in self.nosVisitados:
                    count += 1
                    if not t.distanciaReta:
                        self.caminho = t.caminho
                        self.vacinasRestantes = t.vacinasRestantes
                        break
                    self.filaPrioridade.put((t.custo, count, t))

        if not self.caminho:
            print ("Não foi possível resolver")
        return self.caminho
    
#Recebimento de Entradas#

entry = input().rstrip()
s,t = entry.split(' ')
s = int(s)
t = int(t)
qtd_vacinas = int(input())

num_vac = dict()

for i in range(12):
    entry = input().rstrip()
    estado, vacinados = entry.split(' ')
    num_vac[int(estado)] = float(vacinados)
# Fim das Entradas #

a = A_Estrela(num_vac, qtd_vacinas, s, t)
a.solucao()

if s == t:
    print(s)
    print(a.vacinasRestantes)
    
else:
    
    #saída
    string_caminho = ""
    
    for i in a.caminho:
        string_caminho += str(i) + "-"
        
    string_caminho = string_caminho[:-1]
    
    print(string_caminho)
    print(a.vacinasRestantes)
    

        