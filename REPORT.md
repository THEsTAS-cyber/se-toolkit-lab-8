# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent
Q1:
The agentic loop is the fundamental cycle that autonomous AI agents follow to accomplish tasks. It's the core reasoning and action pattern that enables      
agents to work independently toward goals.

The Basic Loop


 Perceive → Reason → Act → Observe → (repeat)


1. Perceive

The agent gathers information about its environment:

 • Reads user input/requests
 • Observes current state (files, system status, etc.)
 • Collects relevant context

2. Reason

The agent processes information and plans:

 • Analyzes the goal and constraints
 • Breaks down complex tasks into steps
 • Decides which tools/actions to use
 • Considers potential outcomes

3. Act

The agent executes its decision:

 • Calls tools (file operations, web searches, shell commands, etc.)
 • Makes changes to the environment
 • Communicates with users or other systems

4. Observe

The agent evaluates results:

 • Checks if the action succeeded
 • Analyzes outputs and errors
 • Determines if the goal is achieved or if more steps are needed

Why It Matters

This loop enables autonomy — the agent can:

 • Handle multi-step tasks without constant guidance
 • Adapt when things go wrong (error recovery)
 • Make decisions based on real-time feedback
 • Continue working until the goal is achieved

Example

For a task like "create a README for my project":

 1 Perceive: List directory contents, check for existing docs
 2 Reason: Determine what info is needed, plan README structure
 3 Act: Write the README.md file
 4 Observe: Verify file was created successfully → Done!

This loop is what distinguishes agents from simple chatbots — agents can take actions, observe outcomes, and iterate toward goals.

                                                                                                                                                      
Q2:
Based on my exploration, here are the available labs in your LMS:

Required Labs (Lab 8)

 1 Task 1 - Set Up the Agent: Install nanobot, configure Qwen API, add MCP tools, write skill prompt
 2 Task 2 - Deploy and Connect a Web Client: Dockerize nanobot, add WebSocket channel + Flutter chat UI
 3 Task 3 - Give the Agent New Eyes: Explore observability data, write log/trace MCP tools
 4 Task 4 - Diagnose a Failure and Make the Agent Proactive: Investigate a failure, schedule in-chat health checks, fix a planted bug

Optional Labs

 1 Task 1 - Add a Telegram Bot Client: Same agent, different interface

This is Lab 8 — "The Agent is the Interface", where you'll build an AI agent (nanobot) as a natural-language interface to the LMS system. The lab focuses on:

 • Setting up nanobot from scratch
 • Building MCP tools for the agent
 • Creating a web chat client
 • Adding observability capabilities
 • Making the agent proactive with scheduled health checks

Would you like me to read the details of any specific task?

## Task 1B — Agent with LMS tools
Q1:
Here are the available labs:

 1 Lab 01 – Products, Architecture & Roles
 2 Lab 02 — Run, Fix, and Deploy a Backend Service
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4 Lab 04 — Testing, Front-end, and AI Agents
 5 Lab 05 — Data Pipeline and Analytics Dashboard
 6 Lab 06 — Build Your Own Agent
 7 Lab 07 — Build a Client with an AI Coding Agent
 8 lab-08

Is there a specific lab you'd like to explore or get more information about?                                                                                                                                                   

Q2:
Yes, the LMS backend is healthy ✅

 • Status: healthy
 • Item count: 56
 • Errors: none


## Task 1C — Skill prompt

Here are the scores for all labs:

📊 Lab Scores Overview

Lab 01 – Products, Architecture & Roles


 Task                                        Avg Score  Attempts
 ───────────────────────────────────────────────────────────────
 Lab setup                                   84.2%      3,135
 Task 0: Practice the Git workflow           64.5%      306
 Task 1: Product & architecture description  55.1%      161
 Task 2: Roles and skills mapping            49.8%      83
 Optional: Resolve a merge conflict          34.6%      13
 Optional: Create a release                  60.0%      5
 Optional: Add a CI check                    42.9%      7
 Optional: Plan skill development            20.0%      5


Lab 02 – Run, Fix, and Deploy a Backend Service


 Task                                            Avg Score  Attempts
 ───────────────────────────────────────────────────────────────────
 Task 1: Run the web server                      67.9%      210
 Task 2: Identify, report, and fix a bug         66.7%      216
 Task 4: Deploy the web server to the VM         56.2%      84
 Optional 3: Implement the post-order traversal  62.5%      6
 Optional 1: Implement the /outcomes endpoint    36.4%      11
 Optional 2: Make your VM a proxy                0.0%       3


Lab 03 – Backend API: Explore, Debug, Implement, Deploy


 Task                                                Avg Score  Attempts
 ───────────────────────────────────────────────────────────────────────
 Task 2: Enable and debug the interactions endpoint  66.4%      299
 Task 1: Explore the API                             63.5%      382
 Task 4: Deploy to a hardened VM                     43.9%      110
 Optional 2: Set up CI with GitHub Actions           44.0%      5
 Task 3: Implement the learners endpoint             50.0%      4


Lab 04 – Testing, Front-end, and AI Agents


 Task                                          Avg Score  Attempts
 ─────────────────────────────────────────────────────────────────
 Task 3: Add Front-end                         68.8%      4
 Task 1: Observe System Component Interaction  60.9%      686
 Task 2: Back-end Testing                      59.9%      753
 Optional 1: CI/CD with GitHub Actions         33.8%      17


Lab 05 – Data Pipeline and Analytics Dashboard


 Task                             Avg Score  Attempts
 ────────────────────────────────────────────────────
 Task 3: Dashboard Front-end      74.1%      21
 Task 1: Build the Data Pipeline  73.5%      626
 Task 2: Analytics Endpoints      64.4%      629
 Optional 1: Grafana Dashboard    57.2%      60


Lab 06 – Build Your Own Agent


 Task                             Avg Score  Attempts
 ────────────────────────────────────────────────────
 Task 2: The Documentation Agent  73.9%      425
 Task 1: Call an LLM from Code    61.1%      680
 Task 3: The System Agent         42.8%      2,053


Lab 07 – Build a Client with an AI Coding Agent


 Task                                           Avg Score  Attempts
 ──────────────────────────────────────────────────────────────────
 Task 1: Plan and Scaffold                      76.9%      755
 Task 2: Backend Integration                    66.8%      564
 Task 4: Containerize and Document              66.6%      680
 Task 3: Intent-Based Natural Language Routing  58.9%      734


Lab 08 – lab-08

No scores available yet (no submissions).

-------------------------------------------------------------------------------------------------------------------------------------------------------------

Summary: Lab 07 has the highest average scores overall, with Task 1 reaching 76.9%. Lab 05 also shows strong performance. Lab 08 appears to be new with no   
submissions yet.

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
