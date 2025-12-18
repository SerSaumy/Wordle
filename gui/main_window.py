"""Wordle Solver - Final Version with Tab Autocomplete"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from solver.word_bank import WordBank
from solver.solver_engine import WordleSolver


class WordleSolverGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wordle Solver")
        self.root.geometry("1600x900")
        
        # Beautiful colors
        self.colors = {
            'bg': '#FAFBFC',
            'white': '#FFFFFF',
            'border': '#E8EAED',
            'primary': '#6366F1',
            'primary_hover': '#4F46E5',
            'success': '#10B981',
            'warning': '#F59E0B',
            'gray': '#9CA3AF',
            'text': '#1F2937',
            'text_light': '#6B7280',
            'text_lighter': '#9CA3AF',
            'input_bg': '#F9FAFB',
            'danger': '#EF4444',
            'hint': '#D1D5DB'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        print("✨ Initializing Wordle Solver...")
        self.word_bank = WordBank()
        self.solver = WordleSolver(self.word_bank)
        self.attempts = []
        
        self.create_ui()
        print("✅ Ready!")
    
    def create_ui(self):
        """Create scrollable UI"""
        
        # TOP BAR
        top = tk.Frame(self.root, bg=self.colors['white'], height=90)
        top.pack(fill='x', side='top')
        top.pack_propagate(False)
        
        border = tk.Frame(top, bg=self.colors['border'], height=1)
        border.pack(side='bottom', fill='x')
        
        top_content = tk.Frame(top, bg=self.colors['white'])
        top_content.pack(expand=True)
        
        logo_frame = tk.Frame(top_content, bg=self.colors['white'])
        logo_frame.pack(side='left', padx=50)
        
        tk.Label(
            logo_frame,
            text="Wordle",
            font=('Segoe UI', 28, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(side='left')
        
        tk.Label(
            logo_frame,
            text=" Solver",
            font=('Segoe UI', 28),
            bg=self.colors['white'],
            fg=self.colors['text_light']
        ).pack(side='left')
        
        stats_header = tk.Frame(top_content, bg=self.colors['white'])
        stats_header.pack(side='right', padx=50)
        
        self.header_stat = tk.Label(
            stats_header,
            text=f"{len(self.word_bank.all_words):,} words loaded",
            font=('Segoe UI', 11),
            bg=self.colors['white'],
            fg=self.colors['text_lighter']
        )
        self.header_stat.pack()
        
        # SCROLLABLE MAIN AREA
        canvas_frame = tk.Frame(self.root, bg=self.colors['bg'])
        canvas_frame.pack(fill='both', expand=True, side='top')
        
        self.canvas = tk.Canvas(canvas_frame, bg=self.colors['bg'], highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(canvas_frame, orient='vertical', command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg'])
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        
        self.scrollable_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # CONTENT
        container = tk.Frame(self.scrollable_frame, bg=self.colors['bg'])
        container.pack(fill='both', expand=True, padx=50, pady=30)
        
        # LEFT COLUMN
        left = tk.Frame(container, bg=self.colors['bg'])
        left.pack(side='left', fill='both', expand=True, padx=(0, 25))
        
        # Input Card
        input_card = tk.Frame(left, bg=self.colors['white'])
        input_card.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            input_card,
            text="Enter Your Guess",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=30, pady=(25, 5))
        
        tk.Label(
            input_card,
            text="Type the word you guessed in Wordle",
            font=('Segoe UI', 12),
            bg=self.colors['white'],
            fg=self.colors['text_light']
        ).pack(anchor='w', padx=30, pady=(0, 20))
        
        # Word input with placeholder
        word_container = tk.Frame(input_card, bg=self.colors['white'])
        word_container.pack(fill='x', padx=30, pady=(0, 10))
        
        self.word_entry = tk.Entry(
            word_container,
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            relief='flat',
            bd=0,
            insertbackground=self.colors['primary']
        )
        self.word_entry.pack(fill='x', ipady=15, ipadx=20)
        
        # Bind Tab and Enter
        self.word_entry.bind('<Return>', self.on_word_enter)
        self.word_entry.bind('<Tab>', self.on_word_tab)
        
        # Keyboard hints
        hints_frame = tk.Frame(input_card, bg=self.colors['white'])
        hints_frame.pack(fill='x', padx=30, pady=(5, 20))
        
        tk.Label(
            hints_frame,
            text="⌨ ",
            font=('Segoe UI', 10),
            bg=self.colors['white'],
            fg=self.colors['hint']
        ).pack(side='left')
        
        tk.Label(
            hints_frame,
            text="Tab",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['hint'],
            fg='white',
            padx=6,
            pady=2
        ).pack(side='left', padx=(0, 5))
        
        tk.Label(
            hints_frame,
            text="= use suggestion  •  ",
            font=('Segoe UI', 10),
            bg=self.colors['white'],
            fg=self.colors['text_lighter']
        ).pack(side='left')
        
        tk.Label(
            hints_frame,
            text="Enter",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['hint'],
            fg='white',
            padx=6,
            pady=2
        ).pack(side='left', padx=(0, 5))
        
        tk.Label(
            hints_frame,
            text="= use typed word",
            font=('Segoe UI', 10),
            bg=self.colors['white'],
            fg=self.colors['text_lighter']
        ).pack(side='left')
        
        # Feedback section
        tk.Label(
            input_card,
            text="Enter Feedback Pattern",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=30, pady=(10, 5))
        
        tk.Label(
            input_card,
            text="Use: G (Green), Y (Yellow), B (Black/Gray)",
            font=('Segoe UI', 12),
            bg=self.colors['white'],
            fg=self.colors['text_light']
        ).pack(anchor='w', padx=30, pady=(0, 5))
        
        example_frame = tk.Frame(input_card, bg='#F0F9FF')
        example_frame.pack(fill='x', padx=30, pady=(5, 20))
        
        tk.Label(
            example_frame,
            text='💡 Example: "GYBBB" = Green, Yellow, Black, Black, Black',
            font=('Segoe UI', 11),
            bg='#F0F9FF',
            fg='#1E40AF'
        ).pack(anchor='w', padx=15, pady=10)
        
        feedback_container = tk.Frame(input_card, bg=self.colors['white'])
        feedback_container.pack(fill='x', padx=30, pady=(0, 10))
        
        self.feedback_entry = tk.Entry(
            feedback_container,
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            relief='flat',
            bd=0,
            insertbackground=self.colors['primary']
        )
        self.feedback_entry.pack(fill='x', ipady=15, ipadx=20)
        self.feedback_entry.bind('<Return>', lambda e: self.process())
        
        # Feedback hint
        feedback_hint = tk.Frame(input_card, bg=self.colors['white'])
        feedback_hint.pack(fill='x', padx=30, pady=(5, 25))
        
        tk.Label(
            feedback_hint,
            text="⌨ ",
            font=('Segoe UI', 10),
            bg=self.colors['white'],
            fg=self.colors['hint']
        ).pack(side='left')
        
        tk.Label(
            feedback_hint,
            text="Enter",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['hint'],
            fg='white',
            padx=6,
            pady=2
        ).pack(side='left', padx=(0, 5))
        
        tk.Label(
            feedback_hint,
            text="= analyze guess",
            font=('Segoe UI', 10),
            bg=self.colors['white'],
            fg=self.colors['text_lighter']
        ).pack(side='left')
        
        # Buttons
        buttons_row = tk.Frame(input_card, bg=self.colors['white'])
        buttons_row.pack(fill='x', padx=30, pady=(15, 30))
        
        self.submit_btn = tk.Button(
            buttons_row,
            text="✓ Analyze Guess",
            font=('Segoe UI', 15, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_hover'],
            activeforeground='white',
            command=self.process,
            cursor='hand2',
            relief='flat',
            bd=0
        )
        self.submit_btn.pack(side='left', fill='x', expand=True, ipady=14, padx=(0, 10))
        
        self.submit_btn.bind('<Enter>', lambda e: self.submit_btn.config(bg=self.colors['primary_hover']))
        self.submit_btn.bind('<Leave>', lambda e: self.submit_btn.config(bg=self.colors['primary']))
        
        self.undo_btn = tk.Button(
            buttons_row,
            text="↶ Undo Last",
            font=('Segoe UI', 15, 'bold'),
            bg=self.colors['danger'],
            fg='white',
            activebackground='#DC2626',
            activeforeground='white',
            command=self.undo_last,
            cursor='hand2',
            relief='flat',
            bd=0,
            state='disabled'
        )
        self.undo_btn.pack(side='right', fill='x', expand=True, ipady=14, padx=(10, 0))
        
        self.undo_btn.bind('<Enter>', lambda e: self.undo_btn.config(bg='#DC2626') if self.undo_btn['state'] == 'normal' else None)
        self.undo_btn.bind('<Leave>', lambda e: self.undo_btn.config(bg=self.colors['danger']) if self.undo_btn['state'] == 'normal' else None)
        
        # History Card
        history_card = tk.Frame(left, bg=self.colors['white'])
        history_card.pack(fill='both', expand=True)
        
        history_header = tk.Frame(history_card, bg=self.colors['white'])
        history_header.pack(fill='x', padx=30, pady=(25, 15))
        
        tk.Label(
            history_header,
            text="Attempt History",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(side='left')
        
        self.attempt_count_label = tk.Label(
            history_header,
            text="0 attempts",
            font=('Segoe UI', 12),
            bg=self.colors['white'],
            fg=self.colors['text_light']
        )
        self.attempt_count_label.pack(side='right')
        
        history_container = tk.Frame(history_card, bg=self.colors['white'])
        history_container.pack(fill='both', expand=True, padx=30, pady=(0, 25))
        
        self.history_text = tk.Text(
            history_container,
            font=('Consolas', 14),
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            relief='flat',
            bd=0,
            padx=20,
            pady=20,
            height=10
        )
        self.history_text.pack(fill='both', expand=True)
        
        self.history_text.tag_config('green', foreground=self.colors['success'], font=('Consolas', 14, 'bold'))
        self.history_text.tag_config('yellow', foreground=self.colors['warning'], font=('Consolas', 14, 'bold'))
        self.history_text.tag_config('gray', foreground=self.colors['gray'], font=('Consolas', 14, 'bold'))
        self.history_text.tag_config('number', foreground=self.colors['text_lighter'], font=('Consolas', 12))
        
        # RIGHT COLUMN
        right = tk.Frame(container, bg=self.colors['bg'])
        right.pack(side='right', fill='both', expand=True, padx=(25, 0))
        
        # Suggestion Card
        suggest_card = tk.Frame(right, bg=self.colors['white'])
        suggest_card.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            suggest_card,
            text="Recommended Word",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=30, pady=(25, 5))
        
        tk.Label(
            suggest_card,
            text="Press Tab in word field to use this",
            font=('Segoe UI', 11),
            bg=self.colors['white'],
            fg=self.colors['text_light']
        ).pack(anchor='w', padx=30, pady=(0, 15))
        
        suggest_container = tk.Frame(suggest_card, bg='#EEF2FF')
        suggest_container.pack(fill='x', padx=30, pady=(0, 25))
        
        self.suggestion_label = tk.Label(
            suggest_container,
            text="SOARE",
            font=('Segoe UI', 56, 'bold'),
            bg='#EEF2FF',
            fg=self.colors['primary'],
            cursor='hand2'
        )
        self.suggestion_label.pack(pady=30)
        self.suggestion_label.bind('<Button-1>', lambda e: self.copy_suggestion())
        
        # Stats Card
        stats_card = tk.Frame(right, bg=self.colors['white'])
        stats_card.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            stats_card,
            text="Statistics",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=30, pady=(25, 20))
        
        stats_grid = tk.Frame(stats_card, bg=self.colors['white'])
        stats_grid.pack(fill='x', padx=30, pady=(0, 25))
        
        self.stat_labels = {}
        stats = [
            ('possible', 'Possible Words', '12,972', self.colors['primary']),
            ('attempts', 'Attempts Made', '0', self.colors['success']),
            ('eliminated', 'Words Eliminated', '0', self.colors['text_light'])
        ]
        
        for key, label, value, color in stats:
            stat_row = tk.Frame(stats_grid, bg=self.colors['input_bg'])
            stat_row.pack(fill='x', pady=3)
            
            tk.Label(
                stat_row,
                text=label,
                font=('Segoe UI', 12),
                bg=self.colors['input_bg'],
                fg=self.colors['text_light'],
                anchor='w'
            ).pack(side='left', padx=20, pady=12)
            
            val_label = tk.Label(
                stat_row,
                text=value,
                font=('Segoe UI', 18, 'bold'),
                bg=self.colors['input_bg'],
                fg=color,
                anchor='e'
            )
            val_label.pack(side='right', padx=20, pady=12)
            
            self.stat_labels[key] = val_label
        
        # Words Card
        words_card = tk.Frame(right, bg=self.colors['white'])
        words_card.pack(fill='both', expand=True)
        
        words_header = tk.Frame(words_card, bg=self.colors['white'])
        words_header.pack(fill='x', padx=30, pady=(25, 10))
        
        tk.Label(
            words_header,
            text="Possible Words",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(side='left')
        
        self.words_count_label = tk.Label(
            words_header,
            text="12,972",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        self.words_count_label.pack(side='right')
        
        words_container = tk.Frame(words_card, bg=self.colors['white'])
        words_container.pack(fill='both', expand=True, padx=30, pady=(0, 25))
        
        self.words_text = scrolledtext.ScrolledText(
            words_container,
            font=('Consolas', 11),
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            relief='flat',
            bd=0,
            wrap='word',
            padx=15,
            pady=15,
            height=15
        )
        self.words_text.pack(fill='both', expand=True)
        
        # Bottom actions
        bottom_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg'])
        bottom_frame.pack(fill='x', padx=50, pady=(20, 25))
        
        reset_btn = tk.Button(
            bottom_frame,
            text="↻  Start New Game",
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['text'],
            activebackground=self.colors['input_bg'],
            command=self.reset,
            cursor='hand2',
            relief='flat',
            bd=1,
            borderwidth=1,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        reset_btn.pack(side='left', padx=5, pady=5, ipadx=20, ipady=10)
        
        self.update_display()
    
    def on_word_enter(self, event):
        """Enter pressed in word field - move to feedback with typed word"""
        self.feedback_entry.focus()
        return 'break'
    
    def on_word_tab(self, event):
        """Tab pressed in word field - use suggestion and move to feedback"""
        suggestion = self.suggestion_label.cget('text')
        self.word_entry.delete(0, tk.END)
        self.word_entry.insert(0, suggestion)
        self.feedback_entry.focus()
        return 'break'  # Prevent default tab behavior
    
    def _on_mousewheel(self, event):
        """Handle mousewheel"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_canvas_configure(self, event):
        """Canvas resize"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def process(self):
        """Process input"""
        word = self.word_entry.get().strip().upper()
        feedback_str = self.feedback_entry.get().strip().upper()
        
        if len(word) != 5:
            messagebox.showerror("Invalid Input", "Word must be exactly 5 letters")
            return
        
        if not self.word_bank.is_valid(word.lower()):
            messagebox.showerror("Invalid Word", f"'{word}' is not in our dictionary")
            return
        
        if len(feedback_str) != 5:
            messagebox.showerror("Invalid Feedback", "Feedback must be 5 characters (G/Y/B)")
            return
        
        feedback = []
        for i, char in enumerate(feedback_str):
            if char == 'G':
                status = 'correct'
            elif char == 'Y':
                status = 'present'
            elif char == 'B':
                status = 'absent'
            else:
                messagebox.showerror("Invalid Character", f"Use only G, Y, or B (not '{char}')")
                return
            
            feedback.append({
                'letter': word[i].lower(),
                'status': status,
                'position': i
            })
        
        if all(fb['status'] == 'correct' for fb in feedback):
            messagebox.showinfo("🎉 Solved!", f"Puzzle solved in {len(self.attempts) + 1} attempts!\n\nThe word was: {word}")
            return
        
        self.solver.process_feedback(word.lower(), feedback)
        self.attempts.append((word, feedback_str))
        
        self.word_entry.delete(0, tk.END)
        self.feedback_entry.delete(0, tk.END)
        self.word_entry.focus()
        
        self.undo_btn.config(state='normal')
        
        self.display_history()
        self.update_display()
        
        if len(self.solver.possible_words) == 0:
            messagebox.showwarning("No Matches", "No words match your feedback.\n\nPlease check your input.")
    
    def undo_last(self):
        """Undo last attempt"""
        if not self.attempts:
            return
        
        self.attempts.pop()
        self.solver.reset()
        
        for word, feedback_str in self.attempts:
            feedback = []
            for i, char in enumerate(feedback_str):
                if char == 'G':
                    status = 'correct'
                elif char == 'Y':
                    status = 'present'
                else:
                    status = 'absent'
                
                feedback.append({
                    'letter': word[i].lower(),
                    'status': status,
                    'position': i
                })
            
            self.solver.process_feedback(word.lower(), feedback)
        
        if len(self.attempts) == 0:
            self.undo_btn.config(state='disabled')
        
        self.display_history()
        self.update_display()
    
    def display_history(self):
        """Display history"""
        self.history_text.delete('1.0', 'end')
        
        if not self.attempts:
            self.history_text.insert('end', "No attempts yet. Enter your first guess above!")
            self.attempt_count_label.config(text="0 attempts")
            return
        
        self.attempt_count_label.config(text=f"{len(self.attempts)} attempt{'s' if len(self.attempts) > 1 else ''}")
        
        for i, (word, feedback_str) in enumerate(self.attempts):
            self.history_text.insert('end', f"  {i+1}.  ", 'number')
            
            for j, letter in enumerate(word):
                char = feedback_str[j]
                if char == 'G':
                    self.history_text.insert('end', f"{letter} ", 'green')
                elif char == 'Y':
                    self.history_text.insert('end', f"{letter} ", 'yellow')
                else:
                    self.history_text.insert('end', f"{letter} ", 'gray')
            
            self.history_text.insert('end', '\n')
    
    def copy_suggestion(self):
        """Copy suggestion"""
        word = self.suggestion_label.cget('text')
        self.word_entry.delete(0, tk.END)
        self.word_entry.insert(0, word)
        self.word_entry.focus()
    
    def update_display(self):
        """Update display"""
        best, count = self.solver.get_best_guess()
        
        if best:
            self.suggestion_label.config(text=best.upper())
        
        total = len(self.word_bank.all_words)
        eliminated = total - count
        
        self.stat_labels['possible'].config(text=f"{count:,}")
        self.stat_labels['attempts'].config(text=str(len(self.attempts)))
        self.stat_labels['eliminated'].config(text=f"{eliminated:,}")
        
        self.words_count_label.config(text=f"{count:,}")
        self.header_stat.config(text=f"{count:,} possible • {len(self.attempts)} attempts")
        
        words = self.solver.get_possible_words()
        self.words_text.delete('1.0', 'end')
        
        if len(words) == 0:
            self.words_text.insert('end', "No words match your feedback!")
        elif len(words) <= 200:
            for i in range(0, len(words), 5):
                line = '  '.join([w.upper().ljust(6) for w in words[i:i+5]])
                self.words_text.insert('end', line + '\n')
        else:
            self.words_text.insert('end', f"Showing 150 of {len(words):,} words\n\n")
            for i in range(0, 150, 5):
                line = '  '.join([w.upper().ljust(6) for w in words[i:i+5]])
                self.words_text.insert('end', line + '\n')
    
    def reset(self):
        """Reset game"""
        if self.attempts:
            if not messagebox.askyesno("Start New Game", "This will clear all your progress. Continue?"):
                return
        
        self.solver.reset()
        self.attempts = []
        self.word_entry.delete(0, tk.END)
        self.feedback_entry.delete(0, tk.END)
        self.history_text.delete('1.0', 'end')
        self.undo_btn.config(state='disabled')
        self.update_display()
        self.display_history()
        self.canvas.yview_moveto(0)
    
    def run(self):
        """Run app"""
        self.root.mainloop()
