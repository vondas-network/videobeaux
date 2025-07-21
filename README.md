# (Recommended) Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# install 
pip install .

# run
videobeaux --help

videobeaux --program bad_predator --input example.mp4 --output badpred

videobeaux --program convert --help