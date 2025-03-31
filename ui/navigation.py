from typing import Dict, Type, Optional, Callable
from PySide6.QtWidgets import QMainWindow
from ui.base_screen import BaseScreen

class NavigationManager:
    def __init__(self):
        self._screens: Dict[str, BaseScreen] = {}
        self._screen_factories: Dict[str, Callable[[], BaseScreen]] = {}
        self._history: list[str] = []
    
    def register_screen(self, name: str, screen_factory: Callable[[], BaseScreen]):
        """Register a screen factory with a name"""
        self._screen_factories[name] = screen_factory
    
    def navigate_to(self, screen_name: str):
        """Navigate to a screen by name"""
        if screen_name not in self._screen_factories:
            raise ValueError(f"Screen {screen_name} not registered")
        
        # Create screen if it doesn't exist
        if screen_name not in self._screens:
            self._screens[screen_name] = self._screen_factories[screen_name]()
        
        # Add to history
        self._history.append(screen_name)
        
        # Show the screen
        self._screens[screen_name].show_screen()
    
    def navigate_back(self) -> bool:
        """Navigate back to previous screen"""
        if len(self._history) <= 1:
            return False
        
        # Remove current screen from history
        self._history.pop()
        
        # Show previous screen
        previous_screen = self._history[-1]
        self._screens[previous_screen].show_screen()
        return True
    
    def get_current_screen(self) -> Optional[str]:
        """Get the name of the current screen"""
        return self._history[-1] if self._history else None 