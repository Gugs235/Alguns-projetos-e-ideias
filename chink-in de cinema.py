# escolho o cinema
while True:
    print("Cinemas em Campo Grande")
    print("1 - Cinepolis")
    print("2 - Cinemark")
    print("3 - UCI")
    print("0 - Sair")
    cinema = int(input("Digite o código do cinema em que você deseja assistir ou 0 para sair: "))

    # Condição de saída do loop principal
    if cinema == 0:
        print("Encerrando o programa.")
        break

    # escolho o filme
    if cinema == 1:
        while True:
            print("\nCinepolis escolhido com sucesso")
            print("Qual é o filme em que você deseja assistir?")
            print("1 - Sorria 2")
            print("2 - Robô Selvagem")
            print("3 - Coringa: Delírio a Dois")
            print("4 - A Forja")
            print("0 - Voltar")
            filme = int(input("Digite o código do filme que você deseja assistir ou 0 para voltar: "))
            
            if filme == 0:
                break

            elif filme == 1:
                while True:
                    # escolha o dia
                    print("\nSorria 2 foi selecionado")
                    print("Qual dia deseja assistir?")
                    print("1 - segunda")
                    print("2 - quarta")
                    print("3 - sexta")
                    print("4 - sábado")
                    print("0 - Voltar")
                    dia = int(input("Digite o dia em que você deseja assistir ou 0 para voltar: "))
                    
                    if dia == 0:
                        break

                    # escolha o horário
                    if dia == 1:
                        print("\nSegunda foi selecionada")
                        print("1 - 13h")
                        print("2 - 15h")
                        print("3 - 17h")
                        print("4 - 19h")
                        print("0 - Voltar")
                        horario = int(input("Digite o horário em que você deseja assistir ou 0 para voltar: "))
                        
                        if horario == 0:
                            break
                        else:
                            print(f"Filme 'Sorria 2' selecionado para segunda-feira às {horario}h.")
                            # Aqui, adicione qualquer ação que o programa faça após a seleção completa.







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


    # escolha o dia e horario
    # escolho a forma de pagamento