---
title: Alaska Wildfire Occurrence
emoji: 🔥
colorFrom: green
colorTo: red
sdk: docker
pinned: false
license: apache-2.0
app_port: 7860
---

# wildfire-occurrence

Wildfire occurrence modeling using Terrestrial Ecosystem Models and Artificial Intelligence

[CG Lightning Probability Forecast](https://huggingface.co/spaces/jordancaraballo/alaska-wildfire-occurrence)

## Objectives

- Probabilistic wildfire occurrence model
- Model both occurrence, spread and risk of fire
- Create data pipeline between UAF TEM and NCCS/SMCE resources
- 30m local Alaska models, 1km circumpolar models
- Integration of precipitation, temperature and lightning datasets

## Containers

### Python Container

```bash
module load singularity
singularity build --sandbox /lscratch/$USER/container/wildfire-occurrence docker://nasanccs/wildfire-occurrence:latest
```

## Quickstart

### Executing WRF

```bash
singularity exec --env PYTHONPATH="/explore/nobackup/people/$USER/development/wildfire-occurrence" --nv -B /explore/nobackup/projects/ilab,$NOBACKUP,/lscratch,/explore/nobackup/people /lscratch/$USER/container/wildfire-occurrence python /explore/nobackup/people/$USER/development/wildfire-occurrence/wildfire_occurrence/view/wrf_pipeline_cli.py -c /explore/nobackup/people/$USER/development/wildfire-occurrence/wildfire_occurrence/templates/config.yaml --pipeline-step all --start-date 2023-06-05 --forecast-lenght 10
```

## Extracting variables from WRF

Running this script to extract variables from WRF and perform lightning inference

```bash
singularity shell --nv -B /explore/nobackup/projects/ilab,/explore/nobackup/projects/3sl,$NOBACKUP,/lscratch,/explore/nobackup/people /lscratch/jacaraba/container/wildfire-occurrence/
python wrf_analysis.py 
```

## Dataset Generation and Training

```bash
singularity exec --env PYTHONPATH="/explore/nobackup/people/jacaraba/development/wildfire-occurrence" --nv -B /explore/nobackup/projects/ilab,/explore/nobackup/projects/3sl,$NOBACKUP,/lscratch,/explore/nobackup/people /lscratch/jacaraba/container/wildfire-occurrence python /explore/nobackup/people/jacaraba/development/wildfire-occurrence/wildfire_occurrence/model/lightning/lightning_model.py
```

Full Data Pipeline Command

```bash
singularity exec --env PYTHONPATH="/explore/nobackup/people/jacaraba/development/wildfire-occurrence" --nv -B /explore/nobackup/projects/ilab,/explore/nobackup/projects/3sl,$NOBACKUP,/lscratch,/explore/nobackup/people /lscratch/jacaraba/container/wildfire-occurrence python /explore/nobackup/people/jacaraba/development/wildfire-occurrence/wildfire_occurrence/model/lightning/lightning_model.py 
```

## Contributors

- Jordan Alexis Caraballo-Vega, jordan.a.caraballo-vega@nasa.gov