from socket import *
import sys

#===== PARTE I =====#
#Preparação do socket
SOCKET = socket(AF_INET, SOCK_STREAM) #Cria socket com suporte para IPV4 e TCP
PORT = 12345 #Número da porta
SOCKET.bind(('',PORT)) #Ligando porta ao socket
SOCKET.listen() #Espera por resposta
print("O servidor MONSTRUOSO está pronto")

while True:
    #===== PARTE II =====#
    CONNECTION, ADDRESS = SOCKET.accept() #Aceita requests
    print("Requisição aceita de (endereço, porta): %s" % (ADDRESS,))

    try:
        #Rebe mensagem e decodifica
        MESSAGE = CONNECTION.recv(2048).decode()
        #Verifica se a mensagem está vazia
        if MESSAGE != "":

            #===== PARTE III =====#
            #Extrai o nome do arquivo que vem após o GET da mensagem
            FILENAME = MESSAGE.split()[1]
            #===== PARTE IV =====#
            if FILENAME[1:] == '': #Identifica se nenhum arquivo foi requisitado e envia o arquivo de index
                #Abre o arquivo index.html
                FILE = open("index.html", 'r')
                OUTPUT = FILE.read() #Transforma arquivo em string
            else:
                #Abre o arquivo requisitado, ignorando a '/' que vem antes do nome do arquivo
                FILE = open(FILENAME[1:], 'r')
                OUTPUT = FILE.read() #Transforma arquivo em string

            print("Arquivo encontrado.")

            #print(OUTPUT)

            #Informa que o arquivo foi encontrado
            #===== PARTE V & VI =====#
            HEADER = "HTTP/1.1 200 OK\r\n"
            CONNECTION.send(HEADER.encode() + "\r\n".encode())

            #Envia o arquivo ao cliente
            CONNECTION.send(OUTPUT.encode() + "\r\n".encode())
            
            #Encerra a conexão
            print("Arquivo enviado")
            CONNECTION.close()

    #Caso o navegador requisite um arquivo que não esteja presente no servidor, ele deverá retornar uma mensagem de erro “404 Not Found”.
    except IOError:
        print("404 - Arquivo não encontrado.")

        #Retorna a mensagem de erro ao cliente
        HEADER = "HTTP/1.1 404 Not Found\r\n"
        CONNECTION.send(HEADER.encode() + "\r\n".encode())

        #Abre o arquivo de erro
        FILE = open("404.html", 'r')
        OUTPUT = FILE.read() #Transforma arquivo em string

        #Envia o arquivo de erro
        CONNECTION.send(OUTPUT.encode() + "\r\n".encode())

        #Encerra a conexão
        print("Mensagem de erro enviada")
        CONNECTION.close()

    #Linhas comentadas para aceitar mais de uma requisição
    #SOCKET.close()
    #sys.exit()
