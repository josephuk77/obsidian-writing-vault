<!-- daily-resume-monitor:start:troubleshooting:2026-06-16 -->
## 2026-06-16 Automated Review

- Problem: No troubleshooting item was promoted from this run without verified symptoms and root cause.
- Symptoms: Not recorded.
- Root cause: Not recorded.
- Fix: Not recorded.
- Validation: build/test-results/test/TEST-com.faithlog.FaithLogApplicationTests.xml: verified pass; tests=1, passed=1, failures=0, errors=0, skipped=0
- Remaining risk: Transcript source and health/latency target remain pending decisions.
<!-- daily-resume-monitor:end:troubleshooting:2026-06-16 -->

<!-- daily-resume-monitor:start:troubleshooting:2026-06-17 -->
## 2026-06-17 Automated Review

- Problem: `./gradlew asciidoctor` could not complete inside the sandbox.
- Symptoms: Gradle wrapper raised `FileNotFoundException` for `.gradle/wrapper/...zip.lck`.
- Root cause: the wrapper lock path under the user Gradle directory was outside the sandbox write scope.
- Fix: reran the same command with elevated permissions.
- Validation: `./gradlew asciidoctor` succeeded in 3s and `build/docs/asciidoc/index.html` was present afterward.
- Remaining risk: Gradle deprecated feature warnings are still present, and health/latency measurement scope remains a pending decision.
<!-- daily-resume-monitor:end:troubleshooting:2026-06-17 -->
