## Faulty Python Project (for test analysis)

This is a small python project used to evaluate the CI-servers ability to run unit tests. This project is intended to be "faulty" in the sense that we expect at least one of its tests to fail during during test analysis. 

NOTE: The file structure of this project differs in that the test file is not directly in source but in a subfolder tests/. This will evaluate the CI-servers ability to find test files and run them in the appropriate context (the tests need to be called as a module from /src, not /tests).