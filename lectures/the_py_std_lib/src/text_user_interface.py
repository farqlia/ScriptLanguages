from prompt_toolkit.shortcuts import button_dialog, input_dialog


def greet():
    name = input_dialog(
        title='Enter name',
        text='Hello, What is your name?'
    ).run()

    button_dialog(
        title='Hello',
        text=f'Hello {name}',
        buttons=[('OK', None)]
    ).run()


if __name__ == '__main__':
    greet()