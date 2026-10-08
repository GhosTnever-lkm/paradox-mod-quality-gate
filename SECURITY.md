# Security policy

Do not publish unredacted secrets, private mod archives, or personal data in issues. Use GitHub's private vulnerability reporting for security concerns.

The action scans repository files on a runner and stores only generated reports as artifacts. Keep the default `contents: read` permission and use `pull_request` rather than `pull_request_target` for untrusted contributions. Reports can reveal relative file names and diagnostic context; configure artifact access and retention appropriately. Secret detection is best-effort and a clean scan does not prove that a package contains no secrets.
