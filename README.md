# Eisenhower
Welcome to **Eisenhower** framework for analysis of software Backend Development Cost (BDC) for hardware accelerator designs.

TODO: Provide a summary

TODO: What is a backend

Refer to our paper for more details: TODO: Add link

## Feature Trees
We have provided the following **Feature Tree Templates (\<FT>)** in this repo. Please refer to respective \<FT> pages for list of hardware accelerators:

* [Deep Learning](deep_learning/)

## Setup
TODO: Add docker image path

The easiest method uses the pre-built docker image. Use the following command to pull and start the docker image in background.
```
docker run -t -d --name=eisenhower -v <LOCAL_PATH_TO_GIT_REPO>:/eisenhower <DOCKER_IMAGE_PATH>
```
Once the container is running in background, use the following command to perform Eisenhower analysis:
```
docker exec -it util /bin/bash -c "cd eisenhower; python3 ./main.py"
```
Analysis results are generated in `output` directory.

## Citation
TODO: Add citation bibtex

Feel free to reach out at \<TODO: Add email> for any queries or concerns.
