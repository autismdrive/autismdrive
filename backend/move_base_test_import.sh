#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 <search_string> <glob_pattern> [--dry-run]"
    exit 1
}

# Check if there are at least two arguments
if [ $# -lt 2 ]; then
    usage
fi

# Assign arguments to variables
search_string="$1"
glob_pattern="$2"
dry_run=false
edited_count=0  # Counter for edited files

# Check for the dry-run flag
if [ "$3" == "--dry-run" ]; then
    dry_run=true
    echo "Running in dry-run mode: No files will be modified."
fi

# Function to check for command success and handle errors
check_command_success() {
    if [ $? -ne 0 ]; then
        echo "Error: Command failed on line $1!"
        exit 1
    fi
}

# Iterate over files matching the glob pattern
for file in $glob_pattern; do
    if [ -f "$file" ]; then
        echo "Processing file: $file"

        # Temporary file to store modified content
        tmp_file=$(mktemp)
        check_command_success 1  # Check mktemp command

        # Using gawk to process the file
        if [ "$dry_run" = true ]; then
            # Dry-run: Show lines that would be moved and appended
            gawk -v search_string="$search_string" '
            BEGIN { moved = 0 }
            $0 ~ search_string {
                if (moved == 0) {
                    print "Would move the following matching lines to the top of the file:"
                    moved = 1
                }
                print "Would move line: " NR ": " $0
            }
            { non_matching_lines[NR] = $0 }
            END {
                if (moved == 0) {
                    print "No matching lines found."
                }
                print "Would append non-matching lines below."
            }' "$file"
            check_command_success 2  # Check gawk dry-run command
        else
            # Actual processing: Move matching lines to the top and append non-matching lines
            gawk -v search_string="$search_string" '
            BEGIN { moved = 0 }
            $0 ~ search_string {
                if (moved == 0) {
                    moved = 1
                }
                print $0
            }
            { non_matching_lines[NR] = $0 }
            END {
                for (i in non_matching_lines) {
                    if (non_matching_lines[i] !~ search_string) {
                        print non_matching_lines[i]
                    }
                }
            }' "$file" > "$tmp_file"
            check_command_success 3  # Check gawk processing command

            # Overwrite the original file with the modified content
            mv "$tmp_file" "$file"
            check_command_success 4  # Check mv command
            echo "Moved matching lines to the top of $file"
            ((edited_count++))  # Increment the edited file count
        fi
    else
        echo "Skipping $file (not a valid file)"
    fi
done

# Print the number of files edited
echo "Number of files edited: $edited_count"
