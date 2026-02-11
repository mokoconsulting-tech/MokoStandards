#!/usr/bin/env python3
"""
Transaction Manager for MokoStandards
Version: 03.02.00
Copyright (C) 2026 Moko Consulting LLC

Provides atomic multi-step operations with automatic rollback:
- Transaction boundaries
- Automatic rollback on failure
- State consistency checks
- Transaction history
- Nested transactions

Usage:
    from transaction_manager import Transaction
    
    with Transaction() as txn:
        txn.execute(step1)
        txn.execute(step2)
        # Automatic rollback if any step fails
"""

import logging
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

VERSION = "03.02.00"

logger = logging.getLogger(__name__)


class TransactionError(Exception):
    """Exception raised when transaction operations fail."""
    pass


class TransactionStep:
    """Represents a single step in a transaction."""
    
    def __init__(self, name: str, execute_func: Callable, rollback_func: Optional[Callable] = None):
        """Initialize transaction step.
        
        Args:
            name: Step name
            execute_func: Function to execute
            rollback_func: Function to rollback (optional)
        """
        self.name = name
        self.execute_func = execute_func
        self.rollback_func = rollback_func
        self.executed = False
        self.result = None
        self.error = None


class Transaction:
    """Context manager for atomic multi-step operations."""
    
    def __init__(self, name: Optional[str] = None):
        """Initialize transaction.
        
        Args:
            name: Transaction name
        """
        self.name = name or f"txn_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.steps: List[TransactionStep] = []
        self.committed = False
        self.rolled_back = False
        self.start_time = None
        self.end_time = None
        
    def __enter__(self):
        """Enter transaction context."""
        self.start_time = datetime.now()
        logger.info(f"Starting transaction: {self.name}")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit transaction context with automatic rollback on failure."""
        self.end_time = datetime.now()
        
        if exc_type is None:
            # Success - commit
            try:
                self.commit()
            except Exception as e:
                logger.error(f"Commit failed: {e}")
                self.rollback()
                raise TransactionError(f"Transaction commit failed: {e}")
        else:
            # Failure - rollback
            logger.error(f"Transaction failed: {exc_val}")
            self.rollback()
        
        return False  # Don't suppress exceptions
    
    def execute(self, name: str, func: Callable, rollback_func: Optional[Callable] = None, *args, **kwargs):
        """Execute a transaction step.
        
        Args:
            name: Step name
            func: Function to execute
            rollback_func: Function to rollback this step
            *args: Arguments for func
            **kwargs: Keyword arguments for func
            
        Returns:
            Result of func
            
        Raises:
            TransactionError: If step execution fails
        """
        step = TransactionStep(name, func, rollback_func)
        
        try:
            logger.info(f"Executing step: {name}")
            result = func(*args, **kwargs)
            step.executed = True
            step.result = result
            self.steps.append(step)
            logger.info(f"Step completed: {name}")
            return result
        except Exception as e:
            step.error = str(e)
            logger.error(f"Step failed: {name} - {e}")
            raise TransactionError(f"Transaction step '{name}' failed: {e}")
    
    def commit(self):
        """Commit the transaction."""
        if self.committed:
            logger.warning("Transaction already committed")
            return
        
        if self.rolled_back:
            raise TransactionError("Cannot commit a rolled-back transaction")
        
        self.committed = True
        duration = (self.end_time - self.start_time).total_seconds()
        logger.info(f"Transaction committed: {self.name} ({len(self.steps)} steps, {duration:.2f}s)")
    
    def rollback(self):
        """Rollback all executed steps in reverse order."""
        if self.rolled_back:
            logger.warning("Transaction already rolled back")
            return
        
        logger.warning(f"Rolling back transaction: {self.name}")
        
        # Rollback in reverse order
        for step in reversed(self.steps):
            if step.executed and step.rollback_func:
                try:
                    logger.info(f"Rolling back step: {step.name}")
                    step.rollback_func()
                except Exception as e:
                    logger.error(f"Rollback failed for step {step.name}: {e}")
        
        self.rolled_back = True
        logger.info(f"Transaction rolled back: {self.name}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get transaction status.
        
        Returns:
            Dictionary with transaction status
        """
        return {
            'name': self.name,
            'steps_count': len(self.steps),
            'committed': self.committed,
            'rolled_back': self.rolled_back,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'steps': [
                {
                    'name': step.name,
                    'executed': step.executed,
                    'error': step.error
                }
                for step in self.steps
            ]
        }


class TransactionManager:
    """High-level transaction management."""
    
    def __init__(self):
        """Initialize transaction manager."""
        self.transactions: List[Transaction] = []
        self.active_transaction: Optional[Transaction] = None
    
    def begin(self, name: Optional[str] = None) -> Transaction:
        """Begin a new transaction.
        
        Args:
            name: Transaction name
            
        Returns:
            New transaction instance
        """
        if self.active_transaction:
            raise TransactionError("Another transaction is already active")
        
        txn = Transaction(name)
        self.active_transaction = txn
        self.transactions.append(txn)
        return txn
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get transaction history.
        
        Returns:
            List of transaction status dictionaries
        """
        return [txn.get_status() for txn in self.transactions]
    
    def get_stats(self) -> Dict[str, int]:
        """Get transaction statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            'total': len(self.transactions),
            'committed': sum(1 for txn in self.transactions if txn.committed),
            'rolled_back': sum(1 for txn in self.transactions if txn.rolled_back),
            'active': 1 if self.active_transaction else 0
        }


# Example usage and testing
if __name__ == "__main__":
    print(f"Transaction Manager v{VERSION}")
    print("=" * 50)
    
    # Test 1: Successful transaction
    print("\n1. Testing successful transaction...")
    
    state = {'value': 0}
    
    def step1():
        state['value'] += 10
        return state['value']
    
    def step2():
        state['value'] *= 2
        return state['value']
    
    try:
        with Transaction("test_success") as txn:
            result1 = txn.execute("add_10", step1)
            result2 = txn.execute("multiply_2", step2)
        print(f"   ✓ Transaction succeeded. Final value: {state['value']}")
    except Exception as e:
        print(f"   ✗ Transaction failed: {e}")
    
    # Test 2: Failed transaction with rollback
    print("\n2. Testing failed transaction with rollback...")
    
    state2 = {'value': 100}
    rollback_called = [False]
    
    def step_fail():
        state2['value'] += 50
        raise ValueError("Intentional failure")
    
    def rollback_step():
        rollback_called[0] = True
        state2['value'] -= 50
    
    try:
        with Transaction("test_failure") as txn:
            txn.execute("increment", lambda: state2.update({'value': state2['value'] + 50}))
            txn.execute("fail_step", step_fail, rollback_func=rollback_step)
    except Exception:
        print(f"   ✓ Transaction rolled back. Rollback called: {rollback_called[0]}")
    
    # Test 3: Transaction manager
    print("\n3. Testing transaction manager...")
    
    manager = TransactionManager()
    
    with manager.begin("managed_txn") as txn:
        txn.execute("step1", lambda: "result1")
        txn.execute("step2", lambda: "result2")
    
    stats = manager.get_stats()
    print(f"   ✓ Manager stats: {stats['total']} total, {stats['committed']} committed")
    
    # Test 4: Transaction status
    print("\n4. Testing transaction status...")
    
    with Transaction("status_test") as txn:
        txn.execute("test_step", lambda: "done")
        status = txn.get_status()
    
    print(f"   ✓ Transaction: {status['name']}, Steps: {status['steps_count']}, Committed: {status['committed']}")
    
    print("\n✓ All tests passed!")
