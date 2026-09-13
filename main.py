def main():
    height = 10

    while True:
        action = input("f to flap, Enter to fall: ")

        if action == "f":
            height = height + 3
        else:
            height = height - 2

        print("height:", height)

        if height <= 0:
            print("hit the ground, game over")
            break


if __name__ == "__main__":
    main()
