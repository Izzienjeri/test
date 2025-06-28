import re

original_string = "The quick brown fox jumps over the lazy dog."
new_string = re.sub(r"the", "a", original_string, flags=re.IGNORECASE)
print(new_string)