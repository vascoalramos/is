def menu():
    print("Available options:")
    print("(i) register new request")
    print("(c) cancel request")
    print("(s) check request status")
    print("(r) see request' report")
    print("(e) exit")
    return input("Option? ")


def main():
    print("\n\nBem vindo(a) à calculadora do IMC\n\n")

    while True:
        op = menu()
        if op == "e":
            print("\nEXIT\n")
            break

        elif op == "r":
            print("hello")

        else:
            print("Invalid option!\n")


if __name__ == "__main__":
    main()