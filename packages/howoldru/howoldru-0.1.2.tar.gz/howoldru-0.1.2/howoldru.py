import fire
import pendulum


def show_age(birthday):
    age = pendulum.parse(birthday).age
    print(f"あなたは現在{age}歳です。")

def main():
    fire.Fire(show_age)


if __name__ == "__main__":
    main()

