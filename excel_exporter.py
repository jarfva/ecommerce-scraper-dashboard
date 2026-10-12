"""
Professional Styled Excel Exporter
Author: Fajar Setya (@jarfva)
Description: Converts raw scraped DataFrames into an agency-grade formatted Excel spreadsheet
with custom typography, corporate color palettes, KPI summary sheets, and auto-filters.
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def export_to_professional_excel(df, output_path="scraped_catalog_report.xlsx"):
    wb = openpyxl.Workbook()
    
    # -------------------------------------------------------------
    # 1. SUMMARY SHEET (Executive KPIs)
    # -------------------------------------------------------------
    ws_summary = wb.active
    ws_summary.title = "Executive Summary"
    ws_summary.views.sheetView[0].showGridLines = True

    # Color definitions (Modern Corporate Palette)
    navy_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    accent_fill = PatternFill(start_color="0EA5E9", end_color="0EA5E9", fill_type="solid")
    soft_card_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    white_bold = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    title_font = Font(name="Segoe UI", size=16, bold=True, color="0F172A")
    subtitle_font = Font(name="Segoe UI", size=10, italic=True, color="64748B")
    metric_label_font = Font(name="Segoe UI", size=9, bold=True, color="64748B")
    metric_val_font = Font(name="Segoe UI", size=16, bold=True, color="0F172A")
    regular_font = Font(name="Segoe UI", size=10, color="1E293B")
    bold_font = Font(name="Segoe UI", size=10, bold=True, color="1E293B")

    thin_border = Border(
        left=Side(style='thin', color='E2E8F0'),
        right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='E2E8F0'),
        bottom=Side(style='thin', color='E2E8F0')
    )

    # Title Banner
    ws_summary["B2"] = "E-Commerce Market Intelligence Report"
    ws_summary["B2"].font = title_font
    ws_summary["B3"] = "Automated Extraction & Pipeline by Fajar Setya (@jarfva) | Verified Freelance Delivery"
    ws_summary["B3"].font = subtitle_font

    # KPI Calculation
    total_items = len(df)
    avg_price = df["price_gbp"].mean() if total_items > 0 else 0
    min_price = df["price_gbp"].min() if total_items > 0 else 0
    max_price = df["price_gbp"].max() if total_items > 0 else 0
    in_stock_count = df[df["availability"].str.contains("In stock", case=False, na=False)].shape[0]
    stock_rate = (in_stock_count / total_items * 100) if total_items > 0 else 0

    # KPI Cards (Row 5 - 7)
    kpi_cards = [
        ("B", "C", "TOTAL PRODUCTS", f"{total_items:,}"),
        ("D", "E", "AVERAGE PRICE", f"£{avg_price:.2f}"),
        ("F", "G", "PRICE RANGE", f"£{min_price:.2f} - £{max_price:.2f}"),
        ("H", "I", "IN-STOCK RATE", f"{stock_rate:.1f}%")
    ]

    for start_col, end_col, label, val in kpi_cards:
        c1, c2 = f"{start_col}5", f"{end_col}5"
        c3, c4 = f"{start_col}6", f"{end_col}6"
        ws_summary.merge_cells(f"{c1}:{c2}")
        ws_summary.merge_cells(f"{c3}:{c4}")
        
        ws_summary[c1] = label
        ws_summary[c1].font = metric_label_font
        ws_summary[c1].fill = soft_card_fill
        ws_summary[c1].alignment = Alignment(horizontal="center", vertical="center")
        
        ws_summary[c3] = val
        ws_summary[c3].font = metric_val_font
        ws_summary[c3].fill = soft_card_fill
        ws_summary[c3].alignment = Alignment(horizontal="center", vertical="center")

        for r in range(5, 7):
            for c in [start_col, end_col]:
                ws_summary[f"{c}{r}"].border = thin_border

    # Breakdown by Rating Table
    ws_summary["B9"] = "RATING BREAKDOWN"
    ws_summary["B9"].font = bold_font
    
    headers_summary = ["Rating Tier", "Product Count", "Avg Price (£)", "Market Share"]
    for i, h in enumerate(headers_summary, start=2):
        col_letter = get_column_letter(i)
        cell = ws_summary[f"{col_letter}10"]
        cell.value = h
        cell.font = white_bold
        cell.fill = navy_fill
        cell.alignment = Alignment(horizontal="center" if i != 2 else "left")

    rating_summary = df.groupby("rating").agg(
        count=("price_gbp", "count"),
        avg_price=("price_gbp", "mean")
    ).reset_index().sort_values(by="rating", ascending=False)

    curr_row = 11
    for _, row in rating_summary.iterrows():
        r_val = int(row["rating"])
        stars = "★" * r_val + "☆" * (5 - r_val)
        count_val = int(row["count"])
        price_val = float(row["avg_price"])
        share = count_val / total_items * 100 if total_items > 0 else 0

        ws_summary[f"B{curr_row}"] = f"{stars} ({r_val} Stars)"
        ws_summary[f"C{curr_row}"] = count_val
        ws_summary[f"D{curr_row}"] = f"£{price_val:.2f}"
        ws_summary[f"E{curr_row}"] = f"{share:.1f}%"

        for col_idx in range(2, 6):
            cell = ws_summary[f"{get_column_letter(col_idx)}{curr_row}"]
            cell.font = regular_font
            cell.border = thin_border
            if col_idx in (3, 4, 5):
                cell.alignment = Alignment(horizontal="center")

        curr_row += 1

    # -------------------------------------------------------------
    # 2. DATA SHEET (Detailed Catalog)
    # -------------------------------------------------------------
    ws_data = wb.create_sheet(title="Catalog Dataset")
    ws_data.views.sheetView[0].showGridLines = True

    display_cols = [
        ("SKU ID", "id"),
        ("Product Title", "title"),
        ("Price (GBP)", "price_gbp"),
        ("Customer Rating", "stars"),
        ("Stock Status", "availability"),
        ("Product Live URL", "product_url"),
        ("Image Asset URL", "image_url")
    ]

    # Write Headers
    for col_idx, (header_label, _) in enumerate(display_cols, start=1):
        cell = ws_data.cell(row=1, column=col_idx, value=header_label)
        cell.font = white_bold
        cell.fill = navy_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    ws_data.row_dimensions[1].height = 28

    # Zebra fills
    zebra_light = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    in_stock_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    in_stock_font = Font(name="Segoe UI", size=10, bold=True, color="166534")

    # Populate Data
    for row_idx, row in df.iterrows():
        excel_row = row_idx + 2
        is_even = (row_idx % 2 == 0)
        row_fill = None if is_even else zebra_light

        # SKU ID
        cell_sku = ws_data.cell(row=excel_row, column=1, value=f"SKU-{1000 + row_idx}")
        cell_sku.alignment = Alignment(horizontal="center")

        # Title
        cell_title = ws_data.cell(row=excel_row, column=2, value=str(row["title"]))

        # Price
        cell_price = ws_data.cell(row=excel_row, column=3, value=float(row["price_gbp"]))
        cell_price.number_format = '£#,##0.00'
        cell_price.alignment = Alignment(horizontal="right")

        # Rating
        cell_rating = ws_data.cell(row=excel_row, column=4, value=str(row["stars"]))
        cell_rating.alignment = Alignment(horizontal="center")

        # Availability
        cell_avail = ws_data.cell(row=excel_row, column=5, value=str(row["availability"]))
        cell_avail.alignment = Alignment(horizontal="center")
        if "in stock" in str(row["availability"]).lower():
            cell_avail.fill = in_stock_fill
            cell_avail.font = in_stock_font

        # URLs
        cell_purl = ws_data.cell(row=excel_row, column=6, value=str(row["product_url"]))
        cell_iurl = ws_data.cell(row=excel_row, column=7, value=str(row["image_url"]))

        # Apply basic borders and fonts
        for col_idx in range(1, 8):
            c = ws_data.cell(row=excel_row, column=col_idx)
            c.border = thin_border
            if c != cell_avail or not ("in stock" in str(row["availability"]).lower()):
                c.font = regular_font
            if row_fill and c != cell_avail:
                c.fill = row_fill

        ws_data.row_dimensions[excel_row].height = 20

    # Auto-adjust column widths for both sheets
    for ws in [ws_summary, ws_data]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or "")
                # Ignore merged cells in width calculation
                if cell.coordinate in ["B2", "B3"]:
                    continue
                max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    # Enable AutoFilter on Catalog Dataset
    last_col = get_column_letter(len(display_cols))
    last_row = len(df) + 1
    ws_data.auto_filter.ref = f"A1:{last_col}{last_row}"

    # Freeze panes on Catalog Dataset (Freeze Row 1)
    ws_data.freeze_panes = "A2"

    wb.save(output_path)
    return output_path

if __name__ == "__main__":
    import pandas as pd
    sample_df = pd.DataFrame([
        {"title": "A Light in the Attic", "price_gbp": 51.77, "rating": 3, "stars": "★★★☆☆", "availability": "In stock", "product_url": "http://example.com/1", "image_url": "http://example.com/1.jpg"},
        {"title": "Tipping the Velvet", "price_gbp": 53.74, "rating": 1, "stars": "★☆☆☆☆", "availability": "In stock", "product_url": "http://example.com/2", "image_url": "http://example.com/2.jpg"},
    ])
    export_to_professional_excel(sample_df)
    print("Exported successfully!")
