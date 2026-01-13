#!/usr/bin/env python3
"""
Create hallucination detection dataset from annotated captions.
This script generates a dataset where the model needs to determine if a given sentence
is a hallucination or not, based on the video and its caption.
"""

import json
import os
import argparse


def create_hallucination_dataset(annotated_captions_path, video_base_path, output_path, max_samples=None):
    """
    Create hallucination detection dataset.
    
    Args:
        annotated_captions_path: Path to annotated_captions.json
        video_base_path: Base path where video files are located
        output_path: Output path for the generated dataset
        max_samples: Maximum number of samples to generate per video (None for all)
    """
    
    # Load annotated captions
    with open(annotated_captions_path, 'r', encoding='utf-8') as f:
        annotated_data = json.load(f)
    
    dataset = []
    
    for item in annotated_data:
        video_url = item.get('video_url', '')
        caption = item.get('caption', '')
        labels_list = item.get('labels', [])
        video_id = item.get('id', '')
        model_name = item.get('model', 'unknown')
        
        # Try to find the video file in subdirectories (long, medium, short)
        full_video_path = None
        video_filename = os.path.basename(video_url)
        
        # First, try the direct path
        direct_path = os.path.join(video_base_path, video_url.lstrip('/'))
        if os.path.exists(direct_path):
            full_video_path = direct_path
        else:
            # Try to find in subdirectories
            for subdir in ['long', 'medium', 'short']:
                test_path = os.path.join(video_base_path, 'Video-MME_sampled', subdir, video_filename)
                if os.path.exists(test_path):
                    full_video_path = test_path
                    break
        
        # Check if video file exists
        if full_video_path is None:
            print(f"Warning: Video not found: {video_url}")
            continue
        
        # Process each labeled sentence
        sample_count = 0
        for label_item in labels_list:
            text = label_item.get('text', '').strip()
            label_tags = label_item.get('labels', [])
            
            if not text or not label_tags:
                continue
            
            # Determine if it's a hallucination
            # Labels can be: "Accurate", "Illusion", "Inaccurate", etc.
            is_hallucination = any(tag in ['Illusion', 'Inaccurate'] for tag in label_tags)
            is_accurate = any(tag in ['Accurate'] for tag in label_tags)
            
            if is_hallucination:
                label_str = "hallucination"
            elif is_accurate:
                label_str = "accurate"
            else:
                label_str = "unknown"
            
            # Skip if label is unknown
            if label_str == "unknown":
                continue
            
            # Create conversation
            conversations = [
                {
                    "from": "human",
                    "value": f"<video>\nHere is a caption describing this video:\n\n{caption}\n\nNow, please determine whether the following statement is accurate or a hallucination based on what you see and hear in the video:\n\nStatement: \"{text}\"\n\nIs this statement accurate or a hallucination? Please answer with either 'accurate' or 'hallucination'."
                },
                {
                    "from": "gpt",
                    "value": label_str
                }
            ]
            
            dataset.append({
                "video": full_video_path,
                "use_audio": True,
                "conversations": conversations,
                "video_id": video_id,
                "model": model_name,
                "statement": text,
                "ground_truth": label_str,
                "original_labels": label_tags
            })
            
            sample_count += 1
            if max_samples and sample_count >= max_samples:
                break
    
    # Save dataset
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"Created hallucination detection dataset with {len(dataset)} samples")
    print(f"Saved to: {output_path}")
    
    # Print statistics
    hallucination_count = sum(1 for item in dataset if item['ground_truth'] == 'hallucination')
    accurate_count = sum(1 for item in dataset if item['ground_truth'] == 'accurate')
    print(f"\nStatistics:")
    print(f"  Accurate: {accurate_count}")
    print(f"  Hallucination: {hallucination_count}")


def main():
    parser = argparse.ArgumentParser(description='Create hallucination detection dataset')
    parser.add_argument('--annotated_captions', type=str, 
                        default='/data1/changbeenkim/video-SALMONN-2/video_SALMONN2_plus/output/test/annotated_captions.json',
                        help='Path to annotated_captions.json')
    parser.add_argument('--video_base_path', type=str,
                        default='/data1/changbeenkim/videoeval',
                        help='Base path where video files are located')
    parser.add_argument('--output', type=str,
                        default='/data1/changbeenkim/video-SALMONN-2/video_SALMONN2_plus/scripts/hallucination_detection_dataset.json',
                        help='Output path for the dataset')
    parser.add_argument('--max_samples', type=int, default=None,
                        help='Maximum number of samples per video (default: all)')
    
    args = parser.parse_args()
    
    create_hallucination_dataset(
        args.annotated_captions,
        args.video_base_path,
        args.output,
        args.max_samples
    )


if __name__ == '__main__':
    main()
