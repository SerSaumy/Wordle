"""Wordle Solver Engine"""

from typing import List, Dict, Set
from collections import defaultdict
import random


class WordleSolver:
    def __init__(self, word_bank):
        self.word_bank = word_bank
        self.possible_words = set(word_bank.all_words)
        self.constraints = {
            'green': {},
            'yellow': set(),
            'gray': set(),
            'yellow_not': defaultdict(set)
        }
    
    def reset(self):
        """Reset solver"""
        self.possible_words = set(self.word_bank.all_words)
        self.constraints = {
            'green': {},
            'yellow': set(),
            'gray': set(),
            'yellow_not': defaultdict(set)
        }
    
    def process_feedback(self, guess: str, feedback: List[Dict]):
        """
        Process Wordle feedback
        feedback = [
            {'letter': 'a', 'status': 'correct/present/absent', 'position': 0},
            ...
        ]
        """
        guess = guess.lower()
        
        for fb in feedback:
            letter = fb['letter'].lower()
            status = fb['status']
            position = fb['position']
            
            if status == 'correct':
                self.constraints['green'][position] = letter
            elif status == 'present':
                self.constraints['yellow'].add(letter)
                self.constraints['yellow_not'][letter].add(position)
            elif status == 'absent':
                if letter not in self.constraints['yellow']:
                    self.constraints['gray'].add(letter)
        
        self.filter_possible_words()
    
    def filter_possible_words(self):
        """Filter words matching constraints"""
        filtered = set()
        
        for word in self.possible_words:
            if self.matches_constraints(word):
                filtered.add(word)
        
        self.possible_words = filtered
    
    def matches_constraints(self, word: str) -> bool:
        """Check if word matches all constraints"""
        word = word.lower()
        
        # Green letters
        for pos, letter in self.constraints['green'].items():
            if word[pos] != letter:
                return False
        
        # Yellow letters
        for letter in self.constraints['yellow']:
            if letter not in word:
                return False
            for wrong_pos in self.constraints['yellow_not'][letter]:
                if word[wrong_pos] == letter:
                    return False
        
        # Gray letters
        for letter in self.constraints['gray']:
            if letter in word:
                return False
        
        return True
    
    def get_best_guess(self):
        """Get best next guess"""
        if not self.possible_words:
            return None, 0
        
        if len(self.possible_words) == 1:
            return list(self.possible_words)[0], 1
        
        # First guess - use optimal starters
        best_starters = ['soare', 'roate', 'raise', 'slate', 'crane', 'stare']
        if len(self.constraints['green']) == 0 and len(self.constraints['yellow']) == 0:
            for starter in best_starters:
                if starter in self.word_bank.all_words:
                    return starter, len(self.possible_words)
        
        # Pick from possible words
        words_list = list(self.possible_words)
        if len(words_list) > 20:
            sample = random.sample(words_list, 20)
            best = max(sample, key=self.word_bank.get_word_score)
        else:
            best = max(words_list, key=self.word_bank.get_word_score)
        
        return best, len(self.possible_words)
    
    def get_possible_words(self) -> List[str]:
        """Get remaining possible words"""
        return sorted(list(self.possible_words))
