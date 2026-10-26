# Extracted: Test a model in the API playground (Mistral Docs)

Source: https://docs.mistral.ai/getting-started/quickstarts/studio/test-model-playground

## Purpose

Use the Studio › Playground to send prompts to Mistral models, adjust generation parameters, and compare outputs, all without writing code.

- **Interactive testing**: type a prompt and get a response in seconds
- **Model comparison**: switch between models to see how outputs differ
- **Parameter tuning**: adjust temperature, max tokens, and other settings in real time

Goal: evaluate models and parameters before integrating them into your application.
**Time to complete:** ~5 minutes

## Prerequisites

- An active Studio account. Free mode is enabled by default with usage and rate limits.

## Step 1: Open the playground

1. Go to Studio.
2. Click **Playground** in the left sidebar.

The playground opens with a chat interface where you can interact with any available model.

## Step 2: Select a model and send a prompt

1. Open the **Model** dropdown at the top of the playground.
2. Select a model (e.g., `mistral-small-latest` for fast responses or `mistral-large-latest` for higher quality).
3. Type a prompt in the input field:

> Explain the difference between supervised and unsupervised learning in three sentences.

4. Click **Send** (or press Enter).

The response appears in the chat panel. Review the output for quality, accuracy, and style.

## Step 3: Adjust parameters and compare outputs

The right sidebar exposes generation parameters:

1. **Temperature**: controls randomness. Lower values (0.1) produce more deterministic outputs. Higher values (0.9) increase creativity.
2. **Max tokens**: limits response length. Set this to control cost and verbosity.
3. **Top P**: an alternative to temperature for controlling diversity.

Experiment:

1. Set **Temperature** to `0.1` and send the same prompt.
2. Set **Temperature** to `0.9` and send it again.
3. Compare: low temperature → more focused and consistent; high temperature → more variation.

Switch to a different model from the dropdown and send the same prompt to compare how models handle the same task.

## Verify

You have used the playground to:

1. Send a prompt to a Mistral model.
2. Adjust temperature and observe the effect on output.
3. Compare responses across different models.

Understanding model selection and parameters helps you make informed choices when building your application.

## What's next

- Create a reusable Prompt
- Create a Skill in Studio
- Send your first API request
- Studio overview
