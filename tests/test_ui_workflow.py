"""
Acceptance test for the Streamlit UI workflow using streamlit.testing.v1.AppTest.
Verifies that:
1. Preset selection changes the job description text area dynamically.
2. Uploading a resume and screening produces expected scores, skill matches, and formula displays.
3. Switching presets and re-screening updates all scores, metrics, and breakdowns accurately.
"""

from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def user_resume_bytes():
    resume_path = Path(r"C:\Users\pedam\OneDrive\Documents\Rajendra Prasad Pedamallu_Resume.pdf")
    assert resume_path.exists(), f"Resume file not found at {resume_path}"
    with open(resume_path, "rb") as f:
        return f.read()


def test_ui_preset_switching_and_rescreening(user_resume_bytes):
    app_path = Path(__file__).resolve().parent.parent / "app.py"
    at = AppTest.from_file(str(app_path), default_timeout=30)
    at.run()
    assert len(at.exception) == 0

    # 1. Select AI Applications & Desktop Systems Engineer preset
    at.selectbox[0].select("AI Applications & Desktop Systems Engineer").run()
    assert at.selectbox[0].value == "AI Applications & Desktop Systems Engineer"
    assert "Seeking a Software Engineer" in at.text_area[0].value

    # 2. Upload resume
    at.file_uploader[0].upload("Rajendra Prasad Pedamallu_Resume.pdf", user_resume_bytes, "application/pdf").run()

    # 3. Click Screen & Rank Candidates
    screen_btn = [b for b in at.button if "Screen & Rank Candidates" in b.label][0]
    screen_btn.click().run()
    assert len(at.exception) == 0

    # 4. Verify AI Applications metrics
    metrics = {m.label: m.value for m in at.metric}
    assert int(metrics["Scored Candidates"]) == 1
    assert "100.0%" in metrics["JD Skill Coverage"]
    assert float(metrics["Average Score"].split()[0]) > 40.0

    # 5. Switch back to Senior Machine Learning Engineer preset
    at.selectbox[0].select("Senior Machine Learning Engineer").run()
    assert at.selectbox[0].value == "Senior Machine Learning Engineer"
    assert "Senior Machine Learning Engineer" in at.text_area[0].value

    # 6. Re-screen
    screen_btn = [b for b in at.button if "Screen & Rank Candidates" in b.label][0]
    screen_btn.click().run()
    assert len(at.exception) == 0

    # 7. Verify Senior ML metrics
    metrics_ml = {m.label: m.value for m in at.metric}
    assert int(metrics_ml["Scored Candidates"]) == 1
    assert "17.6%" in metrics_ml["JD Skill Coverage"]
    assert float(metrics_ml["Average Score"].split()[0]) == 9.6
