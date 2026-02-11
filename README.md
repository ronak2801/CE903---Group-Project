# AI-Based Recommendation for Food Purchase
This repository contains code bases for a full recommendation system for recommending food purchases as part of CE902 project.

# Project Structure
The repository divides the three codebases into three folders:
- [frontend](/frontend): The frontend that is used for the purpose of demonstrating the capabilities of the recommendation engine.
- [backend](/backend): The backend that is used for allowing the frontend to interact with the recommendation engine.
- [rs-engine](/rs-engine): The code base that is used for developing the recommendation engine to be used in the backend system.

# How to Contribute
The repository utilise different branches to separate development process in [frontend](https://cseegit.essex.ac.uk/22-23-ce9x3-sp/22-23_CE9x3-SP_team17/-/tree/frontend), [backend](https://cseegit.essex.ac.uk/22-23-ce9x3-sp/22-23_CE9x3-SP_team17/-/tree/backend), and [rs-engine](https://cseegit.essex.ac.uk/22-23-ce9x3-sp/22-23_CE9x3-SP_team17/-/tree/rs-engine). To contribute each of the process:

1. Checkout to the appropriate branch. The below script demonstrates how to checkout to the **frontend** branch.
```bash
git checkout frontend
```
2. Create a new branch based on the task you are going to work on. The task will be divided into **feature**, **bug**, and **refactoring**. The below script demonstrate how to do so for an **Authentication Page** in **frontend**.
```bash
git checkout -b frontend/feature/authentication-page
```
3. Start your development/coding process on the branch created in the previous step. **Please commit regularly with descriptive commit messages.**
4. Once you have completed the task. Submit a merge request with the appropraite **Reviewer**.

If the reviewer approves the changes, it will be added to the appropraite source branch and you can checkout back to the source branch (i.e. **frontend**, **backend**, **rs-engine**) and repeat step 1-4 for the next task. On the other hand, if the changes is not approved, you will need to make changes based on the reviewer's comment on the current branch and submit another merge request.