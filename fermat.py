import random
import math


def prime_test(N, k):
    # This is main function, that is connected to the Test button. You don't need to touch it.
    return fermat(N, k), miller_rabin(N, k)


def mod_exp(x, y, N):
    # base case: y == 0 (z^0 = 1 (mod N))
    if y == 0:
        return 1
    # recursively call this function, with y/2 (floored) as the new exponent
    z = mod_exp(x, math.floor(y / 2), N)
    # return (z^2 mod N) or (x*z^2 mod N) depending on whether y is even
    if y % 2 == 0:
        return pow(z, 2) % N  # z^2 mod N
    else:
        return (x * pow(z, 2)) % N  # x * z^2 mod N


def fprobability(k):
    # According to the lemma from the book, for at least half of 0 < a < N, a^(N-1) is not congruent to 1 (
    # mod N)
    # Thus, there is at most a 0.5^k probability that all k number of a's that you have chosen will pass the test
    # when N is actually composite
    return 1 - pow(0.5, k)


def mprobability(k):
    # According to the project description, for at least 3/4 of 0 < a < N, the Miller-Rabin test will tell you the
    # truth about a number being composite.
    # Thus, there is at most a 0.25^k probability that all k number of a's that you have chosen will pass the test
    # when the N is actually composite
    return 1 - pow(0.25, k)


def fermat(N, k):
    # run the primality test using Fermat's Little Theorem k times
    for i in range(k):
        a = random.randint(1, N - 1)  # get a random integer 0 < a < N
        # Find if a^(N-1) is congruent to 1 mod N
        if mod_exp(a, (N - 1), N) != 1:
            # if a^(N-1) is not congruent to 1 mod N, then we know that the number is prime
            return 'composite'
        # otherwise, we don't know whether it is prime
    return 'prime'


def miller_rabin(N, k):
    # first, check if N passes the primality test using Fermat's theorem
    ferm = fermat(N, k)
    # if N failed the test, then we know it is not prime
    if ferm == 'composite':
        return 'composite'

    # run the miller-rabing test k times
    for i in range(k):
        a = random.randint(1, N - 1)  # get a random integer 0 < a < N
        ex = N - 1  # the first exponent is N-1
        is_prime = True
        is_one = True  # to be used in exiting the while loop

        # take the a^(ex) mod N until it is not congruent to 1
        while is_one and ex != 0:
            mod = mod_exp(a, ex, N)  # a^(ex) mod N

            # if a^(ex) mod N is not congruent then we check what it is congruent to, then exit the test
            if mod != 1:
                is_one = False
                # if a^(ex) mod N is congruent to -1 (or N-1), then we know that the number is not prime
                if mod != N - 1:
                    is_prime = False

            ex = (ex / 2)  # divide the exponent by 2 (take the square root of a^ex
            # if the exponent is not divisible by two, then exit the test
            if not isinstance(ex, int):
                is_one = False

        # if the test failed, then return the N is composite
        if not is_prime:
            return 'composite'

    # If the test failed, then we return that it is prime, though we cannot say for certain that it is
    return 'prime'


def mod_exp_m(x, y, N):
    if y == 0:
        return 1, True
    z, is_prime = mod_exp_m(x, math.floor(y / 2), N)
    if z != 1:
        if z != (N - 1):
            return 0, False
        else:
            return 0, True
    elif not is_prime:
        return 0, False
    if y % 2 == 0:
        return pow(z, 2) % N, True
    else:
        return (x * pow(z, 2)) % N, True


###############################################################################
################################################################################
# Total: O(n^3)
def mod_exp(x, y, N):
    # O(n) (all of what is below)
    if y == 0:
        return 1  # c_1 + c_2
    z = mod_exp(x, math.floor(y / 2), N)  # O(n^2) + c_3
    if y % 2 == 0:  # c_1
        return pow(z, 2) % N  # O(n^2) + O(n^2) + c_2
    else:
        return (x * pow(z, 2)) % N  # O(n^2) + O(n^2) + O(n^2) + c_2

# Total: O(1)
def fprobability(k):
    return 1 - pow(0.5, k)

# Total: O(1)
def mprobability(k):
    return 1 - pow(0.25, k)

# Total: O(kn^3+c) = O(n3)
def fermat(N, k):
    # the for loop runs a max of k times
    for i in range(k):
        a = random.randint(1, N - 1)  # c_1
        if mod_exp(a, (N - 1), N) != 1:  # O(n^3)
            return 'composite'  # c_2
    return 'prime'  # c_2

# Total: O(n^4)
def miller_rabin(N, k):
    ferm = fermat(N, k)  # O(n^3)
    if ferm == 'composite':  # c
        return 'composite'  # c

    # runs a max of k times
    for i in range(k):
        a = random.randint(1, N - 1)  # c
        ex = N - 1  # c
        is_prime = True  # c
        is_one = True  # c

        # runs max of log N times
        while is_one and ex != 0:  # c
            mod = mod_exp(a, ex, N)  # O(n^3)
            if mod != 1:  # c
                is_one = False  # c
                if mod != N - 1:  # c
                    is_prime = False  # c

            ex = (ex / 2)  # c
            if not isinstance(ex, int):  # c
                is_one = False  # c

        if not is_prime:  # c
            return 'composite'  # c

    return 'prime'  # c
