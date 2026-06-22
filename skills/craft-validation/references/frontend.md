# Frontend Validation

How to validate a frontend after code changes. Skip if the project has no frontend section in `docs/validation.md`.

## Opening pages

Use the Playwright MCP to navigate to each page listed in the validation doc's Frontend table.

## Login

If login is required:

1. Open the login URL from the validation doc.
2. Ask the user to log in manually — do not automate credentials.
3. Wait for confirmation, then navigate to the target pages.

## What to verify

For each page: it loads without a blank screen, key elements from the table are visible, and there are no JavaScript console errors.

## What NOT to do

Do not click delete/archive buttons, submit payment forms, trigger email sends, or follow OAuth redirects to external providers.
