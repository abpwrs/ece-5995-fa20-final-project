# ece-5995-fa20-final-project
Modern databases (ECE:5995) project querying COVID &amp; population data


# Run the app
1. Install [Neo4j](https://neo4j.com/) and [MongoDB](https://www.mongodb.com/).     

2. Pull the app
```bash
git clone https://github.com/abpwrs/ece-5995-fa20-final-project.git
cd ece-5995-fa20-final-project
git submodule update --init
```

3. Setup virtualenv
```bash
python3 -m virtualenv venv
source venv bin activate
pip install -r requirements.txt
```
4. Load data to mongodb
```bash
cd scripts
for ff in ./*.bash; do echo $ff; bash $ff; done   
```
5. load data to neo4j
```bash
cd src
python mongo_to_neo_two.py
```

6. Launch App
```bash
cd src
bash run_app_dev.bash
```

## Datasets
- [NY Times COVID Dataset](https://github.com/nytimes/covid-19-data)
- [MongoDB Zipcode Population Dataset](https://media.mongodb.org/zips.json)
- [Kaggle ZIP/FIPS Lookup Dataset](https://www.kaggle.com/danofer/zipcodes-county-fips-crosswalk)
