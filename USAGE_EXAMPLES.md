# Usage Examples

This document provides concrete examples of how to use the optimized prompt with GitHub Copilot for different scenarios.

## Example 1: First-Time User Setup

### User Request
```
@workspace I'm a physician-researcher who wants to start using GitHub for 
managing my research code. I've never used version control before. Using the 
learning assistant framework, create a beginner-friendly learning plan.
```

### Expected Copilot Response
```markdown
# GitHub Learning Plan for Research Code Management

## 🎯 Your Profile
- **Background**: Physician-researcher
- **Current State**: No version control experience
- **Learning Style**: Practical, step-by-step preferred
- **Goal**: Manage research code with GitHub

## 📊 Gap Analysis

| Current | Target | Gap | Priority |
|---------|--------|-----|----------|
| Manual file copies | Version control | Git basics | HIGH |
| Local-only code | Collaborative repository | GitHub workflow | HIGH |
| No change tracking | Full history | Commit discipline | MEDIUM |

## 🛤️ Week-by-Week Plan

### Week 1: Foundation
**Goal**: Understand what version control is and why it matters

- [ ] Day 1: Install GitHub Desktop (GUI tool, no command line needed)
  - Download from: https://desktop.github.com
  - Launch and sign in with GitHub account
  
- [ ] Day 2: Create first repository
  - Click "Create New Repository"
  - Name: "research-project-test"
  - Initialize with README
  
- [ ] Day 3: Make your first commit
  - Add a file: `analysis.py` with basic code
  - Write commit message: "Add initial analysis script"
  - Click "Commit to main"

**Analogy**: Version control is like patient medical records - you track every 
change, who made it, and why. You can always review history or revert if needed.

### Week 2: Daily Workflow
[Continue with specific steps...]
```

---

## Example 2: Tool Comparison Request

### User Request
```
@workspace I currently use the Gemini app for data analysis questions. 
I've heard Google Cloud is more powerful. Using the framework, explain 
the differences and when I should use each for my genomics research.
```

### Expected Copilot Response
```markdown
# Gemini App vs Google Cloud for Genomics Research

## 🔍 Quick Comparison

| Aspect | Gemini App | Google Cloud Platform |
|--------|-----------|----------------------|
| **What it is** | Conversational AI | Full computing infrastructure |
| **Data size limit** | Small datasets (MB) | Unlimited (petabytes) |
| **Processing power** | Single-user allocation | Scalable compute clusters |
| **Cost** | Free tier available | Pay for resources used |
| **Setup complexity** | None (just login) | Moderate (account, project, billing) |
| **Best for** | Quick queries, ideation | Production pipelines, large datasets |

## 🎯 When to Use Each

### Use Gemini App When:
✅ Exploring ideas: "How should I approach this analysis?"
✅ Quick questions: "What statistical test should I use?"
✅ Learning concepts: "Explain PCA for genomics"
✅ Drafting code: "Write Python code to parse FASTA files"
✅ Small datasets: Under 100MB, exploratory analysis

**Example**: You have a 50MB CSV of patient outcomes and want to explore 
correlations. Gemini can help you understand the data and draft initial code.

### Use Google Cloud When:
✅ Large-scale processing: 100GB+ genomics files
✅ Production pipelines: Automated, repeatable workflows
✅ Team collaboration: Multiple researchers accessing same data
✅ Advanced ML: Training models on large datasets
✅ Long-running jobs: Hours/days of computation

**Example**: You have 500GB of whole-genome sequencing data that needs 
variant calling across 1000 samples. This requires BigQuery for querying, 
Cloud Storage for files, and Compute Engine for processing.

## 🔄 Optimal Workflow: Use Both Together

1. **Ideation** (Gemini): "How should I design my variant analysis pipeline?"
2. **Planning** (Gemini): "What Google Cloud services do I need?"
3. **Setup** (Cloud): Create project, enable APIs, configure storage
4. **Coding** (Gemini + Cloud): Draft code in Gemini, deploy to Cloud Functions
5. **Execution** (Cloud): Run pipeline on large dataset
6. **Troubleshooting** (Gemini): "Why am I getting this Cloud error?"

## 📋 Migration Path: Gemini → Cloud

### Step 1: Start with Cloud Shell (Week 1)
- Access Cloud directly from browser
- Try BigQuery with sample datasets
- No local setup needed

### Step 2: Deploy First Function (Week 2)
- Take Python code drafted in Gemini
- Deploy as Cloud Function
- Process small dataset

### Step 3: Scale Up (Week 3-4)
- Move larger files to Cloud Storage
- Run batch processing jobs
- Monitor costs and optimize
```

---

## Example 3: Gap Analysis and Learning Path

### User Request
```
@workspace Analyze my GitHub commit history and VS Code usage patterns. 
Identify gaps in my workflow and suggest improvements for better efficiency.
```

### Expected Copilot Response
```markdown
# Workflow Analysis & Improvement Plan

## 📊 Current Workflow Analysis

**Patterns Detected from Commit History:**
- Commits every 2-3 days (irregular cadence)
- Generic commit messages: "update", "fix", "changes"
- No branching (all commits to main)
- Large commits with many file changes
- No pull requests or code reviews

**Patterns Detected from VS Code Usage:**
- Manual file navigation (not using search)
- Copy-paste heavy editing
- No keyboard shortcuts usage
- Single file view (not split editor)
- Limited extension usage

## 🎯 Identified Gaps

| Category | Current Practice | Best Practice | Impact |
|----------|-----------------|---------------|--------|
| **Commits** | Irregular, large | Small, frequent | Better history tracking |
| **Messages** | Generic | Descriptive | Easier to find changes |
| **Branching** | None | Feature branches | Safe experimentation |
| **Navigation** | Manual clicking | Cmd+P search | 10x faster file access |
| **Editing** | Copy-paste | Multi-cursor | Batch edits |

## 🚀 Improvement Plan

### This Week: Core Habits

1. **Better Commit Practice** (Days 1-3)
   - [ ] Commit after each logical change (30min-1hr work)
   - [ ] Use format: `[TYPE] Description`
     - Types: `[DATA]` `[ANALYSIS]` `[FIX]` `[DOCS]`
   - Example: `[ANALYSIS] Add PCA dimensionality reduction`
   
2. **Keyboard Shortcuts** (Days 4-5)
   - [ ] Cmd+P / Ctrl+P: Quick file search
   - [ ] Cmd+Shift+F: Search across all files
   - [ ] Alt+Click: Multi-cursor editing
   - [ ] Cmd+D: Select next occurrence
   
3. **VS Code Extensions** (Days 6-7)
   - [ ] Install: Python (by Microsoft)
   - [ ] Install: GitLens (see commit history inline)
   - [ ] Install: Copilot (if not already active)

### Next Two Weeks: Advanced Workflow

4. **Branching Workflow** (Week 2)
   - [ ] Create feature branch: `git checkout -b feature-name`
   - [ ] Make commits on branch
   - [ ] Merge back to main: `git merge feature-name`
   
5. **Efficiency Boost** (Week 3)
   - [ ] Learn split editor: Cmd+\
   - [ ] Use integrated terminal: Cmd+`
   - [ ] Create code snippets for common patterns

## 📈 Expected Results

After 3 weeks:
- ✅ 3x more frequent commits with clear history
- ✅ 50% faster file navigation
- ✅ Safe experimentation with branches
- ✅ Easier collaboration with better commit messages
- ✅ More efficient editing with shortcuts

## 🔍 Self-Assessment

Check these weekly:
- [ ] Week 1: Using Cmd+P instead of file explorer?
- [ ] Week 2: Making small, focused commits?
- [ ] Week 3: Creating branches for new features?
```

---

## Example 4: Specific Technical Problem

### User Request
```
@workspace I need to process 200GB of clinical trial data stored in CSV files 
using Google Cloud BigQuery. I've never used BigQuery before. Give me exact 
steps from account setup to running my first query.
```

### Expected Copilot Response
```markdown
# BigQuery Quick Start for Clinical Trial Data

## ✅ Prerequisites Check

- [ ] Google account (Gmail or organizational)
- [ ] Credit card for billing (free tier available, ~$300 credit)
- [ ] CSV files ready (location accessible)

## 🚀 Step-by-Step Setup

### Phase 1: Account Setup (15 minutes)

**Step 1: Create Google Cloud Account**
1. Go to: https://console.cloud.google.com
2. Click "Get started for free"
3. Sign in with Google account
4. Enter billing information (won't charge during free tier)
5. Click "Start my free trial"

**Step 2: Create Project**
1. In Cloud Console, click project dropdown (top left)
2. Click "New Project"
3. Name: `clinical-trial-analysis`
4. Click "Create"
5. Wait for project to be created (~30 seconds)

**Step 3: Enable BigQuery API**
1. Go to: Navigation menu (☰) → BigQuery
2. If prompted, click "Enable BigQuery API"
3. Wait for API to be enabled

### Phase 2: Data Upload (30 minutes)

**Step 4: Create Cloud Storage Bucket**
```bash
# In Cloud Shell (click >_ icon at top right):
gsutil mb gs://clinical-trial-data-bucket-YOUR-NAME
```

**Step 5: Upload CSV Files**
```bash
# Upload from local computer
gsutil -m cp -r /path/to/csv/files/* gs://clinical-trial-data-bucket-YOUR-NAME/

# Or use Web UI:
# 1. Go to: Navigation menu → Cloud Storage → Buckets
# 2. Click your bucket name
# 3. Click "Upload files"
# 4. Select your CSV files
```

**Step 6: Create BigQuery Dataset**
```bash
bq mk --dataset --location=US clinical_trials
```

**Step 7: Load CSV into BigQuery Table**
```bash
bq load \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --autodetect \
  clinical_trials.patient_data \
  gs://clinical-trial-data-bucket-YOUR-NAME/patients.csv
```

### Phase 3: First Query (5 minutes)

**Step 8: Run Analysis Query**

1. Go to: BigQuery Console
2. Click "Compose New Query"
3. Paste this example query:

```sql
-- Count patients by treatment group
SELECT 
  treatment_group,
  COUNT(*) as patient_count,
  AVG(age) as avg_age,
  AVG(outcome_score) as avg_outcome
FROM 
  `clinical_trials.patient_data`
GROUP BY 
  treatment_group
ORDER BY 
  treatment_group;
```

4. Click "Run"
5. View results in bottom pane

### Phase 4: Common Queries for Clinical Trials

**Filter by Date Range**
```sql
SELECT * FROM `clinical_trials.patient_data`
WHERE enrollment_date BETWEEN '2023-01-01' AND '2023-12-31';
```

**Calculate Statistics**
```sql
SELECT 
  treatment_group,
  COUNT(*) as n,
  AVG(outcome_score) as mean,
  STDDEV(outcome_score) as std_dev,
  MIN(outcome_score) as min,
  MAX(outcome_score) as max
FROM `clinical_trials.patient_data`
GROUP BY treatment_group;
```

**Export Results**
```sql
# Save query results to Cloud Storage:
bq extract \
  --destination_format=CSV \
  --compression=GZIP \
  clinical_trials.results_table \
  gs://clinical-trial-data-bucket-YOUR-NAME/results/results-*.csv
```

## 💰 Cost Estimate

For 200GB data:
- **Storage**: ~$4/month (BigQuery active storage)
- **Queries**: First 1TB/month free, then $5/TB
- **Expected**: ~$0-10/month for typical research usage

## ⚠️ Best Practices

1. **Use `LIMIT` for testing**: Add `LIMIT 100` to queries while developing
2. **Partition large tables**: By date for faster queries
3. **Monitor costs**: Set up budget alerts at $50/month
4. **Schedule queries**: For recurring analyses

## 🆘 Troubleshooting

**Error: "Permission denied"**
→ Ensure BigQuery API is enabled in project

**Error: "Exceeded rate limits"**
→ Add delays between rapid queries or use batch processing

**Query taking too long**
→ Add WHERE clause to filter data, or partition table by date

## 📚 Next Steps

- [ ] Load all CSV files into separate tables
- [ ] Join tables for cross-analysis
- [ ] Create scheduled queries for daily reports
- [ ] Export results to Data Studio for visualization
```

---

## Example 5: Debugging and Problem Solving

### User Request
```
@workspace I'm getting an error when trying to deploy a Cloud Function. 
The error is "ERROR: (gcloud.functions.deploy) ResponseError: status=[7], 
code=[Forbidden], message=[The caller does not have permission]". 
What's wrong and how do I fix it?
```

### Expected Copilot Response
```markdown
# Debugging: Cloud Function Permission Error

## 🔍 Error Analysis

**Error Type**: Permission/Authorization
**Cause**: Your account lacks necessary IAM roles to deploy Cloud Functions

## 🛠️ Solution Steps

### Step 1: Verify You're Using Correct Project
```bash
# Check current project
gcloud config get-value project

# If wrong project, set correct one:
gcloud config set project YOUR-PROJECT-ID
```

### Step 2: Check Your IAM Roles
```bash
# List your current permissions
gcloud projects get-iam-policy YOUR-PROJECT-ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:YOUR-EMAIL"
```

### Step 3: Add Required Permissions

**If you're project owner:**
```bash
# Grant yourself Cloud Functions Developer role
gcloud projects add-iam-policy-binding YOUR-PROJECT-ID \
  --member="user:YOUR-EMAIL" \
  --role="roles/cloudfunctions.developer"

# Also need Cloud Build role
gcloud projects add-iam-policy-binding YOUR-PROJECT-ID \
  --member="user:YOUR-EMAIL" \
  --role="roles/cloudbuild.builds.builder"
```

**If you're NOT project owner:**
- Contact your organization's Cloud admin
- Request these roles:
  - `Cloud Functions Developer`
  - `Cloud Build Service Account`
  - `Storage Object Admin` (for function code storage)

### Step 4: Enable Required APIs
```bash
# Enable Cloud Functions API
gcloud services enable cloudfunctions.googleapis.com

# Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Enable Cloud Run API (needed for 2nd gen functions)
gcloud services enable run.googleapis.com
```

### Step 5: Retry Deployment
```bash
# Try deploying again
gcloud functions deploy FUNCTION-NAME \
  --runtime=python39 \
  --trigger-http \
  --allow-unauthenticated
```

## ✅ Verification

If successful, you should see:
```
Deploying function (may take a while - up to 2 minutes)...done.
availableMemoryMb: 256
buildId: ...
entryPoint: hello_world
httpsTrigger:
  url: https://REGION-PROJECT.cloudfunctions.net/FUNCTION-NAME
```

## 🔄 Alternative Approach: Use Cloud Console UI

If command line continues to fail:

1. Go to: https://console.cloud.google.com/functions
2. Click "Create Function"
3. Fill in details in the UI
4. Click "Deploy"

This often works when CLI has permission issues.

## 📚 Understanding IAM Roles

| Role | What It Allows | When You Need It |
|------|---------------|------------------|
| **Cloud Functions Developer** | Deploy/delete functions | Always for deployment |
| **Cloud Build Editor** | Build function code | Always (automatic builds) |
| **Storage Admin** | Store function artifacts | Always (code storage) |
| **Service Account User** | Run function as service account | For production functions |

## 🎓 Prevention

To avoid future permission issues:
1. Always check project: `gcloud config list`
2. Verify APIs enabled before deployment
3. Request all necessary roles upfront
4. Use service accounts for production deployments
```

---

## Summary of Patterns

These examples demonstrate:

1. **Personalization**: Tailored to user's background and skill level
2. **Step-by-step**: Exact commands and clicks, no guesswork
3. **Context**: Why each step matters, analogies to familiar concepts
4. **Completeness**: From zero to working solution
5. **Troubleshooting**: Common errors and fixes
6. **Best Practices**: Not just "how" but "how well"
7. **Next Steps**: Path forward after initial success

## Using These Examples

- Copy the **User Request** format for your own prompts
- Adapt the structure to your specific needs
- Mix and match elements from different examples
- Iterate based on Copilot's responses

---

*Remember: The quality of output depends on the quality and specificity of your input. Provide context, state your goal clearly, and mention your background/constraints.*
