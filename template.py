import random
import math
import sys
linha = 3
coluna = 5
bitsDeDados = linha*coluna
bitDeParidadeDasLinhas=bitsDeDados+coluna
pacoteInteiro8BitsdeDados6bitsDeParidade = bitsDeDados+linha+coluna
#########
# Implementacao simplificada de um esquema de paridade bidimensional 2x4
# (paridade par).
#
# Cada byte do pacote (2x4 = 8 bits) eh mapeado para uma matrix 2x4:
# d0 d1 d2 d3 d4 d5 d6 d7 => --           --
#                            | d0 d1 d2 d3 |
#                            | d4 d5 d6 d7 |
#                            --           --
# Cada coluna 0 <= i <= 3 da origem a uma paridade pc_i.
# Cada linha 0 <= i <= 1 da origem a uma paridade pl_i.
#
# No pacote codificado, os bits sao organizados na forma:
# d0 d1 d2 d3 d4 d5 d6 d7 pc0 pc1 pc2 pc3 pl0 pl1
#
# Isso se repete para cada byte do pacote original.
########

###
##
# Funcoes a serem alteradas!
##
###

##
# Codifica o pacote de entrada, gerando um pacote
# de saida com bits redundantes.
##
def codePacket(originalPacket):
    
    parityMatrix = [[0 for x in range(coluna)] for y in range(linha)]
    codedLen = len(originalPacket) / bitsDeDados * pacoteInteiro8BitsdeDados6bitsDeParidade;
    codedPacket = [0 for x in range(codedLen)]

    ##
    # Itera por cada byte do pacote original.
    ##
    for i in range(len(originalPacket) / bitsDeDados):

        ##
        # Bits do i-esimo byte sao dispostos na matriz.
        ##
        for j in range(linha):
            for k in range(coluna):
                parityMatrix[j][k] = originalPacket[i * bitsDeDados + coluna * j + k]

        ##
        # Replicacao dos bits de dados no pacote codificado.
        ##
        for j in range(bitsDeDados):
            codedPacket[i * pacoteInteiro8BitsdeDados6bitsDeParidade + j] = originalPacket[i * bitsDeDados + j]

        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das colunas.
        ##
        for j in range(coluna):
            if (parityMatrix[0][j] + parityMatrix[1][j]) % linha == 0:
                codedPacket[i * pacoteInteiro8BitsdeDados6bitsDeParidade + bitsDeDados + j] = 0
            else:
                codedPacket[i * pacoteInteiro8BitsdeDados6bitsDeParidade + bitsDeDados + j] = 1

        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das linhas.
        ##
        for j in range(linha):
            ## TODO refatorar isso 
            if calculaBitDeParidade(parityMatrix,j) == 0 :
                codedPacket[i * pacoteInteiro8BitsdeDados6bitsDeParidade + bitDeParidadeDasLinhas + j] = 0
            else:
                codedPacket[i * pacoteInteiro8BitsdeDados6bitsDeParidade + bitDeParidadeDasLinhas + j] = 1

    return codedPacket

## TODO Refatorar isso 
def calculaBitDeParidade(parityMatrix,j):
    sum = 0
    for i in range(len(parityMatrix[j])):
        sum += parityMatrix[j][i]
    return sum % linha

##
# Executa decodificacao do pacote transmittedPacket, gerando
# novo pacote decodedPacket.
##
def decodePacket(transmittedPacket):

    parityMatrix = [[0 for x in range(coluna)] for y in range(linha)]
    parityColumns = [0 for x in range(coluna)]
    parityRows = [0 for x in range(linha)]
    decodedPacket = [0 for x in range(len(transmittedPacket))]

    n = 0 # Contador de bytes no pacote decodificado.

    ##
    # Itera por cada sequencia de pacoteInteiro8BitsdeDados6bitsDeParidade bits (8 de dados + 6 de paridade).
    ##
    for i in range(0, len(transmittedPacket), pacoteInteiro8BitsdeDados6bitsDeParidade):

        ##
        # Bits do i-esimo conjunto sao dispostos na matriz.
        ##
        for j in range(linha):
            for k in range(coluna):
                parityMatrix[j][k] = transmittedPacket[i + coluna * j + k]

        ##
        # Bits de paridade das colunas.
        ##
        for j in range(coluna):
            parityColumns[j] = transmittedPacket[i + bitsDeDados + j]

        ##
        # Bits de paridade das linhas.
        ##
        for j in range(linha):
            parityRows[j] = transmittedPacket[i + bitDeParidadeDasLinhas + j]

        ##
        # Verificacao dos bits de paridade: colunas.
        # Note que paramos no primeiro erro, ja que se houver mais
        # erros, o metodo eh incapaz de corrigi-los de qualquer
        # forma.
        ##
        errorInColumn = -1
        for j in range(coluna):
            if (parityMatrix[0][j] + parityMatrix[1][j]) % linha != parityColumns[j]:
                errorInColumn = j
                break

        ##
        # Verificacao dos bits de paridade: linhas.
        # Note que paramos no primeiro erro, ja que se houver mais
        # erros, o metodo eh incapaz de corrigi-los de qualquer
        # forma.
        ##
        errorInRow = -1
        for j in range(linha):

            if calculaBitDeParidade(parityMatrix, j) != parityRows[j]:
                errorInRow = j
                break

        ##
        # Se algum erro foi encontrado, corrigir.
        ##
        if errorInRow > -1 and errorInColumn > -1:

            if parityMatrix[errorInRow][errorInColumn] == 1:
                parityMatrix[errorInRow][errorInColumn] = 0
            else:
                parityMatrix[errorInRow][errorInColumn] = 1

        ##
        # Colocar bits (possivelmente corrigidos) na saida.
        ##
        for j in range(linha):
            for k in range(coluna):
                decodedPacket[bitsDeDados * n + coluna * j + k] = parityMatrix[j][k]

        ##
        # Incrementar numero de bytes na saida.
        ##
        n = n + 1

    return decodedPacket

###
##
# Outras funcoes.
##
###

##
# Gera conteudo aleatorio no pacote passado como
# parametro. Pacote eh representado por um vetor
# em que cada posicao representa um bit.
# Comprimento do pacote (em bytes) deve ser
# especificado.
##
def generateRandomPacket(l):

    return [random.randint(0,1) for x in range(bitsDeDados * l)]

##
# Gera um numero pseudo-aleatorio com distribuicao geometrica.
##
def geomRand(p):

    uRand = 0
    while(uRand == 0):
        uRand = random.uniform(0, 1)

    return int(math.log(uRand) / math.log(1 - p))

##
# Insere erros aleatorios no pacote, gerando uma nova versao.
# Cada bit tem seu erro alterado com probabilidade errorProb,
# e de forma independente dos demais bits.
# Retorna o numero de erros inseridos no pacote e o pacote com erros.
##
def insertErrors(codedPacket, errorProb):

    i = -1
    n = 0 # Numero de erros inseridos no pacote.

    ##
    # Copia o conteudo do pacote codificado para o novo pacote.
    ##
    transmittedPacket = list(codedPacket)

    while 1:

        ##
        # Sorteia a proxima posicao em que um erro sera inserido.
        ##
        r = geomRand(errorProb)
        i = i + 1 + r

        if i >= len(transmittedPacket):
            break

        ##
        # Altera o valor do bit.
        ##
        if transmittedPacket[i] == 1:
            transmittedPacket[i] = 0
        else:
            transmittedPacket[i] = 1

        n = n + 1

    return n, transmittedPacket

##
# Conta o numero de bits errados no pacote
# decodificado usando como referencia
# o pacote original. O parametro packetLength especifica o
# tamanho dos dois pacotes em bytes.
##
def countErrors(originalPacket, decodedPacket):

    errors = 0

    for i in range(len(originalPacket)):
        if originalPacket[i] != decodedPacket[i]:
            errors = errors + 1

    return errors

##
# Exibe modo de uso e aborta execucao.
##
def help(selfName):

    sys.stderr.write("Simulador de metodos de FEC/codificacao.\n\n")
    sys.stderr.write("Modo de uso:\n\n")
    sys.stderr.write("\t" + selfName + " <tam_pacote> <reps> <prob. erro>\n\n")
    sys.stderr.write("Onde:\n")
    sys.stderr.write("\t- <tam_pacote>: tamanho do pacote usado nas simulacoes (em bytes).\n")
    sys.stderr.write("\t- <reps>: numero de repeticoes da simulacao.\n")
    sys.stderr.write("\t- <prob. erro>: probabilidade de erro de bits (i.e., probabilidade\n")
    sys.stderr.write("de que um dado bit tenha seu valor alterado pelo canal.)\n\n")

    sys.exit(1)

##
# Programa principal:
#  - le parametros de entrada;
#  - gera pacote aleatorio;
#  - gera bits de redundancia do pacote
#  - executa o numero pedido de simulacoes:
#      + Introduz erro
#  - imprime estatisticas.
##

##
# Inicializacao de contadores.
##
totalBitErrorCount = 0
totalPacketErrorCount = 0
totalInsertedErrorCount = 0

##
# Leitura dos argumentos de linha de comando.
##
if len(sys.argv) != 4:
    help(sys.argv[0])

packetLength = int(sys.argv[1])
reps = int(sys.argv[2])
errorProb = float(sys.argv[3])

if packetLength <= 0 or reps <= 0 or errorProb < 0 or errorProb > 1:
    help(argv[0])

##
# Inicializacao da semente do gerador de numeros
# pseudo-aleatorios.
##
random.seed()

##
# Geracao do pacote original aleatorio.
##

originalPacket = generateRandomPacket(packetLength)
codedPacket = codePacket(originalPacket)

##
# Loop de repeticoes da simulacao.
##
for i in range(reps):

    ##
    # Gerar nova versao do pacote com erros aleatorios.
    ##
    insertedErrorCount, transmittedPacket = insertErrors(codedPacket, errorProb)
    totalInsertedErrorCount = totalInsertedErrorCount + insertedErrorCount

    ##
    # Gerar versao decodificada do pacote.
    ##
    decodedPacket = decodePacket(transmittedPacket)

    ##
    # Contar erros.
    ##
    bitErrorCount = countErrors(originalPacket, decodedPacket)

    if bitErrorCount > 0:

        totalBitErrorCount = totalBitErrorCount + bitErrorCount
        totalPacketErrorCount = totalPacketErrorCount + 1

print 'Numero de transmissoes simuladas: {0:d}\n'.format(reps)
print 'Numero de bits transmitidos: {0:d}'.format(reps * packetLength * bitsDeDados)
print 'Numero de bits errados inseridos: {0:d}\n'.format(totalInsertedErrorCount)
print 'Taxa de erro de bits (antes da decodificacao): {0:.2f}%'.format(float(totalInsertedErrorCount) / float(reps * len(codedPacket)) * 100.0)
print 'Numero de bits corrompidos apos decodificacao: {0:d}'.format(totalBitErrorCount)
print 'Taxa de erro de bits (apos decodificacao): {0:.2f}%\n'.format(float(totalBitErrorCount) / float(reps * packetLength * bitsDeDados) * 100.0)
print 'Numero de pacotes corrompidos: {0:d}'.format(totalPacketErrorCount)
print 'Taxa de erro de pacotes: {0:.2f}%'.format(float(totalPacketErrorCount) / float(reps) * 100.0)