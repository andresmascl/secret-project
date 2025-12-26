flowchart TB
    A[Bot Listens] --> C{Workflow Activation Keyword?}
    C -- Yes --> D[Bot Beeps]
    C -- No --> A

    D --> E{Context Flush Keyword?}
    E -- Yes --> F[Start New Session]
    E -- No --> G[Resume Session]

    F --> H[Send Prompt with Intent List and JSON Spec]
    G --> H

    H --> I[Open Socket and Stream Audio]
    I --> J[Stop Stream on Silence]

    J --> K[LLM Responds with JSON]
    K --> L[Bot Executes Automation and Speaks Response]

    L --> M[Sleep 7 Hours]
    M --> N[Delete Existing Sessions]
