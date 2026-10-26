# SS3 Part B — STADIOEquities activation model

## Submission contents

- `SS3_PartB.ipynb`: fully documented end-to-end Jupyter notebook with all marking sections (2 + 5 + 5 + 5 + 3 = 20 marks).
- `data/`: original supplied nine-table synthetic client extract;
- `data/README.md`: data dictionary, target rationale, leakage decisions and limitations.
- `requirements.txt`: Python library dependencies.
- `outputs/` (created by running the notebook): metrics, holdout predictions and trained pipeline.

## Running instructions

1. Install Python 3.10 or newer and Jupyter Notebook/JupyterLab.
2. In a terminal in this folder, run `python -m pip install -r requirements.txt`.
3. Launch `jupyter notebook SS3_PartB.ipynb` or open the notebook in VS Code.
4. Click **Run All** (restart kernel first if rerunning). Sections run top to bottom and finish by writing `outputs/` files.
5. Review the actual printed class proportions, metrics, model plots and final markdown discussion.

## Approach

**Target:** `activation_outcome` (first successful deposit activation definition). The observation is a unique registered client. **Final chosen method:** Random Forest classification using only registration-time features. Chronological 60%/20%/20% train/validation/test split, with all preprocessing fitted on training data only. The untouched last 20% is the final unseen test cohort. The Random Forest classifier does not have learning rate or epochs. A majority-class dummy baseline provides context.

## Reproducibility and limitations

- Random state = 42; dataset has 3,109 original account/label rows and 3,100 unique clients after removal of 9 duplicate IDs.
- Model inputs: age, acquisition cost, registration month, province/region, stated goal, risk appetite, client segment, acquisition channel and campaign. Post-registration fields are excluded to avoid label leakage.
- Synthetic dataset: performance should not be interpreted as real-world production effectiveness.
- Exact library versions can change metrics slightly. `joblib` model files should only be loaded from trusted sources.
- Original source `stadioequities/README.md` (inside the ZIP) provides complete descriptions of all nine tables.

## Observed performance and honest interpretation

Completed run: train accuracy **94.1%**, validation accuracy **50.2%**, test accuracy **50.5%**, test ROC-AUC **0.500**. This indicates severe overfitting: the model is an exercise in a correct, leak-free workflow, **not a deployable predictor**. See the notebook’s final interpretation section.
