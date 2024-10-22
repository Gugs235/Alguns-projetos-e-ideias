# escolho o cinema
while True:
    print("Cinemas em Campo Grande")
    print("1 - Cinepolis")
    print("2 - Cinemark")
    print("3 - UCI")
    cinema = int(input("Digite o código do cinema em que você deseja assitir: "))

    # escolho o filme
    if cinema == 1:
        while True:
            print("Cinepolis escolhido com sucesso")
            print("Qual é o filme em que voce deseja assistir?")
            print("1 - Sorria 2")
            print("2 - Robô Selvagem")
            print("3 - Coringa: Delírio a Dois")
            print("4 - A Forja")
            filme = int(input("Digite o código do filme que você deseja assitir: "))
            if filme ==0:
                break
            elif filme ==1:
                while True:
                    print("Sorria 2")
                    print("Qual horário deseja assistir?")
                    print("1 - 13h")
                    print("2 - 15h")
                    print("3 - 17h")
                    print("4 - 19h")
                    horario = int(input("Digite o horário do filme que você deseja assitir: "))
                    if horario == 1:
                        print("13h")
                    elif horario == 0:
                        break






    elif cinema == 2:
        print("Cinemark escolhido com sucesso")

        print("Qual é o filme em que voce deseja assistir?")
        print("1 - SuperMan: A História De Christopher Reeve")
        print("2 - Perfekta: Uma Aventura da Escola de Gênios")
        print("3 - O Aprendiz")
        print("4 - A Garota da Vez")
        filme = int(input("Digite o código do filme que você deseja assitir: "))

    elif cinema == 3:
        print("UCI escolhido com sucesso")

        print("Qual é o filme em que voce deseja assistir?")
        print("1 - Tudo Por Um Pop Star 2")
        print("2 - A Substância")
        print("3 - Zuzubalândia - O Filme")
        print("4 - Maximiliano Kolbe e Eu")
        filme = int(input("Digite o código do filme que você deseja assitir: "))
    if cinema ==0: 
        break
    
    else:
        print("Código invalido")


    # escolho o dia e horaio
    # escolho a forma de pagamento