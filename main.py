import psutil
import pandas as pd
import boto3
import os
from datetime import datetime

cpu = psutil.cpu_percent()

memory = psutil.virtual_memory()

disk = psutil.disk_usage('C:')

print(f"CPU: {cpu}")
print(f"RAM: {memory.percent}")
print(f"Disk: {disk.percent}")

reports_folder = r"C:\Users\User\IT-Support-Automation-Toolkit\reports"

os.makedirs(reports_folder, exist_ok=True)

report_df = pd.DataFrame({
    "Metric": ["CPU Usage", "RAM Usage", "Disk Usage"],
    "Value": [cpu, memory.percent, disk.percent]
})

excel_file = os.path.join(
    reports_folder,
    "daily_report.xlsx"
)

report_df.to_excel(
    excel_file,
    index=False
)

print("Excel report created")

history_file = os.path.join(
    reports_folder,
    "history.csv"
)

new_row = pd.DataFrame({
    "timestamp": [datetime.now()],
    "cpu": [cpu],
    "ram": [memory.percent],
    "disk": [disk.percent]
})

if os.path.exists(history_file):
    new_row.to_csv(
        history_file,
        mode="a",
        header=False,
        index=False
    )
else:
    new_row.to_csv(
        history_file,
        index=False
    )

print("History updated")

try:
    s3 = boto3.client("s3")

    s3.upload_file(
        excel_file,
        "mathew-it-automation-reports-2026",
        "daily_report.xlsx"
    )

    print("AWS Upload Successful!")

except Exception as e:

    print("AWS Upload Failed")
    print(e)

print("Monitoring Complete")
