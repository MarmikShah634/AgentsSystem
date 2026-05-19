# Task Plan Template

```json
{
  "plan_id": "<uuid>",
  "goal": "<human goal>",
  "created_at": "<iso8601>",
  "owner_agent": "planner",
  "steps": [
    {
      "step_id": "1",
      "agent": "coder",
      "skill": "implement-function",
      "category": "coding",
      "inputs": { "file_path": "src/foo.py", "function_spec": "..." },
      "expected_outputs": ["patch"],
      "depends_on": [],
      "test_pair": "2",
      "human_gate": false
    },
    {
      "step_id": "2",
      "agent": "tester",
      "skill": "generate-unit-test",
      "category": "testing",
      "inputs": { "target_path": "src/foo.py", "acceptance_criteria": "..." },
      "expected_outputs": ["test_file_path"],
      "depends_on": ["1"],
      "test_pair": null,
      "human_gate": false
    }
  ],
  "human_gates": []
}
```

## Invariants

- Every `coding` step has a `test_pair` pointing at a `testing` step.
- Steps form a DAG (no cycles in `depends_on`).
- Any step touching a sensitive surface sets `human_gate: true`.
