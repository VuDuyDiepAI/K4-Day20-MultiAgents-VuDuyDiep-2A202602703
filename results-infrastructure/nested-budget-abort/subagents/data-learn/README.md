# Interrupted learning attempt

The non-thinking subagent data-learn attempt was interrupted before a final record existed. The parent was invoked with recursion_limit=60, but installed langchain/deepagents child graphs bind recursion_limit=9999 and their bound config takes precedence. A nested agent kept issuing model requests after the intended parent step budget.

No score or token total is claimed for this unfinished attempt. It is excluded from the official comparison. A shared 180-second wall-clock deadline was added within the runner TODO function before rerunning the task. All previously finalized non-thinking learning runs finished below that deadline; their outputs are retained. The final report must disclose the guard introduction and the missing cost of this interrupted attempt.
