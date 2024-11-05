resposta = 0  # Inicializar com 0 para entrar no loop

while resposta != 5:
    print("\nEscolha uma das opções abaixo:")
    print("1 - Soma")
    print("2 - Subtração")
    print("3 - Multiplicação")
    print("4 - Divisão")
    print("5 - Sair")
    
    try:
        resposta = int(input("O que você deseja? "))
    except ValueError:
        print("Digite apenas números inteiros.")
        continue  # Retorna ao início do loop se houver erro
    
    if resposta == 1:
        print("Soma foi escolhida")
        try:
            num1 = float(input("Digite o primeiro número: "))
            num2 = float(input("Digite o segundo número: "))
            resultado = num1 + num2
        except ValueError:
            print("Digite apenas números válidos.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        else:
            print(f"O resultado foi de {resultado}")
    
    elif resposta == 2:
        print("Subtração foi escolhida")
        try:
            num1 = float(input("Digite o primeiro número: "))
            num2 = float(input("Digite o segundo número: "))
            resultado = num1 - num2
        except ValueError:
            print("Digite apenas números válidos.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        else:
            print(f"O resultado foi de {resultado}")
    
    elif resposta == 3:
        print("Multiplicação foi escolhida")
        try:
            num1 = float(input("Digite o primeiro número: "))
            num2 = float(input("Digite o segundo número: "))
            resultado = num1 * num2
        except ValueError:
            print("Digite apenas números válidos.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        else:
            print(f"O resultado foi de {resultado}")
    
    elif resposta == 4:
        print("Divisão foi escolhida")
        try:
            num1 = float(input("Digite o primeiro número: "))
            num2 = float(input("Digite o segundo número: "))
            resultado = num1 / num2
        except ZeroDivisionError:
            print("Não é possível fazer divisão por zero.")
        except ValueError:
            print("Digite apenas números válidos.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        else:
            print(f"O resultado foi de {resultado}")
    
    elif resposta == 5:
        print("Saindo...")
    
    else:
        print("Opção inválida. Tente novamente.")
        
print("Desconectado")
