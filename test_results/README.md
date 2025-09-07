# Test Results Directory

This directory contains test results and output files generated during testing.

## Contents

- **Output files**: Processed audio files from tests
- **Temporary files**: Intermediate files created during testing
- **Log files**: Test execution logs
- **Coverage reports**: Code coverage analysis results

## Usage

This directory is automatically created and used by the test suite. It should be cleaned up after testing to avoid accumulating large files.

## Cleanup

To clean up test results:

```bash
# Remove all test output files
rm -rf test_results/output/*
rm -rf test_results/temp/*

# Or remove the entire directory
rm -rf test_results/*
```

## Git Ignore

This directory is included in `.gitignore` to prevent test artifacts from being committed to the repository.

