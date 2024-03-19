def remove_duplicate_urls(input_file, output_file):
    # Open the input file in read mode and output file in write mode
    with open(input_file, 'r') as file_in, open(output_file, 'w') as file_out:
        # Read all lines from the input file
        lines = file_in.readlines()

        # Create a set to store unique URLs
        unique_urls = set()

        # Iterate through each line in the list of lines
        for line in lines:
            # Strip any leading or trailing whitespace characters
            url = line.strip()

            # Check if the URL is not empty and add it to the set
            if url:
                unique_urls.add(url)

        # Write the unique URLs back to the output file
        for unique_url in unique_urls:
            file_out.write(unique_url + '\n')

    print(f"Duplicate URLs removed. Unique URLs written to {output_file}")

# Example usage
input_file = 'pdf_links.txt'  # Replace 'input.txt' with your input file name
output_file = 'pdf.txt'  # Replace 'output.txt' with your output file name
remove_duplicate_urls(input_file, output_file)
