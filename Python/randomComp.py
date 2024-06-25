import random
import time
import matplotlib.pyplot as plt
import numpy as np

try:
    import sympy
except ImportError:
    import os
    os.system('pip install sympy')
    import sympy

def generate_large_prime(bits):
    while True:
        prime_candidate = random.getrandbits(bits)
        if prime_candidate % 4 == 3 and sympy.isprime(prime_candidate):
            return prime_candidate

def blum_blum_shub(bits, num_bits):
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    n = p * q

    x = random.randint(2, n - 2)

    random_bits = []
    for _ in range(num_bits):
        x = (x * x) % n
        random_bits.append(x & 1)

    random_number = int(''.join(map(str, random_bits)), 2)
    return random_number

def mersenne_twister(num_bits):
    return random.getrandbits(num_bits)

def compare_generators(bits, num_bits, num_samples):
    bbs_times = []
    mt_times = []

    bbs_numbers = []
    mt_numbers = []

    for i in range(num_samples):
        start_time = time.time()
        bbs_number = blum_blum_shub(bits, num_bits)
        bbs_times.append(time.time() - start_time)
        bbs_numbers.append(bbs_number)

        start_time = time.time()
        mt_number = mersenne_twister(num_bits)
        mt_times.append(time.time() - start_time)
        mt_numbers.append(mt_number)

        # Debugging prints
        if i < 5:  # Print the first few numbers for inspection
            print(f"BBS {i}: {bbs_number}")
            print(f"MT {i}: {mt_number}")

    return bbs_times, mt_times, bbs_numbers, mt_numbers

def plot_results(bbs_times, mt_times, bbs_numbers, mt_numbers):
    # Ensure the numbers are cast to int if needed
    bbs_numbers = list(map(int, bbs_numbers))
    mt_numbers = list(map(int, mt_numbers))

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # Plot generation times
    axs[0, 0].boxplot([bbs_times, mt_times], labels=['BBS', 'MT19937'])
    axs[0, 0].set_title('Generation Time Comparison')
    axs[0, 0].set_ylabel('Time (s)')

    # Plot histograms
    axs[0, 1].hist(bbs_numbers, bins=50, alpha=0.7, label='BBS')
    axs[0, 1].hist(mt_numbers, bins=50, alpha=0.7, label='MT19937')
    axs[0, 1].set_title('Random Number Distribution')
    axs[0, 1].legend(loc='upper right')

    # Plot statistical properties
    bbs_mean = np.mean(bbs_numbers)
    bbs_std = np.std(bbs_numbers)
    mt_mean = np.mean(mt_numbers)
    mt_std = np.std(mt_numbers)

    axs[1, 0].bar(['BBS Mean', 'MT19937 Mean'], [bbs_mean, mt_mean], color=['blue', 'orange'])
    axs[1, 0].set_title('Mean Comparison')

    axs[1, 1].bar(['BBS Std', 'MT19937 Std'], [bbs_std, mt_std], color=['blue', 'orange'])
    axs[1, 1].set_title('Standard Deviation Comparison')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    bits = 512  # Number of bits for prime numbers in BBS
    num_bits = 256  # Number of random bits to generate
    num_samples = 100  # Number of samples to generate for comparison

    # Seed the random number generator
    random.seed()

    bbs_times, mt_times, bbs_numbers, mt_numbers = compare_generators(bits, num_bits, num_samples)
    plot_results(bbs_times, mt_times, bbs_numbers, mt_numbers)
