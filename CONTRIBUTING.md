# Contributing to PEGAI_Academics

Thanks for your interest in contributing! This repository is a collection of academic materials for the PEGAI course — including assignments, study material, and case studies. Contributions that improve accuracy, add useful resources, or fix errors are welcome.

## Ways to Contribute

- **Fix errors** in existing notes, assignments, or case studies (typos, broken links, incorrect explanations, outdated content).
- **Add study material** such as notes, summaries, references, or worked examples that align with the course syllabus.
- **Improve assignments** by clarifying instructions, adding sample solutions, or fixing formatting issues.
- **Contribute case studies** relevant to the course topics.
- **Report issues** if you spot a mistake but aren't able to fix it yourself.

## Before You Start

1. Check the [existing issues](https://github.com/Mihir-Mithani/PEGAI_Academics/issues) and [open pull requests](https://github.com/Mihir-Mithani/PEGAI_Academics/pulls) to avoid duplicating work.
2. For larger additions (e.g. a new module of study material), open an issue first to discuss the idea before investing significant time.
3. Small fixes (typos, broken links, formatting) can go straight to a pull request without prior discussion.

## Getting Started

1. **Fork** the repository.
2. **Clone** your fork:
   ```bash
   git clone https://github.com/<your-username>/PEGAI_Academics.git
   cd PEGAI_Academics
   ```
3. **Create a branch** for your change:
   ```bash
   git checkout -b add-topic-name
   ```
   Use a descriptive branch name, e.g. `fix-assignment1-typo` or `add-case-study-nlp`.

## Making Changes

- Place new files in the appropriate folder:
  - `Assignments/` — assignment files and related material
  - `Study_Material/` — notes, references, and study resources
  - `case_study/` — case studies
- Use clear, descriptive file names (avoid spaces where possible; prefer `Topic_Name.ext`).
- Keep documents well-organized: use headings, bullet points, and consistent formatting.
- If adding a Jupyter notebook, please **clear cell outputs** before committing (`Cell > All Output > Clear` in Jupyter, or `jupyter nbconvert --clear-output`) to keep the repo lightweight.
- Double-check that any content you add is your own work, properly attributed, or otherwise permissible to share (see [License and Academic Integrity](#license-and-academic-integrity) below).

## Submitting Your Contribution

1. Commit your changes with a clear message:
   ```bash
   git add .
   git commit -m "Add case study on <topic>"
   ```
2. Push to your fork:
   ```bash
   git push origin add-topic-name
   ```
3. Open a **pull request** against the `main` branch of this repository.
4. In your PR description, briefly explain:
   - What the change is
   - Why it's useful
   - Which files are affected

## Review Process

- Pull requests will be reviewed for accuracy, relevance to the course, and formatting consistency.
- You may be asked to make small revisions before a PR is merged.
- Please be patient — this is a small, actively maintained academic repository.

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md). Please be respectful and constructive in all interactions.

## License and Academic Integrity

- Only submit material you have the right to share (your own notes, properly cited sources, or content that is freely shareable for educational purposes).
- Do not submit content that violates academic integrity policies (e.g. answer keys intended to be restricted, plagiarized material).
- If you're unsure whether something is appropriate to contribute, open an issue to ask before submitting a pull request.

## Questions?

If you have questions or need help getting started, feel free to open an issue and tag it with `question`.

Thank you for helping improve PEGAI_Academics!
