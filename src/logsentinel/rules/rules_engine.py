"""
Rules engine for executing security rules.

This module provides the main rules engine for evaluating security rules.
"""

from typing import List, Optional, Iterator
from datetime import datetime

from .base import Rule, RuleResult
from ..parsers import LogEntry


class RulesEngine:
    """
    Engine for executing security rules against log entries.
    
    This class follows the Single Responsibility Principle by focusing solely on
    rule execution and management.
    """
    
    def __init__(self, rules: Optional[List[Rule]] = None):
        """
        Initialize the rules engine.
        
        Args:
            rules: Optional list of rules to initialize with
        """
        self.rules = rules or []
    
    def add_rule(self, rule: Rule) -> None:
        """
        Add a rule to the engine.
        
        Args:
            rule: Rule to add
        """
        self.rules.append(rule)
    
    def remove_rule(self, rule_id: str) -> bool:
        """
        Remove a rule from the engine.
        
        Args:
            rule_id: ID of the rule to remove
            
        Returns:
            True if rule was removed, False if not found
        """
        for i, rule in enumerate(self.rules):
            if rule.rule_id == rule_id:
                del self.rules[i]
                return True
        return False
    
    def get_rule(self, rule_id: str) -> Optional[Rule]:
        """
        Get a rule by ID.
        
        Args:
            rule_id: ID of the rule to get
            
        Returns:
            Rule if found, None otherwise
        """
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None
    
    def evaluate_log_entry(self, log_entry: LogEntry) -> List[RuleResult]:
        """
        Evaluate all rules against a log entry.
        
        Args:
            log_entry: Log entry to evaluate
            
        Returns:
            List of rule results that matched
        """
        results = []
        
        for rule in self.rules:
            if rule.is_enabled():
                result = rule.evaluate(log_entry)
                if result:
                    results.append(result)
        
        return results
    
    def evaluate_log_entries(self, log_entries: Iterator[LogEntry]) -> List[RuleResult]:
        """
        Evaluate all rules against multiple log entries.
        
        Args:
            log_entries: Iterator of log entries to evaluate
            
        Returns:
            List of all rule results that matched
        """
        all_results = []
        
        for log_entry in log_entries:
            results = self.evaluate_log_entry(log_entry)
            all_results.extend(results)
        
        return all_results
    
    def get_enabled_rules(self) -> List[Rule]:
        """
        Get all enabled rules.
        
        Returns:
            List of enabled rules
        """
        return [rule for rule in self.rules if rule.is_enabled()]
    
    def get_rules_by_severity(self, severity: str) -> List[Rule]:
        """
        Get rules by severity level.
        
        Args:
            severity: Severity level to filter by
            
        Returns:
            List of rules with the specified severity
        """
        return [rule for rule in self.rules if rule.severity == severity]
    
    def get_rule_count(self) -> int:
        """
        Get the total number of rules.
        
        Returns:
            Number of rules
        """
        return len(self.rules)
    
    def get_enabled_rule_count(self) -> int:
        """
        Get the number of enabled rules.
        
        Returns:
            Number of enabled rules
        """
        return len(self.get_enabled_rules())
