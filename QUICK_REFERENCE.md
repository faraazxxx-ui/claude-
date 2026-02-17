# Quick Reference Guide

## 🚀 One-Minute Setup

1. Open your project in VS Code with GitHub Copilot enabled
2. Copy the content from `copilot-optimized-prompt.md`
3. Create `.github/copilot-instructions.md` in your project
4. Paste the prompt content
5. Start using: `@workspace [your learning request]`

## 💬 Sample Prompts to Get Started

### For Learning Plan Generation
```
@workspace Using the learning assistant framework, create a personalized 
learning plan to help me master [TOOL] for [PURPOSE]. My background: 
[DESCRIPTION]. Current skill level: [LEVEL].
```

### For Gap Analysis
```
@workspace Analyze the gap between my current capabilities and what I need 
to achieve [GOAL]. Extract patterns from my previous work and identify 
specific missing skills.
```

### For Tool Comparison
```
@workspace Explain the differences between [TOOL A] and [TOOL B] in the 
context of [MY USE CASE]. Which should I use and why?
```

### For Step-by-Step Guidance
```
@workspace I need to [SPECIFIC TASK] using [TOOL]. Provide exact, executable 
steps tailored to my background as a [PROFESSION] who prefers [LEARNING STYLE].
```

## 🎯 Key Concepts

### What Makes This Prompt Different

| Feature | Traditional Prompt | Optimized Prompt |
|---------|-------------------|------------------|
| Approach | One-size-fits-all | Personalized to verbal thinkers |
| Depth | Surface explanations | Evidence-based gap analysis |
| Structure | Ad-hoc responses | Systematic learning paths |
| Output | Technical jargon | Analogies + practical steps |
| Follow-up | Isolated answers | Iterative improvement |

### Prompting Strategy

**DO:**
- ✅ Provide context about your background and learning style
- ✅ Specify your end goal clearly
- ✅ Mention tools you're comfortable/uncomfortable with
- ✅ Request specific formats (checklist, table, steps)
- ✅ Ask for analogies if concepts are unclear

**DON'T:**
- ❌ Assume AI knows your skill level
- ❌ Ask vague questions without context
- ❌ Skip mentioning relevant past experiences
- ❌ Ignore follow-up clarification questions

## 🔧 Tool-Specific Quick Commands

### Google Cloud
```bash
# Initial setup
gcloud init
gcloud config set project YOUR_PROJECT_ID

# Common operations
gcloud projects list
gcloud services enable SERVICE_NAME
gcloud functions deploy FUNCTION_NAME
```

### GitHub
```bash
# Basic workflow
git clone REPO_URL
git add .
git commit -m "Description"
git push origin main

# Check status
git status
git log --oneline
```

### VS Code + Copilot
```
# In Copilot Chat:
@workspace explain [CODE/CONCEPT]
@workspace fix [ERROR]
/help - Show all available commands
```

## 📊 Success Checklist

Use this to track your progress:

- [ ] Understood my learning style and verbal thinking strengths
- [ ] Identified specific capability gaps
- [ ] Created personalized learning plan with timeline
- [ ] Completed first hands-on exercise for each priority tool
- [ ] Successfully executed basic workflow independently
- [ ] Adapted examples to my research/work context
- [ ] Built confidence to explore advanced features

## 🆘 Troubleshooting

### "The prompt isn't working in Copilot"
- Ensure `.github/copilot-instructions.md` exists in project root
- Try `@workspace` prefix before requests
- Check Copilot is enabled and authenticated

### "Responses are too technical"
- Add to your prompt: "Explain like I'm a [YOUR PROFESSION], not a developer"
- Request analogies: "Use medical/research analogies"
- Ask for step-by-step: "Break this into smaller steps"

### "I'm stuck on a specific step"
- Describe exactly where you're stuck
- Share the error message or unexpected result
- Ask: "What are alternative approaches?"

## 📖 Learning Resources by Tool

### Google Cloud
- [GCP Console](https://console.cloud.google.com) - Web interface
- [Cloud SDK](https://cloud.google.com/sdk) - Command-line tools
- [BigQuery](https://cloud.google.com/bigquery) - For large datasets
- [Cloud Functions](https://cloud.google.com/functions) - Serverless code

### GitHub
- [GitHub Desktop](https://desktop.github.com) - GUI for beginners
- [Git Basics](https://git-scm.com/doc) - Official documentation
- [GitHub Skills](https://skills.github.com) - Interactive tutorials

### VS Code
- [Copilot Chat](https://docs.github.com/copilot/using-github-copilot/asking-github-copilot-questions) - AI pair programmer
- [Extensions](https://marketplace.visualstudio.com/vscode) - Add functionality
- [Keyboard Shortcuts](https://code.visualstudio.com/shortcuts) - Efficiency tips

## 🎓 Pro Tips

1. **Start Small**: Master one tool before combining multiple
2. **Use Analogies**: Connect new concepts to familiar domains
3. **Practice Daily**: 15-minute exercises beat 3-hour weekly sessions
4. **Document Wins**: Keep a log of successful commands/workflows
5. **Ask "Why"**: Understand reasoning, not just memorize steps
6. **Iterate**: Refine your prompts based on what works

## 📞 Getting Better Results

### Effective Prompt Formula
```
[Context: who you are + current situation]
+
[Goal: what you want to achieve]
+
[Constraints: time, experience level, preferences]
+
[Format: how you want the answer delivered]
```

### Example
```
I'm a physician-researcher (context) who needs to process 100GB genomics 
datasets using Google Cloud BigQuery (goal). I have 2 weeks and prefer 
step-by-step guides over theory (constraints). Please provide a checklist 
with exact commands and expected outputs (format).
```

## 🔄 Feedback Loop

After using the prompt:
1. What worked well?
2. What was confusing?
3. What's missing?
4. How can it be improved for your use case?

Use these insights to refine your future prompts!

---

**Remember**: This is a framework, not a script. Adapt it to your needs, experiment with variations, and find what works best for your learning style.
