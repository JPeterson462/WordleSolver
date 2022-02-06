class WordleSolver:
    # words: list<string>
    # match_pattern: list<tuple<string, bool>>
    # excluded_letters: list<string>
    # running: bool

    def load_words(self):
        with open('words.txt', 'r') as f:
            contents = f.read()
            words = contents.split('\n')
            for idx in range(len(words)):
                words[idx] = words[idx].strip()
            self.words = words
        # add scrabble letter distributions for scoring words
        self.distributions = [9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,6,4,2,2,1,2,1]

    def prompt_for_pattern(self):
        known_letters = input("Enter the known letters: ")
        excluded_letters = input("Enter the excluded letters: ")
        match_pattern = []
        for letter in known_letters.split(" "):
            letter = letter.strip()
            if len(letter) == 0:
                continue
            is_blank = letter == '_'
            is_wrong_spot = len(letter) > 1 and letter[1] == '?'
            match = (letter[0], is_wrong_spot, is_blank)
            match_pattern.append(match)
        self.match_pattern = match_pattern
        self.excluded_letters = list(excluded_letters)

    def score_word(self, word):
        letters = list(word)
        score = 0
        for letter in letters:
            score += self.distributions[ord(letter.lower()) - ord('a')]
        return score

    def find_matches(self):
        matches = []
        for word in self.words:
            if len(word) < 5:
                continue
            # Skip any words with a known missing letter
            is_excluded = False
            for excluded in self.excluded_letters:
                if excluded in word:
                    is_excluded = True
                    break
            if is_excluded:
                continue
            # Skip any words that don't have the known letters
            idx = 0
            letters = list(word)
            for cell in self.match_pattern:
                if not cell[2] and not cell[1]:
                    if letters[idx] != cell[0]:
                        is_excluded = True
                        break
                idx += 1
            if is_excluded:
                continue
            # Skip any words that don't contain a wrong spot letter
            idx = 0
            for cell in self.match_pattern:
                if not cell[2] and cell[1]:
                    if not cell[0] in word:
                        is_excluded = True
                        break
                    if letters[idx] == cell[0]:
                        # if it's in the wrong spot then word[idx] can't be that letter
                        is_excluded = True
                        break
                idx += 1
            if is_excluded:
                continue
            matches.append(word)
        print('== POSSIBLE WORDS ==')
        matches.sort(key=lambda val: self.score_word(val))
        matches.reverse()
        print(matches)

    def run(self):
        self.running = True
        self.load_words()
        while self.running:
            self.prompt_for_pattern()
            self.find_matches()
            print('')

if __name__ == '__main__':
    solver = WordleSolver()
    solver.run()
