import os
import json

from config import *

input_directory = "articles"

output_directory = "reports"
os.makedirs(output_directory, exist_ok=True)



for pattern_name, pattern_url in bad_patterns.items():

    domain_count = {}

    report_filename = os.path.join(output_directory, f"{pattern_name}_report.json")

    for filename in os.listdir(input_directory):
        if filename.endswith(".json") and filename.startswith(pattern_name):
            with open(os.path.join(input_directory, filename), "r", encoding="utf-8") as file:
                articles = json.load(file)

                for article in articles:
                    domain_url = article.get("domain_url")
                    if domain_url:
                        domain_count[domain_url] = domain_count.get(domain_url, 0) + 1


    sorted_report = dict(sorted(domain_count.items(), key=lambda x: x[1], reverse=True))

    with open(report_filename, "w", encoding="utf-8") as report_file:
        json.dump(sorted_report, report_file, ensure_ascii=False, indent=4)
    print(f"Saved sorted report for pattern '{pattern_name}' as {report_filename}")
