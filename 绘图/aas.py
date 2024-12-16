import os


def check_digits_in_files(directory):
    digits_found = set()

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                for line in file:
                    if line and line[0].isdigit():
                        digits_found.add(line[0])
                    if len(digits_found) == 10:
                        break
    return digits_found


directory_path = r'E:\yyj_file\datasets\SODA-A-1024\labels\train'
found_digits = check_digits_in_files(directory_path)

if len(found_digits) == 10:
    print("All digits from 0 to 9 were found.")
else:
    print(f"Not all digits were found. Digits found: {sorted(found_digits)}")
