#!/usr/bin/env python3
"""
Ralph Wiggum Persistence Loop for AI Employee

This module implements the "Ralph Wiggum" pattern - a stop hook that keeps
the AI agent working until tasks are complete. It intercepts the AI's exit
attempts and re-injects prompts if tasks are incomplete.

From reqment.md:
> Claude Code runs in interactive mode - after processing a prompt, it waits 
> for more input. To keep your AI Employee working autonomously until a task 
> is complete, use the Ralph Wiggum pattern: a Stop hook that intercepts 
> Claude's exit and feeds the prompt back.

Usage:
    from ralph_wiggum import RalphWiggumHook
    
    hook = RalphWiggumHook(task_file, max_iterations=10)
    
    while hook.should_continue():
        # Run AI processing
        response = brain.process(prompt)
        
        # Check if task is complete
        if hook.is_task_complete(response):
            break
"""

import time
import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable


# Configure logging
logger = logging.getLogger(__name__)


class RalphWiggumHook:
    """
    Ralph Wiggum persistence loop for AI Employee.
    
    Keeps the AI working on tasks until they're complete by:
    1. Checking if task file moved to Done folder
    2. Blocking exit if task incomplete
    3. Re-injecting prompt for another iteration
    4. Respecting max iterations limit
    """
    
    def __init__(self, task_file: Path, max_iterations: int = 10,
                 completion_checker: Optional[Callable] = None):
        """
        Initialize the Ralph Wiggum hook.
        
        Args:
            task_file: Path to the task file being processed
            max_iterations: Maximum number of iterations before giving up
            completion_checker: Optional custom function to check completion
        """
        self.task_file = task_file
        self.max_iterations = max_iterations
        self.iterations = 0
        self.start_time = datetime.now()
        self.completion_checker = completion_checker
        
        # Paths
        self.done_folder = task_file.parent.parent / 'Done'
        self.plans_folder = task_file.parent.parent / 'Plans'
        
        logger.info(f"Ralph Wiggum Hook initialized for: {task_file.name}")
        logger.info(f"Max iterations: {max_iterations}")
    
    def should_continue(self) -> bool:
        """
        Check if the AI should continue working on the task.
        
        Returns:
            True if should continue, False if should stop
        """
        self.iterations += 1
        
        # Check iteration limit
        if self.iterations > self.max_iterations:
            logger.warning(f"Max iterations ({self.max_iterations}) reached")
            return False
        
        # Check if task file moved to Done
        if self._is_in_done_folder():
            logger.info(f"Task complete: File moved to Done folder")
            return False
        
        # Check custom completion condition
        if self.completion_checker:
            try:
                if self.completion_checker(self.task_file):
                    logger.info(f"Task complete: Custom checker satisfied")
                    return False
            except Exception as e:
                logger.error(f"Completion checker error: {e}")
        
        # Continue working
        logger.info(f"Continuing iteration {self.iterations}/{self.max_iterations}")
        return True
    
    def _is_in_done_folder(self) -> bool:
        """Check if task file has been moved to Done folder."""
        done_file = self.done_folder / self.task_file.name
        return done_file.exists()
    
    def get_status(self) -> dict:
        """Get current status of the loop."""
        elapsed = datetime.now() - self.start_time
        
        return {
            'task_file': str(self.task_file),
            'iterations': self.iterations,
            'max_iterations': self.max_iterations,
            'elapsed_seconds': elapsed.total_seconds(),
            'in_done_folder': self._is_in_done_folder(),
            'should_continue': self.should_continue()
        }
    
    def on_iteration_start(self) -> None:
        """Called at the start of each iteration."""
        logger.info(f"Starting iteration {self.iterations}")
        
        # Log status every 3 iterations
        if self.iterations % 3 == 0:
            status = self.get_status()
            logger.info(f"Status: {status}")
    
    def on_iteration_complete(self, response: str) -> None:
        """
        Called at the end of each iteration.
        
        Args:
            response: AI response from the iteration
        """
        logger.info(f"Iteration {self.iterations} complete ({len(response)} chars)")
        
        # Check for completion markers in response
        if self._check_completion_markers(response):
            logger.info("Completion markers found in response")
    
    def _check_completion_markers(self, response: str) -> bool:
        """Check for completion markers in AI response."""
        markers = [
            'TASK_COMPLETE',
            'COMPLETION: YES',
            'STATUS: DONE',
            '[X] All actions completed',
            '✓ Complete'
        ]
        
        response_upper = response.upper()
        for marker in markers:
            if marker.upper() in response_upper:
                return True
        
        return False
    
    def create_retry_prompt(self, original_prompt: str, 
                           previous_response: str,
                           error_message: str = "") -> str:
        """
        Create a prompt for retry iteration.
        
        Args:
            original_prompt: The original prompt
            previous_response: Previous AI response
            error_message: Optional error message
            
        Returns:
            New prompt for retry
        """
        retry_prompt = f"""{original_prompt}

---

## Previous Attempt
Your previous response:
{previous_response[:500]}...

"""
        
        if error_message:
            retry_prompt += f"""
## Error
The following error occurred:
{error_message}

Please try again with a different approach.
"""
        else:
            retry_prompt += """
## Status
The task is not yet complete. Please continue working on it.
Review your previous response and identify what still needs to be done.
"""
        
        return retry_prompt
    
    def __str__(self) -> str:
        """Return string representation."""
        return f"RalphWiggumHook(iterations={self.iterations}/{self.max_iterations})"


class RalphWiggumManager:
    """
    Manager for Ralph Wiggum loops across multiple tasks.
    
    Provides centralized tracking and management of all active loops.
    """
    
    def __init__(self):
        """Initialize the manager."""
        self.active_loops = {}
        self.completed_loops = []
        self.failed_loops = []
    
    def start_loop(self, task_file: Path, max_iterations: int = 10) -> RalphWiggumHook:
        """
        Start a new Ralph Wiggum loop for a task.
        
        Args:
            task_file: Path to the task file
            max_iterations: Maximum iterations
            
        Returns:
            RalphWiggumHook instance
        """
        hook = RalphWiggumHook(task_file, max_iterations)
        self.active_loops[str(task_file)] = hook
        
        logger.info(f"Started Ralph Wiggum loop for: {task_file.name}")
        return hook
    
    def end_loop(self, task_file: Path, success: bool = True) -> None:
        """
        End a Ralph Wiggum loop.
        
        Args:
            task_file: Path to the task file
            success: Whether the loop completed successfully
        """
        task_key = str(task_file)
        
        if task_key in self.active_loops:
            hook = self.active_loops.pop(task_key)
            
            if success:
                self.completed_loops.append(hook)
                logger.info(f"Completed loop for: {task_file.name}")
            else:
                self.failed_loops.append(hook)
                logger.warning(f"Failed loop for: {task_file.name}")
    
    def get_stats(self) -> dict:
        """Get statistics about all loops."""
        return {
            'active': len(self.active_loops),
            'completed': len(self.completed_loops),
            'failed': len(self.failed_loops),
            'total': len(self.active_loops) + len(self.completed_loops) + len(self.failed_loops)
        }


def run_with_ralph_loop(brain, prompt: str, task_file: Path,
                       max_iterations: int = 10) -> str:
    """
    Run AI processing with Ralph Wiggum loop.
    
    Convenience function that handles the entire loop pattern.
    
    Args:
        brain: AI Brain instance
        prompt: Initial prompt
        task_file: Task file to process
        max_iterations: Maximum iterations
        
    Returns:
        Final AI response
    """
    hook = RalphWiggumHook(task_file, max_iterations)
    
    current_prompt = prompt
    last_response = ""
    
    while hook.should_continue():
        hook.on_iteration_start()
        
        try:
            # Process with AI
            response = brain.process(current_prompt)
            
            # Check iteration
            hook.on_iteration_complete(response)
            
            # Check for completion
            if hook._check_completion_markers(response):
                logger.info("Task marked as complete by AI")
                break
            
            last_response = response
            
            # Prepare retry prompt if needed
            if hook.should_continue():
                current_prompt = hook.create_retry_prompt(
                    prompt,
                    response,
                    "Task not yet complete. Please continue."
                )
            
        except Exception as e:
            logger.error(f"Iteration error: {e}")
            
            if hook.should_continue():
                current_prompt = hook.create_retry_prompt(
                    prompt,
                    last_response,
                    str(e)
                )
            else:
                raise
    
    return last_response


if __name__ == "__main__":
    # Test the Ralph Wiggum hook
    print("Testing Ralph Wiggum Hook...")
    
    # Create a test task file
    test_dir = Path(__file__).parent / "AI_Employee_Vault" / "Needs_Action"
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_file = test_dir / "TEST_RALPH.md"
    test_file.write_text("""---
type: test
status: pending
---

# Test Task

This is a test task for Ralph Wiggum loop.
""")
    
    # Create hook
    hook = RalphWiggumHook(test_file, max_iterations=3)
    
    print(f"Hook initialized: {hook}")
    print(f"Task file: {test_file}")
    print(f"Done folder: {hook.done_folder}")
    
    # Test iterations
    print("\nTesting iterations...")
    iteration = 0
    
    while hook.should_continue() and iteration < 5:
        iteration += 1
        hook.on_iteration_start()
        print(f"  Iteration {iteration}: should_continue=True")
        
        # Simulate AI response
        response = f"Working on iteration {iteration}..."
        hook.on_iteration_complete(response)
        
        time.sleep(0.5)
    
    # Cleanup
    test_file.unlink()
    
    print("\n✓ Ralph Wiggum Hook test completed!")
    print(f"Final status: {hook.get_status()}")
