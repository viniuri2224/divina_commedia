import os
import json


class CantoNotFoundError(Exception):
    def __init__(self):
        super().__init__("canto_number must be between 1 and 34")


class Virgilio:
    def __init__(self, directory: str):
        self.directory = directory

    def read_canto_lines(self, canto_number: int, strip_lines: bool = False, num_lines: int = None) -> list:
        try:
            if type(canto_number) is not int:
                raise TypeError("canto_number must be an integer")
            elif canto_number <= 0 or canto_number > 34:
                raise CantoNotFoundError
            else:
                file_path = os.path.join(self.directory, f"Canto_{canto_number}.txt")
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        file_rows = file.readlines()
                except Exception:
                    return f"error while opening {file_path}"
                if strip_lines:
                    file_rows_stripped = []
                    for rows in file_rows:
                        file_rows_stripped.append(rows.strip())
                    return file_rows_stripped
                elif num_lines:
                    file_limited_rows = []
                    for row in file_rows[:num_lines]:
                        file_limited_rows.append(row)
                    return file_limited_rows
                else:
                    return file_rows
        except TypeError as e:
            return print(f"{e}")
        except CantoNotFoundError as e:
            return print(f"{e}")
        except Exception as e:
            return print(F"{e}")

    def canto_verses(self, canto_number: int) -> int:
        file_rows = self.read_canto_lines(canto_number)
        return len(file_rows)

    def count_tercets(self, canto_number: int) -> int:
        canto_verses = self.canto_verses(canto_number)
        if canto_verses % 3 == 0:
            return canto_verses / 3
        else:
            return canto_verses // 3

    def count_word(self, canto_number: int, word: str) -> int:
        number_of_words = 0
        file_rows = self.read_canto_lines(canto_number)
        for row in file_rows:
            number_of_words += row.count(word)
        return number_of_words

    def get_verse_with_word(self, canto_number: int, word: str) -> str:
        file_rows = self.read_canto_lines(canto_number)
        for row in file_rows:
            if row.count(word) > 0:
                return row

    def get_verses_with_word(self, canto_number: int, word: str) -> list:
        all_verses = []
        file_rows = self.read_canto_lines(canto_number)
        for row in file_rows:
            if row.count(word) > 0:
                all_verses.append(row)
        return all_verses

    def get_longest_verse(self, canto_number: int) -> str:
        file_rows = self.read_canto_lines(canto_number)
        longest_row = file_rows[0].strip()
        max_length = len(file_rows[0].strip())
        for row in file_rows[1:]:
            length = len(row.strip())
            if (length > max_length):
                longest_row = row.strip()
                max_length = length
        return longest_row

    def get_longest_canto(self) -> dict:
        longest_canto = {
            "canto_number": 0,
            "canto_len": 0,
        }
        files = os.listdir(self.directory)
        canto_number = self.get_canto_number(files[0])
        rows_number = self.canto_verses(canto_number)
        for file in files[1:]:
            next_canto_number = self.get_canto_number(file)
            next_rows_number = self.canto_verses(next_canto_number)
            if next_rows_number > rows_number:
                canto_number = next_canto_number
                rows_number = next_rows_number
        longest_canto["canto_number"] = canto_number
        longest_canto["canto_len"] = rows_number
        return longest_canto

    def get_canto_number(self, file_name: str) -> int:
        '''
        Recupera il numero del canto del file

        Args:
            file_name: è il nome del file
        Returns:
            int: il numero del canto del file
        Esempio:
            Canto_33.txt
            Ritorna 33
        '''
        if (len(file_name) == 11):
            return int(file_name[6:7])
        else:
            return int(file_name[6:8])

    def count_words(self, canto_number: int, words: str) -> dict:
        words_found = {}
        for word in words:
            number_of_words = self.count_word(canto_number, word)
            words_found[word] = number_of_words
        with open(os.path.join(self.directory, "words.json"), "w") as file:
            json.dump(words_found, file)
        return words_found

    def get_hell_verses(self) -> list:
        hell = []
        files = os.listdir(self.directory)
        for file in files:
            canto_number = self.get_canto_number(file)
            file_rows = self.read_canto_lines(canto_number)
            for row in file_rows:
                hell.append(row.strip())
        return hell

    def count_hell_verses(self) -> int:
        hell = self.get_hell_verses()
        return len(hell)

    def get_hell_verse_mean_len(self) -> float:
        files = os.listdir(self.directory)
        hell_verses = self.count_hell_verses()
        return float(hell_verses/len(files))
