# ML Web Deployment - House Price Predictor

A Flask web app that serves a Ridge regression model predicting house prices from a handful of property features (King County, WA housing data). Fill in a small form, get back an estimated price.

## How it works

```
house_price_prediction.csv → model.py (Ridge regression) → model.pkl → app.py (Flask) → templates/index.html
```

- **`model.py`** reads the dataset, selects six feature columns, fits a `Ridge` regression against `price`, and pickles the trained model to `model.pkl`.
- **`app.py`** loads `model.pkl` once at startup, renders the form on `/`, and on `POST /predict` reads the submitted form values, runs them through the model, and re-renders the page with the predicted price.
- **`templates/index.html`** is the form the model is served through.

## Features used

The model is trained on six features, in this exact order:

| # | Feature | Description |
|---|---|---|
| 1 | `sqft_living15` | Living area (sq ft), averaged with the 15 nearest neighbors |
| 2 | `sqft_above` | Square footage above ground |
| 3 | `grade` | Overall build/design grade (1–13) |
| 4 | `condition` | Property condition (1–5) |
| 5 | `bedrooms` | Number of bedrooms |
| 6 | `floors` | Number of floors |

> **⚠️ Field order matters.** `app.py` reads submitted values with `request.form.values()`, which has no field names attached - it just takes values in the order the HTML inputs appear on the page. That order **must** match the `top_6` list in `model.py` exactly (`sqft_living15 → sqft_above → grade → condition → bedrooms → floors`), or the model will silently score the wrong columns. If you add, remove, or reorder form fields, update `model.py`'s `top_6` list (and retrain) to match, or vice versa.

## Project structure

```
ML_Web_Deployment/
├── app.py                       # Flask app - serves the form and the /predict endpoint
├── model.py                     # Trains the Ridge regression model and writes model.pkl
├── model.pkl                    # Pre-trained model (pickled)
├── house_price_prediction.csv   # Training dataset
├── requirements.txt             # Python dependencies
├── env_setup_commands.txt       # Reference commands for setting up an EC2 instance
└── templates/
    └── index.html               # Form UI
```

## Getting started locally

**1. Clone the repo**
```bash
git clone https://github.com/j019/ML_Web_Deployment.git
cd ML_Web_Deployment
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. (Optional) Retrain the model**

A trained `model.pkl` is already included, so this step isn't required to run the app. Retrain only if you've changed the dataset or feature set:
```bash
python model.py
```

**5. Run the app**
```bash
python app.py
```

The server starts on `http://0.0.0.0:9000` - open **http://127.0.0.1:9000** in your browser.

## Usage

1. Open the app in your browser.
2. Fill in all six fields: living area, area above ground, grade, condition, bedrooms, and floors.
3. Submit the form via the **Predict** button.
4. The predicted price is rendered back on the same page.

> Note: the form submits via `POST`. Visiting `/predict` directly (or refreshing the results page) sends a `GET` request and will return a `405 Method Not Allowed` - always submit through the form.

## Deploying to an EC2 instance

`env_setup_commands.txt` in this repo has the reference commands; summarized here:

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

python3 -m venv myenv
source ~/myenv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

Then start the app:
```bash
python3 app.py
```

Since `app.run(host="0.0.0.0", port=9000)` is already set in `app.py`, the server listens on all interfaces - make sure port `9000` is open in your EC2 instance's security group, then visit `http://<your-ec2-public-ip>:9000`.

For production use, consider running behind Gunicorn + Nginx instead of Flask's built-in dev server:
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:9000 app:app
```

## Tech stack

- **Python**, **Flask** - web server
- **pandas** - data loading
- **scikit-learn** - Ridge regression model
- **NumPy** - array handling for prediction input
- **HTML/CSS** - form UI

## Known limitations

- Form inputs are cast with `int(x)`, so decimal values will raise a `ValueError`. Stick to whole numbers.
- No server-side validation beyond `required` on the HTML inputs - out-of-range values (e.g. `condition` outside 1–5) will still be passed to the model.
- Debug mode is off by default in `app.py`, which is correct for production but means you won't get detailed error pages locally unless you add `debug=True`.

## License

No license file is currently included in this repository. Add one (e.g. MIT) if you intend for others to reuse this code.
