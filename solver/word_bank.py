"""Word Bank - Loads all 5-letter words"""

import os
import urllib.request
from typing import Set
from collections import Counter


class WordBank:
    def __init__(self):
        self.all_words: Set[str] = set()
        self.letter_freq = {}
        
        self.load_words()
        self.calculate_frequencies()
    
    def load_words(self):
        """Load word lists"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        answers_file = os.path.join(data_dir, 'wordle_answers.txt')
        guesses_file = os.path.join(data_dir, 'valid_guesses.txt')
        
        # Download if needed
        if not os.path.exists(answers_file) or not os.path.exists(guesses_file):
            print("📥 Downloading word lists...")
            self._download_words(answers_file, guesses_file)
        
        # Load words
        try:
            with open(answers_file, 'r') as f:
                answers = {w.strip().lower() for w in f if len(w.strip()) == 5}
            
            with open(guesses_file, 'r') as f:
                guesses = {w.strip().lower() for w in f if len(w.strip()) == 5}
            
            self.all_words = answers.union(guesses)
            print(f"✅ Loaded {len(self.all_words):,} words")
        except:
            print("⚠ Using fallback word list")
            self.all_words = self._get_fallback_words()
    
    def _download_words(self, answers_file, guesses_file):
        """Download official Wordle word lists"""
        try:
            # Answers
            url1 = "https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/wordle-answers-alphabetical.txt"
            urllib.request.urlretrieve(url1, answers_file)
            
            # Guesses
            url2 = "https://gist.githubusercontent.com/cfreshman/cdcdf777450c5b5301e439061d29694c/raw/wordle-allowed-guesses.txt"
            urllib.request.urlretrieve(url2, guesses_file)
            
            print("✅ Downloaded word lists!")
        except:
            print("⚠ Download failed, using fallback")
    
    def _get_fallback_words(self) -> Set[str]:
        """Backup word list if download fails"""
        return {
            "soare", "roate", "raise", "raile", "slate", "sauce", "slice", "shale",
            "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult",
            "after", "again", "agent", "agree", "ahead", "alarm", "album", "alert",
            "alien", "align", "alike", "alive", "allow", "alone", "along", "alter",
            "angel", "anger", "angle", "angry", "apart", "apple", "apply", "arena",
            "argue", "arise", "array", "arrow", "aside", "asset", "audio", "audit",
            "avoid", "award", "aware", "badly", "baker", "bases", "basic", "basis",
            "beach", "began", "begin", "being", "below", "bench", "billy", "birth",
            "black", "blame", "blind", "block", "blood", "board", "boost", "booth",
            "bound", "brain", "brand", "bread", "break", "breed", "brief", "bring",
            "broad", "broke", "brown", "build", "built", "buyer", "cable", "calif",
            "carry", "catch", "cause", "chain", "chair", "chart", "chase", "cheap",
            "check", "chest", "chief", "child", "china", "chose", "civil", "claim",
            "class", "clean", "clear", "click", "clock", "close", "coach", "coast",
            "could", "count", "court", "cover", "craft", "crash", "crazy", "cream",
            "crime", "cross", "crowd", "crown", "crude", "curve", "cycle", "daily",
            "dance", "dated", "dealt", "death", "debut", "delay", "depth", "doing",
            "doubt", "dozen", "draft", "drama", "drank", "drawn", "dream", "dress",
            "drill", "drink", "drive", "drove", "dying", "eager", "early", "earth"
        }
    
    def calculate_frequencies(self):
        """Calculate letter frequencies"""
        counter = Counter()
        for word in self.all_words:
            for letter in set(word):
                counter[letter] += 1
        
        total = len(self.all_words)
        self.letter_freq = {letter: count/total for letter, count in counter.items()}
    
    def is_valid(self, word: str) -> bool:
        """Check if word is valid"""
        return word.lower() in self.all_words
    
    def get_word_score(self, word: str) -> float:
        """Score word by letter frequency"""
        unique = set(word.lower())
        return sum(self.letter_freq.get(letter, 0) for letter in unique)
