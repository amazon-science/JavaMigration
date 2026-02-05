"""Hooks for monitoring and controlling agent behavior."""

import json
import logging

from strands.experimental.hooks import (
    AfterModelInvocationEvent,
    AfterToolInvocationEvent,
    BeforeModelInvocationEvent,
    BeforeToolInvocationEvent,
)
from strands.hooks import HookProvider, HookRegistry


class ToolLoggingHook(HookProvider):
    """Concise hook to log tool invocations to file."""

    def __init__(self, log_file: str = "tool_logs.log"):
        """
        Initialize the tool logging hook.

        Args:
            log_file: Path to log file
        """
        self.logger = logging.getLogger("ToolLogger")
        if not self.logger.handlers:
            handler = logging.FileHandler(log_file)
            handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def get_turn_number(self, invocation_state) -> int:
        """
        Get the current turn number from invocation state.

        Args:
            invocation_state: State of the invocation

        Returns:
            Turn number
        """
        messages = invocation_state.get("messages", [])
        return sum(1 for msg in messages if msg.get("role") == "user")

    def register_hooks(self, registry: HookRegistry) -> None:
        """Register callbacks with the hook registry."""
        registry.add_callback(BeforeToolInvocationEvent, self.log_before)
        registry.add_callback(AfterToolInvocationEvent, self.log_after)

    def log_before(self, event: BeforeToolInvocationEvent) -> None:
        """Log before tool invocation."""
        data = {
            "event": "BEFORE",
            "turn": self.get_turn_number(dict(event.invocation_state)),
            "tool_name": event.tool_use.get("name"),
            "tool_use": dict(event.tool_use),
        }
        self.logger.info(json.dumps(data, default=str))

    def log_after(self, event: AfterToolInvocationEvent) -> None:
        """Log after tool invocation."""
        data = {
            "event": "AFTER",
            "turn": self.get_turn_number(dict(event.invocation_state)),
            "tool_name": event.tool_use.get("name"),
            "tool_use": dict(event.tool_use),
            "result": str(event.result),
            "exception": str(event.exception) if event.exception else None,
        }
        self.logger.info(json.dumps(data, default=str))


class MaxMessageLimitException(Exception):
    """Exception raised when the agent reaches the maximum conversation turn limit."""

    def __init__(self, message: str):
        """
        Initialize the exception.

        Args:
            message: Error message
        """
        super().__init__(message)


class MessageLimitHook(HookProvider):
    """Hook to limit the maximum number of messages in a conversation."""

    def __init__(self, max_messages: int):
        """
        Initialize the message limit hook.

        Args:
            max_messages: Maximum number of messages allowed
        """
        self.max_messages = max_messages

    def register_hooks(self, registry: HookRegistry) -> None:
        """Register callbacks with the hook registry."""
        registry.add_callback(AfterModelInvocationEvent, self.check_message_limit)

    def check_message_limit(self, event: AfterModelInvocationEvent) -> None:
        """
        Check if message limit has been exceeded.

        Args:
            event: After model invocation event

        Raises:
            MaxMessageLimitException: If message limit is exceeded
        """
        if len(event.agent.messages) / 2 >= self.max_messages:
            raise MaxMessageLimitException(
                f"Message limit of {self.max_messages} exceeded."
            )
