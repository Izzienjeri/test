text = "  Hello World!  \n"

trimmed_text = text.strip()
print(trimmed_text)  # Output: "Hello World!"

left_trimmed_text = text.lstrip()
print(left_trimmed_text) # Output: "Hello World!  \n"

right_trimmed_text = text.rstrip()
print(right_trimmed_text) # Output: "  Hello World!"

text_with_chars = "---Hello---"
trimmed_chars = text_with_chars.strip("-")
print(trimmed_chars)  # Output: "Hello"