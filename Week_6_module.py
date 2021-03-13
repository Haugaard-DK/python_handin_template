import requests
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

class TextComparer():
    def __init__(self, url_list = []):
        self.url_list = url_list
        self.filenames = []

    def download(self, url, filename):
        response = requests.get(url)
        
        if response.ok:
            with open(filename, 'wb') as fd:
                self.filenames.append(filename)
                for chunk in response.iter_content(chunk_size=1024):
                    fd.write(chunk)
                    
        elif response.status_code == 404:
            raise NotFoundException(f'Statuse code: {response.status_code} , Please try again')

    def multi_download(self, workers = 5):
        with ThreadPoolExecutor(workers) as ex:
            for i in range(0, len(self.url_list)):
                print("Downloading book: " + str(i+1))
                self.download(self.url_list[i], 'book' + str(i+1) + ".txt")


    def __iter__(self):
        self.n = 0
        return self
    
    def __next__(self):
        index = self.n
        if index != len(self.filenames):
            self.n += 1
            return self.filenames[index]
        else:
            raise StopIteration

    def urllist_generator(self):
        for url in self.url_list:
            yield url

    def avg_vowels(self, text):
        vowel_list = ["A", "E", "I", "O", "U", "Y"]

        with open(text) as file:
            read_file = file.read()

        words_in_file = read_file.split()
        word_count = len(words_in_file)
        vowel_amount = 0

        for word in words_in_file:
            for char in word:
                if char.upper() in vowel_list:
                    vowel_amount += 1
        
        vowel_average = round(vowel_amount / word_count, 2)
        return vowel_average, text

    def hardest_read(self):
        workers = multiprocessing.cpu_count()

        with ProcessPoolExecutor(workers) as ex:
            results = ex.map(self.avg_vowels, self.filenames)

        hardest_book = None

        for result in results:
            if hardest_book is None or hardest_book[0] < result[0]:
                hardest_book = result

        return self.avg_vowels(hardest_book[1])


class NotFoundException(Exception):
    pass