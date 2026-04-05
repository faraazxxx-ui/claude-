'''
name: ghusoon-business-launcher
description: "A comprehensive skill to launch and manage the Ghusoon e-commerce business, from legal setup to marketing automation. Use when the user wants to work on any aspect of the Ghusoon business, including LLC formation, Shopify setup, product management, marketing, or fulfillment."

# Ghusoon Business Launcher Skill

This skill provides a structured workflow and the necessary tools to launch and manage the Ghusoon business. It is designed to be used by an AI agent to assist the user in every step of the process.

## Workflow

The workflow is divided into 8 steps. Each step must be completed in order.

### Step 1: Business Discovery

**Goal:** Deeply understand the Ghusoon business, its products, target audience, and unique selling propositions.

**Instructions:**
1. Read the `knowledge_base.md` file to get a complete overview of the project.
2. Analyze the product list, ingredient philosophy (100% alcohol-free), and pricing structure.
3. Review the target audience personas ("Fatima" and "Aisha").
4. Summarize the key findings and create a `business_plan_template.md` in the `templates/` directory.

### Step 2: LLC and Legal Setup

**Goal:** Formally establish Ghusoon as a legal business entity.

**Instructions:**
1.  Use the `llc_formation_guide.md` in the `references/` directory to guide the user through the process of filing for an LLC.
2.  The LLC should be listed as a subsidiary of the Rahman Foundation.
3.  Generate the necessary legal documents and store them in a secure location.

### Step 3: E-commerce Platform Setup

**Goal:** Build a fully functional Shopify store for Ghusoon.

**Instructions:**
1.  Execute the `shopify_setup.py` script in the `scripts/` directory. This script will:
    *   Create a new Shopify store.
    *   Apply the "Sensory Luxury" theme with the specified color palette and fonts.
    *   Set up the basic store structure (homepage, about page, contact page).
2.  Refer to `shopify_best_practices.md` for guidance on creating a high-converting store.

### Step 4: Product Catalog Management

**Goal:** Populate the Shopify store with Ghusoon's products, scents, and pricing.

**Instructions:**
1.  Use the `product_listing_template.md` from the `templates/` directory to structure the product information.
2.  Write compelling descriptions for each of the 50+ fragrances.
3.  Upload high-quality product images (once available).
4.  Configure the pricing, including the import surcharge and customization options.

### Step 5: Marketing Strategy

**Goal:** Develop and execute a comprehensive marketing plan to drive traffic and sales.

**Instructions:**
1.  Use the `marketing_templates.md` in the `references/` directory to create a content calendar.
2.  Run the `marketing_calendar.py` script to generate a schedule for social media posts, email campaigns, and promotions.
3.  Develop ad copy and creative assets for the target personas.

### Step 6: Shipping and Fulfillment

**Goal:** Automate the shipping and order fulfillment process.

**Instructions:**
1.  Integrate a drop shipping service with the Shopify store.
2.  Use the `shipping_calculator.py` script to determine shipping rates based on customer location.
3.  Set up automated label printing and order tracking.

### Step 7: Financial Setup

**Goal:** Establish a system for managing the business's finances.

**Instructions:**
1.  Choose and integrate an accounting software (e.g., QuickBooks, Xero) with the Shopify store.
2.  Set up a chart of accounts and bookkeeping procedures.
3.  Establish a system for tracking inventory and cost of goods sold.

### Step 8: Automation

**Goal:** Connect all the systems and automate workflows to create a "second brain" for the business.

**Instructions:**
1.  Use a tool like Make or Zapier to create integrations between Shopify, the accounting software, the email marketing platform, and other services.
2.  Create a dashboard that provides a real-time overview of the business performance.
3.  Set up automated reports and alerts to keep the user informed of key metrics.

## Scripts

*   `scripts/shopify_setup.py`: A Python script to automate the setup of the Shopify store.
*   `scripts/marketing_calendar.py`: A Python script to generate a marketing content calendar.
*   `scripts/shipping_calculator.py`: A Python script to calculate shipping rates.

## References

*   `references/llc_formation_guide.md`: A guide to forming an LLC.
*   `references/shopify_best_practices.md`: Best practices for setting up a Shopify store.
*   `references/marketing_templates.md`: Templates for marketing materials.

## Templates

*   `templates/business_plan_template.md`: A template for the Ghusoon business plan.
*   `templates/product_listing_template.md`: A template for product listings.
'''
