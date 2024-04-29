import matplotlib.pyplot as plt
import requests
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import re

# MapReduce implementation
def map_function(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)

def reduce_function(counters):
    return sum(counters, Counter())

# Function to visualize top words
def visualize_top_words(word_freq, top_n=10):
    top_words = word_freq.most_common(top_n)
    words, frequencies = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, frequencies, color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Words')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Main function
def main(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()

        # Map step
        with ThreadPoolExecutor() as executor:
            chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
            counters = list(executor.map(map_function, chunks))

        # Reduce step
        total_counter = reduce_function(counters)

        # Visualize top words
        visualize_top_words(total_counter)

    else:
        print("Failed to retrieve data from URL")

if __name__ == "__main__":
    url = "https://djinni.co/my/dashboard/"  
    main(url)
