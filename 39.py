def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):  
        if n % i == 0:
            return False
    return True

def filter_prime(numbers):
    return [n for n in numbers if is_prime(n)]



nums = list(map(int, input("Введите числа через пробел: ").split()))
primes = filter_prime(nums)
print("Простые числа:", primes)
