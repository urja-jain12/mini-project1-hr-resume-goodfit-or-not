# HR Resume Good-Fit Analyzer

An AI-powered tool that helps recruiters quickly understand whether a candidate's resume matches the requirements of a job.

## What does this project do?

Imagine a recruiter has a job description with several requirements and receives a candidate's resume.

Instead of manually comparing every requirement with the resume, this project uses AI to perform the initial comparison automatically.

It reads:

- The candidate's resume
- The HR/job requirements

and produces a structured analysis showing:

- Skills found in the resume
- Relevant experience found
- Relevant projects found
- Requirements that match
- Requirements that are missing
- Overall match percentage

In simple words:

> It answers the question: "How well does this candidate's resume fit the given job requirements?"

---

## Why did I build this?

Recruiters may have to review a large number of resumes for a single position.

Manually checking every resume against every requirement can be time-consuming.

This project explores how Generative AI and structured output can be used to make the initial resume screening process faster and more organized.

It is designed as an initial screening assistant, not as a replacement for a recruiter's final decision.

---

## How it works

The process is simple:

```text
             HR Requirements
                    +
             Candidate Resume
                    |
                    v
               AI Analysis
                    |
                    v
          +---------------------+
          |   Resume Analysis   |
          +---------------------+
          | Skills Found        |
          | Experience Found    |
          | Projects Found      |
          | Matched Requirements|
          | Missing Requirements|
          | Match Percentage    |
          +---------------------+
