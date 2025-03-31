# Navigation System Implementation Lessons

## Problem
When implementing a screen navigation system, we encountered several issues that required multiple iterations to resolve. The main problems were:
- Tests failing due to missing screen registration
- Implicit dependencies between components
- Complex test setup requirements

## Root Causes
1. **Implementation-First Approach**
   - Started with implementation before tests
   - Missed critical dependencies during initial design
   - Had to retrofit tests to match implementation

2. **Incomplete Initial Design**
   - Didn't fully map out component relationships
   - Missed implicit dependencies between screens and navigation manager
   - No clear dependency documentation

3. **Complex Test Setup**
   - Test fixtures became more complex than expected
   - Each screen needed registration with navigation manager
   - Signal connections weren't clearly documented

## Better Approach
1. **Test-First Development**
   ```python
   def test_new_game_navigation():
       # Requirements:
       # - Navigation manager with registered screens
       # - Connected signals
       # - Way to verify screen transitions
   ```

2. **Clear Navigation API Design**
   ```python
   # Minimal required interface:
   nav_manager.register_screen(name, screen_class)
   nav_manager.navigate_to(screen_name)
   nav_manager.get_current_screen()
   ```

3. **Explicit Dependencies**
   ```python
   # Component relationships:
   BaseScreen -> NavigationManager (via signal)
   NavigationManager -> Screen classes (via registration)
   Tests -> Both screens registered
   ```

4. **Clean Setup**
   ```python
   def setup_navigation():
       nav_manager = NavigationManager()
       nav_manager.register_screen("start", StartScreen)
       nav_manager.register_screen("civilisation", CivilisationGenerationScreen)
       return nav_manager
   ```

## Key Learnings
1. **Test-Driven Development**
   - Write tests first to drive design
   - Tests reveal missing dependencies early
   - Tests help maintain system integrity

2. **Dependency Management**
   - Make dependencies explicit
   - Document component relationships
   - Consider dependency injection

3. **System Design**
   - Design complete system before implementation
   - Consider test requirements during design
   - Create dependency maps

4. **Documentation**
   - Document implicit dependencies
   - Keep setup requirements clear
   - Maintain clear component relationships

## Prevention
To prevent similar issues in future:
1. Start with test cases
2. Design complete system architecture
3. Document all dependencies
4. Use dependency injection where appropriate
5. Keep test setup simple and clear

## Testability Prompts

Before implementing any component, ask yourself these questions:

1. **Signal and Event Questions**
   - How will I test asynchronous operations?
   - How can I verify signal connections without waiting for timeouts?
   - What happens if events occur in a different order during testing?
   - Can I mock or fake time-dependent processes?

2. **State Management Questions**
   - How do I verify internal state changes?
   - Is there a reliable way to check component state after each operation?
   - Are state getters and setters symmetric (what I set is what I get)?
   - Can I isolate state changes from rendering/UI updates?

3. **Dependency Questions**
   - Can I test this component in isolation?
   - What mock objects will I need to create?
   - What's the minimum setup required for a meaningful test?
   - Can I inject test dependencies instead of creating them internally?

4. **Test Structure Questions**
   - What fixtures will this component require?
   - How will I simulate user interactions?
   - Can I test edge cases and failure modes?
   - Will the test be reliable or could it be flaky?

5. **Testing Hooks**
   - Do I need to add testing-specific methods or properties?
   - Should I expose internal state for testing purposes?
   - How can I make asynchronous processes synchronous for testing?
   - What seams should I create to allow mocking?

Using these prompts before implementation can help identify potential testing challenges early. For the specific issues encountered with `test_generate_button_enabled_after_loading`, asking questions like "Are state getters and setters symmetric?" and "How will I test asynchronous operations?" would have revealed the inconsistencies in the `ProgressButton` implementation.

## UI Component Testing Guidelines

Testing UI components presents unique challenges, especially with composite components like our `ProgressButton`. Here are specific guidelines for testing UI components:

1. **State vs. Appearance Separation**
   - Clearly separate the component's logical state from its visual appearance
   - Provide dedicated methods for state inspection that don't rely on rendering
   - Example: `is_enabled()` should directly check the logical state, not query the UI element

2. **Synchronization Guarantees**
   - Ensure state-changing methods complete all their side effects before returning
   - Provide ways to wait for animations/transitions to complete
   - Consider adding testing hooks like `waitForStateChange()` or `isFullyRendered()`

3. **Consistent API Design**
   ```python
   # Good: Symmetrical getters/setters
   button.set_enabled(True)
   assert button.is_enabled() == True
   
   # Bad: Asymmetrical API
   button.setEnabled(True)  # Qt style
   assert button.is_enabled() == True  # Custom method
   ```

4. **Test at the Right Level**
   - Unit test internal logic separately from rendering
   - Integration test the component as part of a screen
   - Consider end-to-end tests for critical UI workflows

5. **Threading and Event Loop Awareness**
   - Be explicit about when events need processing
   - Provide utilities to safely wait for async operations
   - Mock time-dependent operations to make tests deterministic

Applying these guidelines to the `ProgressButton` would have led to a design where:
1. Setting the enabled state would guarantee all internal elements are updated
2. The `is_enabled()` method would directly reflect the state set via `setEnabled()`
3. Signal connections would be more clearly documented and testable
4. The component would have test-specific utilities to inspect its internal state

## Practical Example: ProgressButton Refactoring

To illustrate how these principles improve testability, here's how the `ProgressButton` class could be refactored based on the lessons learned:

```python
class ProgressButton(QWidget):
    """A button component that includes a progress bar.
    
    This component combines a button and progress bar, where the button is disabled
    while the progress bar is active.
    """
    
    # Signals
    progress_complete = Signal()
    clicked = Signal()
    state_changed = Signal(bool)  # New signal for testing
    
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self._enabled = False  # Internal state tracking
        self._setup_ui(text)
        
    def _setup_ui(self, text: str):
        # ... existing UI setup ...
        self.button.clicked.connect(self.clicked.emit)
    
    def start_progress(self):
        """Start the progress animation"""
        self._progress = 0
        self._is_progressing = True
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.set_enabled(False)
        self._timer.start(50)
    
    def set_progress(self, value: int):
        """Set the progress value directly"""
        self._progress = value
        self.progress_bar.setValue(value)
        if value >= 100:
            self._timer.stop()
            self._is_progressing = False
            self.progress_bar.hide()
            self.set_enabled(True)
            self.progress_complete.emit()
    
    def is_enabled(self) -> bool:
        """Check if the button is enabled"""
        return self._enabled  # Use internal state instead of widget state
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the button"""
        if self._enabled != enabled:
            self._enabled = enabled
            self.button.setEnabled(enabled)
            self.state_changed.emit(enabled)
            
    # For Qt compatibility
    def isEnabled(self) -> bool:
        return self.is_enabled()
        
    def setEnabled(self, enabled: bool):
        self.set_enabled(enabled)
    
    # Testing utilities
    def wait_for_progress_complete(self, qtbot, timeout=1000):
        """Wait until progress is complete (for testing)"""
        if not self._is_progressing:
            return True
            
        result = [False]
        def on_complete():
            result[0] = True
            
        self.progress_complete.connect(on_complete)
        return qtbot.waitUntil(lambda: result[0], timeout=timeout)
```

This refactored version addresses several issues:
1. **State consistency**: Uses internal `_enabled` variable to track state
2. **API consistency**: Provides both Qt-style and Python-style methods
3. **Testing signals**: Adds `state_changed` signal for better test observability
4. **Testing utilities**: Provides a dedicated method for waiting for progress completion
5. **Clear documentation**: Documents testing considerations

With this design, the test would be much more reliable:

```python
def test_generate_button_enabled_after_loading(qtbot, window):
    # Simulate tables loaded
    window._on_tables_loaded({"test_table": MockTable()})
    
    # Use the testing utility to wait for state change
    assert qtbot.waitSignal(window.generate_button.state_changed, timeout=1000)
    
    # This now works reliably
    assert window.generate_button.is_enabled()
```

This example demonstrates how thinking about testability from the beginning leads to a more robust, consistent, and easily testable API design.
