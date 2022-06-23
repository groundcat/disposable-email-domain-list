import requests
import validators
import DoHClient
import json


def main():
    # Get the invalid domains from the file
    with open('domains_invalid.txt', 'r') as domains_invalid:
        domains_invalid = domains_invalid.read().splitlines()
    print(f"Loaded {len(domains_invalid)} invalid domains saved from your previous run. "
          f"They will be excluded from the scan.")

    # Get URLs from the sources file
    with open('sources.txt', 'r') as sources:
        sources_list = sources.readlines()
    print(f"Found {len(sources_list)} sources")

    # Combine the content from sources urls
    combined_content = ''
    for source in sources_list:
        source = source.strip()
        response = requests.get(source)
        if response.status_code == 200:
            print(f"List contains lines: {len(response.text.splitlines())}")
            combined_content += response.text
        else:
            print(f"{source} could not be accessed")
            exit(1)
    print(f"Total lines: {len(combined_content.splitlines())}")

    combined_list = combined_content.splitlines()
    combined_list_cleaned = []

    # Loop through the combined list and clean up the lines
    for line in combined_list:
        line = line.replace('\n', '').replace('"', '').replace(',', '').strip()
        if line and line not in (combined_list_cleaned or domains_invalid) and validators.domain(line):
            combined_list_cleaned.append(line)
    print(f"Total lines after cleaning: {len(combined_list_cleaned)}")

    # Write the cleaned list to a file
    with open('domains_staged.txt', 'w') as combined_list_file:
        for line in combined_list_cleaned:
            combined_list_file.write(f"{line}\n")
    print(f"Saved {len(combined_list_cleaned)} lines to domains_staged.txt")

    # Check if the domains have MX records
    combined_list_with_mx = []
    combined_list_without_mx = []
    count = 0
    total_cleaned = len(combined_list_cleaned)

    for domain in combined_list_cleaned:
        # clean print output
        print(f"Checking {count} out of {total_cleaned} domains. Percentage complete: {round(count/total_cleaned*100, 2)}%")
        if has_mx_record(domain):
            combined_list_with_mx.append(domain)
        else:
            combined_list_without_mx.append(domain)
        count += 1

    # Write to domains.txt
    with open('domains.txt', 'w') as domains_file:
        for line in combined_list_with_mx:
            domains_file.write(f"{line}\n")
    print(f"Saved {len(combined_list_with_mx)} lines to domains.txt")

    # Write to domains.json
    with open('domains.json', 'w') as domains_json_file:
        # Dump the list to a json file
        domains_json_file.write(f"{json.dumps(combined_list_with_mx, indent=4)}")
    print(f"Saved {len(combined_list_with_mx)} lines to domains.json")

    # Write combined_list_without_mx to domains_invalid.txt
    with open('domains_invalid.txt', 'w') as domains_invalid_file:
        for line in combined_list_without_mx:
            domains_invalid_file.write(f"{line}\n")
    print(f"Saved {len(combined_list_without_mx)} lines to domains_invalid.txt")


def has_mx_record(domain, query_type='MX'):
    try:
        ips = DoHClient.query(name=domain, type=query_type, server='cloudflare-dns.com')
        ip = ips[0]
    except Exception as e:
        # print(f"Unable to resolve: {e}")
        return None
    else:
        # print(f"MX records for {domain}: {ips}")
        if ip:
            # print(f"MX records found for {domain}")
            return True
        else:
            # print(f"No MX records found for {domain}")
            return False


if __name__ == '__main__':
    main()
