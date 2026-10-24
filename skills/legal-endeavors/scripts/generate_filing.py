#!/usr/bin/env python3
"""
Legal Filing Generator for Rahman v. UHS et al.
Case No. 3:26-CV-00197 (AJB/ML)

Generates properly formatted legal document shells for common filings.

Usage:
    python3 generate_filing.py --type motion --title "Motion to Compel" --output motion_to_compel.md
    python3 generate_filing.py --type letter --title "Demand Letter" --recipient "UHS" --output demand.md
    python3 generate_filing.py --type memo --title "Research Memo" --output memo.md
    python3 generate_filing.py --list  # List available templates
"""

import argparse
import os
from datetime import datetime

CASE_INFO = {
    "caption": "MOHAMMED FARAAZ RAHMAN, M.D.",
    "case_no": "3:26-CV-00197 (AJB/ML)",
    "court": "UNITED STATES DISTRICT COURT\nNORTHERN DISTRICT OF NEW YORK",
    "defendants": "UNITED HEALTH SERVICES HOSPITALS, INC., AWAIS AHMED, MD, M. FARHAN NADEEM, MD, AFZEL UR REHMAN, MD, and MUHAMMAD IMRAN ALI, MD",
    "plaintiff_attorney": "Douglas Walter Drazen, Esq.",
    "plaintiff_address": "11-12 30th Dr., Apt 214 W, Astoria, New York 11102",
}

TEMPLATES = {
    "motion": {
        "description": "Motion template (Motion to Compel, MSJ, MIL, etc.)",
        "generate": lambda title, **kw: f"""{CASE_INFO['court']}

{CASE_INFO['caption']},
                    Plaintiff,
        v.                                          Case No. {CASE_INFO['case_no']}

{CASE_INFO['defendants']},
                    Defendants.

---

# {title.upper()}

Plaintiff Mohammed Faraaz Rahman, M.D., by and through his attorney, {CASE_INFO['plaintiff_attorney']}, respectfully moves this Court for an Order [SPECIFY RELIEF SOUGHT], and in support thereof states as follows:

## PRELIMINARY STATEMENT

[Provide a concise overview of the motion and the relief sought.]

## STATEMENT OF FACTS

[Set forth the relevant facts supporting the motion.]

## ARGUMENT

### I. [First Legal Argument]

[Develop the argument with citations to authority.]

### II. [Second Legal Argument]

[Develop the argument with citations to authority.]

## CONCLUSION

For the foregoing reasons, Plaintiff respectfully requests that this Court grant [SPECIFY RELIEF].

Dated: {datetime.now().strftime('%B %d, %Y')}

Respectfully submitted,

{CASE_INFO['plaintiff_attorney']}
Attorney for Plaintiff
"""
    },
    "letter": {
        "description": "Formal letter template (demand letters, correspondence)",
        "generate": lambda title, **kw: f"""**{CASE_INFO['plaintiff_attorney']}**
Attorney at Law

{datetime.now().strftime('%B %d, %Y')}

**VIA [METHOD OF SERVICE]**

{kw.get('recipient', '[RECIPIENT NAME AND ADDRESS]')}

Re: {title}
    Case No. {CASE_INFO['case_no']}
    {CASE_INFO['caption']} v. {CASE_INFO['defendants']}

Dear [RECIPIENT]:

[Body of letter.]

Please govern yourself accordingly.

Very truly yours,

{CASE_INFO['plaintiff_attorney']}
Attorney for {CASE_INFO['caption']}

cc: All counsel of record
"""
    },
    "memo": {
        "description": "Legal research memorandum template",
        "generate": lambda title, **kw: f"""# LEGAL MEMORANDUM

**To:** {CASE_INFO['plaintiff_attorney']}
**From:** [Author]
**Date:** {datetime.now().strftime('%B %d, %Y')}
**Re:** {title} — {CASE_INFO['caption']} v. UHS et al., Case No. {CASE_INFO['case_no']}

---

## QUESTION PRESENTED

[State the legal question(s) to be analyzed.]

## SHORT ANSWER

[Provide a brief answer to each question.]

## STATEMENT OF FACTS

[Set forth the relevant facts.]

## DISCUSSION

### I. [First Issue]

[Analysis with citations to authority.]

### II. [Second Issue]

[Analysis with citations to authority.]

## CONCLUSION

[Summarize conclusions and recommended course of action.]
"""
    },
    "discovery": {
        "description": "Discovery request template (interrogatories, RFPs, RFAs)",
        "generate": lambda title, **kw: f"""{CASE_INFO['court']}

{CASE_INFO['caption']},
                    Plaintiff,
        v.                                          Case No. {CASE_INFO['case_no']}

{CASE_INFO['defendants']},
                    Defendants.

---

# {title.upper()}

Plaintiff Mohammed Faraaz Rahman, M.D., by and through his attorney, {CASE_INFO['plaintiff_attorney']}, hereby propounds the following [INTERROGATORIES / REQUESTS FOR PRODUCTION / REQUESTS FOR ADMISSION] upon Defendant [NAME]:

## DEFINITIONS AND INSTRUCTIONS

1. "You" and "Your" refer to Defendant [NAME] and all agents, employees, and representatives.
2. "Document" has the broadest meaning permitted under FRCP 34(a).
3. "Communication" means any exchange of information, whether oral, written, or electronic.
4. The relevant time period is June 2021 through the present unless otherwise specified.

## [INTERROGATORIES / REQUESTS]

**[Request/Interrogatory] No. 1:**
[Specific request.]

**[Request/Interrogatory] No. 2:**
[Specific request.]

**[Request/Interrogatory] No. 3:**
[Specific request.]

Dated: {datetime.now().strftime('%B %d, %Y')}

Respectfully submitted,

{CASE_INFO['plaintiff_attorney']}
Attorney for Plaintiff
"""
    },
    "affidavit": {
        "description": "Affidavit / Declaration template",
        "generate": lambda title, **kw: f"""{CASE_INFO['court']}

{CASE_INFO['caption']},
                    Plaintiff,
        v.                                          Case No. {CASE_INFO['case_no']}

{CASE_INFO['defendants']},
                    Defendants.

---

# {title.upper()}

I, [DECLARANT NAME], declare under penalty of perjury pursuant to 28 U.S.C. § 1746 as follows:

1. I am [relationship to case / basis for personal knowledge].

2. [Factual statement.]

3. [Factual statement.]

4. [Factual statement.]

5. I declare under penalty of perjury that the foregoing is true and correct.

Executed on {datetime.now().strftime('%B %d, %Y')}, at [CITY, STATE].

_________________________
[DECLARANT NAME]
"""
    }
}


def list_templates():
    print("\nAvailable Filing Templates:")
    print("-" * 50)
    for name, info in TEMPLATES.items():
        print(f"  {name:15s} — {info['description']}")
    print()


def generate(template_type, title, output_path, **kwargs):
    if template_type not in TEMPLATES:
        print(f"Error: Unknown template type '{template_type}'. Use --list to see available templates.")
        return False

    content = TEMPLATES[template_type]["generate"](title, **kwargs)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w") as f:
        f.write(content)

    print(f"Generated {template_type}: {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Legal Filing Generator for Rahman v. UHS")
    parser.add_argument("--type", choices=list(TEMPLATES.keys()), help="Type of filing to generate")
    parser.add_argument("--title", default="[TITLE]", help="Title of the filing")
    parser.add_argument("--output", default="filing.md", help="Output file path")
    parser.add_argument("--recipient", default="[RECIPIENT]", help="Recipient (for letters)")
    parser.add_argument("--list", action="store_true", help="List available templates")
    args = parser.parse_args()

    if args.list:
        list_templates()
        return

    if not args.type:
        parser.print_help()
        return

    generate(args.type, args.title, args.output, recipient=args.recipient)


if __name__ == "__main__":
    main()
