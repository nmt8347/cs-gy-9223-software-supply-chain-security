# Contributing

## Issues

- Search existing issues before filing. Duplicates are closed.
- One problem per issue.
- Bug reports must include: version, OS/runtime, reproduction steps, expected behavior, actual behavior, logs or stack trace.
- Feature requests must state the problem being solved, not only the proposed solution.
- Security vulnerabilities: do not file publicly. Email security@example.com.

## Pull Requests

### Before Opening

- Open an issue first for any non-trivial change. Unapproved large PRs may be rejected.
- Fork the repo and branch from `main`. Branch naming: `fix/<short-desc>`, `feat/<short-desc>`, `docs/<short-desc>`.

### Requirements

- Maximum of 2 logical changes per PR. No unrelated refactors.
- Reference the issue: `Fixes #123`.
- All CI checks must pass. Failing PRs are not reviewed.
- Rebase on `main` before requesting review. No merge commits.
- Update docs and CHANGELOG for user-facing changes.

### Commits

- Follow Conventional Commits: `type(scope): summary`.
- Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.
- Summary: imperative mood, 72 characters maximum.
- Squash fixup commits before review.

### Code Style

- Formatting and linting are enforced by tooling.
- Do not disable lint rules without a comment justifying it.
- Public functions and classes require docstrings/doc comments.
- No commented-out code, no stray debug output, no unexplained TODOs.

### Testing

- Every bug fix requires a regression test.
- Every new feature requires unit tests covering success and failure paths.
- Coverage must not decrease. Minimum: 80%.
- Tests must be deterministic: no network access, no reliance on wall-clock time or execution order.

### Review

- At least one maintainer approval required.
- Address all review comments or state why not.
- Maintainers may close PRs inactive for 30 days.

## Licensing

By submitting a contribution, you agree it is licensed under the project license. Sign off commits with `git commit -s` (DCO).