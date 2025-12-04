import base64
import gradio as gr
import pandas as pd
from pathlib import Path
from typing import Tuple, List, Dict, Any, Iterable
from model import analyze_sentiment, analyze_sentiments_bulk

# =========================
# Configurable app settings
# =========================
CASE_INSENSITIVE_COLUMN_MATCH = True   # If True, matches 'review' to 'Review'
MAX_PREVIEW_ROWS = 20
# Set to None to process all at once (uses analyze_sentiments_bulk)
BATCH_SIZE = 1000
CSV_ENCODINGS_TRY = ["utf-8", "utf-8-sig",
                     "latin-1"]  # fallback encodings for CSVs

# -----------------------------------
# Helpers
# -----------------------------------


def _normalize_result(item: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize model result to ensure keys exist and are typed properly."""
    label = (item.get("label") or "NEUTRAL").strip().upper()
    if label not in {"POSITIVE", "NEGATIVE", "NEUTRAL"}:
        label = "NEUTRAL"
    try:
        score = float(item.get("score", 0.0))
    except (TypeError, ValueError):
        score = 0.0
    explanation = item.get("explanation") or ""
    return {"label": label, "score": score, "explanation": explanation}


def _find_column(df: pd.DataFrame, name: str) -> str:
    """Find a column by (optionally) case-insensitive name. Returns the actual column name or raises."""
    if name in df.columns:
        return name
    if CASE_INSENSITIVE_COLUMN_MATCH:
        lower_map = {c.lower(): c for c in df.columns}
        key = name.lower().strip()
        if key in lower_map:
            return lower_map[key]
    raise gr.Error(
        f"Column '{name}' not found. Available columns: {', '.join(map(str, df.columns))}"
    )


def _read_any_csv(path: Path) -> pd.DataFrame:
    """Try common encodings to read CSV more robustly."""
    last_err = None
    for enc in CSV_ENCODINGS_TRY:
        try:
            return pd.read_csv(path, encoding=enc, encoding_errors="ignore")
        except Exception as e:
            last_err = e
    raise gr.Error(f"Could not read CSV file: {last_err}")


def _chunked(iterable: List[str], size: int) -> Iterable[List[str]]:
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]


# -----------------------------
# Single text analysis (UI fn)
# -----------------------------
def sentiment_ui(text: str) -> Tuple[str, float, str]:
    res = analyze_sentiment(text)
    norm = _normalize_result(res)

    badge_class = "aip365-label-badge "
    if norm["label"] == "POSITIVE":
        badge_class += "aip365-label-positive"
    elif norm["label"] == "NEGATIVE":
        badge_class += "aip365-label-negative"
    else:
        badge_class += "aip365-label-neutral"

    badge_html = f'<span class="{badge_class}">{norm["label"]}</span>'
    return badge_html, norm["score"], norm["explanation"]


# -----------------------------------------
# Batch processing helper (CSV / Excel I/O)
# -----------------------------------------
def process_file(
    file_path: str,
    text_column: str,
    export_as: str = "xlsx"
) -> Tuple[str, pd.DataFrame]:
    """
    Reads CSV/Excel, runs sentiment on the given text column,
    writes an output file alongside the upload, and returns (path, preview_df).
    """
    if not file_path:
        raise gr.Error("Please upload a file first.")
    if not text_column or not text_column.strip():
        raise gr.Error("Please enter the column name that contains the text.")

    src = Path(file_path)
    ext = src.suffix.lower()

    # Read file
    try:
        if ext == ".csv":
            df = _read_any_csv(src)
        elif ext == ".xlsx":
            df = pd.read_excel(src, engine="openpyxl")
        elif ext == ".xls":
            df = pd.read_excel(src, engine="xlrd")
        else:
            raise gr.Error(
                "Unsupported file type. Please upload .csv, .xlsx, or .xls")
    except Exception as e:
        raise gr.Error(f"Could not read file: {e}")

    if df.empty:
        raise gr.Error("The uploaded file has no rows.")

    # Validate column
    actual_col = _find_column(df, text_column)

    # Prepare texts
    texts_series = df[actual_col]
    if texts_series.isna().all():
        raise gr.Error(
            f"Column '{actual_col}' is empty or all values are NaN.")
    texts = texts_series.astype(str).fillna("").tolist()

    # Run bulk sentiment (optionally chunked)
    results: List[Dict[str, Any]] = []
    try:
        if BATCH_SIZE and BATCH_SIZE > 0 and len(texts) > BATCH_SIZE:
            for chunk in _chunked(texts, BATCH_SIZE):
                chunk_results = analyze_sentiments_bulk(chunk)
                results.extend([_normalize_result(r) for r in chunk_results])
        else:
            results = [_normalize_result(r)
                       for r in analyze_sentiments_bulk(texts)]
    except Exception as e:
        raise gr.Error(f"Sentiment analysis failed: {e}")

    if len(results) != len(texts):
        raise gr.Error(
            f"Mismatch in results. Expected {len(texts)} results, got {len(results)}."
        )

    # Append result columns
    df["SentimentLabel"] = [r["label"] for r in results]
    df["SentimentScore"] = [r["score"] for r in results]
    df["SentimentExplanation"] = [r["explanation"] for r in results]

    # Write output next to source file
    try:
        if export_as == "csv":
            out_path = src.with_name(src.stem + "_sentiment.csv")
            df.to_csv(out_path, index=False)
        else:
            out_path = src.with_name(src.stem + "_sentiment.xlsx")
            df.to_excel(out_path, index=False, engine="openpyxl")
    except Exception as e:
        raise gr.Error(f"Could not write the output file: {e}")

    preview = df.head(MAX_PREVIEW_ROWS)
    return str(out_path), preview


# ---------------------------------
# Logo → base64 data URI
# ---------------------------------
logo_path = Path("logo.png")  # must be in same folder as app.py on disk
logo_data_uri = ""
if logo_path.exists():
    ext = logo_path.suffix.lower()
    if ext == ".png":
        mime = "image/png"
    elif ext in (".jpg", ".jpeg"):
        mime = "image/jpeg"
    elif ext == ".svg":
        mime = "image/svg+xml"
    else:
        mime = "image/png"

    b64 = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
    logo_data_uri = f"data:{mime};base64,{b64}"
else:
    print("⚠️ logo.png not found next to app.py")

# ✅ make logo clickable (no text shown)
logo_img_html = (
    f'<a href="https://aipowered365.com/" '
    f'target="_blank" rel="noopener noreferrer">'
    f'<img src="{logo_data_uri}" alt="AIpowered365 logo" />'
    f'</a>'
) if logo_data_uri else ""


# =========
# Build UI
# =========
with gr.Blocks(elem_id="aipowered365-app") as demo:
    # Inject CSS from theme.css
    css_text = ""
    theme_css_path = Path("theme.css")
    if theme_css_path.exists():
        css_text = theme_css_path.read_text(encoding="utf-8")
    gr.HTML(f"<style>{css_text}</style>")

    gr.HTML("<div class='aip365-container'>")
    gr.HTML("</div>")

    # ---------- Top hero + logo ----------
    notes_html = f"""
    <div class="aip365-hero">
        <div class="aip365-hero-left">
            <h1 class="aip365-hero-title">Sentiment Intelligence</h1>
            <p class="aip365-hero-subtitle">
                Analyze the tone of single messages or entire CSV / Excel files in one place.
            </p>

            <div class="aip365-hero-meta">
                <span class="aip365-hero-pill">Single &amp; batch mode</span>
                <span class="aip365-hero-pill">Downloadable results</span>
                <span class="aip365-hero-pill">Powered by Hugging Face &amp; Gradio</span>
            </div>

            <div class="aip365-hero-how">
    <strong>How to use</strong>

    <div class="aip365-how-item">
        <strong>Single:</strong>
        Type your text and click <em>Analyze Sentiment</em>.
    </div>

    <div class="aip365-how-item">
        <strong>Batch:</strong>
        Upload CSV/Excel, set the text column, then click
        <em>Run Batch Sentiment</em>.
    </div>
</div>


        <div class="aip365-hero-right">
            {logo_img_html}
        </div>
    </div>
    """
    gr.HTML(notes_html)

    # ---------- Single Sentiment card ----------
    with gr.Column(elem_classes=["aip365-card"]):
        gr.Markdown("### Single Sentiment", elem_classes=[
                    "aip365-section-title"])

        txt_input = gr.Textbox(
            label="Your text",
            placeholder="Type or paste a sentence, email, or message here...",
            lines=3,
        )

        analyze_btn = gr.Button(
            "Analyze Sentiment",
            elem_classes=["aip365-button"],
        )

        with gr.Row():
            sentiment_badge = gr.HTML(label="Sentiment")
            score_output = gr.Number(
                label="Confidence Score",
                interactive=False,
            )

        explanation_output = gr.Markdown(label="Explanation")

        analyze_btn.click(
            fn=sentiment_ui,
            inputs=txt_input,
            outputs=[sentiment_badge, score_output, explanation_output],
        )

    # ---------- Batch Sentiment card ----------
    with gr.Column(elem_classes=["aip365-card"]):
        gr.Markdown("### Batch Sentiment (CSV / Excel)",
                    elem_classes=["aip365-section-title"])

        file_input = gr.File(
            label="Upload CSV or Excel",
            file_types=[".csv", ".xlsx", ".xls"],
            type="filepath",
        )
        text_column = gr.Textbox(
            label="Text column name",
            placeholder="e.g., comment, review, message",
        )
        export_as = gr.Radio(
            choices=["xlsx", "csv"],
            value="xlsx",
            label="Export as",
        )

        run_batch_btn = gr.Button(
            "Run Batch Sentiment",
            elem_classes=["aip365-button"],
        )

        output_file = gr.File(label="Download result file")
        preview_df = gr.Dataframe(
            label=f"Preview (first {MAX_PREVIEW_ROWS} rows)",
            interactive=False,
        )

        run_batch_btn.click(
            fn=process_file,
            inputs=[file_input, text_column, export_as],
            outputs=[output_file, preview_df],
        )

    # ---------- Footer ----------

    gr.HTML('<div class="aip365-footer">    © 2025 AIpowered365 - Sentiment Intelligence</div>')

if __name__ == "__main__":
    demo.launch()
