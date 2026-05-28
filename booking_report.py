

import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yagmail
import os
import schedule
import time


# =============================
# 1. DATABASE CONNECTION
# =============================
def get_data_from_sql():
    
    print("🔌 Connecting to SQL Server...")

    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=125.22.246.228;"
        "DATABASE=GCT;"
        "UID=Intern;"
        "PWD=Welcome@123!;"
        "TrustServerCertificate=yes;"
    )

    query = "EXEC sp_ReportBooking ?, ?, ?, ?, ?"
    params = (" where bookingId > 0", " where bookingId > 0", 535, 0, "")

    df = pd.read_sql(query, conn, params=params)
    conn.close()

    print("✅ Data fetched from SQL Server")
    
    return df


# =============================
# 2. EXCEL REPORT GENERATION
# =============================
def generate_excel_report(df):
    print("📊 Generating Excel report...")

    df['BookingDate'] = pd.to_datetime(df['BookingDate'], errors='coerce')
    df.fillna(0, inplace=True)

    tenant_summary = df.groupby('tenantId')['bookingId'].count().reset_index(name='TotalBookings')
    finance_summary = df.groupby('tenantId')[['paymentamount', 'totalamount', 'PROFIT']].sum().reset_index()

    report_path = os.path.join(os.getcwd(), "BookingReport.xlsx")

    with pd.ExcelWriter(report_path) as writer:
        df.to_excel(writer, sheet_name='RawData', index=False)
        tenant_summary.to_excel(writer, sheet_name='TenantSummary', index=False)
        finance_summary.to_excel(writer, sheet_name='FinanceSummary', index=False)

    print("✅ Excel report created")
    return tenant_summary, report_path


# =============================
# 3. CHART GENERATION
# =============================
def generate_chart(df):
    print("📈 Generating chart...")

    charts_folder = os.path.join(os.getcwd(), "charts")
    os.makedirs(charts_folder, exist_ok=True)

    chart_path = os.path.join(charts_folder, "BookingsChart.png")

    # Ensure datetime
    df['BookingDate'] = pd.to_datetime(df['BookingDate'], errors='coerce')

    df['Month'] = df['BookingDate'].dt.to_period('M').astype(str)

    monthly_summary = (
        df.groupby('Month')['bookingId']
        .count()
        .reset_index(name='TotalBookings')
        .sort_values('Month')
    )

    plt.figure(figsize=(10, 5))
    plt.plot(
        monthly_summary['Month'],
        monthly_summary['TotalBookings'],
        marker='o'
    )
    plt.xticks(rotation=45)
    plt.xlabel("Month")
    plt.ylabel("Total Bookings")
    plt.title("Bookings per Month")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    print("✅ Chart saved")
    return chart_path



# =============================
# 4. GMAIL SENDING
# =============================
def send_gmail(report_path, chart_path):
    print("📧 Sending email...")

    yag = yagmail.SMTP(
        user="santy1nova2@gmail.com",
        password="cwmn vxkx qgzi lyto"
    )

    yag.send(
        to="prabu@seaknots.in",
        cc=["kuppu@seaknots.in", "nanda@seaknots.in","releaseengineer@seaknots.in"],
        subject="Daily Booking Report",
        contents=[
            "Hello,\n\nPlease find attached the automated booking report(20min).\n\nRegards,\nIntern",
            report_path,
            chart_path
        ]
    )

    print("✅ Email sent successfully")


# =============================
# 5. MAIN CONTROLLER
# =============================
def main():
    df = get_data_from_sql()
    tenant_summary, report_path = generate_excel_report(df)
    chart_path = generate_chart(df)
    send_gmail(report_path, chart_path)
    print("🎉 Entire process completed successfully")
# =============================
# SCHEDULER SETUP
# =============================
def scheduled_job():
    try:
        
        print("⏰ Scheduled job started")
        main()
    except Exception as e:
        print("❌ Error in scheduled job:", e)


if __name__ == "__main__":
    print("🚀 Scheduler started (runs every 20 minutes)")
    scheduled_job()
    schedule.every(2).minutes.do(scheduled_job)

    while True:
        schedule.run_pending()
        time.sleep(1)




# =============================
# PROGRAM STARTS HERE
# =============================
if __name__ == "__main__":
    main()

# i have this content


# i am going this with again please gimme steps to do it
