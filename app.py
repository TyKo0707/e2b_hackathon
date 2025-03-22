def input_action():
    s = input('Choose your action: \n1. Animate your slides.\n2. Terminate the program.\nYour choice: ')

    while s not in ['1', '2']:
        s = input('Invalid input. Please enter 1 or 2: ')

    return s


action = input_action()
while int(action) == 1:
    pdf_path = input('Enter the path to your PDF file: ')
    output_dir = input('Enter the path to the directory where you want to save the video files: ')
    action = input_action()
