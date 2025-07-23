# GOSAE Test Dataset Documentation

This directory contains test datasets for validating the GOSAE (Genome Ocean Sparse Autoencoder) pipeline functionality.

## Dataset Overview

The test dataset consists of two classes:
- **Positive samples**: Beta-lactamase sequences (BLA)
- **Negative samples**: Non-beta-lactamase resistance sequences (Non-BLA)

## Data Collection and Processing Pipeline

### 1. Positive Dataset: Beta-lactamase Sequences

#### Initial Data Collection
**NCBI Search Query:**
```
("beta-lactamase"[All Fields] OR "bla"[All Fields]) AND (bacteria[Organism] OR archaea[Organism] OR fungi[Organism]) AND cds[Feature key]
```

This query retrieves all CDS sequences annotated as "beta-lactamase" or "bla" from bacteria, archaea, and fungi.

**Initial Results:**
- Total sequences downloaded: 13,144

#### Sequence Count Verification
```bash
grep ">" sequence.fasta | wc -l
# Output: 13144
```

#### Deduplication
```bash
python3 scripts/remove_duplicates.py sequence.fasta dedup_sequence.fasta --method both
```
**Results:**
- Input sequences: 13,144
- Duplicate sequences removed: 5,823
- Unique sequences retained: 7,321

#### Length Distribution Analysis
```bash
python3 scripts/plot_cds_length_distribution.py test/beta_lactamase/dedup_sequence.fasta
```
**Statistics:**
- Total sequences: 7,321
- Length range: 201 - 133,342 bp
- Mean length: 1,365.04 bp
- Median length: 1,025.00 bp

### 2. Negative Dataset: Non-Beta-lactamase Sequences

#### Data Collection Strategy
To create a balanced dataset, negative samples were collected using resistance-related sequences that exclude beta-lactamase genes.

**NCBI Search Query:**
```
(resistance[Title] OR antimicrobial[Title] OR antibiotic[Title]) NOT (beta-lactamase[Title] OR "bla"[Title]) AND (("Bacteria"[Organism] OR "Bacteria Latreille et al. 1825"[Organism]) OR "Archaea"[Organism] OR "Fungi"[Organism]) AND cds[Feature key] NOT "complete genome"[Title] NOT "complete sequence"[Title] AND "complete cds"[Title]
```

#### Processing Pipeline

**Step 1: Deduplication**
```bash
python3 scripts/remove_duplicates.py test/NonBLA/NON_BLA.fasta test/NonBLA/filted_Non_BLA_sequence.fasta
```
**Results:**
- Input sequences: 2,442
- Duplicate sequences removed: 585
- Unique sequences retained: 1,857

**Step 2: Length Distribution Analysis**
```bash
python3 scripts/plot_cds_length_distribution.py test/NonBLA/filted_Non_BLA_sequence.fasta
```
**Statistics:**
- Total sequences: 1,857
- Length range: 108 - 236,673 bp
- Mean length: 3,316.26 bp
- Median length: 1,920.00 bp

**Step 3: Length-based Filtering**
To ensure comparable sequence lengths between positive and negative datasets:
```bash
python3 scripts/filter_sequences_by_length.py test/NonBLA/filted_Non_BLA_sequence.fasta test/NonBLA/pickedfromrange_filted_Non_BLA_sequence.fasta --min 201 --max 133342
```
**Results:**
- Input sequences: 1,857
- Sequences within range (201-133,342 bp): 1,849
- Selection rate: 99.57%

### 3. Dataset Balancing and Splitting

#### Balanced Dataset Creation
Since the negative dataset contains 1,857 sequences, an equal number of positive samples were randomly selected from the 7,321 available beta-lactamase sequences.

**Positive Sample Subsetting:**
```bash
python3 scripts/subset_split.py test/beta_lactamase/dedup_sequence.fasta subset0.2537.fasta split_train_0.2537.fasta val_train_0.2537.fasta --subset_ratio 0.2537 --split_ratio 0.5 --seed 42
```
**Results:**
- Total sequences: 7,321
- Subset sequences: 1,857 (25.4%)
- Training split: 928 sequences (50.0%)
- Validation split: 929 sequences (50.0%)

**Negative Sample Splitting:**
```bash
python3 scripts/split_train_val.py test/NonBLA/filted_Non_BLA_sequence.fasta test/NonBLA/train_NonBLA.fasta test/NonBLA/val_NonBLA.fasta --ratio 0.5 --seed 42
```
**Results:**
- Total sequences: 1,857
- Training sequences: 928 (50.0%)
- Validation sequences: 929 (50.0%)

#### Final Dataset Assembly
```bash
# Combine training sets
cat split_train_0.2537.fasta train_NonBLA.fasta > True_false_train_set.fasta

# Combine validation sets
cat val_train_0.2537.fasta val_NonBLA.fasta > True_false_validate_set.fasta
```

**Final Dataset Summary:**
- **Training set**: 1,856 sequences (928 positive + 928 negative)
- **Validation set**: 1,858 sequences (929 positive + 929 negative)
- **Total**: 3,714 sequences with 1:1 class balance


## Training Experiments

### Experiment Setup
The balanced dataset was transferred to Lawrencium HPC cluster for training experiments using the GOSAE pipeline.

### Run 4: Initial Training Attempt

**Training Command:**
```bash
python3 train_sae.py \
    --data_dir data \
    --train_files /global/scratch/users/lilei/GOSAE_project/data/EC3.5.2.6/True_false_train_set.fasta.gz \
    --val_files /global/scratch/users/lilei/GOSAE_project/data/EC3.5.2.6/True_false_validate_set.fasta.gz \
    --input_dim 768 \
    --latent_dim 7680 \
    --hidden_dim 180 \
    --sparsity_target 0.01 \
    --l1_coefficient 0.001 \
    --topk 32 \
    --model_name pGenomeOcean/GenomeOcean-100M \
    --target_layers model.layers.10.mlp.up_proj \
    --max_length 5000 \
    --cache_dir cache \
    --use_cache \
    --output_dir /global/scratch/users/lilei/GOSAE_project/data/EC3.5.2.6/output/run4 \
    --batch_size 10 \
    --learning_rate 0.0003 \
    --num_epochs 6 \
    --save_interval 5 \
    --eval_interval 5 \
    --seed 42 \
    --device cuda
```

**Results Analysis:**

✅ **Loss Reduction**: Training loss successfully decreased from ~10⁻² to below 6×10⁻³ over 6 epochs, indicating effective learning.

❌ **Sparsity Target Not Met**:
- Observed sparsity: ~0.5 across all epochs
- Target sparsity: 0.01
- Issue: L1 regularization coefficient (0.001) insufficient to achieve desired sparsity

✅ **No Dead Neurons**: All neurons remained active throughout training, contributing to the learning process.

**Recommendation**: Increase L1 coefficient to strengthen sparsity penalty.

### Run 5: Adjusted L1 Coefficient

**Training Command:**
```bash
python3 train_sae.py \
    --data_dir data \
    --train_files /global/scratch/users/lilei/GOSAE_project/data/EC3.5.2.6/True_false_train_set.fasta.gz \
    --val_files /global/scratch/users/lilei/GOSAE_project/data/EC3.5.2.6/True_false_validate_set.fasta.gz \
    --input_dim 768 \
    --latent_dim 7680 \
    --hidden_dim 180 \
    --sparsity_target 0.01 \
    --l1_coefficient 0.1 \
    --topk 32 \
    --model_name pGenomeOcean/GenomeOcean-100M \
    --target_layers model.layers.10.mlp.up_proj \
    --max_length 5000 \
    --cache_dir cache \
    --use_cache \
    --output_dir /global/scratch/users/lilei/GOSAE_project/data/EC3.5.2.6/output/run5 \
    --batch_size 10 \
    --learning_rate 0.0003 \
    --num_epochs 6 \
    --save_interval 5 \
    --eval_interval 5 \
    --seed 42 \
    --device cuda
```

**Key Changes:**
- Increased L1 coefficient from 0.001 to 0.1 (100x increase)

**Results**: No significant improvement in sparsity achievement.

### Feature Extraction and Analysis

**Activation Extraction Command:**
```bash
python3 extract_activations.py \
    --fasta_file /global/scratch/users/lilei/GOSAE_project/data/EC3.5.2.6/True_false_train_set.fasta.gz \
    --output_dir /global/scratch/users/lilei/GOSAE_project/data/EC3.5.2.6/output/run5 \
    --model pGenomeOcean/GenomeOcean-100M \
    --target_layers model.layers.10.mlp.up_proj \
    --batch_size 10 \
    --max_sequences 5000 \
    --use_cache
```

## File Structure

```
test/
├── beta_lactamase/
│   ├── sequence.fasta              # Raw beta-lactamase sequences (13,144)
│   └── dedup_sequence.fasta        # Deduplicated sequences (7,321)
├── NonBLA/
│   ├── NON_BLA.fasta              # Raw non-BLA sequences (2,442)
│   ├── filted_Non_BLA_sequence.fasta    # Deduplicated sequences (1,857)
│   ├── pickedfromrange_filted_Non_BLA_sequence.fasta  # Length-filtered (1,849)
│   ├── train_NonBLA.fasta         # Training split (928)
│   └── val_NonBLA.fasta           # Validation split (929)
├── subset0.2537.fasta             # BLA subset (1,857)
├── split_train_0.2537.fasta       # BLA training split (928)
├── val_train_0.2537.fasta         # BLA validation split (929)
├── True_false_train_set.fasta     # Combined training set (1,856)
├── True_false_validate_set.fasta  # Combined validation set (1,858)
└── readme.md                      # This documentation
```

## Next Steps

1. **Hyperparameter Optimization**: Further adjust L1 coefficient and other sparsity-related parameters
2. **Feature Analysis**: Analyze extracted activations to understand learned representations
3. **Model Evaluation**: Assess classification performance on the balanced test dataset
4. **Interpretability**: Investigate which genomic features the sparse autoencoder captures

---

**Author**: Li Lei
**Date**: July 2025
**Institution**: Lawrence Berkeley National Laboratory