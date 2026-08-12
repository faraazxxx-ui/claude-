# Contributing to the Optimized Prompt Framework

Thank you for your interest in improving this prompt framework! This guide will help you contribute effectively.

## 🎯 What Can You Contribute?

### 1. **Use Case Examples**
Share how you've used the prompt successfully in your field:
- Medical/healthcare applications
- Scientific research workflows  
- Data analysis pipelines
- Educational contexts
- Other domains

### 2. **Prompt Improvements**
Suggest enhancements to the core prompt:
- Better reasoning frameworks
- More effective data extraction methods
- Improved learning plan structures
- Additional tool-specific guidance

### 3. **Documentation Updates**
Help make the docs clearer:
- Fix typos or unclear explanations
- Add missing information
- Improve examples
- Translate to other languages

### 4. **Bug Reports**
Report when the prompt doesn't work as expected:
- Specific scenarios where output was poor
- Edge cases not handled well
- Confusing or contradictory responses

## 📝 How to Contribute

### Quick Improvements (No Coding)

**For small fixes:**
1. Fork this repository
2. Edit the relevant file directly on GitHub
3. Submit a pull request with clear description
4. We'll review and merge!

### Detailed Contributions

**For substantial changes:**

1. **Fork the Repository**
   ```bash
   # Click "Fork" button on GitHub
   git clone https://github.com/YOUR-USERNAME/claude-
   cd claude-
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-improvement-name
   ```

3. **Make Your Changes**
   - Edit relevant files
   - Follow existing formatting style
   - Add examples if applicable

4. **Test Your Changes**
   - Try the updated prompt with Copilot
   - Verify it produces better results
   - Check for unintended side effects

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "Brief description of improvement"
   git push origin feature/your-improvement-name
   ```

6. **Submit Pull Request**
   - Go to GitHub and create PR
   - Describe what you changed and why
   - Include example outputs if possible

## 🎨 Style Guidelines

### For Prompt Text (`copilot-optimized-prompt.md`)

**Do:**
- ✅ Use clear, action-oriented language
- ✅ Include concrete examples
- ✅ Provide reasoning for recommendations
- ✅ Structure with markdown headers and tables
- ✅ Test with actual Copilot usage

**Don't:**
- ❌ Use vague or ambiguous terms
- ❌ Add theoretical content without practical application
- ❌ Make claims without examples
- ❌ Break existing formatting patterns

### For Documentation Files

**Formatting:**
- Use markdown syntax consistently
- Include code blocks with proper language tags
- Add emojis for visual scanning (but not excessively)
- Break long paragraphs into shorter ones

**Content:**
- Start with clear purpose/goal
- Provide step-by-step instructions
- Include expected outputs
- Add troubleshooting sections

## 🧪 Testing Your Contributions

### Manual Testing Checklist

Before submitting prompt improvements:

- [ ] Test with GitHub Copilot in VS Code
- [ ] Try at least 3 different prompts using the framework
- [ ] Verify responses are more helpful than before
- [ ] Check for any confusing or contradictory guidance
- [ ] Ensure backward compatibility (old prompts still work)

### Example Testing Script

```
Test 1: Basic Learning Plan Request
Input: "@workspace Create learning plan for Python beginner"
Expected: Structured plan with timeline and resources
Actual: [Your result]

Test 2: Tool Comparison
Input: "@workspace Compare Google Cloud vs AWS for genomics"
Expected: Clear comparison table with use cases
Actual: [Your result]

Test 3: Gap Analysis
Input: "@workspace Analyze my skill gaps for data engineering"
Expected: Current vs target state with specific gaps
Actual: [Your result]
```

## 📊 What Makes a Good Contribution?

### High-Quality Examples

**Good Example Addition:**
```markdown
## Example: Bioinformatics Pipeline Setup

**User Request:**
"Help me set up BLAST analysis pipeline in Google Cloud for 10,000 sequences"

**Prompt Used:**
"@workspace Using the learning framework, guide me through setting up 
a BLAST pipeline in GCP for large-scale sequence analysis. I'm comfortable 
with biology but new to cloud infrastructure."

**Result:**
[Include actual helpful output Copilot provided]

**Why This Worked:**
- Specific domain context (bioinformatics)
- Clear scale (10,000 sequences)
- Acknowledged skill level (biology background, cloud newbie)
- Requested infrastructure guidance
```

**Poor Example Addition:**
```markdown
## Example: Cloud Setup

I asked Copilot about cloud stuff and it helped me.
```

### Useful Improvements

**Good Improvement:**
```markdown
### Change: Added branch-specific reasoning for different learning styles

**Before:** 
"Adapt teaching to user's learning style"

**After:**
"Identify learning style through questions, then:
- Visual learners → Include diagrams and flowcharts
- Kinesthetic learners → Hands-on exercises first
- Verbal learners → Analogies and detailed explanations
- Reading/writing learners → Documentation and written examples"

**Benefit:** More actionable guidance for Copilot to customize responses
```

**Poor Improvement:**
```markdown
Changed some wording to make it sound better.
```

## 🌟 Feature Requests

Have an idea but don't want to implement it yourself?

**Open an Issue:**
1. Go to GitHub Issues
2. Click "New Issue"
3. Use this template:

```markdown
## Feature Request: [Brief Title]

**Problem to Solve:**
[What current limitation or pain point does this address?]

**Proposed Solution:**
[How would you solve it? Be specific.]

**Example Use Case:**
[Concrete scenario where this would help]

**Alternatives Considered:**
[Other approaches that might work]

**Additional Context:**
[Anything else relevant]
```

## 🐛 Bug Reports

Found something not working correctly?

**Report It:**
1. Check existing issues first (might already be known)
2. Create new issue with this template:

```markdown
## Bug Report: [Brief Description]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Steps to Reproduce:**
1. [First step]
2. [Second step]
3. [And so on...]

**Copilot Prompt Used:**
```
[Exact prompt that caused issue]
```

**Copilot Response:**
```
[Actual response received]
```

**Environment:**
- VS Code version:
- Copilot version:
- Operating System:

**Additional Context:**
[Any other relevant information]
```

## 🎓 Domain-Specific Extensions

Want to create specialized version for your field?

**Process:**
1. Fork this repository
2. Create new file: `copilot-optimized-prompt-[DOMAIN].md`
   - Example: `copilot-optimized-prompt-genomics.md`
3. Customize for your domain:
   - Domain-specific tools
   - Field-relevant examples
   - Common workflows in your area
4. Add domain-specific docs:
   - `USAGE_EXAMPLES_[DOMAIN].md`
   - Tool guides for field
5. Submit PR or maintain as separate fork

**Suggested Domains:**
- Genomics/Bioinformatics
- Clinical Research
- Epidemiology
- Chemistry/Drug Discovery
- Physics/Engineering
- Social Sciences
- Business Analytics

## 🔄 Review Process

**Timeline:**
- Small fixes: Usually merged within 1-3 days
- Documentation updates: 3-5 days
- Prompt improvements: 5-10 days (needs testing)
- Major features: 2-3 weeks (extensive testing)

**Criteria for Acceptance:**
1. ✅ Clearly improves prompt effectiveness
2. ✅ Well-documented with examples
3. ✅ Tested with real Copilot usage
4. ✅ Maintains backward compatibility
5. ✅ Follows style guidelines
6. ✅ No contradictions with existing content

## 💬 Questions?

- **General questions:** Open a discussion on GitHub
- **Implementation help:** Comment on relevant issue/PR
- **Urgent concerns:** Tag repository maintainers

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (if file created)
- Mentioned in release notes for their contributions
- Credited in documentation where their examples are used

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as this project (to be determined by repository owner).

---

**Thank you for helping make this prompt framework better for everyone!**

## Quick Links

- [Main Prompt File](./copilot-optimized-prompt.md)
- [Usage Examples](./USAGE_EXAMPLES.md)
- [Quick Reference](./QUICK_REFERENCE.md)
- [User Template](./USER_TEMPLATE.md)
- [GitHub Issues](../../issues)
- [Pull Requests](../../pulls)
