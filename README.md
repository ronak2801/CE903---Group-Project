AI-Based Recommendation for Food Purchase

This repository contains codebases for a full recommendation system for food purchase recommendations as part of the CE902 project.

Project Structure

The repository divides the three codebases into three folders:

frontend: The frontend used for demonstrating the capabilities of the recommendation engine.

backend: The backend used to allow the frontend to interact with the recommendation engine.

rs-engine: The codebase used for developing the recommendation engine to be integrated into the backend system.

How to Contribute

The repository utilizes different branches to separate the development process for frontend, backend, and rs-engine. To contribute to each process:

Checkout to the appropriate branch. The command below demonstrates how to checkout to the frontend branch.

git checkout frontend

Create a new branch based on the task you are going to work on. Tasks are divided into feature, bug, and refactoring. The command below demonstrates how to create a branch for an Authentication Page feature in the frontend.

git checkout -b frontend/feature/authentication-page

Start your development process on the branch created in the previous step. Please commit regularly with descriptive commit messages.

Once you have completed the task, submit a merge request to the appropriate reviewer.

If the reviewer approves the changes, they will be added to the appropriate source branch. You can then checkout back to the source branch (frontend, backend, or rs-engine) and repeat steps 1–4 for the next task. 

If the changes are not approved, make the required updates based on the reviewer’s comments on the current branch and submit another merge request.
