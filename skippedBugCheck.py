#!/usr/bin/env python3
import csv
import argparse
import subprocess
import os
from collections import defaultdict

def parse_analyzed_bugs_from_csv(csv_file):
    """
    Parse the CSV file to extract analyzed bugs, distinguishing between
    buggy and fixed versions.
    
    Returns two sets: bugs analyzed in buggy state and bugs analyzed in fixed state.
    """
    buggy_analyzed = set()
    fixed_analyzed = set()
    
    try:
        with open(csv_file, 'r') as f:
            csv_reader = csv.DictReader(f)
            
            for row in csv_reader:
                if 'Bug ID' in row and row['Bug ID'].strip() and 'Bug Present' in row:
                    try:
                        bug_id = int(row['Bug ID'].strip())
                        bug_present = row['Bug Present'].strip().lower() == 'true'
                        
                        if bug_present:
                            buggy_analyzed.add(bug_id)
                        else:
                            fixed_analyzed.add(bug_id)
                    except ValueError:
                        continue
    
    except Exception as e:
        print(f"Error parsing CSV file: {e}")
    
    return buggy_analyzed, fixed_analyzed

def get_active_bugs_for_project(project):
    """
    Get the list of active bugs for a specific project from defects4j.
    
    Returns a set of bug IDs.
    """
    try:
        cmd = ['defects4j', 'bids', '-p', project]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error running defects4j for project {project}: {result.stderr}")
            return set()
        
        bug_ids = set()
        for line in result.stdout.strip().split('\n'):
            try:
                if line.strip():
                    bug_ids.add(int(line.strip()))
            except ValueError:
                continue
                
        return bug_ids
        
    except Exception as e:
        print(f"Error getting active bugs for project {project}: {e}")
        return set()

def get_cached_active_bugs(project, cache_dir=".bug_cache"):
    """
    Get active bugs from cache if available, otherwise fetch and cache them.
    """
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    cache_file = os.path.join(cache_dir, f"{project.lower()}_bugs.txt")
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            content = f.read().strip()
            if content:
                bug_ids = set()
                for line in content.split('\n'):
                    try:
                        if line.strip():
                            bug_ids.add(int(line.strip()))
                    except ValueError:
                        continue
                print(f"Using cached active bugs for {project}")
                return bug_ids
    
    print(f"Fetching active bugs for {project} from defects4j (this may take a moment)...")
    active_bugs = get_active_bugs_for_project(project)
    
    if active_bugs:
        with open(cache_file, 'w') as f:
            for bug_id in sorted(active_bugs):
                f.write(f"{bug_id}\n")
    
    return active_bugs

def manually_specify_active_bugs(project, bug_range=None):
    """
    Allow manual specification of active bugs, either by range or by reading from a file.
    """
    if bug_range:
        try:
            start, end = map(int, bug_range.split('-'))
            active_bugs = set(range(start, end + 1)) 
            print(f"Using manual range {bug_range} for {project}")
            return active_bugs
        except ValueError:
            print(f"Invalid range format: {bug_range}. Please use format like '1-106'")
            return set()
    else:
        return set()

def main():
    parser = argparse.ArgumentParser(description='Find skipped bugs in defects4j projects')
    parser.add_argument('--input', '-i', required=True, help='Path to your CSV file with analyzed bugs')
    parser.add_argument('--project', '-p', default='Math', help='Project name to check (default: Math)')
    parser.add_argument('--use-defects4j', '-d', action='store_true', help='Always use defects4j command even if cached')
    parser.add_argument('--range', '-r', help='Optional manual range of active bugs (e.g., "1-106" for Math)')
    parser.add_argument('--active-bugs-file', '-a', help='Optional file with list of active bug IDs (one per line)')
    
    args = parser.parse_args()

    buggy_analyzed, fixed_analyzed = parse_analyzed_bugs_from_csv(args.input)
    
    all_analyzed = buggy_analyzed | fixed_analyzed
    
    only_buggy_analyzed = buggy_analyzed - fixed_analyzed
    only_fixed_analyzed = fixed_analyzed - buggy_analyzed
    both_versions_analyzed = buggy_analyzed & fixed_analyzed
    
    print(f"Found {len(all_analyzed)} unique bugs in CSV file:")
    print(f"  - {len(both_versions_analyzed)} bugs with both buggy and fixed versions analyzed")
    print(f"  - {len(only_buggy_analyzed)} bugs with only buggy version analyzed")
    print(f"  - {len(only_fixed_analyzed)} bugs with only fixed version analyzed")
    
    active_bugs = set()
    
    if args.range:
        active_bugs = manually_specify_active_bugs(args.project, args.range)
    elif args.active_bugs_file:
        try:
            with open(args.active_bugs_file, 'r') as f:
                for line in f:
                    try:
                        if line.strip():
                            active_bugs.add(int(line.strip()))
                    except ValueError:
                        continue
            print(f"Read {len(active_bugs)} active bugs from {args.active_bugs_file}")
        except Exception as e:
            print(f"Error reading active bugs file: {e}")
    elif args.use_defects4j:
        active_bugs = get_active_bugs_for_project(args.project)
    else:
        active_bugs = get_cached_active_bugs(args.project)
    
    if not active_bugs:
        print(f"Warning: No active bugs found for project {args.project}")
        return
    
    completely_skipped_bugs = active_bugs - all_analyzed
    
    incomplete_bugs = (active_bugs & only_buggy_analyzed) | (active_bugs & only_fixed_analyzed)
    
    complete_bugs = active_bugs & both_versions_analyzed
    
    extra_bugs = all_analyzed - active_bugs
  
    print(f"\nResults for project: {args.project}")
    print(f"  Active bugs: {len(active_bugs)}")
    print(f"  Active bug ID range: {min(active_bugs)}-{max(active_bugs)}")
    
    print(f"\nAnalysis breakdown:")
    print(f"  Completely analyzed bugs (both versions): {len(complete_bugs)}")
    print(f"  Partially analyzed bugs (one version): {len(incomplete_bugs)}")
    if incomplete_bugs:
        missing_buggy = active_bugs & only_fixed_analyzed
        missing_fixed = active_bugs & only_buggy_analyzed
        
        if missing_buggy:
            print(f"    - Bugs missing buggy version: {sorted(list(missing_buggy))}")
        if missing_fixed:
            print(f"    - Bugs missing fixed version: {sorted(list(missing_fixed))}")
    
    print(f"  Completely skipped bugs: {len(completely_skipped_bugs)}")
    if completely_skipped_bugs:
        print(f"    - Skipped bug IDs: {sorted(list(completely_skipped_bugs))}")
    
    if extra_bugs:
        print(f"\nNote: Found {len(extra_bugs)} bug IDs in your CSV that aren't in the active bugs list")
        print(f"  Extra bug IDs: {sorted(list(extra_bugs))}")

if __name__ == "__main__":
    main()