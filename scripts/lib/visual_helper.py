#!/usr/bin/env python3
"""
Visual Output Utilities for MokoStandards Scripts

Provides rich terminal output including:
- Progress bars
- Colored status messages
- Spinners
- Tables
- Box frames
- ASCII art

FILE: scripts/lib/visual_helper.py
AUTHOR: Moko Consulting <hello@mokoconsulting.tech>
VERSION: 03.01.03
LICENSE: GPL-3.0-or-later
"""

import sys
import time
import shutil
from typing import Optional, List, Dict, Any
from enum import Enum

class Color(Enum):
    """Terminal color codes"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Bright foreground colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


class StatusIcon(Enum):
    """Status indicator icons"""
    SUCCESS = '✓'
    ERROR = '✗'
    WARNING = '⚠'
    INFO = 'ℹ'
    PENDING = '○'
    RUNNING = '▶'
    SKIPPED = '⊗'
    QUESTION = '?'


def supports_color() -> bool:
    """Check if terminal supports color output"""
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


def colorize(text: str, color: Color, bold: bool = False) -> str:
    """
    Apply color to text if terminal supports it.
    
    Args:
        text: Text to colorize
        color: Color to apply
        bold: Make text bold
        
    Returns:
        Colorized text or plain text if colors not supported
    """
    if not supports_color():
        return text
    
    result = color.value + text + Color.RESET.value
    if bold:
        result = Color.BOLD.value + result
    return result


def print_status(message: str, status: str = 'info', prefix: str = '', 
                 icon: bool = True, bold: bool = False):
    """
    Print a status message with color and optional icon.
    
    Args:
        message: Message to print
        status: Status type (success, error, warning, info, pending, running)
        prefix: Optional prefix before icon
        icon: Show status icon
        bold: Make message bold
    """
    status_map = {
        'success': (StatusIcon.SUCCESS, Color.GREEN),
        'error': (StatusIcon.ERROR, Color.RED),
        'warning': (StatusIcon.WARNING, Color.YELLOW),
        'info': (StatusIcon.INFO, Color.BLUE),
        'pending': (StatusIcon.PENDING, Color.CYAN),
        'running': (StatusIcon.RUNNING, Color.CYAN),
        'skipped': (StatusIcon.SKIPPED, Color.DIM),
        'question': (StatusIcon.QUESTION, Color.MAGENTA),
    }
    
    icon_char, color = status_map.get(status, (StatusIcon.INFO, Color.RESET))
    
    if icon:
        icon_str = colorize(f" {icon_char.value} ", color, bold=True)
        message_str = colorize(message, color, bold=bold)
        print(f"{prefix}{icon_str}{message_str}")
    else:
        message_str = colorize(message, color, bold=bold)
        print(f"{prefix}{message_str}")


def print_success(message: str, prefix: str = ''):
    """Print success message"""
    print_status(message, 'success', prefix)


def print_error(message: str, prefix: str = ''):
    """Print error message"""
    print_status(message, 'error', prefix)


def print_warning(message: str, prefix: str = ''):
    """Print warning message"""
    print_status(message, 'warning', prefix)


def print_info(message: str, prefix: str = ''):
    """Print info message"""
    print_status(message, 'info', prefix)


def print_header(title: str, subtitle: str = '', width: int = 70):
    """
    Print a formatted header with box.
    
    Args:
        title: Main title
        subtitle: Optional subtitle
        width: Total width of box
    """
    terminal_width = shutil.get_terminal_size((width, 20)).columns
    width = min(width, terminal_width - 4)
    
    top_border = '╔' + '═' * (width - 2) + '╗'
    bottom_border = '╚' + '═' * (width - 2) + '╝'
    
    print('\n' + colorize(top_border, Color.CYAN, bold=True))
    
    # Title
    title_line = title.center(width - 2)
    print(colorize('║', Color.CYAN, bold=True) + colorize(title_line, Color.BRIGHT_WHITE, bold=True) + colorize('║', Color.CYAN, bold=True))
    
    # Subtitle
    if subtitle:
        subtitle_line = subtitle.center(width - 2)
        print(colorize('║', Color.CYAN, bold=True) + colorize(subtitle_line, Color.BRIGHT_BLACK) + colorize('║', Color.CYAN, bold=True))
    
    print(colorize(bottom_border, Color.CYAN, bold=True) + '\n')


def print_box(message: str, box_type: str = 'info', width: int = 70):
    """
    Print a message in a colored box.
    
    Args:
        message: Message to display
        box_type: Type of box (info, success, warning, error)
        width: Box width
    """
    terminal_width = shutil.get_terminal_size((width, 20)).columns
    width = min(width, terminal_width - 4)
    
    color_map = {
        'info': Color.BLUE,
        'success': Color.GREEN,
        'warning': Color.YELLOW,
        'error': Color.RED,
    }
    
    color = color_map.get(box_type, Color.BLUE)
    
    # Split message into lines
    words = message.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= width - 6:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Print box
    print('\n' + colorize('┌' + '─' * (width - 2) + '┐', color))
    for line in lines:
        padded_line = line.ljust(width - 4)
        print(colorize('│ ', color) + padded_line + colorize(' │', color))
    print(colorize('└' + '─' * (width - 2) + '┘', color) + '\n')


class ProgressBar:
    """
    ASCII progress bar with percentage.
    
    Example:
        progress = ProgressBar(total=100, prefix='Processing')
        for i in range(100):
            progress.update(i + 1)
            time.sleep(0.01)
        progress.finish()
    """
    
    def __init__(self, total: int, prefix: str = 'Progress', width: int = 50, 
                 show_percentage: bool = True, show_count: bool = True):
        """
        Initialize progress bar.
        
        Args:
            total: Total number of items
            prefix: Prefix text
            width: Width of bar in characters
            show_percentage: Show percentage complete
            show_count: Show item count
        """
        self.total = total
        self.prefix = prefix
        self.width = width
        self.show_percentage = show_percentage
        self.show_count = show_count
        self.current = 0
        self.start_time = time.time()
        
    def update(self, current: int, suffix: str = ''):
        """
        Update progress bar.
        
        Args:
            current: Current progress value
            suffix: Optional suffix text
        """
        self.current = current
        percent = (current / self.total) * 100 if self.total > 0 else 0
        filled = int(self.width * current / self.total) if self.total > 0 else 0
        bar = '█' * filled + '░' * (self.width - filled)
        
        # Build status line
        parts = [self.prefix + ':']
        
        if self.show_count:
            parts.append(f'{current}/{self.total}')
        
        if self.show_percentage:
            parts.append(f'{percent:>5.1f}%')
        
        parts.append(f'[{colorize(bar, Color.GREEN)}]')
        
        if suffix:
            parts.append(suffix)
        
        # Calculate ETA
        if current > 0:
            elapsed = time.time() - self.start_time
            rate = current / elapsed
            remaining = (self.total - current) / rate if rate > 0 else 0
            if remaining > 0:
                parts.append(f'ETA: {remaining:.1f}s')
        
        line = ' '.join(parts)
        
        # Print with carriage return
        sys.stdout.write('\r' + line + ' ' * 10)
        sys.stdout.flush()
        
    def finish(self, message: str = 'Complete!'):
        """
        Finish progress bar and print completion message.
        
        Args:
            message: Completion message
        """
        self.update(self.total)
        elapsed = time.time() - self.start_time
        print(f'\n{colorize(f"✓ {message}", Color.GREEN)} (took {elapsed:.2f}s)')


class Spinner:
    """
    Animated spinner for long-running operations.
    
    Example:
        spinner = Spinner('Loading')
        spinner.start()
        # ... do work ...
        spinner.stop('Done!')
    """
    
    FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    def __init__(self, message: str = 'Processing'):
        """
        Initialize spinner.
        
        Args:
            message: Message to display
        """
        self.message = message
        self.running = False
        self.frame_index = 0
        
    def start(self):
        """Start the spinner animation"""
        self.running = True
        self._animate()
        
    def _animate(self):
        """Animate the spinner"""
        if not self.running:
            return
            
        frame = self.FRAMES[self.frame_index % len(self.FRAMES)]
        sys.stdout.write(f'\r{colorize(frame, Color.CYAN)} {self.message}...')
        sys.stdout.flush()
        
        self.frame_index += 1
        
        # Continue animation
        if self.running:
            import threading
            threading.Timer(0.1, self._animate).start()
    
    def stop(self, final_message: str = 'Done'):
        """
        Stop the spinner and print final message.
        
        Args:
            final_message: Message to display when complete
        """
        self.running = False
        sys.stdout.write('\r' + ' ' * (len(self.message) + 20) + '\r')
        print_success(final_message)


def print_table(headers: List[str], rows: List[List[str]], 
                title: str = '', show_index: bool = False):
    """
    Print a formatted table.
    
    Args:
        headers: List of column headers
        rows: List of row data (list of lists)
        title: Optional table title
        show_index: Show row numbers
    """
    if show_index:
        headers = ['#'] + headers
        rows = [[str(i + 1)] + row for i, row in enumerate(rows)]
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Print title
    if title:
        print('\n' + colorize(title, Color.BRIGHT_WHITE, bold=True))
    
    # Print headers
    header_line = ' │ '.join(colorize(h.ljust(w), Color.CYAN, bold=True) 
                              for h, w in zip(headers, col_widths))
    separator = '─┼─'.join('─' * w for w in col_widths)
    
    print('┌─' + '─┬─'.join('─' * w for w in col_widths) + '─┐')
    print('│ ' + header_line + ' │')
    print('├─' + separator + '─┤')
    
    # Print rows
    for row in rows:
        row_line = ' │ '.join(str(cell).ljust(w) for cell, w in zip(row, col_widths))
        print('│ ' + row_line + ' │')
    
    print('└─' + '─┴─'.join('─' * w for w in col_widths) + '─┘\n')


def print_summary(items: Dict[str, Any], title: str = 'Summary'):
    """
    Print a summary box with key-value pairs.
    
    Args:
        items: Dictionary of key-value pairs
        title: Summary title
    """
    # Calculate max key length
    max_key_len = max(len(str(k)) for k in items.keys()) if items else 0
    
    print('\n' + colorize('═' * 60, Color.BRIGHT_BLUE))
    print(colorize(f'  {title}', Color.BRIGHT_WHITE, bold=True))
    print(colorize('═' * 60, Color.BRIGHT_BLUE))
    
    for key, value in items.items():
        key_str = colorize(f'{key}:'.ljust(max_key_len + 2), Color.CYAN)
        value_str = colorize(str(value), Color.BRIGHT_WHITE)
        print(f'  {key_str} {value_str}')
    
    print(colorize('═' * 60, Color.BRIGHT_BLUE) + '\n')


def confirm(message: str, default: bool = False) -> bool:
    """
    Ask for user confirmation with colored prompt.
    
    Args:
        message: Confirmation message
        default: Default response
        
    Returns:
        True if confirmed, False otherwise
    """
    suffix = '[Y/n]' if default else '[y/N]'
    prompt = colorize(f'{StatusIcon.QUESTION.value} {message} {suffix}: ', Color.MAGENTA)
    
    response = input(prompt).strip().lower()
    
    if not response:
        return default
    
    return response in ('y', 'yes')


if __name__ == '__main__':
    # Demo of all visual components
    print_header('MokoStandards Visual Helper', 'Demo of all components')
    
    print_success('This is a success message')
    print_error('This is an error message')
    print_warning('This is a warning message')
    print_info('This is an info message')
    
    print_box('This is an informational box with some longer text that will wrap to multiple lines automatically.', 'info')
    print_box('Operation completed successfully!', 'success')
    print_box('Warning: This action cannot be undone.', 'warning')
    print_box('Error: Something went wrong.', 'error')
    
    # Progress bar demo
    progress = ProgressBar(total=50, prefix='Processing files')
    for i in range(50):
        progress.update(i + 1, suffix=f'file_{i}.txt')
        time.sleep(0.02)
    progress.finish('All files processed')
    
    # Table demo
    print_table(
        headers=['Name', 'Status', 'Count'],
        rows=[
            ['validate_structure.py', 'Pass', '150'],
            ['check_repo_health.py', 'Pass', '87'],
            ['security_scan.py', 'Warn', '3'],
        ],
        title='Script Execution Results',
        show_index=True
    )
    
    # Summary demo
    print_summary({
        'Total Files': 150,
        'Passed': 147,
        'Warnings': 3,
        'Errors': 0,
        'Duration': '2.5s',
    }, title='Execution Summary')
    
    # Confirmation demo
    if confirm('Continue with demo?', default=True):
        print_success('User confirmed!')
    else:
        print_info('User declined.')
