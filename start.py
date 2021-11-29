# Print prime numbers to 10
def is_prime(n):
    if n == 1:
        return False
    for x in range(2, n):
        if n % x == 0:
            return False
    else:
        return True

for n in range(1, 11):
    if is_prime(n):
        print(n)