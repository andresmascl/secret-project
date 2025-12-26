---
config:
  theme: neo
---
flowchart TB
    A(["Bot Listens"]) --> C["Bot Detects Workflow Activation Keyword"]
    C -- Si --> n4["Bot **Beeps**"]
    n1["Bot Detects Keyword for Context Flush"] -- Yes --> n2["Bot Starts New Session"]
    n2 --> n3["Bot Sends Current Prompt w/ Intent List and Json Response Spec"]
    n4 --> n1
    C -- No --> A
    n3 --> n5["Bot Opens Socket and Starts Sending Audio"]
    n1 -- No --> n6["Bot Tries to Resume Session"]
    n6 --> n3
    n5 --> n7["Bot Stops Stream When it Detects Silence"]
    n11["LLM Sends Json w/ Detected Intent, Targets &amp; Feedback Text"] --> n15["Bot Transforms TTS, Speaks Back to User, &amp; Executes Automation"]
    n7 --> n17["LLM Reads Prompt &amp; Responds in Instructed Json Format"]
    n15 --> n20["Bot Sleeps 7 hrs."]
    n20 --> n21["Bot Deletes Existing Sessionss"]
    n17 --> n11
    n18["Yellow = Local Bot executes"]
    n19["Green = Cloud LLM executes"]

    C@{ shape: diam}
    n1@{ shape: diam}
    n7@{ shape: rect}
    n17@{ shape: rect}
    n18@{ shape: rect}
    n19@{ shape: rect}
    style A stroke:#FFD600
    style C stroke:#FFD600
    style n4 stroke:#FFD600
    style n1 stroke:#FFD600
    style n2 stroke:#FFD600
    style n3 stroke:#FFD600
    style n5 stroke:#FFD600
    style n6 stroke:#FFD600
    style n7 stroke:#FFD600
    style n11 stroke:#00C853
    style n15 stroke:#FFD600
    style n17 stroke:#00C853
    style n20 stroke:#FFD600
    style n21 stroke:#FFD600
    style n18 stroke:#FFD600
    style n19 stroke:#00C853