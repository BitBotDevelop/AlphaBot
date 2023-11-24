import os
import sys

sys.path.append(os.getcwd())

from common.inscribe import generate_random_private_key

random_private_key = generate_random_private_key()

print(random_private_key)