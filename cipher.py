def shift_character(char, start, end, shift):
    size = ord(end) - ord(start) + 1
    position = ord(char) - ord(start)
    new_position = (position + shift) % size
    return chr(ord(start) + new_position) 

#Encryption Function 
def encrypt_file(shift1: int, shift2: int,
                 input_path: str, output_path: str) -> None:

    with open(input_path, "r", encoding="utf-8") as file:
        text = file.read()

    encrypted_text = ""

    for char in text:

        # Lowercase a-n
        if "a" <= char <= "n":
            shift = shift1 * shift2
            encrypted_text += shift_character(char, "a", "n", shift)

        # Lowercase o-z
        elif "o" <= char <= "z":
            shift = -(shift1 + shift2)
            encrypted_text += shift_character(char, "o", "z", shift)

        #UPPERCASE A-M
        elif "A" <= char <= "M":
            shift = -shift1
            encrypted_text += shift_character(char, "A", "M", shift)

            #UOOERCASE N-Z
        elif "N" <= char <= "Z":
            shift = shift2 ** 2
            encrypted_text += shift_character(char, "N", "Z", shift)

        #Digits 0-9
        elif "0" <= char <= "9":
            shift = shift1 - shift2
            encrypted_text += shift_character(char, "0", "9", shift)

        #Everything else remains unchanged
        else:
            encrypted_text += char

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(encrypted_text)


#Decryption Function 
# Decryption Function

def decrypt_file(shift1: int, shift2: int,
                 input_path: str, output_path: str) -> None:

    with open(input_path, "r", encoding="utf-8") as file:
        text = file.read()

    decrypted_text = ""

    for char in text:

        # Lowercase a-n
        if "a" <= char <= "n":
            shift = -(shift1 * shift2)
            decrypted_text += shift_character(char, "a", "n", shift)

        # Lowercase o-z
        elif "o" <= char <= "z":
            shift = shift1 + shift2
            decrypted_text += shift_character(char, "o", "z", shift)

        # Uppercase A-M
        elif "A" <= char <= "M":
            shift = shift1
            decrypted_text += shift_character(char, "A", "M", shift)

        # Uppercase N-Z
        elif "N" <= char <= "Z":
            shift = -(shift2 ** 2)
            decrypted_text += shift_character(char, "N", "Z", shift)

        # Digits 0-9
        elif "0" <= char <= "9":
            shift = -(shift1 - shift2)
            decrypted_text += shift_character(char, "0", "9", shift)

        # Everything else remains unchanged
        else:
            decrypted_text += char

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(decrypted_text)

#Verification Function
def verify_files(original_path: str, decrypted_path: str) -> bool:

    with open(original_path, "r", encoding="utf-8") as file:
        original = file.read()

    with open(decrypted_path, "r", encoding="utf-8") as file:
        decrypted = file.read()

    if original == decrypted:
        print("Decryption successful.")
        return True
    else:
        print("Decryption unsuccessful.")
        return False

#Run the whole program
def main():

    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    if shift1 < 0 or shift2 < 0:
        print("shift1 and shift2 must be non-negative integers.")
        return

    encrypt_file(
        shift1,
        shift2,
        "raw_text.txt",
        "encrypted_text.txt"
    )

    decrypt_file(
        shift1,
        shift2,
        "encrypted_text.txt",
        "decrypted_text.txt"
    )

    verify_files(
        "raw_text.txt",
        "decrypted_text.txt"
    )


if __name__ == "__main__":
    main()