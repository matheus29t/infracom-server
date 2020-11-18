from socket import *
import sys

#Preparação do socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12345 #Número da porta
serverSocket.bind(('',serverPort)) #Ligando porta ao socket
serverSocket.listen() #Espera por resposta
print("O servidor MONSTRUOSO está pronto")

while True:
    connectionSocket, addr = serverSocket.accept() #Aceita requests
    print("Requisição aceita de (endereço, porta): %s" % (addr,))

    try:
        #Rebe mensagem e decodifica
        message = connectionSocket.recv(2048).decode()
        #Verifica se a mensagem está vazia
        if message != "":
            #Extrai o nome do arquivo que vem após o GET da mensagem
            filename = message.split()[1]
            #Abre o arquivo, ignorando a '/' que vem antes do nome do arquivo
            f = open(filename[1:], 'r')
            outputdata = f.read()

            print("File found.")
            #Informa que o arquivo foi encontrado
            headerLine = "HTTP/1.1 200 OK\r\n"
            connectionSocket.send(headerLine.encode())
            connectionSocket.send("\r\n".encode())

            #Envia o arquivo ao cliente
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())

            #Encerra a conexão
            print("Arquivo enviado")
            connectionSocket.close()

    except IOError:
        print("404 - Arquivo não encontrado.")

        #Retorna a mensagem de erro ao cliente
        errHeader = "HTTP/1.1 404 Not Found\r\n"
        connectionSocket.send(errHeader.encode())
        connectionSocket.send("\r\n".encode())

        #Abre a tela de erro no navegador
        ferr = open("404.html", 'r')
        outputerr = ferr.read()

        for i in range(0, len(outputerr)):
            connectionSocket.send(outputerr[i].encode())
        connectionSocket.send("\r\n".encode())

        # Terminates the connection
        print("Error message sent.")
        connectionSocket.close()

    #
    #serverSocket.close()
    #sys.exit()
