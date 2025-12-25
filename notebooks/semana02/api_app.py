import script_v3 as scr

MODEL_PATH = "artifacts/flightontime_pipeline.pkl"
app = scr.criar_app_fastapi(MODEL_PATH)
