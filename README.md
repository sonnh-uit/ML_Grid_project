# CS2215.CH1701 - Cloud and Grid computing

## Introduce

This is Final project of course CS2215.CH1701 - Cloud and Grid computing. In this project, we will build a production-ready end-to-end batch ML system to forecast energy consumption levels for the next 24 hours across multiple consumer types (e.g., residential, commercial, industrial) from Denmark. For detail of project, you can see in [FINAL-PROJECT-MLOP](FINAL-PROJECT-MLOP.pdf)

Student:
- Nguyen Hong Son (Mr.)
- Nguyen Duong Truc Phuong (Ms.)

## Acknowledgement

For idea in project, we would like to acknowledge and appreciate Paul Iusztin for their valuable project idea. His project is powerful and have more feature than us. You can [visit his repository](https://github.com/iusztinpaul/energy-forecasting) to get more experienced

## Prerequisites

### Register account and tooling

- You must register an account in [https://app.hopsworks.ai/](https://app.hopsworks.ai/). `Hopsworks` easy to use by your github or google account

### Software require

This project is easy to use by `docker`. To run this project, you need [INSTALL DOCKER](https://docs.docker.com/engine/install/) and run the following command.

```shell
sudo docker compose up
```
Notice that you fill all require param for project in [.env](src/utils/.env-template)


## Project structure

Project structure have file and directory which are describe below. In each directory, we will explain more detail in them.
- `docker-compose.yml`:
- `src`:
- `model_training`:
- `feature_engineering`:
- `data`

<!-- WANDB -->