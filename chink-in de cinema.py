# Escolha do cinema
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

    # Escolha do filme
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
                    # Escolha do dia
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

                    # Escolha do horário
                    if dia in [1, 2, 3, 4]:  # Adiciona a escolha de horários para todos os dias
                        dia_semana = ["Segunda", "Quarta", "Sexta", "Sábado"][dia - 1]
                        print(f"\n{dia_semana} foi selecionada")
                        print("1 - 13h")
                        print("2 - 15h")
                        print("3 - 17h")
                        print("4 - 19h")
                        print("0 - Voltar")
                        horario = int(input("Digite o horário em que você deseja assistir ou 0 para voltar: "))
                        
                        if horario == 0:
                            break
                        elif horario in [1, 2, 3, 4]:
                            hora = ["13h", "15h", "17h", "19h"][horario - 1]
                            print(f"Filme 'Sorria 2' selecionado para {dia_semana} às {hora}.")

                            # Escolha da forma de pagamento
                            while True:
                                print("\nEscolha a forma de pagamento:")
                                print("1 - Cartão de Crédito")
                                print("2 - Cartão de Débito")
                                print("3 - Pix")
                                print("4 - Dinheiro")
                                print("0 - Cancelar")
                                pagamento = int(input("Digite a opção de pagamento desejada ou 0 para cancelar: "))

                                if pagamento == 0:
                                    print("Pagamento cancelado.")
                                    break
                                elif pagamento in [1, 2, 3, 4]:
                                    forma_pagamento = ["Cartão de Crédito", "Cartão de Débito", "Pix", "Dinheiro"][pagamento - 1]
                                    print(f"Forma de pagamento '{forma_pagamento}' selecionada.")
                                    print("Processando pagamento...")
                                    print("Pagamento concluído com sucesso!")
                                    print(f"Filme 'Sorria 2' confirmado para {dia_semana} às {hora} no Cinepolis.\n")
                                    
                                    # Pergunta se deseja encerrar o programa
                                    encerrar = input("Deseja encerrar o programa? (s/n): ").strip().lower()
                                    if encerrar == 's':
                                        print("Encerrando o programa. Obrigado por usar nosso sistema!")
                                        exit()  # Encerra o programa completamente
                                    else:
                                        print("Voltando ao menu principal...\n")
                                        break

                            # Quebra o loop de horários e dias após o pagamento
                            if pagamento != 0:
                                break









    # elif cinema == 2:
    #     print("Cinemark escolhido com sucesso")

    #     print("Qual é o filme em que voce deseja assistir?")
    #     print("1 - SuperMan: A História De Christopher Reeve")
    #     print("2 - Perfekta: Uma Aventura da Escola de Gênios")
    #     print("3 - O Aprendiz")
    #     print("4 - A Garota da Vez")
    #     filme = int(input("Digite o código do filme que você deseja assitir: "))

    # elif cinema == 3:
    #     print("UCI escolhido com sucesso")

    #     print("Qual é o filme em que voce deseja assistir?")
    #     print("1 - Tudo Por Um Pop Star 2")
    #     print("2 - A Substância")
    #     print("3 - Zuzubalândia - O Filme")
    #     print("4 - Maximiliano Kolbe e Eu")
    #     filme = int(input("Digite o código do filme que você deseja assitir: "))
    # if cinema ==0: 
    #     break
    
    # else:
    #     print("Código invalido")


    # # escolha o dia e horario
    # # escolho a forma de pagamento