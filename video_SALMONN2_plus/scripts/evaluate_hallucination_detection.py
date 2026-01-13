#!/usr/bin/env python3
"""
Evaluate hallucination detection results.
This script compares model predictions with ground truth labels.
"""

import json
import argparse
import os
from collections import defaultdict


def normalize_label(text):
    """Normalize the label text to handle variations."""
    text = text.lower().strip()
    
    # Check for hallucination keywords
    if any(keyword in text for keyword in ['hallucination', 'illusion', 'inaccurate', 'false', 'incorrect']):
        return 'hallucination'
    
    # Check for accurate keywords
    if any(keyword in text for keyword in ['accurate', 'correct', 'true', 'valid']):
        return 'accurate'
    
    # Default: return the text as-is
    return text


def evaluate_predictions(dataset_path, predictions_path, output_path=None):
    """
    Evaluate hallucination detection predictions.
    
    Args:
        dataset_path: Path to the original dataset with ground truth
        predictions_path: Path to the predictions JSON file
        output_path: Optional path to save detailed results
    """
    
    # Load dataset with ground truth
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    # Create a mapping from video path to ground truth
    ground_truth_map = {}
    for item in dataset:
        video_path = item['video']
        statement = item['statement']
        ground_truth = item['ground_truth']
        model = item.get('model', 'unknown')
        key = f"{video_path}||{statement}"
        ground_truth_map[key] = {'ground_truth': ground_truth, 'model': model}
    
    # Load predictions
    with open(predictions_path, 'r', encoding='utf-8') as f:
        predictions = json.load(f)
    
    # Evaluate
    results = []
    correct = 0
    total = 0
    
    # Track performance by category
    category_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    model_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    
    for pred in predictions:
        video_path = pred.get('video', '')
        statement = pred.get('statement', '')
        predicted = normalize_label(pred.get('pred', ''))
        
        key = f"{video_path}||{statement}"
        
        if key not in ground_truth_map:
            print(f"Warning: No ground truth found for: {key[:100]}...")
            continue
        
        gt_data = ground_truth_map[key]
        ground_truth = gt_data['ground_truth']
        model = gt_data['model']
        is_correct = (predicted == ground_truth)
        
        if is_correct:
            correct += 1
        total += 1
        
        # Track by category
        category_stats[ground_truth]['total'] += 1
        if is_correct:
            category_stats[ground_truth]['correct'] += 1
        
        # Track by model
        model_stats[model]['total'] += 1
        if is_correct:
            model_stats[model]['correct'] += 1
        
        results.append({
            'video': video_path,
            'statement': statement,
            'ground_truth': ground_truth,
            'predicted': predicted,
            'correct': is_correct,
            'model': model
        })
    
    # Calculate metrics
    accuracy = correct / total if total > 0 else 0
    
    print("=" * 80)
    print("HALLUCINATION DETECTION EVALUATION RESULTS")
    print("=" * 80)
    print(f"\nOverall Accuracy: {accuracy:.4f} ({correct}/{total})")
    print("\nPer-Category Performance:")
    print("-" * 80)
    
    for category in sorted(category_stats.keys()):
        stats = category_stats[category]
        cat_acc = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
        print(f"  {category.capitalize():15s}: {cat_acc:.4f} ({stats['correct']}/{stats['total']})")
    
    print("\nPer-Model Performance:")
    print("-" * 80)
    for model in sorted(model_stats.keys()):
        stats = model_stats[model]
        model_acc = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
        print(f"  {model:20s}: {model_acc:.4f} ({stats['correct']}/{stats['total']})")
    
    # Calculate precision, recall, and F1 for hallucination detection
    true_positives = sum(1 for r in results if r['ground_truth'] == 'hallucination' and r['predicted'] == 'hallucination')
    false_positives = sum(1 for r in results if r['ground_truth'] == 'accurate' and r['predicted'] == 'hallucination')
    false_negatives = sum(1 for r in results if r['ground_truth'] == 'hallucination' and r['predicted'] == 'accurate')
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    print("\nHallucination Detection Metrics:")
    print("-" * 80)
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
    print("=" * 80)
    
    # Save detailed results if output path is provided
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'accuracy': accuracy,
                'total': total,
                'correct': correct,
                'category_stats': dict(category_stats),
                'model_stats': dict(model_stats),
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'detailed_results': results
            }, f, indent=2, ensure_ascii=False)
        print(f"\nDetailed results saved to: {output_path}")
    
    return accuracy, category_stats


def main():
    parser = argparse.ArgumentParser(description='Evaluate hallucination detection results')
    parser.add_argument('--dataset', type=str, 
                        default='/data1/changbeenkim/video-SALMONN-2/video_SALMONN2_plus/scripts/hallucination_detection_dataset.json',
                        help='Path to the dataset with ground truth')
    parser.add_argument('--predictions', type=str,
                        default='/data1/changbeenkim/video-SALMONN-2/video_SALMONN2_plus/output/hallucination_detection/results.json',
                        help='Path to the predictions file')
    parser.add_argument('--output', type=str, default=None,
                        help='Path to save detailed evaluation results')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.predictions):
        print(f"Error: Predictions file not found: {args.predictions}")
        print("\nPlease run the hallucination detection inference first:")
        print("  bash 1_run_hallucination_detection.sh")
        return
    
    evaluate_predictions(args.dataset, args.predictions, args.output)


if __name__ == '__main__':
    main()
