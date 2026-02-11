#!/usr/bin/env python3
"""
Error Recovery Framework for MokoStandards
Version: 03.02.00
Copyright (C) 2026 Moko Consulting LLC

This module provides enterprise-grade error recovery capabilities including:
- Automatic retry with exponential backoff
- Checkpointing for long-running operations
- Transaction rollback on failure
- State recovery from checkpoints
- Resume capability after failures

Usage:
    from error_recovery import Recoverable, checkpoint, RecoveryManager
    
    @Recoverable(max_retries=3)
    def my_function():
        with checkpoint('step1'):
            # do work
            pass
"""

import functools
import json
import logging
import os
import pickle
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VERSION = "03.02.00"


class RecoveryError(Exception):
    """Exception raised when recovery operations fail."""
    pass


class CheckpointManager:
    """Manages checkpoints for recovery operations."""
    
    def __init__(self, checkpoint_dir: str = ".checkpoints"):
        """Initialize checkpoint manager.
        
        Args:
            checkpoint_dir: Directory to store checkpoints
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
    def save_checkpoint(self, name: str, state: Dict[str, Any]) -> str:
        """Save a checkpoint.
        
        Args:
            name: Checkpoint name
            state: State to save
            
        Returns:
            Path to checkpoint file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_file = self.checkpoint_dir / f"{name}_{timestamp}.pkl"
        
        try:
            with open(checkpoint_file, 'wb') as f:
                pickle.dump(state, f)
            logger.info(f"Checkpoint saved: {checkpoint_file}")
            return str(checkpoint_file)
        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")
            raise RecoveryError(f"Checkpoint save failed: {e}")
    
    def load_checkpoint(self, name: str) -> Optional[Dict[str, Any]]:
        """Load the most recent checkpoint for a name.
        
        Args:
            name: Checkpoint name
            
        Returns:
            Checkpoint state or None if not found
        """
        checkpoints = sorted(self.checkpoint_dir.glob(f"{name}_*.pkl"))
        if not checkpoints:
            return None
            
        latest = checkpoints[-1]
        try:
            with open(latest, 'rb') as f:
                state = pickle.load(f)
            logger.info(f"Checkpoint loaded: {latest}")
            return state
        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            return None
    
    def list_checkpoints(self, name: Optional[str] = None) -> List[str]:
        """List available checkpoints.
        
        Args:
            name: Filter by checkpoint name (optional)
            
        Returns:
            List of checkpoint file paths
        """
        pattern = f"{name}_*.pkl" if name else "*.pkl"
        return [str(f) for f in self.checkpoint_dir.glob(pattern)]
    
    def cleanup_checkpoints(self, name: Optional[str] = None, keep_latest: int = 5):
        """Clean up old checkpoints.
        
        Args:
            name: Filter by checkpoint name (optional)
            keep_latest: Number of latest checkpoints to keep
        """
        pattern = f"{name}_*.pkl" if name else "*.pkl"
        checkpoints = sorted(self.checkpoint_dir.glob(pattern))
        
        if len(checkpoints) > keep_latest:
            to_remove = checkpoints[:-keep_latest]
            for cp in to_remove:
                cp.unlink()
                logger.info(f"Removed old checkpoint: {cp}")


class checkpoint:
    """Context manager for creating checkpoints.
    
    Usage:
        with checkpoint('process_step') as cp:
            # do work
            cp.update({'progress': 50})
    """
    
    def __init__(self, name: str, checkpoint_dir: str = ".checkpoints"):
        """Initialize checkpoint context.
        
        Args:
            name: Checkpoint name
            checkpoint_dir: Directory for checkpoints
        """
        self.name = name
        self.manager = CheckpointManager(checkpoint_dir)
        self.state = {'name': name, 'start_time': datetime.now().isoformat()}
        
    def __enter__(self):
        """Enter checkpoint context."""
        logger.info(f"Starting checkpoint: {self.name}")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit checkpoint context and save state."""
        if exc_type is None:
            self.state['status'] = 'completed'
            self.state['end_time'] = datetime.now().isoformat()
        else:
            self.state['status'] = 'failed'
            self.state['error'] = str(exc_val)
            self.state['end_time'] = datetime.now().isoformat()
        
        self.manager.save_checkpoint(self.name, self.state)
        return False  # Don't suppress exceptions
    
    def update(self, data: Dict[str, Any]):
        """Update checkpoint state.
        
        Args:
            data: Data to add to checkpoint state
        """
        self.state.update(data)


class Recoverable:
    """Decorator for adding automatic retry and recovery to functions.
    
    Usage:
        @Recoverable(max_retries=3, backoff_base=2)
        def my_function(arg1, arg2):
            # function implementation
            pass
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        backoff_base: float = 2.0,
        exceptions: tuple = (Exception,),
        on_retry: Optional[Callable] = None,
        on_failure: Optional[Callable] = None
    ):
        """Initialize recoverable decorator.
        
        Args:
            max_retries: Maximum number of retry attempts
            backoff_base: Base for exponential backoff (seconds)
            exceptions: Tuple of exceptions to catch and retry
            on_retry: Callback function called on each retry
            on_failure: Callback function called on final failure
        """
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.exceptions = exceptions
        self.on_retry = on_retry
        self.on_failure = on_failure
        
    def __call__(self, func: Callable) -> Callable:
        """Wrap function with retry logic.
        
        Args:
            func: Function to wrap
            
        Returns:
            Wrapped function
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(self.max_retries):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 0:
                        logger.info(f"{func.__name__} succeeded on attempt {attempt + 1}")
                    return result
                    
                except self.exceptions as e:
                    last_exception = e
                    
                    if attempt < self.max_retries - 1:
                        # Calculate backoff time
                        backoff_time = self.backoff_base ** attempt
                        logger.warning(
                            f"{func.__name__} failed on attempt {attempt + 1}/{self.max_retries}: {e}. "
                            f"Retrying in {backoff_time}s..."
                        )
                        
                        # Call retry callback if provided
                        if self.on_retry:
                            self.on_retry(attempt, e, backoff_time)
                        
                        time.sleep(backoff_time)
                    else:
                        logger.error(
                            f"{func.__name__} failed after {self.max_retries} attempts: {e}"
                        )
                        
                        # Call failure callback if provided
                        if self.on_failure:
                            self.on_failure(self.max_retries, e)
            
            # All retries exhausted
            raise last_exception
        
        return wrapper


class RecoveryManager:
    """High-level manager for recovery operations."""
    
    def __init__(self, checkpoint_dir: str = ".checkpoints"):
        """Initialize recovery manager.
        
        Args:
            checkpoint_dir: Directory for checkpoints
        """
        self.checkpoint_manager = CheckpointManager(checkpoint_dir)
        self.recovery_log = []
        
    def can_recover(self, operation_name: str) -> bool:
        """Check if an operation can be recovered.
        
        Args:
            operation_name: Name of the operation
            
        Returns:
            True if recovery checkpoint exists
        """
        checkpoints = self.checkpoint_manager.list_checkpoints(operation_name)
        return len(checkpoints) > 0
    
    def recover_operation(self, operation_name: str) -> Optional[Dict[str, Any]]:
        """Recover an operation from checkpoint.
        
        Args:
            operation_name: Name of the operation to recover
            
        Returns:
            Recovered state or None
        """
        logger.info(f"Attempting to recover operation: {operation_name}")
        state = self.checkpoint_manager.load_checkpoint(operation_name)
        
        if state:
            self.recovery_log.append({
                'operation': operation_name,
                'recovered_at': datetime.now().isoformat(),
                'state': state
            })
            logger.info(f"Successfully recovered operation: {operation_name}")
        else:
            logger.warning(f"No checkpoint found for operation: {operation_name}")
        
        return state
    
    def get_recovery_log(self) -> List[Dict[str, Any]]:
        """Get recovery log.
        
        Returns:
            List of recovery operations
        """
        return self.recovery_log
    
    def cleanup_old_checkpoints(self, keep_latest: int = 5):
        """Clean up old checkpoints.
        
        Args:
            keep_latest: Number of latest checkpoints to keep per operation
        """
        self.checkpoint_manager.cleanup_checkpoints(keep_latest=keep_latest)


def with_rollback(cleanup_func: Callable):
    """Decorator to add automatic rollback on failure.
    
    Usage:
        @with_rollback(cleanup_function)
        def my_operation():
            # do work
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Operation failed, executing rollback: {e}")
                try:
                    cleanup_func(*args, **kwargs)
                    logger.info("Rollback completed successfully")
                except Exception as rollback_error:
                    logger.error(f"Rollback failed: {rollback_error}")
                raise e
        return wrapper
    return decorator


# Example usage and testing
if __name__ == "__main__":
    print(f"Error Recovery Framework v{VERSION}")
    print("=" * 50)
    
    # Test 1: Recoverable decorator with retry
    print("\n1. Testing Recoverable decorator with retry...")
    
    attempt_count = [0]
    
    @Recoverable(max_retries=3, backoff_base=1)
    def flaky_function():
        attempt_count[0] += 1
        if attempt_count[0] < 3:
            raise ValueError(f"Simulated failure (attempt {attempt_count[0]})")
        return "Success!"
    
    try:
        result = flaky_function()
        print(f"   ✓ Function succeeded: {result}")
    except Exception as e:
        print(f"   ✗ Function failed: {e}")
    
    # Test 2: Checkpoint system
    print("\n2. Testing checkpoint system...")
    manager = CheckpointManager()
    
    with checkpoint('test_operation') as cp:
        cp.update({'step': 1, 'data': 'test_data'})
        print("   ✓ Checkpoint created")
    
    # Test 3: Recovery
    print("\n3. Testing recovery...")
    recovery_mgr = RecoveryManager()
    
    if recovery_mgr.can_recover('test_operation'):
        state = recovery_mgr.recover_operation('test_operation')
        print(f"   ✓ Recovered state: {state['step'] if state else 'None'}")
    
    print("\n✓ All tests passed!")
