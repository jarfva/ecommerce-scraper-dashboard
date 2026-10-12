"""
Interactive Web Dashboard Generator for Scraped Datasets
Author: Fajar Setya (@jarfva)
Description: Generates an elegant, modern dark-themed web dashboard to explore,
filter, and visualize extracted web data with Chart.js and Tailwind CSS.
"""

import json

def generate_web_dashboard(df, output_html="dashboard.html", excel_filename="scraped_catalog_report.xlsx"):
    records = df.to_dict(orient="records")
    data_json = json.dumps(records)

    html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Data Extraction & Market Intelligence Dashboard</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{
                            50: '#f0fdf4',
                            500: '#22c55e',
                            600: '#16a34a',
                            700: '#15803d'
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased selection:bg-emerald-500 selection:text-white">

    <!-- Top Navigation -->
    <nav class="border-b border-slate-800 bg-slate-900/70 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-cyan-500 flex items-center justify-center text-slate-950 font-black text-xl shadow-lg shadow-emerald-500/20">
                    <i class="fa-solid fa-bolt"></i>
                </div>
                <div>
                    <span class="font-bold text-lg tracking-tight text-white">ScraperFlow <span class="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">v2.4 Production</span></span>
                    <p class="text-xs text-slate-400">Automated Web Extraction by <span class="text-slate-200 font-medium">Fajar Setya (@jarfva)</span></p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <a href="{excel_filename}" download class="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-slate-900 bg-emerald-400 hover:bg-emerald-300 rounded-lg shadow-sm transition">
                    <i class="fa-solid fa-file-excel"></i>
                    <span>Download Clean Excel</span>
                </a>
            </div>
        </div>
    </nav>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

        <!-- Header Hero -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/40 p-6 rounded-2xl border border-slate-800">
            <div>
                <h1 class="text-2xl sm:text-3xl font-extrabold text-white">E-Commerce Market Catalog Dashboard</h1>
                <p class="text-slate-400 text-sm mt-1">Live visualization of structured data extracted using Python, BeautifulSoup, and automated pipeline.</p>
            </div>
            <div class="flex items-center gap-2 text-xs text-slate-400 bg-slate-800/80 px-3 py-2 rounded-lg border border-slate-700">
                <i class="fa-solid fa-circle-check text-emerald-400"></i>
                <span>Status: Pipeline Executed Successfully (100% Parsed)</span>
            </div>
        </div>

        <!-- Metrics Overview Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
                <div>
                    <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Total Products</p>
                    <p id="metric-total" class="text-2xl font-black text-white mt-1">0</p>
                </div>
                <div class="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center text-xl">
                    <i class="fa-solid fa-box-archive"></i>
                </div>
            </div>

            <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
                <div>
                    <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Average Price</p>
                    <p id="metric-avg-price" class="text-2xl font-black text-white mt-1">£0.00</p>
                </div>
                <div class="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center text-xl">
                    <i class="fa-solid fa-tag"></i>
                </div>
            </div>

            <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
                <div>
                    <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">In-Stock Rate</p>
                    <p id="metric-stock-rate" class="text-2xl font-black text-white mt-1">0%</p>
                </div>
                <div class="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center text-xl">
                    <i class="fa-solid fa-warehouse"></i>
                </div>
            </div>

            <div class="p-5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
                <div>
                    <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Average Rating</p>
                    <p id="metric-avg-rating" class="text-2xl font-black text-amber-400 mt-1">0.0 / 5.0</p>
                </div>
                <div class="w-12 h-12 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center text-xl">
                    <i class="fa-solid fa-star"></i>
                </div>
            </div>
        </div>

        <!-- Chart Section -->
        <div class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800">
            <h2 class="text-base font-semibold text-white mb-4 flex items-center gap-2">
                <i class="fa-solid fa-chart-simple text-emerald-400"></i>
                Rating Distribution & Inventory Breakdown
            </h2>
            <div class="h-64">
                <canvas id="ratingChart"></canvas>
            </div>
        </div>

        <!-- Filter & Search Control Bar -->
        <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 flex flex-col md:flex-row gap-4 items-center justify-between">
            <div class="relative w-full md:w-96">
                <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-3.5 text-slate-400 text-sm"></i>
                <input id="searchInput" type="text" placeholder="Search book title..." class="w-full pl-10 pr-4 py-2 bg-slate-950 border border-slate-700 rounded-lg text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition">
            </div>

            <div class="flex flex-wrap items-center gap-3 w-full md:w-auto">
                <select id="ratingFilter" class="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-emerald-500">
                    <option value="all">All Ratings</option>
                    <option value="5">5 Stars</option>
                    <option value="4">4 Stars</option>
                    <option value="3">3 Stars</option>
                    <option value="2">2 Stars</option>
                    <option value="1">1 Star</option>
                </select>

                <select id="sortFilter" class="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-emerald-500">
                    <option value="default">Sort by: Default</option>
                    <option value="price-asc">Price: Low to High</option>
                    <option value="price-desc">Price: High to Low</option>
                    <option value="rating-desc">Rating: Highest</option>
                </select>

                <button id="resetBtn" class="px-3 py-2 text-sm text-slate-400 hover:text-white transition">
                    <i class="fa-solid fa-arrow-rotate-left mr-1"></i> Reset
                </button>
            </div>
        </div>

        <!-- Products Table -->
        <div class="rounded-xl border border-slate-800 bg-slate-900 overflow-hidden shadow-xl">
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm">
                    <thead class="bg-slate-950/80 border-b border-slate-800 text-slate-400 uppercase text-xs font-semibold">
                        <tr>
                            <th class="py-3.5 px-4">Item</th>
                            <th class="py-3.5 px-4">Title</th>
                            <th class="py-3.5 px-4">Price</th>
                            <th class="py-3.5 px-4">Rating</th>
                            <th class="py-3.5 px-4">Availability</th>
                            <th class="py-3.5 px-4 text-right">Action</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody" class="divide-y divide-slate-800/60 font-normal">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
            <div id="noResults" class="hidden p-8 text-center text-slate-400">
                <i class="fa-regular fa-folder-open text-3xl mb-2"></i>
                <p>No products found matching the criteria.</p>
            </div>
        </div>

        <!-- Footer Portfolio Attribution -->
        <footer class="pt-8 border-t border-slate-800/80 text-center text-xs text-slate-500 space-y-2">
            <p>Designed & Engineered by <span class="text-slate-300 font-semibold">Fajar Setya</span> • Specialist in Python Automation & Web Scraping</p>
            <p>Available on <a href="https://fastwork.id/user/jarfva" target="_blank" class="text-emerald-400 hover:underline">Fastwork</a>, <a href="https://www.fiverr.com/jarfva" target="_blank" class="text-emerald-400 hover:underline">Fiverr</a>, <a href="https://www.upwork.com/freelancers/~01f02c11dadbf80c0a" target="_blank" class="text-emerald-400 hover:underline">Upwork</a>, & Contra</p>
        </footer>

    </main>

    <!-- Embedded Scraped Dataset -->
    <script>
        const rawData = {data_json};

        // Initialize Metrics
        const totalItems = rawData.length;
        const totalPrice = rawData.reduce((acc, curr) => acc + curr.price_gbp, 0);
        const avgPrice = totalItems > 0 ? (totalPrice / totalItems).toFixed(2) : '0.00';
        const inStockCount = rawData.filter(item => item.availability.toLowerCase().includes('in stock')).length;
        const inStockRate = totalItems > 0 ? ((inStockCount / totalItems) * 100).toFixed(1) : 0;
        const totalRating = rawData.reduce((acc, curr) => acc + curr.rating, 0);
        const avgRating = totalItems > 0 ? (totalRating / totalItems).toFixed(1) : '0.0';

        document.getElementById('metric-total').textContent = totalItems.toLocaleString();
        document.getElementById('metric-avg-price').textContent = `£${{avgPrice}}`;
        document.getElementById('metric-stock-rate').textContent = `${{inStockRate}}%`;
        document.getElementById('metric-avg-rating').textContent = `${{avgRating}} / 5.0`;

        // Render Chart
        const ratingCounts = [0, 0, 0, 0, 0];
        rawData.forEach(item => {{
            if (item.rating >= 1 && item.rating <= 5) {{
                ratingCounts[item.rating - 1]++;
            }}
        }});

        const ctx = document.getElementById('ratingChart').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'],
                datasets: [{{
                    label: 'Product Count',
                    data: ratingCounts,
                    backgroundColor: [
                        'rgba(239, 68, 68, 0.7)',
                        'rgba(249, 115, 22, 0.7)',
                        'rgba(234, 179, 8, 0.7)',
                        'rgba(59, 130, 246, 0.7)',
                        'rgba(34, 197, 94, 0.7)'
                    ],
                    borderColor: [
                        '#ef4444', '#f97316', '#eab308', '#3b82f6', '#22c55e'
                    ],
                    borderWidth: 1,
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
                        ticks: {{ color: '#94a3b8' }}
                    }},
                    x: {{
                        grid: {{ display: false }},
                        ticks: {{ color: '#94a3b8' }}
                    }}
                }}
            }}
        }});

        // Table Rendering & Filtering
        const tableBody = document.getElementById('tableBody');
        const noResults = document.getElementById('noResults');
        const searchInput = document.getElementById('searchInput');
        const ratingFilter = document.getElementById('ratingFilter');
        const sortFilter = document.getElementById('sortFilter');
        const resetBtn = document.getElementById('resetBtn');

        function renderTable(items) {{
            tableBody.innerHTML = '';
            if (items.length === 0) {{
                noResults.classList.remove('hidden');
                return;
            }}
            noResults.classList.add('hidden');

            items.forEach((item, index) => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-800/40 transition';
                
                const isStock = item.availability.toLowerCase().includes('in stock');
                const badgeStock = isStock 
                    ? '<span class="px-2.5 py-1 text-xs rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">In Stock</span>'
                    : '<span class="px-2.5 py-1 text-xs rounded-full bg-red-500/10 text-red-400 border border-red-500/20 font-medium">Out of Stock</span>';

                tr.innerHTML = `
                    <td class="py-3 px-4">
                        <img src="${{item.image_url}}" alt="cover" class="w-10 h-14 object-cover rounded shadow border border-slate-700 bg-slate-800" onerror="this.src='https://via.placeholder.com/40x56?text=Book'">
                    </td>
                    <td class="py-3 px-4 font-medium text-white max-w-xs truncate" title="${{item.title}}">
                        ${{item.title}}
                    </td>
                    <td class="py-3 px-4 font-semibold text-emerald-400 whitespace-nowrap">
                        £${{item.price_gbp.toFixed(2)}}
                    </td>
                    <td class="py-3 px-4 whitespace-nowrap text-amber-400 text-xs">
                        ${{item.stars}} <span class="text-slate-400 ml-1">(${{item.rating}}.0)</span>
                    </td>
                    <td class="py-3 px-4 whitespace-nowrap">
                        ${{badgeStock}}
                    </td>
                    <td class="py-3 px-4 text-right whitespace-nowrap">
                        <a href="${{item.product_url}}" target="_blank" class="text-xs text-slate-400 hover:text-white px-2.5 py-1.5 rounded bg-slate-800 hover:bg-slate-700 transition">
                            <i class="fa-solid fa-arrow-up-right-from-square"></i>
                        </a>
                    </td>
                `;
                tableBody.appendChild(tr);
            }});
        }}

        function applyFilters() {{
            let filtered = [...rawData];
            const q = searchInput.value.toLowerCase().trim();
            const r = ratingFilter.value;
            const s = sortFilter.value;

            if (q) {{
                filtered = filtered.filter(item => item.title.toLowerCase().includes(q));
            }}
            if (r !== 'all') {{
                filtered = filtered.filter(item => item.rating === parseInt(r));
            }}

            if (s === 'price-asc') {{
                filtered.sort((a, b) => a.price_gbp - b.price_gbp);
            }} else if (s === 'price-desc') {{
                filtered.sort((a, b) => b.price_gbp - a.price_gbp);
            }} else if (s === 'rating-desc') {{
                filtered.sort((a, b) => b.rating - a.rating);
            }}

            renderTable(filtered);
        }}

        searchInput.addEventListener('input', applyFilters);
        ratingFilter.addEventListener('change', applyFilters);
        sortFilter.addEventListener('change', applyFilters);
        resetBtn.addEventListener('click', () => {{
            searchInput.value = '';
            ratingFilter.value = 'all';
            sortFilter.value = 'default';
            applyFilters();
        }});

        // Initial Render
        renderTable(rawData);
    </script>
</body>
</html>
"""
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    return output_html

if __name__ == "__main__":
    import pandas as pd
    sample_df = pd.DataFrame([
        {"title": "Sample Book A", "price_gbp": 25.00, "rating": 5, "stars": "★★★★★", "availability": "In stock", "product_url": "#", "image_url": ""},
        {"title": "Sample Book B", "price_gbp": 15.50, "rating": 4, "stars": "★★★★☆", "availability": "In stock", "product_url": "#", "image_url": ""}
    ])
    generate_web_dashboard(sample_df)
    print("Dashboard generated successfully!")
